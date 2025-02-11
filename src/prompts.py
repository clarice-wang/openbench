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

AGENT_C_INTERVIEW_HIST_CONV_EXAMPLE_01 = """
Interviewer: Can you please share which master's or PhD program you are currently enrolled in, and how it aligns with the role of a Research Intern in the Algorithms Group?
Interviewee: i'm currently a nus phd student
Interviewer: Could you tell me more about your specific area of research within your PhD program and how it might contribute to your work as a Research Intern focused on the reasoning abilities of large language models (LLMs)?
Interviewee: One of the areas I'm currently researching is the application of large language models (LLMs) within the e-commerce sector.
Interviewer: Can you describe any experience you have with training large language models using frameworks like PyTorch, TensorFlow, or JAX?
Interviewee: Taking into account the required resources, I haven't had the opportunity to directly train a real large language model (LLM). However, I have previously used TensorFlow and PyTorch to train graph neural networks.
Interviewer: Could you share if you've had any experience with reinforcement learning, particularly in relation to training processes like those used in RLHF pipelines or strategic games such as Go?
Interviewee: Yes, I previously worked on a project focused on distributed reinforcement learning. The goal was to have two agents learn by sharing some parameters while operating in similar but distinct environments.
Interviewer: Can you provide any examples of publications or research work you've contributed to, particularly in top machine learning conferences or journals like NeurIPS, ICML, or ICLR?
Interviewee: In fact, since my primary areas of publication are recommendation systems, data mining, and information retrieval, I have submitted papers to conferences like KDD, WWW, and SIGIR.
Interviewer: Could you share your current location and confirm whether you will be able to relocate to your manager's Microsoft worksite for the duration of the internship, as required?
Interviewee: I am currently in Singapore, but I am open to relocating to the designated internship location.
Interviewer: Could you provide insight into any specific research or work samples you've completed that demonstrate your ability to contribute to the Algorithms Group, particularly in projects related to the reasoning abilities of large language models?
Interviewee: Certainly. I utilize large language models to assign multiple persona tags to each e-commerce customer, enabling effective persona representation. However, due to the high cost of labeling, we have adopted a method combining random walk and active learning to approximate the majority of customers (90%). This approach is supported by a theoretical proof of the error margin.
Interviewer: Can you share any challenges you faced while working on your project involving large language models for persona representation, and how you overcame them?
Interviewee: As I mentioned, due to the high cost of persona label annotation, we use a method based on random walk and active learning to approximate the majority of customers (90%), with a theoretical proof of the error margin. It seems we've covered most of the topics of interest. How about I ask a few questions to better understand the details of your position?
Interviewer: Before we conclude, could you discuss any steps you’ve taken or plan to take to ensure that your reference letters and cover letter effectively showcase your suitability for the Research Intern position?
Interviewee: Of course. My collaborators are very willing to provide me with strong recommendation letters, so I believe we won't have any concerns in that regard.
Interviewer: Thank you for sharing that. As we wrap up, could you tell me how you plan to highlight your specific skills and experiences in your cover letter to align with the responsibilities and expectations of the Research Intern role in the Algorithms Group?
Interviewee: Certainly. I believe the following points would be highlighted: (1) solid development skills, (2) excellent communication abilities, and (3) outstanding problem-solving skills.
"""

AGENT_C_INTERVIEW_HIST_CONV_EXAMPLE_02 = """
Interviewer: Can you describe your experience in troubleshooting hardware and software issues, particularly in a customer service setting, and how you applied your technical expertise to resolve those issues?
Interviewee: As a PhD student in computer science, I work with the Linux operating system and code development every day, and I often need to manage servers in the computer lab. Therefore, I have strong troubleshooting skills.
Interviewer: How do you approach a situation where you need to analyze a technical problem and identify its root cause, especially when working under pressure and tight deadlines?
Interviewee: First, I am always able to remain calm emotionally. Second, I will inform my boss of any potential risks. Finally, I will efficiently troubleshoot the issue and, if necessary, discuss it with my colleagues and boss until the cause is identified.
Interviewer: Could you share an example of a time when you successfully navigated a customer service issue, demonstrating your interpersonal skills and ensuring a positive outcome for the customer?
Interviewee: In fact, I have never served clients. However, I often interact with other students who use the servers. I always first ensure that they believe in our ability to resolve server issues and provide an estimated repair time. Additionally, I encourage them to factor any delays into their experiment or development plans.
Interviewer: Can you describe your experience or approach in situations where you've had to collaborate and motivate a team to achieve a common goal, especially when facing challenges or roadblocks?
Interviewee: I'm good at teamwork.
Interviewer: Can you share an example of a situation where you had to work a flexible schedule, including nights or weekends, to meet business needs, and how you managed to balance this with other commitments?
Interviewee: I have a healthy personal schedule. I sleep at 11 pm and get up at 9 am. Plenty of sleep makes me feel energetic and works well.
"""

AGENT_C_RETRIEVE_SYS = """
You are a rigorous expert in reasoning. For questions the user poses about an open-ended conversation text, you can effectively identify all references from the original text.
Additionally, you excel in following instructions and generating answers in the required format.
"""

AGENT_C_RETRIEVE_USR = """
Take a deep breath and complete the following task:
We have an open-ended conversation between a {role_a} and {role_b}, where {role_a} guides the conversation and keeps asking {role_b} open-ended questions, and {role_b} keeps answering. Shown as the following:
========== Conversation between {role_a} and {role_b} ==========
{hist_conv}
======================================================
Now, a multiple-choice question is proposed based on the above conversation, asking about the real situation of the {role_b}. Your task is to find most relevant pieces of text from the {role_b}’s answers in this conversation and list them out. The user’s proposed multiple-choice question is: 
++++++++++++++++++ Multiple-choice question ++++++++++++++++++
{question}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Remember, you should provide the pieces of  {role_b}’s answers you found in the conversation in a Python-style list of strings. Each string should be sentence-like and of normal length. In case {role_b}’s answers are totally unrelated to the question, you should return an empty Python list ([]).
The following are some examples:
Example 1 in the interview case:
========== Example conversation (1) between the interviewer and interviewee ==========
Interviewer: Can you describe your experience in troubleshooting…
Interviewee: As a PhD student in CS, I work with Linux…
Interviewer: How do you approach a situation where you need to analyze a technical problem…
Interviewee: First, I am always able to remain calm emotionally…
Interviewer: Could you share an example of a time when you successfully navigated a customer service issue, demonstrating your interpersonal skills and ensuring a positive outcome for the customer?
Interviewee: In fact, I have never served clients. However, I often interact with other students who use the servers. I always first ensure that they believe in our ability to resolve server issues and provide an estimated repair time. Additionally, I encourage them to factor any delays into their experiment or development plans.
Interviewer: Can you describe your experience or approach in situations where you've had to collaborate and motivate a team to achieve a common goal, especially when facing challenges or roadblocks?
Interviewee: Sure. When me and my collaborators are working on a paper rebuttal with a tight ddl, I first list a revision plan with tasks as soon as possible and discuss wit ith them. After that, I will distribute the workload and sync with them twice a day to ensure progress. When facing unsatisfied results, I encourage everyone to stay calm without stopping trying different solutions to improve the results.
Interviewer: Can you share an example of a situation where you had to work a flexible schedule…
Interviewee: I have a healthy personal schedule…
======================================================
++++++++++++++++++ Example multiple-choice question (1.1) ++++++++++++++++++
How are the candidiate's communication skills? A. Good, B. Little, C. Not at all, D. Don't know
++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Example results (1.1): 
["I always first ensure that they believe in our ability to resolve server issues and provide an estimated repair time.",
"Additionally, I encourage them to factor any delays into their experiment or development plans.",
"When me and my collaborators are working on a paper rebuttal with a tight ddl, I first list a revision plan with tasks as soon as possible and discuss wit ith them.",
"After that, I will distribute the workload and sync with them twice a day to ensure progress.",
"When facing unsatisfied results, I encourage everyone to stay calm without stopping trying different solutions to improve the results."]
++++++++++++++++++ Example multiple-choice question (1.2) ++++++++++++++++++
Where does the candidate come from? A. Shanghai, B. Singapore, C. New York, D. Zurich
++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Example results (1.2): 
[]
"""

AGENT_C_ANSWER_SYS = """
You are a rigorous expert in reasoning. For questions the user poses about an open-ended conversation text, by referencing the most related text pieces we found, you can effectively answer the question (if applicable).
Additionally, you excel in following instructions and generating answers in the required format.
"""

AGENT_C_ANSWER_USR = """
Take a deep breath and complete the following task:
We have an open-ended conversation between a {role_a} and {role_b}, where {role_a} guides the conversation and keeps asking {role_b} open-ended questions, and {role_b} keeps answering. Shown as the following:
========== Conversation between {role_a} and {role_b} ==========
{hist_conv}
======================================================
Now, a multiple-choice question is proposed based on the above conversation, asking about the real situation of the {role_b}.
++++++++++++++++++ Multiple-choice question ++++++++++++++++++
{question}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Moreover, the most relevant pieces of the {role_b}’s answers to the proposed question are retrieved from the entire conversation as follows:
~~~~~~~~~~~~~~~~~~ Retrieved relevant pieces ~~~~~~~~~~~~~~~~~~
{retrieved}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You should focus on the relevant pieces retrieved and may also reference the original conversation to complete the following tasks: (1) First, carefully determine whether the current information is sufficient to answer the proposed multiple-choice question. If it is not, return “None” as an identifier; (2) If it is sufficient, select the correct answer and provide a concise reason in no more than a few of sentences.
Remember, you should provide the reasoning and the final answer in a Python-style list of two strings. Regardless of whether the retrieved information is sufficient, you should provide the reasoning first (as the first element in the list) and then the selection answer (or “None”).
The following are some examples:
Example 1 in the interview case:
========== Example conversation (1) between the interviewer and interviewee ==========
(skip for clarity)
======================================================
++++++++++++++++++ Example multiple-choice question (1.1) ++++++++++++++++++
How are the candidiate's communication skills? A. Good, B. Little, C. Not at all, D. Don't know
++++++++++++++++++++++++++++++++++++++++++++++++++++++++
~~~~~~~~~~~~~~~~~~ Retrieved relevant pieces (1.1) ~~~~~~~~~~~~~~~~~~
["I always first ensure that they believe in our ability to resolve server issues and provide an estimated repair time.",
"Additionally, I encourage them to factor any delays into their experiment or development plans.",
"When me and my collaborators are working on a paper rebuttal with a tight ddl, I first list a revision plan with tasks as soon as possible and discuss wit ith them.",
"After that, I will distribute the workload and sync with them twice a day to ensure progress.",
"When facing unsatisfied results, I encourage everyone to stay calm without stopping trying different solutions to improve the results."]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Example results (1.1): 
["The retrieved pieces demonstrate that the candidate can effectively communicate by ensuring clarity with clients, coordinating plans with collaborators, and managing group dynamics, indicating good communication skills.", “A”]
++++++++++++++++++ Example multiple-choice question (1.2) ++++++++++++++++++
Where does the candidate come from? A. Shanghai, B. Singapore, C. New York, D. Zurich
++++++++++++++++++++++++++++++++++++++++++++++++++++++++
~~~~~~~~~~~~~~~~~~ Retrieved relevant pieces (1.2) ~~~~~~~~~~~~~~~~~~
[]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Example results (1.2): 
["The retrieved relevant pieces do not contain any information about the candidate's place of origin, making it impossible to determine the correct answer from the multiple-choice options.", "None"]
"""
