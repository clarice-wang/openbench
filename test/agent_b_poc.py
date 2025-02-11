import sys
import os
sys.path.append('../src/')
import json
from oracle import Oracle
import agent_b
import prompts
from dotenv import load_dotenv

load_dotenv()

def test_agent_b(model_name, script_path):
    """Test Agent B with a specific model and script"""
    print(f"\nTesting Agent B with model: {model_name}")
    print("-" * 50)
    
    # Initialize Agent B
    agent = agent_b.Agent_B(
        script_path=script_path,
        backbone=model_name,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Sample interview questions to test responses
    test_questions = [
        "Can you tell me about your experience with Python?",
        "How comfortable are you with statistics?",
        "What's your strongest technical skill?",
        "Can you describe a challenging project you worked on?",
        "What areas are you looking to improve in?"
    ]
    
    # Run through test questions
    for i, question in enumerate(test_questions, 1):
        print(f"\nQ{i}: {question}")
        response = agent.respond(question)
        print(f"A: {response}")
        print("-" * 30)

def interactive_test(model_name, script_path):
    """Interactive testing of Agent B"""
    print(f"\nStarting interactive test with model: {model_name}")
    print("Type 'quit' to end the conversation")
    print("-" * 50)
    
    # Initialize Agent B
    agent = agent_b.Agent_B(
        script_path=script_path,
        backbone=model_name,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    while True:
        # Get interviewer's question
        question = input("\nInterviewer: ")
        
        if question.lower() in ['quit', 'exit', 'q']:
            break
            
        # Get response from Agent B
        try:
            response = agent.respond(question)
            print(f"Interviewee: {response}")
        except Exception as e:
            print(f"Error: {str(e)}")
            break
    
    print("\nConversation ended")
    print("Final conversation history:")
    print(agent.hist_conv)

def main():
    # Available scripts
    scripts = {
        "1": ("Fullstack Developer", "../scripts/fullstack_dev.json"),
        "2": ("Data Scientist", "../scripts/data_scientist.json"),
        "3": ("DevOps Engineer", "../scripts/devops_engineer.json")
    }
    
    # Available models
    models = {
        "1": "gpt-4o-mini",
        "2": "gpt-4o",
        # "3": "gemini-1.5-pro",
        # "4": "phi-3-mini",
        # "5": "llama-3-8B"
    }
    
    # Select script
    print("Available scripts:")
    for key, (name, _) in scripts.items():
        print(f"{key}: {name}")
    script_choice = input("Select script number: ")
    
    if script_choice not in scripts:
        print("Invalid script selection")
        return
        
    # Select model
    print("\nAvailable models:")
    for key, name in models.items():
        print(f"{key}: {name}")
    model_choice = input("Select model number: ")
    
    if model_choice not in models:
        print("Invalid model selection")
        return
    
    # Start interactive test
    interactive_test(models[model_choice], scripts[script_choice][1])

if __name__ == "__main__":
    # Ensure OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
        
    main()
