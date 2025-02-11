import json
import os
import random
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
clientOpenAI = OpenAI(api_key=OPENAI_API_KEY)
clientAnthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

class ResponseEvaluator:
    def __init__(self):
        self.interview_questions = [
            "Tell me about a project you managed and what you learned from it.",
            "Describe a situation where you had to lead a team through a challenge.",
            # "What's your approach to handling complex problems?",
            # "Can you share an experience where you improved a process?",
            # "How do you ensure effective communication in team settings?"
        ]
        
        self.response_styles = [
            ("complete", "Provide a well-organized, detailed response with specific examples, metrics, and clear outcomes. Include context, methodology, and lessons learned."),
            
            ("brief", "Give an overly condensed response that touches main points but lacks detail. Keep it high-level and superficial."),
            
            ("abstract", "Answer with metaphors and general principles instead of concrete examples. Use analogies rather than actual experiences."),
            
            ("irrelevant", "Provide an answer that demonstrates skills but is not directly related to the question asked. Share an experience from a different context."),
            
            ("incomplete", "Start describing a relevant situation but trail off before providing any resolution or outcome."),
            
            ("rambling", "Give a long, meandering response that includes unnecessary details and tangents. Jump between different aspects without clear organization."),
            
            ("vague", "Respond with general statements and unclear references. Avoid specific details, numbers, or concrete examples."),
            
            ("tangential", "Begin with a relevant point but shift to discussing loosely related topics or drawing unexpected parallels."),
            
            ("contradictory", "Include statements that conflict with each other or undermine the main point being made."),
            
            ("defensive", "Describe a situation while deflecting responsibility and blaming others for any negative outcomes.")
        ]

        self.behavior_personas = [
            ("need_followup", """You are a job candidate who has relevant experience but struggles to communicate it effectively. 
            Your responses should:
            - Dance around the core answer without directly addressing it
            - Include hints at valuable experience that need to be drawn out
            - Show potential but lack specific details or concrete examples
            - Leave obvious openings for follow-up questions
            - Demonstrate nervousness or uncertainty in presentation, but not in capability"""),
            
            ("dead_end", """You are a job candidate who lacks the relevant experience but tries to hide this fact. 
            Your responses should:
            - Use industry buzzwords incorrectly or out of context
            - Make claims that reveal fundamental misunderstandings of basic concepts
            - Provide examples that demonstrate a lack of real-world experience
            - Include contradictions or impossible scenarios
            - Show confidence in delivery despite clear knowledge gaps""")
        ]

    def generate_response(self, question, style_instruction, behavior_instruction, model="gpt"):
        """Generate a response using either GPT or Claude."""
        prompt = f"""You are a job candidate answering interview questions.

        Response Style Instruction: {style_instruction}

        Behavior Persona Instruction: {behavior_instruction}

        Answer this interview question: {question}"""
        
        if model == "gpt":
            messages = [
                {"role": "system", "content": "You are a job candidate answering interview questions."},
                {"role": "user", "content": f"""Response Style Instruction: {style_instruction}

                Behavior Persona Instruction: {behavior_instruction}

                Answer this interview question: {question}"""}
            ]
            response = clientOpenAI.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
            return response.choices[0].message.content
        else:  # model == "claude"
            response = clientAnthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

    def generate_evaluation_set(self, num_samples_per_style=5):
        """Generate a set of responses for human evaluation from both models."""
        evaluation_data = []
        
        for style_name, style_instruction in self.response_styles:
            for behavior_name, behavior_instruction in self.behavior_personas:
                for _ in range(num_samples_per_style):
                    question = random.choice(self.interview_questions)
                    
                    # Generate responses from both models
                    gpt_response = self.generate_response(question, style_instruction, behavior_instruction, "gpt")
                    claude_response = self.generate_response(question, style_instruction, behavior_instruction, "claude")
                    
                    # Add GPT response
                    evaluation_data.append({
                        "question": question,
                        "response": gpt_response,
                        "model": "gpt-4",
                        "intended_style": style_name,
                        "style_instruction": style_instruction,
                        "intended_behavior": behavior_name,
                        "behavior_instruction": behavior_instruction,
                        "style_rating": None,
                        "behavior_rating": None,
                        "human_notes": None
                    })
                    
                    # Add Claude response
                    evaluation_data.append({
                        "question": question,
                        "response": claude_response,
                        "model": "claude-3",
                        "intended_style": style_name,
                        "style_instruction": style_instruction,
                        "intended_behavior": behavior_name,
                        "behavior_instruction": behavior_instruction,
                        "style_rating": None,
                        "behavior_rating": None,
                        "human_notes": None
                    })
        
        # Shuffle the data to prevent bias in evaluation
        random.shuffle(evaluation_data)
        return evaluation_data

    def conduct_human_evaluation(self, evaluation_data):
        """Conduct interactive human evaluation of responses."""
        print("\n=== Response Evaluation ===\n")
        print("Rate each response on two dimensions:")
        print("1. Style Rating: How well it matches its intended style (1-5)")
        print("2. Behavior Rating: How well it matches its intended behavior (1-5)")
        
        for i, item in enumerate(evaluation_data, 1):
            print(f"\n--- Sample {i}/{len(evaluation_data)} ---")
            print(f"\nQuestion: {item['question']}")
            print(f"\nResponse: {item['response']}")
            print(f"\nIntended Style: {item['intended_style']}")
            print(f"Style Description: {item['style_instruction']}")
            print(f"\nIntended Behavior: {item['intended_behavior']}")
            print(f"Behavior Description: {item['behavior_instruction']}")
            
            while True:
                try:
                    style_rating = int(input("\nStyle Rating (1-5): "))
                    if 1 <= style_rating <= 5:
                        break
                    print("Please enter a number between 1 and 5.")
                except ValueError:
                    print("Please enter a valid number.")
            
            while True:
                try:
                    behavior_rating = int(input("Behavior Rating (1-5): "))
                    if 1 <= behavior_rating <= 5:
                        break
                    print("Please enter a number between 1 and 5.")
                except ValueError:
                    print("Please enter a valid number.")
            
            notes = input("Additional notes (optional): ")
            
            item['style_rating'] = style_rating
            item['behavior_rating'] = behavior_rating
            item['human_notes'] = notes

        return evaluation_data

    def analyze_results(self, evaluated_data):
        """Analyze and summarize evaluation results by model, style, and behavior."""
        results = {}
        
        # Calculate statistics per model
        for model in ["gpt-4", "claude-3"]:
            results[model] = {
                'styles': {},
                'behaviors': {}
            }
            
            # Analyze style ratings
            for style_name, _ in self.response_styles:
                style_responses = [item for item in evaluated_data 
                                 if item['intended_style'] == style_name and item['model'] == model]
                
                if style_responses:
                    ratings = [r['style_rating'] for r in style_responses]
                    results[model]['styles'][style_name] = {
                        'average_rating': sum(ratings) / len(ratings),
                        'num_samples': len(ratings),
                        'rating_distribution': {i: ratings.count(i) for i in range(1, 6)}
                    }
            
            # Analyze behavior ratings
            for behavior_name, _ in self.behavior_personas:
                behavior_responses = [item for item in evaluated_data 
                                   if item['intended_behavior'] == behavior_name and item['model'] == model]
                
                if behavior_responses:
                    ratings = [r['behavior_rating'] for r in behavior_responses]
                    results[model]['behaviors'][behavior_name] = {
                        'average_rating': sum(ratings) / len(ratings),
                        'num_samples': len(ratings),
                        'rating_distribution': {i: ratings.count(i) for i in range(1, 6)}
                    }
        
        return results

    def save_results(self, evaluation_data, analysis_results, filename="evaluation_results.json"):
        """Save raw evaluation data and analysis results."""
        output = {
            'raw_evaluations': evaluation_data,
            'analysis': analysis_results
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)

def main():
    evaluator = ResponseEvaluator()
    
    # Generate evaluation set
    print("Generating responses for evaluation...")
    eval_data = evaluator.generate_evaluation_set(num_samples_per_style=2)
    
    # Conduct human evaluation
    print("\nStarting human evaluation...")
    evaluated_data = evaluator.conduct_human_evaluation(eval_data)
    
    # Analyze results
    print("\nAnalyzing results...")
    analysis = evaluator.analyze_results(evaluated_data)
    
    # Save results
    evaluator.save_results(evaluated_data, analysis)
    
    # Print summary
    print("\n=== Evaluation Summary ===")
    for model, model_results in analysis.items():
        print(f"\nModel: {model}")
        
        print("\nStyle Ratings:")
        for style, stats in model_results['styles'].items():
            print(f"\nStyle: {style}")
            print(f"Average Rating: {stats['average_rating']:.2f}/5.0")
            print(f"Number of Samples: {stats['num_samples']}")
            print("Rating Distribution:")
            for rating, count in stats['rating_distribution'].items():
                print(f"  {rating}: {'*' * count} ({count})")
        
        print("\nBehavior Ratings:")
        for behavior, stats in model_results['behaviors'].items():
            print(f"\nBehavior: {behavior}")
            print(f"Average Rating: {stats['average_rating']:.2f}/5.0")
            print(f"Number of Samples: {stats['num_samples']}")
            print("Rating Distribution:")
            for rating, count in stats['rating_distribution'].items():
                print(f"  {rating}: {'*' * count} ({count})")

if __name__ == "__main__":
    main()