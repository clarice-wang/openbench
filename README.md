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


## Response Style Evaluation (response_evaluator.py)

### Purpose
This script serves as a proof of concept to validate whether GPT can consistently generate interview responses that match specific quality labels (brief, vague, superficial, and good). It helps establish the reliability of the mock candidate responses in the main interview simulation.

### What it Tests
The script evaluates GPT's ability to generate responses across four styles:
- **Brief**: Overly general responses lacking detail
- **Vague**: Responses missing convincing specifics
- **Superficial**: Surface-level answers without depth
- **Good**: Clear, specific responses with compelling details

### How it Works
1. **Response Generation**
   - Generates 3 responses per style (12 total)
   - Uses real interview questions
   - Applies style-specific instructions to GPT

2. **Human Evaluation Process**
   - Presents responses in random order to prevent bias
   - Shows:
     - Interview question
     - Generated response
     - Intended style
     - Style description
   - Collects:
     - Rating (1-5 scale)
     - Optional evaluator notes

3. **Analysis**
   - Calculates average ratings per style
   - Shows rating distribution
   - Saves raw data and analysis for further study

### Usage

1. Run the evaluator: `python3 response_evaluator.py`

2. For each response:
   - Read the question and response
   - Consider how well it matches the intended style
   - Rate from 1 (Poor match) to 5 (Perfect match)
   - Add optional notes about the response quality

3. Review results:
   - Terminal shows summary statistics
   - Full data saved to `evaluation_results.json`

### Data Collection
Results are saved in `evaluation_results.json` containing:
- Raw evaluation data
  - Questions and responses
  - Intended styles
  - Human ratings and notes
- Analysis per style
  - Average ratings
  - Sample counts
  - Rating distributions

### Using as Proof of Concept
This tool helps validate the interview simulation by:
1. Quantifying GPT's ability to generate style-specific responses
2. Collecting human evaluation data
3. Providing statistical evidence of response quality
4. Creating a dataset for future improvements

The results can be used to:
- Justify the use of GPT for mock interviews
- Identify which response styles work best
- Fine-tune style instructions
- Document the system's effectiveness