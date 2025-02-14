import json
from openai import OpenAI
import oracle
import prompts
from utils import DEFAULT_BACKBONE_CONFIG

class Agent_B:
    def __init__(self, b_params, sce='job interview', backbone_config=DEFAULT_BACKBONE_CONFIG,):
        # b_params: {"script_path", "role_a", "role_b"}
        self.sce = sce
        self.hist_conv = 'empty'
        
        # Load and validate script
        script_path = b_params['script_path']
        with open(script_path, 'r') as f:
            self.script = json.load(f)
        self._validate_script() # i commented this since our schema changed
        self.role_a = b_params['role_a']
        self.role_b = b_params['role_b']
            
        # Initialize state tracking
        self.disclosed_info = {topic["Name"]: [] for topic in self.script["Topics"]}
        backbone_model = backbone_config['model']
        api_key = backbone_config['api_key']
        end_point = backbone_config['end_point']
        self.temp = backbone_config['temp']
        self.top_p = backbone_config['top_p']
        self.backbone = oracle.Oracle(backbone_model, api_key, end_point)
    
    def _validate_script(self):
        """Validates that the script contains required fields and structure"""
        assert "Topics" in self.script, "Script must contain 'Topics' key"
        for topic in self.script["Topics"]:
            assert "Name" in topic, "Each topic must have a 'Name'"
            assert "Attributes" in topic, "Each topic must have 'Attributes'"
    
    def update_conv(self, role, message):
        curr = self.hist_conv if self.hist_conv != "empty" else ""
        self.hist_conv = curr + f"\n {role}: " + message

    def update_conv_a(self, message):
        self.update_conv(self.role_a, message)
    
    def respond(self, question):
        script_str = json.dumps({"Topics":self.script["Topics"]}, indent=2)
        public_str = json.dumps({"Public":self.script["Public"]}, indent=2)

        prompt_script = prompts.SCRIPT_EXPLANATION.format(
            role_a=self.role_a,
            role_b=self.role_b
        )

        prompt_sys = prompts.AGENT_B_SYS.format(
            script_explanation=prompt_script,
            script=script_str,
            sce=self.sce,
            role_a=self.role_a,
            role_b=self.role_b,
            public=public_str,
        )

        # disclosed_info_str = json.dumps(self.disclosed_info, indent=2) # is this implemented??

        prompt_user = prompts.AGENT_B_USR.format(
            question=question,
            hist_conv=self.hist_conv,
            sce=self.sce,
            role_a=self.role_a,
            role_b=self.role_b
            # disclosed_info=disclosed_info_str
        )

        response = self.backbone.query(prompt_sys, prompt_user, self.temp, self.top_p)['answer']
        self.update_conv(self.role_b, response)
            
        return response

        # if self.sce == 'interview':
        #     # Format the script into a string representation for the prompt
        #     script_str = json.dumps(self.script, indent=2)
            
        #     prompt_sys = prompts.AGENT_B_INTERVIEW_SYS.format(
        #         script_explanation=prompts.SCRIPT_EXPLANATION_INTERVIEW,
        #         script=script_str
        #     )
            
        #     # Convert disclosed_info to JSON-serializable format
        #     disclosed_info_str = json.dumps(self.disclosed_info, indent=2) # is this implemented??
            
        #     prompt_user = prompts.AGENT_B_INTERVIEW_USR.format(
        #         question=question,
        #         hist_conv=self.hist_conv,
        #         disclosed_info=disclosed_info_str
        #     )
            
        #     response = self.backbone.query(prompt_sys, prompt_user, self.temp, self.top_p)['answer']
        #     self.update_conv(self.role_b, response)
            
        #     return response
