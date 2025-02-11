import os
from openai import OpenAI
import oracle
import prompts

class Agent_A:
    def __init__(self, a_params, sce='interview', backbone='gpt-4o', api_key=None, end_point=None):
        assert sce in ['interview'], f'err: {sce} scenario is not supported yet.'
        self.a_params = a_params
        self.sce = sce
        self.hist_conv = 'empty'
        if sce == 'interview':
            self.sys_prompt_temp = prompts.AGENT_A_INTERVIEW_SYS
            self.usr_prompt_temp = prompts.AGENT_A_INTERVIEW_USR
            self.role_a = 'Interviewer'
            self.role_b = 'Interviewee'
        # todo: other scenarios
        self.backbone = oracle.Oracle(backbone, api_key, end_point)
    
    def update_conv(self, role, message):
        curr = self.hist_conv if self.hist_conv != "empty" else ""
        self.hist_conv = curr + f"\n {role}: " + message

    def update_conv_b(self, message):
        self.update_conv(self.role_b, message)

    def ask(self, i,):
        if self.sce == 'interview':
            prompt_sys_ass = prompts.AGENT_A_INTERVIEW_SYS.format(area=self.a_params['area'])
            prompt_user_ass = prompts.AGENT_A_INTERVIEW_USR.format(position=self.a_params['position'], aspects=self.a_params['aspects'],
                                                           hist_conv=self.hist_conv, itr_num=self.a_params['itr_num'],
                                                           itr_left=self.a_params['itr_num']-i, itr_index=i)
        # todo: other scenarios
        new_q = self.backbone.query(prompt_sys_ass, prompt_user_ass, )['answer']
        self.update_conv(self.role_a, new_q)
        return new_q
    
    def answer_question(self, question):
        # TODO: implement this
        pass
    
    def answer_questionnaire(self, questionnaire):
        # TODO: implement this
        pass
