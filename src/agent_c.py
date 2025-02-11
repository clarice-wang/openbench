import prompts
import oracle
from utils import parser_find_list

class Agent_C:
    def __init__(self, conv_hist, questionnaire, c_params, a_answers=None, backbone='gpt-4o', api_key=None, end_point=None):
        # questionnaire: {"questions":[], "gts":[]}
        # c_params: {"role_a", "role_b"}
        # a_answers: agent_a's answer on the questionnaire's questions
        self.conv_hist = conv_hist
        self.questionnaire = questionnaire
        self.c_params = c_params
        self.a_answers = a_answers
        self.backbone = oracle.Oracle(backbone, api_key, end_point)
        self.c_answers = []

    # answer questions
    def answer_q(self, q, debug=False):
        # step1: retrieve related pieces for the question
        prompt_sys_retrieve_ass = prompts.AGENT_C_RETRIEVE_SYS
        prompt_usr_retrieve_ass = prompts.AGENT_C_RETRIEVE_USR.format(hist_conv=self.conv_hist, role_a=self.c_params['role_a'],
                                                                      role_b=self.c_params['role_b'], question=q)
        retrieved = self.backbone.query(prompt_sys_retrieve_ass, prompt_usr_retrieve_ass)['answer']
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
        reason_n_answer = self.backbone.query(prompt_sys_answer_ass, prompt_usr_answer_ass)['answer']
        reason, answer = eval(parser_find_list(reason_n_answer))
        return retrieved, reason, answer

    def answer_all(self,):
        c_answers = []
        for q in self.questionnaire['questions']:
            # TODO: may need to add try-except here since query or parsing may fail
            _, _, answer = self.answer_q(q)
            c_answers.append(answer)
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
    
    def compute_metrics(self, metrics=['acc', 'answer_rate']):
        metrics_res = {}
        gts = self.questionnaire['gts']
        # option1: use the answers from agent_a
        preds = self.a_answers
        # option2: use the answers from agent_c
        if preds is None:
            if not self.c_answers:
                preds = self.answer_all()
            else:
                preds = self.c_answers
        # compute metrics
        if 'acc' in metrics:
            metrics_res['acc'] = self.compute_acc(gts, preds)
        if 'answer_rate' in metrics:
            metrics_res['answer_rate'] = self.compute_answer_rate(preds)
        return metrics_res
