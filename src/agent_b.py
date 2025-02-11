import json
from openai import OpenAI
import oracle
import prompts

class Agent_B:
    def __init__(self, script_path, sce='interview', backbone='gpt-4', api_key=None, end_point=None):
        assert sce in ['interview'], f'err: {sce} scenario is not supported yet.'
        self.sce = sce
        self.hist_conv = 'empty'
        
        # Load and validate script
        with open(script_path, 'r') as f:
            self.script = json.load(f)
        self._validate_script()
        
        # Initialize role names based on scenario
        if sce == 'interview':
            self.sys_prompt_temp = prompts.AGENT_B_INTERVIEW_SYS
            self.usr_prompt_temp = prompts.AGENT_B_INTERVIEW_USR
            self.role_a = 'Interviewer'
            self.role_b = 'Interviewee'
            
        # Initialize state tracking
        self.disclosed_info = {topic["Name"]: [] for topic in self.script["Topics"]}
        self.backbone = oracle.Oracle(backbone, api_key, end_point)
    
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
        """Generate a response to the interviewer's question"""
        if self.sce == 'interview':
            # Format the script into a string representation for the prompt
            script_str = json.dumps(self.script, indent=2)
            
            prompt_sys = prompts.AGENT_B_INTERVIEW_SYS.format(
                script_explanation=prompts.SCRIPT_EXPLANATION,
                script=script_str
            )
            
            # Convert disclosed_info to JSON-serializable format
            disclosed_info_str = json.dumps(self.disclosed_info, indent=2)
            
            prompt_user = prompts.AGENT_B_INTERVIEW_USR.format(
                question=question,
                hist_conv=self.hist_conv,
                disclosed_info=disclosed_info_str
            )
            
            response = self.backbone.query(prompt_sys, prompt_user)['answer']
            self.update_conv(self.role_b, response)
            
            return response