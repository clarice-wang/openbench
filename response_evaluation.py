import json
import os
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

class ResponseEvaluator:
    def __init__(self):
        self.interview_questions = [
            "Can you walk us through a project in your portfolio that best demonstrates your UX/UI design skills?",
            "Tell me about a time when you had to handle a difficult client situation.",
            "Describe your most significant leadership experience.",
            "What's the most innovative solution you've implemented?",
            "How do you approach learning new technologies?"
        ]
        
        self.response_styles = [
            ("brief", "You should respond in an overly general way, avoiding concrete details, even if you are asked to provide a detailed story."),
            ("vague", "You should answer in a vague manner, without providing the convincing specifics that would make your story fully compelling."),
            ("superficial", "You should answer in a superficial manner, avoiding in-depth details that would make your response more engaging."),
            ("good", "You need to answer in a clear and specific manner, providing convincing details to make your story compelling.")
        ]

    def generate_response(self, question, style_instruction):
        """Generate a response using GPT for a given question and style."""
        prompt = [
            {
                "role": "system",
                "content": "You are a job candidate answering interview questions. " + style_instruction
            },
            {
                "role": "user",
                "content": f"Answer this interview question: {question}"
            }
        ]
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=prompt
        )
        return response.choices[0].message.content

    def generate_evaluation_set(self, num_samples_per_style=5):
        """Generate a set of responses for human evaluation."""
        evaluation_data = []
        
        for style_name, style_instruction in self.response_styles:
            for _ in range(num_samples_per_style):
                question = random.choice(self.interview_questions)
                response = self.generate_response(question, style_instruction)
                
                evaluation_data.append({
                    "question": question,
                    "response": response,
                    "intended_style": style_name,
                    "style_instruction": style_instruction,
                    "human_rating": None,
                    "human_notes": None
                })
        
        # Shuffle the data to prevent bias in evaluation
        random.shuffle(evaluation_data)
        return evaluation_data

    def conduct_human_evaluation(self, evaluation_data):
        """Conduct interactive human evaluation of responses."""
        print("\n=== Response Style Evaluation ===\n")
        print("Rate each response on how well it matches its intended style.")
        print("Rating scale: 1 (Poor match) to 5 (Perfect match)")
        
        for i, item in enumerate(evaluation_data, 1):
            print(f"\n--- Sample {i}/{len(evaluation_data)} ---")
            print(f"\nQuestion: {item['question']}")
            print(f"\nResponse: {item['response']}")
            print(f"\nIntended Style: {item['intended_style']}")
            print(f"Style Description: {item['style_instruction']}")
            
            while True:
                try:
                    rating = int(input("\nRating (1-5): "))
                    if 1 <= rating <= 5:
                        break
                    print("Please enter a number between 1 and 5.")
                except ValueError:
                    print("Please enter a valid number.")
            
            notes = input("Additional notes (optional): ")
            
            item['human_rating'] = rating
            item['human_notes'] = notes

        return evaluation_data

    def analyze_results(self, evaluated_data):
        """Analyze and summarize evaluation results."""
        results = {}
        
        # Calculate statistics per style
        for style_name, _ in self.response_styles:
            style_responses = [item for item in evaluated_data 
                             if item['intended_style'] == style_name]
            
            if style_responses:
                ratings = [r['human_rating'] for r in style_responses]
                results[style_name] = {
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
    eval_data = evaluator.generate_evaluation_set(num_samples_per_style=3)
    
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
    for style, stats in analysis.items():
        print(f"\nStyle: {style}")
        print(f"Average Rating: {stats['average_rating']:.2f}/5.0")
        print(f"Number of Samples: {stats['num_samples']}")
        print("Rating Distribution:")
        for rating, count in stats['rating_distribution'].items():
            print(f"  {rating}: {'*' * count} ({count})")

if __name__ == "__main__":
    main()