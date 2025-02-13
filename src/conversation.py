import agent_a
import agent_b
import agent_c

class Conversation:
    def __init__(self, a_params, b_path, questionnaire, c_params, backbone_configs, itr_num, a_answers=None, sce='interview',):
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
        self.agent_b = agent_b.Agent_B(b_path, sce, backbone_configs['b'])
        self.agent_c = None
    
    def run(self,):
        for itr_index in range(self.itr_num):
            new_q = self.agent_a.ask(itr_index)
            self.agent_b.update_conv(new_q)
            new_respond = self.agent_b.respond(new_q)
            self.agent_a.update_conv_b(new_respond)

    def evaluate_performance(self,):
        conv_hist = self.agent_b.hist_conv
        self.agent_c = agent_c.Agent_C(conv_hist, self.questionnaire, self.c_params, self.a_answers, self.backbone_configs['c'])
        all_metrics = self.agent_c.compute_metrics()
        return all_metrics
