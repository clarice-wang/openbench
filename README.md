# Interview Simulation

This Python script simulates a job interview between an interviewer and a candidate. It can run in two modes:
1. Interactive mode where you provide responses through the terminal
2. Automated mode where GPT generates candidate responses

## Setup

1. Clone the repository
2. Create a `.env` file in the root directory with your OpenAI API key.
3. Install the required packages: `pip install -r requirements.txt`.


## Usage

### Interactive Mode
Run the simulation with real user input: `python3 simulation.py`.
- The interviewer will ask questions
- Type your responses in the terminal
- Press Ctrl+D (Unix) or Ctrl+Z (Windows) to submit each answer

### Automated Mode
Run the simulation with GPT-generated responses: `python3 simulation.py --auto`.
- This will run 5 automated interviews
- GPT will generate responses with random styles (brief, vague, superficial, or good)
- All interactions are logged

## Output Files

### conversation.txt
A detailed log of the interview dialogue, including:
- Interviewer questions (labeled as Initial or Follow-up)
- Candidate responses (with response style labels)
- Clear formatting with separators


### conversation.csv
A structured record of all interviews with columns for:
- Initial questions and their evaluation criteria
- Candidate answers and their style labels
- Follow-up questions and responses
- Clear tracking of conversation flow


## Notes
- `conversation.txt` is cleared at the start of each run
- The simulation uses GPT-4o for generating responses in automated mode
- The interview questions are configured for a UX/UI Designer position but can be modified in the code