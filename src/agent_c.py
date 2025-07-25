from tqdm import tqdm
import prompts
import oracle
from utils import parser_find_list, DEFAULT_BACKBONE_CONFIG

class Agent_C:
    def __init__(self, questionnaire, c_params, a_answers=None, backbone_config=DEFAULT_BACKBONE_CONFIG,):
        # questionnaire: {"questions":[], "gts":[]}
        # c_params: {"conv_hist,", "role_a", "role_b"}
        # a_answers: agent_a's answer on the questionnaire's questions
        self.conv_hist = c_params['conv_hist']
        self.questionnaire = questionnaire
        self.c_params = c_params
        self.a_answers = a_answers
        backbone_model = backbone_config['model']
        api_key = backbone_config['api_key']
        end_point = backbone_config['end_point']
        self.temp = backbone_config['temp']
        self.top_p = backbone_config['top_p']
        self.backbone = oracle.Oracle(backbone_model, api_key, end_point)
        self.c_answers = []

    # answer questions
    def answer_q(self, q, debug=False):
        # step1: retrieve related pieces for the question
        prompt_sys_retrieve_ass = prompts.AGENT_C_RETRIEVE_SYS
        prompt_usr_retrieve_ass = prompts.AGENT_C_RETRIEVE_USR.format(hist_conv=self.conv_hist, role_a=self.c_params['role_a'],
                                                                      role_b=self.c_params['role_b'], question=q)
        retrieved = self.backbone.query(prompt_sys_retrieve_ass, prompt_usr_retrieve_ass, self.temp, self.top_p)['answer']
        retrieved = parser_find_list(retrieved)
        if debug:
            print(retrieved)
        # step2: answer the question
        prompt_sys_answer_ass = prompts.AGENT_C_ANSWER_SYS
        prompt_usr_answer_ass = prompts.AGENT_C_ANSWER_USR.format(hist_conv=self.conv_hist, role_a=self.c_params['role_a'],
                                                                  role_b=self.c_params['role_b'], question=q, retrieved=retrieved)
        if debug:
            print(prompt_sys_answer_ass)
            print(prompt_usr_answer_ass)
        reason_n_answer = self.backbone.query(prompt_sys_answer_ass, prompt_usr_answer_ass, self.temp, self.top_p)['answer']
        reason, answer = eval(parser_find_list(reason_n_answer))
        return retrieved, reason, answer

    def answer_all(self, debug=False):
        c_retrieveds, c_reasons, c_answers = [], [], []
        question_list = self.questionnaire['questions']
        for q in tqdm(question_list, desc="Answering questions", total=len(question_list)):
            # TODO: may need to add try-except here since query or parsing may fail
            retrieved, reason, answer = self.answer_q(q)
            if debug:
                print(f"retrieved: {retrieved}")
                print(f"reason: {reason}")
                print(f"answer: {answer}")
            c_retrieveds.append(retrieved)
            c_reasons.append(reason)
            c_answers.append(answer)

        self.c_retrieveds = c_retrieveds
        self.c_reasons = c_reasons
        self.c_answers = c_answers
        return c_answers

    # for metrics
    def compute_answer_rate(self, preds):
        answer_ctr = 0
        for pred in preds:
            if pred != 'None':
                answer_ctr += 1
        return answer_ctr / len(preds)

    def compute_acc(self, gts, preds):
        assert len(gts) == len(preds)
        correct_ctr = 0
        for gt, pred in zip(gts, preds):
            if gt == pred:
                correct_ctr += 1
        return correct_ctr / len(gts)
    
    def compute_metrics(self, metrics=['acc', 'answer_rate'], debug=False):
        metrics_res = {}
        gts = self.questionnaire['gts']
        # option1: use the answers from agent_a
        preds = self.a_answers
        # option2: use the answers from agent_c
        if preds is None:
            if not self.c_answers:
                preds = self.answer_all(debug=debug)
            else:
                preds = self.c_answers
        # compute metrics
        if 'acc' in metrics:
            metrics_res['acc'] = self.compute_acc(gts, preds)
        if 'answer_rate' in metrics:
            metrics_res['answer_rate'] = self.compute_answer_rate(preds)
        return metrics_res
