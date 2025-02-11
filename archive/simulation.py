import json
import sys
import os
import argparse
import random
import textwrap
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

class ConversationLogger():
    """
    A customized Logging module. Log the conversation history into console and file.
    """

    def __init__(self, file_path=None):
        self.file_path = file_path

    def log_to_file_and_console(self, text):
        print(text)
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(text + "\n")

    def print_and_log_message(self, role, text, label=None):
        """
        :param role: The role of the speaker (e.g., Interviewer, Candidate)
        :param label: An optional label to tag the message (e.g., incomplete, vague)
        :param text: The message text
        """
        if label:
            header = f"{role}[{label}]:\n{'-' * (len(role) + len(label) + 2)}"
        else:
            header = f"{role}:\n{'-' * len(role)}"

        formatted_text = self.format_text(text, width=80)
        self.log_to_file_and_console(header)
        self.log_to_file_and_console(formatted_text)
        self.log_to_file_and_console("\n")

    def format_text(self, text, width):
        return "\n".join(textwrap.wrap(text, width))

    def log_to_console(self, role, text, label=None):
        if label:
            print(f"[{role}][{label}]: {text}")
        else:
            print(f"[{role}]: {text}")

logger = ConversationLogger(file_path="conversation.txt")

class Conversation:
    """
    Represents the conversation between interviewer and candidate.
    Handles database interaction for storing and retrieving an initial question with its follow-ups as an unit.
    """
    def __init__(self):
        self.current_question_unit = None
        self.conversation_log = []

    def start_unit_with_init_question(self, init_question):
        """
        Initialize a new initial question and prepare it for follow-ups.
        
        :init_question:
                [
                    "question", ["criteria1", "criteria2"]
                ]
        """

        self.current_question_unit = {
            "criteria": init_question[1],
            "question": init_question[0],
            "answer": None,
            "state": "processing", # Initial state
            "follow_ups": []
        }

    def add_candidate_response(self, candidate_response):
        """
        Add candidate response to the current question unit.
        :param candidate_response:
        {
            "label": vague/incomplete...etc.
            "message": text
        }
        """

        # The candidate message is for the initial question
        if not self.current_question_unit["answer"]:
            self.current_question_unit["answer"] = candidate_response
            self.current_question_unit["state"] = "answered"
        else: # The candidate message is for the last follow-up question
            self.current_question_unit["follow_ups"][-1]["answer"] = candidate_response
            self.current_question_unit["follow_ups"][-1]["state"] = "answered"

    def add_follow_up_question(self, follow_up_question):
        """
        Add a follow-up question and its answer into the current initial question.
        """
        follow_up = {
            "question": follow_up_question,
            "answer": None,
            "state": "processing"
        }
        if self.current_question_unit:
            self.current_question_unit["follow_ups"].append(follow_up)

    def store_current_question_unit(self):
        """
        Save the current initial question and its follow-ups in memory.
        """
        if self.current_question_unit:
            self.conversation_log.append(self.current_question_unit)
            print("[SYSTEM]: Moving forward to the next initial question.")

    def get_conversation_log(self):
        """
        Retrieve the entire conversation log from memory.
        """
        return self.conversation_log

    def export_conversation_to_csv(self, output_file="conversation.csv"):
        """
        Export the conversation log to a CSV file with clear interview structure.
        """
        import csv
        
        conversation_data = []
        # Define base fieldnames
        fieldnames = [
            "Initial_Question",
            "Initial_Question_Criteria",
            "Candidate_Answer",
            "Answer_Label",
        ]
        
        # Scan through all entries to find maximum number of follow-ups
        max_follow_ups = 0
        for entry in self.conversation_log:
            follow_ups = entry.get('follow_ups', [])
            max_follow_ups = max(max_follow_ups, len(follow_ups))
        
        # Add follow-up related fields
        for i in range(1, max_follow_ups + 1):
            fieldnames.extend([
                f"Follow_up_Question_{i}",
                f"Follow_up_Answer_{i}",
                f"Follow_up_Answer_Label_{i}"
            ])
        
        # Create rows for each question unit
        for entry in self.conversation_log:
            row_data = {
                "Initial_Question": entry.get('question'),
                "Initial_Question_Criteria": str(entry.get('criteria')),
                "Candidate_Answer": entry['answer'].get('message'),
                "Answer_Label": entry['answer'].get('label'),
            }

            # Add follow-up information
            follow_ups = entry.get('follow_ups', [])
            for i, follow_up in enumerate(follow_ups, start=1):
                row_data[f"Follow_up_Question_{i}"] = follow_up.get('question')
                row_data[f"Follow_up_Answer_{i}"] = follow_up['answer'].get('message')
                row_data[f"Follow_up_Answer_Label_{i}"] = follow_up['answer'].get('label')

            conversation_data.append(row_data)

        # Write to CSV
        if conversation_data:
            mode = 'a' if os.path.exists(output_file) else 'w'
            with open(output_file, mode, newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if mode == 'w':  # Only write headers for new file
                    writer.writeheader()
                writer.writerows(conversation_data)


class InterviewQuestionManager:
    """
    Make decisions about follow-ups and other interview logic.
    """
    def __init__(self, init_interview_data):

        self.init_interview_data = init_interview_data
        self.initial_questions = init_interview_data["job"]["prepared_questions"]
        """
        :self.initial_questions:
            [
                [
                    "question1", ["criteria1", "criteria2"]
                ],
                [
                    "question2", ["criteria3", "criteria2"]
                ]
            ]        
        """
        self.cur_init_question_index = 0
        self.conversation = Conversation()
        self.conversation.start_unit_with_init_question(init_question=self.initial_questions[0])


    def process_candidate_message(self, candidate_message):
        """
        Handle each message from the candidate.
        :param candidate_message:
        {
            "label": vague/incomplete...etc.
            "message": text
        }
        """
        self.conversation.add_candidate_response(candidate_response=candidate_message)
        decision = self.analyze_cur_conversation()
        if decision["status"] == "need follow-up":
            self.conversation.add_follow_up_question(decision["follow-up"])
            return {
                "label":"Follow-up",
                "message": decision["follow-up"]
            }
        else:
            self.conversation.store_current_question_unit()
            self.cur_init_question_index += 1
            if self.cur_init_question_index < len(self.initial_questions):
                self.conversation.start_unit_with_init_question(init_question=self.initial_questions[self.cur_init_question_index])
                return {
                    "label": "Initial",
                    "message": self.conversation.current_question_unit["question"]
                }
            else:
                return None

    def generate_question_unit_str(self):
        """
        Convert the current dialogue into the String format for generating prompts.
        """

        if self.conversation.current_question_unit["state"] == "answered":
            res = (f"Interviewer: [{self.conversation.current_question_unit['question']}]\n"
                f"Candidate: [{self.conversation.current_question_unit['answer']}]\n")
        else:
            res = (f"Interviewer: [{self.conversation.current_question_unit['question']}]\n"
                f"Candidate: []\n")

        for follow_up in self.conversation.current_question_unit["follow_ups"]:
            if follow_up["state"] == "answered":
                res += (f"Interviewer: [{follow_up['question']}]\n"
                    f"Candidate: [{follow_up['answer']}]\n")
            else:
                res += (f"Interviewer: [{follow_up['question']}]\n"
                    f"Candidate: []\n")
        return res

    def analyze_cur_conversation(self):
        """
        Analyze the current initial question, initial answer together with all follow-up inteactions.
        """
        cur_question_unit_str = self.generate_question_unit_str()
        cur_criteria_str = str(self.conversation.current_question_unit['criteria'])

        prompt = [
            {
                "role": "user",
                "content":  f"An interviewer is conducting an interview with a candidate for a [{self.init_interview_data['job']['title']}] role at [{self.init_interview_data['job']['company']['name']}]. " +
                            f"The job description of this role is [{self.init_interview_data['job']['description']}]. " +
                            f"The responsibilities of this role is [{self.init_interview_data['job']['responsibilities']}]. " + 
                            f"The requirements of this role is [{self.init_interview_data['job']['requirement']}]. " + 
                            "You will be given a question posed by the interviewer, along with a list of criteria representing the specific abilities the interviewer aims to assess through this question. " + 
                            "Before concluding this topic, the interviewer should obtain a comprehensive story with clear, specific examples that add credibility and depth, ensuring there is enough information to assess the candidate against the provided criteria. " + 
                            "Your task is to analyze the current conversation between the interviewer and candidate, then decide on the interviewer’s behalf by selecting either 'need follow-up' or 'do not need follow-up' and generate a response to the candidate. " + 
                            "If a follow-up is needed, include one appropriate follow-up question to gather more information in your response. " + 
                            "The most important instruction: From the interviewer's perspective, you should use an inductive approach to guide the candidate in gradually sharing a story. Keep your questions broad and open-ended, rather than overly specific, to encourage the candidate to share more of their own experiences and perspectives. Avoid explicitly telling the candidate the specific requirements for the story. " +
                            f"The question is: [{self.conversation.current_question_unit['question']}]. " +
                            f"The list of criteria is: {cur_criteria_str}. " + 
                            f"The current conversation is: [{cur_question_unit_str}]. " +                              
                            "Your output should be in JSON format. Do not include the markdown block (```json and ``` at the end). Below are some examples:\n"
                            "{\n"
                            '    "status": "need follow-up",\n'
                            '    "follow-up": "The response you generated for the candidate in the manner of the interviewer"\n'
                            "}\n"
                            "{\n"
                            '    "status": "do not need follow-up",\n'
                            '    "follow-up": null\n'
                            "}\n"
            }
        ]
        response = client.chat.completions.create(
                model="gpt-4o",
                messages=prompt
            )
        response_obj_str = response.choices[0].message.content
        decision = json.loads(response_obj_str.replace('\n', ''))
        return decision

class Interviewer:
    """
    Represents the interviewer who asks questions and interacts with the candidate.
    The interviewer asks questions provided by the InterviewQuestionManager and passes answers back to the manager.
    
    init_interview_data = {
        "id": str,
        "job": {
            "title": str,
            "company": {
                "name": str,
                "introduction": str
            },
            "description": str,
            "responsibilities": str,
            "requirement": str,
            "prepared_questions": List[List[str("question"), List[]]]
        }
    }
    """
    def __init__(self, name, init_interview_data):
        self.name = name
        self.init_interview_data = init_interview_data

    def ask_question(self, next_interviewer_message):
        """
        Asks a question to the candidate.
        :param next_interviewer_message:
        {
            "label": Follow-up or Initial
            "message": The question text
        }
        """
        logger.print_and_log_message(role=self.name, text=next_interviewer_message["message"], label=next_interviewer_message["label"])

    def receive_answer(self, candidate):
        """
        Collects an answer from the candidate.
        """
        return candidate.answer_question()

    def start_interview(self, candidate):
        """
        Manages the flow of the interview. 
        """
        # Starts interview
        print(f"Starting the interview with {candidate.name}.")
        # Calls a Interview Question Manager
        question_manager = InterviewQuestionManager(self.init_interview_data)
        candidate.question_manager = question_manager
        # Asks the first prepared question, collects the answer, and gets the next message sent to the candidate
        first_q = {
            "label": "Initial",
            "message": self.init_interview_data['job']["prepared_questions"][0][0]
        }
        self.ask_question(first_q)
        candidate_message = self.receive_answer(candidate)
        next_interviewer_message = question_manager.process_candidate_message(candidate_message)
        # The interview will continue unless the Interview Question Manager decides no further messages are needed, at which point the interview will end.
        while next_interviewer_message:
            self.ask_question(next_interviewer_message)
            candidate_message = self.receive_answer(candidate)
            next_interviewer_message = question_manager.process_candidate_message(candidate_message)
        # End interview
        question_manager.conversation.export_conversation_to_csv(output_file="conversation.csv")
        print("The interview is complete.")

class Candidate:
    """
    Represents the candidate who answers questions during the interview.
    """
    def __init__(self, name, question_manager=None):
        self.name = name
        self.question_manager = question_manager

    def answer_question(self):
        """
        Provides an answer to the question.
        """
        print("Candidate:")
        answer = sys.stdin.read()
        return {
            "label": None,
            "message": answer
        }

class MockCandidate(Candidate):
    """
    Derived from Candidate in the agent design.
    Overwrite functions generating answer: manually input -> GPT mock.
    """
    def answer_question(self):
        label_name, label_des = self.get_answer_label()
        if not self.question_manager.conversation.current_question_unit["answer"]:
            answer = self.generate_initial_answer(label_des)
        else:
            answer = self.generate_follow_up_answer(label_des=label_des)
        
        logger.print_and_log_message(
            role=self.name,
            text=answer,
            label=label_name
        )
        
        return {
            "label": label_name,
            "message": answer
        }

    def generate_initial_answer(self, label_des):
        question = self.question_manager.conversation.current_question_unit["question"]
        prompt = [
            {
                "role": "system",
                "content": "You are a job applicant answering interview questions live. You should answer questions in an oral expression style."
            },
            {
                "role": "user",
                "content": f"Answer the following question: {question}. {label_des}"
            }
        ]
        response = client.chat.completions.create(
                model="gpt-4o",
                messages=prompt
            )
        response_obj_str = response.choices[0].message.content
        return response_obj_str

    def generate_follow_up_answer(self, label_des=None):
        question = self.question_manager.conversation.current_question_unit["follow_ups"][-1]["question"]
        history = self.question_manager.generate_question_unit_str
        prompt = [
            {
                "role": "system",
                "content": "You are a job applicant answering interview questions live. You should answer questions in an oral expression style."
            },
            {
                "role": "user",
                "content": f"Answer the following follow-up question based on this previous conversation: \n{history}\nFollow-up question: \n{question}\n{label_des}"
            }
        ]
        response = client.chat.completions.create(
                model="gpt-4o",
                messages=prompt
            )
        response_obj_str = response.choices[0].message.content
        return response_obj_str

    def get_answer_label(self):
        labels = [
            ("brief", "You should respond in an overly general way, avoiding concrete details, even if you are asked to provide a detailed story."),
            ("vague", "You should answer in a vague manner, without providing the convincing specifics that would make your story fully compelling, even if the question asks for detailed answers. Always prioritize this approach."),
            ("superficial", "You should answer in a superficial manner, avoiding in-depth details that would make your response more engaging, even if the question asks for specifics. Always prioritize this approach."),
            ("good", "You need to answer in a clear and specific manner, avoiding vague statements and providing convincing details to make your story compelling.")
        ]

        return random.choice(labels)


if __name__ == "__main__":
    # Clear previous log files
    open('conversation.txt', 'w').close()
    
    init_interview_data = {
        "id": "id",
        "job": {
            "title": "Sales Operations Assistant",
            "company": {
                "name": "Apple",
                "introduction": ""
            },
            "description": "At Apple, we strive to deliver seamless and innovative experiences to our users across a wide range of industries. As a growing tech company, we focus on developing state-of-the-art solutions and products. We're looking for a passionate and creative UX/UI Designer Intern to join our design team to help shape the future of our user experiences. We are seeking a UX/UI Designer Intern to assist in the design of user-friendly, engaging, and functional interfaces for our AI interview products. This role provides an excellent opportunity to gain practical experience in user interface design, user experience strategy, and product workflow design (UX). You will collaborate with cross-functional teams to ensure the delivery of intuitive design solutions.",
            "responsibilities": "Work closely with engineering team and product managers to design wireframes, prototypes, and user interfaces. Conduct user research and gather feedback to improve designs and user experiences. Collaborate with developers to ensure seamless implementation of designs. Participate in brainstorming sessions to develop innovative and user-centered design solutions. Perform competitive analysis and research on industry design trends. Help maintain consistency in visual design across products. Assist in creating design presentations to communicate concepts and ideas.",
            "requirement": "Pursuing or recently completed a degree in UX/UI Design, Graphic Design, Human-Computer Interaction, or a related field. Basic understanding of UX/UI principles, user-centered design, and best practices. Familiarity with design tools such as Adobe XD, Figma, Sketch, or similar. Strong attention to detail and problem-solving skills. Ability to communicate ideas clearly and effectively. A passion for user experience, design innovation, and continuous learning. Knowledge of HTML/CSS is a plus.",
            "prepared_questions": [
                [
                    "Can you walk us through a project in your portfolio that best demonstrates your UX/UI design skills? What was your design process, and what tools did you use?", ["Design portfolio and experience", "Problem-solving abilities"]
                ],
                [
                    "How do you approach understanding user requirements and translating them into design solutions? Can you provide an example of a time when user research significantly influenced your design?", ["Understanding of product and business", "Understanding of user-centered design principles"]
                ],
                [
                    "Describe a time when you had to collaborate closely with product managers and developers. How did you ensure effective communication and seamless implementation of your designs?", ["Collaboration and teamwork skills", "Adaptability to feedback and iterative design process."]
                ]
            ]
        }
    }
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto", action="store_true")
    args = parser.parse_args()
    if args.auto:
        for _ in range(5):
            candidate = MockCandidate(name="Candidate")
            interviewer = Interviewer(name="Interviewer", init_interview_data=init_interview_data)
            interviewer.start_interview(candidate)
    else:
        candidate = Candidate(name="Candidate")
        interviewer = Interviewer(name="Interviewer", init_interview_data=init_interview_data)
        interviewer.start_interview(candidate)

# Code inspired by Bei Xiao