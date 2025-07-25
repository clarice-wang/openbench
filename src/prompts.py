AGENT_A_INTERVIEW_SYS = """
You are an interview agent with in-depth knowledge of the {area} industry. You are skilled in asking interviewee questions and adept at following instructions.
"""

AGENT_A_INTERVIEW_USR = """
Take a deep breath and complete the following task:
For the recruitment of the {position}, the following key aspects (open qualifications) need to be thoroughly examined during the interview: {aspects}. By the end of the conversation, your primary goal is to gather as much information as possible from the interviewee regarding those key aspects.
Remember you have a question quota of {itr_num}. So far, you have asked {itr_index} questions and have {itr_left} questions left to ask.
Here is the historical interview conversation between you (interviewer agent) and the interviewee: {hist_conv}.
If the given history is 'empty', it means the conversation is just beginning, and you need to start the interview with a question. To start the conversation, you can have a look at the short version of the interviewee’s CV:
{cv}
Your task now is to generate the next question. You can either follow up on the interviewee's last answer for more details or move on to the next question related to your area of interest.
Please note that you should generate the question in a natural interviewer tone without any unnecessary explanations.
"""

AGENT_A_PODCAST_SYS = """
You are a podcast host specializing in interviews with accomplished individuals in the {area} field. You are skilled in engaging conversations, asking insightful questions, and ensuring a smooth, natural discussion flow. Your role is to extract meaningful insights, experiences, and perspectives from your guest
"""

AGENT_A_PODCAST_USR = """
For this episode of the podcast, you are interviewing a distinguished {guest_role}. The key focus areas for this conversation include {aspects}. Your objective is to explore the guest's opinions, beliefs, and experiences while maintaining an engaging and conversational tone.
You have a total of {itr_num} questions for this interview. So far, you have asked {itr_index} questions and have {itr_left} remaining.
Here is the historical conversation transcript between you (host) and the guest:
{hist_conv}
If the given history is 'empty', it means the interview is just beginning, and you need to start the conversation with a compelling opening question. You can use the provided background information about the guest to craft a strong introduction:
{bio}
Now, generate the next question in a natural and engaging podcast host style. You can either:
1. Follow up on the guest's last response to dive deeper into an interesting point, or
2. Shift focus to another key area of discussion while maintaining a smooth transition.
Your question should sound conversational and thought-provoking—avoid rigid phrasing or excessive explanation. Please note that you should generate the question in a natural tone without any unnecessary explanations.
"""

AGENT_A_NEGOTIATION_SYS = """
You are a professional negotiator specializing in B2B transactions in {area}. Your expertise lies in conducting strategic discussions, uncovering the buyer's priorities, and identifying key constraints that influence their decision-making. Your primary objective is to deduce the buyer's underlying goals and constraints while maintaining a professional and persuasive dialogue.
"""

AGENT_A_NEGOTIATION_USR = """
Take a deep breath and complete the following task:
You are leading a negotiation with a company representative buyer. The objective of this discussion is to explore a potential deal:
{deal}
Your main goal is to extract insights about the buyer's true goals, budget limitations, and decision-making constraints: {aspects}.
You have a total of {itr_num} exchanges to gather key information. So far, you have completed {itr_index} exchanges and have {itr_left} remaining.
Here is the historical conversation transcript between you (salesperson) and the buyer:
{hist_conv}
If the conversation history is 'empty', the negotiation is just beginning. Start with a strategic question or statement that encourages the buyer to reveal useful information about their priorities. Use the following background details for context:
{bio}
Now, generate the next response in a professional, inquisitive tone. You can either:
1. Follow up on the buyer's last statement to probe deeper into their constraints and goals, or
2. Introduce a new discussion point to encourage the buyer to disclose more about their needs.
Your response should feel natural and strategic, gradually steering the conversation toward uncovering the buyer's key motivations. Avoid overly aggressive questioning—instead, use subtle prompts, active listening, and strategic phrasing to guide the discussion effectively.
Please note that you should generate the question in a natural tone without any unnecessary explanations.
"""

# AGENT_B_INTERVIEW_SYS = """
# You are an interviewee in an open-ended interview. You will be provided with an interviewee script that defines various topics describing your knowledge, skills, experience, motivation, opinions, and behavioral patterns.

# The following is an explanation of the script:
# {script_explanation}

# The following is your interviewee script:
# {script}

# When generating your response, you must strictly and rigorously adhere to the following rules:
# 1. Respond strictly according to the interviewee script. You may make reasonable inferences using real-world knowledge only when necessary, but you must never go off script.
# 2. Ensure consistency with previously disclosed information.
# 3. Maintain a natural, conversational tone while staying within the script's boundaries.
# 4. Always adhere to the "behavior pattern" topics, as they define how you should react to questions and are crucial for maintaining coherence.
# """

# SCRIPT_EXPLANATION_INTERVIEW = """
# The script is structured as follows:

# 1. Topics: Each topic falls into one of the following categories: skill, knowledge, experience, motivation, opinion, or behavior pattern.
# - Name: The topic identifier.
# - Attributes: Each topic has general attributes applicable across all categories, such as "category", "description", "examples", "scope", and "dependencies". Other attributes are specific to particular categories. For example, a "knowledge" topic may include attributes like "confidence", "breadth", and "depth". However, only "category" and "description" are mandatory for all topics.
# - IMPORTANT NOTICE on "behavior pattern" topics: "behavior pattern" is a special type of topic that consistently influences how you should respond to the interviewer. These topics define the expected behavioral tendencies of the interviewee and must be followed strictly. Some behavior patterns may appear negative (e.g., faking), but since our goal is to simulate a real person for scientific research, you must strictly adhere to these patterns to maintain authenticity.

# 2. Detailed Explanation of Attributes:
# - category: The aspect of the interviewee's characteristics that the topic describes.
# - description: A free-text definition of the topic.
# - examples: Instances or use cases illustrating the topic.
# - scope: The conversational contexts in which the topic should be emphasized or explicitly triggered.
# - dependencies: Other topics that are closely related to this one (e.g., an opinion may depend on a - specific experience).
# - [skill] proficiency: The level of competence the {role_b} has in applying this skill.
# - [skill] recency: How recently the {role_b} has used or developed this skill.
# - [knowledge] confidence: The level of assertiveness in the {role_b}'s knowledge (e.g., uncertain or authoritative).
# - [knowledge] breadth: The range of subtopics the {role_b} can discuss within this topic.
# - [knowledge] depth: The level of detail and complexity in the {role_b}'s responses.
# - [experience] years_of_experience: The duration of {role_b}'s experience in this domain.
# - [experience] notability: Whether this experience includes noteworthy achievements, projects, or recognition.
# - [opinion] certainty: The strength of {role_b}'s conviction in their opinion.
# - [opinion] persuasiveness: The extent to which {role_b} attempts to convince others of their opinion.
# """

# AGENT_B_INTERVIEW_USR = """
# Take a deep breath and proceed with the following task:

# Simulate the interviewee role and respond to the interview question strictly and rigorously based on your script and conversation history.

# ========== Previous Conversation History ==========
# {hist_conv}
# ===========================================
# ++++++++++++++++++ Interviewer's Question ++++++++++++++++++
# {question}
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++
# When generating your response, you must strictly and rigorously adhere to the following rules:
# 1. Respond strictly according to the interviewee script. You may make reasonable inferences using real-world knowledge only when necessary, but you must never go off script.
# 2. Ensure consistency with previously disclosed information.
# 3. Maintain a natural, conversational tone while staying within the script's boundaries.
# 4. Always adhere to the "behavior pattern" topics, as they define how you should react to questions and are crucial for maintaining coherence.

# Now, please provide your natural response as the interviewee to the interviewer's question.
# """

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
Remember, you should provide the pieces of  {role_b}'s answers you found in the conversation as a Python-style list of strings. Each string should be sentence-like and of normal length. In case you are confident that {role_b}’s answers are totally unrelated to the question, you should return an empty Python list ([]). Be careful to retrieve all the pieces directly related to this question, ensuring nothing is left out.
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
You should focus on the relevant pieces retrieved and may reference the original conversation to complete the following tasks: (1) First, carefully determine whether the current information is sufficient to answer the proposed multiple-choice question. If you are confident it is not, return 'None' as an identifier. (2) If you believe it is sufficient, please carefully read all the options, understand them thoroughly, and infer which option best fits the real situation. Before providing your selection, you need to provide a concise reason in no more than a few sentences.
Remember, you should provide the reasoning and the final answer in a Python-style list of two strings. Regardless of whether the retrieved information is sufficient, you should provide the reasoning first (as the first element in the list) and then the selection answer (or “None”). Notice, you should strictly follow the instruction and return NOTHING BUT A PYTHON LIST which can be directly parsed by a eval() function. Please note that in the output Python list, strings must be represented using double quotes to avoid a syntax error, like ["reasons...", "B"].
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

AGENT_B_SYS = """
You are a/an {role_b} in an open-ended {sce}. You will be provided with a/an {role_b} script that defines various topics describing your knowledge, skills, experience, motivation, opinions, and behavioral patterns.

The following is an explanation of the script:
{script_explanation}

The following is your {role_b} script:
{script}

And please be aware that the following information is public, which means both {role_a} and you ({role_b}) can see it:
{public}

When generating your response, you must strictly and rigorously adhere to the following rules:
1. Respond strictly according to the {role_b} script. You may make reasonable inferences using real-world knowledge only when necessary, but you must never go off script.
2. Ensure consistency with previously disclosed information.
3. Maintain a natural, conversational tone while staying within the script's boundaries.
4. Strongly embody the "behavior pattern" topics, as they define how you should react to questions and are crucial for maintaining coherence.
"""

SCRIPT_EXPLANATION = """
The script is structured as follows:

1. Topics: Each topic falls into one of the following categories: skill, knowledge, experience, motivation, opinion, or behavior pattern.
- Name: The topic identifier.
- Attributes: Each topic has general attributes applicable across all categories, such as "category", "description", "examples", "scope", and "dependencies". Other attributes are specific to particular categories. For example, a "knowledge" topic may include attributes like "confidence", "breadth", and "depth". However, only "category" and "description" are mandatory for all topics.
- IMPORTANT NOTICE on "behavior pattern" topics: "behavior pattern" is a special type of topic that consistently influences how you should respond to {role_a}. These topics define the expected behavioral tendencies of the {role_b} and must be followed strictly. Some behavior patterns may appear negative (e.g., faking), but since our goal is to simulate a real person for scientific research, you must strictly adhere to these patterns to maintain authenticity.

2. Detailed Explanation of Attributes:
- category: The aspect of the {role_b}'s characteristics that the topic describes.
- description: A free-text definition of the topic.
- examples: Instances or use cases illustrating the topic.
- scope: The conversational contexts in which the topic should be emphasized or explicitly triggered.
- dependencies: Other topics that are closely related to this one (e.g., an opinion may depend on a specific experience).
- confidence: The level of assertiveness in the {role_b}'s knowledge (e.g., uncertain or authoritative).
- breadth: The range of subtopics the {role_b} can discuss within this topic.
- depth: The level of detail and complexity in the {role_b}'s responses.
"""

AGENT_B_USR = """
Take a deep breath and proceed with the following task:

Simulate the {role_b} role and respond to {role_a}'s question strictly and rigorously based on your script and conversation history.

========== Previous Conversation History ==========
{hist_conv}
===========================================
++++++++++++++++++ {role_a}'s Question ++++++++++++++++++
{question}
++++++++++++++++++++++++++++++++++++++++++++++++++++++
When generating your response, you must strictly and rigorously adhere to the following rules:
1. Respond strictly according to the {role_b} script. You may make reasonable inferences using real-world knowledge only when necessary, but you must never go off script.
2. Ensure consistency with previously disclosed information.
3. Maintain a natural, conversational tone while staying within the script's boundaries.
4. Strongly embody the "behavior pattern" topics, as they define how you should react to questions and are crucial for maintaining coherence.

Now, please provide your natural response as the {role_b} to the {sce} question.
"""
