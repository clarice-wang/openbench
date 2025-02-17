import oracle
import prompts
from utils import DEFAULT_BACKBONE_CONFIG

class Agent_A:
    def __init__(self, a_params, sce='job interview', backbone_config=DEFAULT_BACKBONE_CONFIG,):
        assert sce in ['job interview', 'podcast interview', 'b2b negotiation'], f'err: {sce} scenario is not supported for agent A yet.'
        self.a_params = a_params
        self.sce = sce
        self.hist_conv = 'empty'
        if sce == 'job interview':
            self.sys_prompt_temp = prompts.AGENT_A_INTERVIEW_SYS
            self.usr_prompt_temp = prompts.AGENT_A_INTERVIEW_USR
            self.role_a = 'Interviewer'
            self.role_b = 'Interviewee'
        elif sce == 'podcast interview':
            self.sys_prompt_temp = prompts.AGENT_A_PODCAST_SYS
            self.usr_prompt_temp = prompts.AGENT_A_PODCAST_USR
            self.role_a = 'Host'
            self.role_b = 'Guest'
        elif sce == 'b2b negotiation':
            self.sys_prompt_temp = prompts.AGENT_A_NEGOTIATION_SYS
            self.usr_prompt_temp = prompts.AGENT_A_NEGOTIATION_USR
            self.role_a = 'Salesperson'
            self.role_b = 'Buyer'

        backbone_model = backbone_config['model']
        api_key = backbone_config['api_key']
        end_point = backbone_config['end_point']
        self.temp = backbone_config['temp']
        self.top_p = backbone_config['top_p']
        self.backbone = oracle.Oracle(backbone_model, api_key, end_point)
    
    def update_conv(self, role, message):
        curr = self.hist_conv if self.hist_conv != "empty" else ""
        self.hist_conv = curr + f"\n {role}: " + message

    def update_conv_b(self, message):
        self.update_conv(self.role_b, message)

    def ask(self, i,):
        if self.sce == 'job interview':
            prompt_sys_ass = prompts.AGENT_A_INTERVIEW_SYS.format(area=self.a_params['area'])
            prompt_user_ass = prompts.AGENT_A_INTERVIEW_USR.format(position=self.a_params['position'], aspects=self.a_params['aspects'],
                                                                   cv=self.a_params['short-cv'], hist_conv=self.hist_conv,
                                                                   itr_num=self.a_params['itr_num'], itr_left=self.a_params['itr_num']-i, itr_index=i)
        elif self.sce == 'podcast interview':
            prompt_sys_ass = prompts.AGENT_A_PODCAST_SYS.format(area=self.a_params['area'])
            prompt_user_ass = prompts.AGENT_A_PODCAST_USR.format(guest_role=self.a_params['guest_role'], aspects=self.a_params['aspects'],
                                                                   bio=self.a_params['bio'], hist_conv=self.hist_conv,
                                                                   itr_num=self.a_params['itr_num'], itr_left=self.a_params['itr_num']-i, itr_index=i)
        elif self.sce == 'b2b negotiation':
            prompt_sys_ass = prompts.AGENT_A_NEGOTIATION_SYS.format(area=self.a_params['area'])
            prompt_user_ass = prompts.AGENT_A_NEGOTIATION_USR.format(deal=self.a_params['deal'], aspects=self.a_params['aspects'],
                                                                   bio=self.a_params['bio'], hist_conv=self.hist_conv,
                                                                   itr_num=self.a_params['itr_num'], itr_left=self.a_params['itr_num']-i, itr_index=i)

        # todo: other scenarios
        new_q = self.backbone.query(prompt_sys_ass, prompt_user_ass, self.temp, self.top_p)['answer']
        self.update_conv(self.role_a, new_q)
        return new_q
    
    def answer_question(self, question):
        # TODO: implement this
        pass
    
    def answer_questionnaire(self, questionnaire):
        # TODO: implement this
        pass
