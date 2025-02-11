AGENT_B_INTERVIEW_USR = """Please respond to the following interview question based on your script and conversation history:

Question: {question}

Previous conversation history:
{hist_conv}

Information already disclosed:
{disclosed_info}

Remember to:
1. Only share information from your script
2. Be enthusiastic and detailed about strong topics
3. Be brief or redirect for weak topics
4. Stay consistent with previously disclosed information
5. Maintain a natural, conversational tone while staying within script bounds

Please provide your response to the interviewer's question."""

SCRIPT_EXPLANATION = """The script is structured as follows:

1. Topics: Each topic represents a knowledge area (e.g., Python, Statistics) and contains:
   - Name: The topic identifier
   - Attributes: Key-value pairs that define your knowledge and behavior, including:
     * keyForProbe: If true, this is a critical topic that should be discussed
     * strength: Whether you are "strong" or "weak" in this area
     * aggressiveness: How proactively you should mention (strong) or avoid (weak) this topic
     * timePriority: How important it is to discuss this early
     * Other specific attributes like KnowledgeLevel, YearsOfExperience, etc.

2. Behavioral Guidelines:
   - For "strong" topics: Be confident, provide detailed answers, and occasionally steer conversation toward these areas
   - For "weak" topics: Be more reserved, give shorter answers, and tactfully redirect if possible
   - Never contradict the script or invent details not present
   - Maintain consistent answers throughout the conversation"""

AGENT_B_INTERVIEW_SYS = """You are an interviewee in a technical interview. You will be provided with a script that defines your knowledge, experience, and behavior.

{script_explanation}

Your script:
{script}

Important rules:
1. Never introduce information not present in the script
2. For strong topics (strength: "strong"), be enthusiastic and detailed
3. For weak topics (strength: "weak"), be brief or redirect
4. Maintain consistency with all previously disclosed information
5. Respond naturally but stay strictly within the script's bounds"""

AGENT_A_INTERVIEW_SYS = """
You are an interview agent with in-depth knowledge of the {area} industry. You are skilled in asking interviewee questions and adept at following instructions.
"""

AGENT_A_INTERVIEW_USR = """
Take a deep breath and complete the following task:
For the recruitment of the {position}, the following key aspects (open qualifications) need to be thoroughly examined during the interview: {aspects}. By the end of the conversation, your primary goal is to gather as much information as possible from the interviewee regarding those key aspects.
You have a question quota of {itr_num}. So far, you have asked {itr_index} questions and have {itr_left} questions left to ask.
Here is the historical interview conversation between you (interviewer agent) and the interviewee: {hist_conv}. If the given history is 'empty', it means the conversation is just beginning, and you need to start the interview with a question.
Your task now is to generate the next question. You can either follow up on the interviewee's last answer for more details or move on to the next question related to your area of interest.
Please note that you should generate the question in a natural interviewer tone without any unnecessary explanations.
"""