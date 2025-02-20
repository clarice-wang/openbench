import os
import json
from datetime import datetime
from tqdm import tqdm
import pickle
import agent_a
import agent_b
import agent_c

def make_conversation(script_path, questionnaire_path, backbone_path, itr_num=10, role_a='Interviewer', role_b='Interviewee', sce='job interview'):
    # load data
    with open(script_path, 'r') as f:
        script = json.load(f)
    with open(questionnaire_path, 'r') as f:
        questionnaire = json.load(f)
    with open(backbone_path, 'r') as f:
        backbone_configs = json.load(f)
    
    # initialize parameters
    a_params = script["Public"]
    a_params["itr_num"] = itr_num
    b_params = {"script_path": script_path,
                "role_a": role_a,
                "role_b": role_b}
    c_params = {"role_a": role_a,
                "role_b": role_b}
    return Conversation(a_params, b_params, questionnaire, c_params, backbone_configs, itr_num, a_answers=None, sce=sce)

def make_conversation_dynamic(script_path, questionnaire_path, backbone_configs, itr_num=10, role_a='Interviewer', role_b='Interviewee', sce='job interview'):
    # load data
    with open(script_path, 'r') as f:
        script = json.load(f)
    with open(questionnaire_path, 'r') as f:
        questionnaire = json.load(f)
    
    # initialize parameters
    a_params = script["Public"]
    a_params["itr_num"] = itr_num
    b_params = {"script_path": script_path,
                "role_a": role_a,
                "role_b": role_b}
    c_params = {"role_a": role_a,
                "role_b": role_b}
    return Conversation(a_params, b_params, questionnaire, c_params, backbone_configs, itr_num, a_answers=None, sce=sce)

class Conversation:
    def __init__(self, a_params, b_params, questionnaire, c_params, backbone_configs, itr_num, a_answers=None, sce='job interview',):
        # questionnaire: {"questions":[], "gts":[]}
        # b_params: {"script_path", "role_a", "role_b"}
        # c_params: {"conv_hist,", "role_a", "role_b"}
        # backbone_configs: {"a": back_config_a, ...}
        # itr_num: constrained iteration number
        self.sce = sce
        self.backbone_configs = backbone_configs
        self.questionnaire = questionnaire
        self.c_params = c_params
        self.itr_num = itr_num
        self.a_answers = a_answers
        # initialize agent instances
        self.agent_a = agent_a.Agent_A(a_params, sce, backbone_configs['a'])
        self.agent_b = agent_b.Agent_B(b_params, sce, backbone_configs['b'])
        self.agent_c = None
    
    def run(self, cal_price=False):
        a_costs = 0 # counts in usd
        for itr_index in tqdm(range(self.itr_num), desc="Iterative conversation"):
            new_q, a_cost_i = self.agent_a.ask(itr_index, cal_price)
            a_costs += a_cost_i
            self.agent_b.update_conv_a(new_q)
            new_respond = self.agent_b.respond(new_q)
            self.agent_a.update_conv_b(new_respond)
        return a_costs

    def evaluate_performance(self, debug=False):
        conv_hist = self.agent_b.hist_conv
        self.c_params['conv_hist'] = conv_hist
        self.agent_c = agent_c.Agent_C(self.questionnaire, self.c_params, self.a_answers, self.backbone_configs['c'])
        all_metrics = self.agent_c.compute_metrics(debug=debug)
        return all_metrics

    def log(self, log_dir):
        # add a timestamp to the log file
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # make this a single sequence of characters
        timestamp = timestamp.replace(":", "_").replace(" ", "_") # replace both space and colon with underscore
        log_file_path = log_dir + f"log_{timestamp}.txt"
        pkl_path = log_dir + f"pkl_{timestamp}.pkl"
        
        # log all the things as text
        with open(log_file_path, 'w') as f:
            f.write(self.agent_b.hist_conv + "\n(!spliter!)\n")
            for i in range(len(self.agent_c.c_retrieveds)):
                f.write(self.questionnaire['questions'][i] + "\n\n")
                f.write(self.agent_c.c_retrieveds[i] + "\n\n")
                f.write(self.agent_c.c_reasons[i] + "\n\n")
                f.write(self.agent_c.c_answers[i] + "\n\n")
                f.write(self.questionnaire['gts'][i] + "\n\n")
                f.write("--------------------------------\n\n")
        
        # log self: a conversation instance
        with open(pkl_path, 'wb') as f:
            things_to_save = {"hist_conv": self.agent_b.hist_conv,
                              "retrieveds": self.agent_c.c_retrieveds,
                              "reasons": self.agent_c.c_reasons,
                              "answers": self.agent_c.c_answers,
                              "questionnaire": self.questionnaire,
                              "configs": self.backbone_configs}
            pickle.dump(things_to_save, f)
