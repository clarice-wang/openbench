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


## Response Style Evaluation (response_evaluation.py)

### Purpose
This script evaluates how accurately GPT-4 and Claude can generate interview responses matching specific response styles. It helps validate the models' ability to simulate various types of interview responses, from well-structured to problematic answers.

### What it Tests
The script evaluates 10 distinct response styles:

1. **Complete, Well-Organized**
   - Detailed responses with specific examples
   - Includes metrics and clear outcomes
   - Demonstrates structured planning and lessons learned
   - Example: "In my previous role, I managed a project across three departments. We followed agile methodology... This led to a 20% efficiency increase..."

2. **Brief, High-Level**
   - Overly condensed responses
   - Touches main points without depth
   - Lacks supporting details
   - Example: "I led a project with different teams. We used agile methods and completed it successfully."

3. **Abstract**
   - Uses metaphors instead of concrete examples
   - Focuses on general principles
   - Avoids specific experiences
   - Example: "Leadership is like navigating a ship through a storm..."

4. **Irrelevant**
   - Demonstrates skills but from unrelated contexts
   - Misaligned with question focus
   - Example: "I once organized a community bake sale..."

5. **Incomplete**
   - Starts describing relevant situations
   - Trails off without resolution
   - Example: "I managed a project that required coordination between multiple teams, and it was..."

6. **Rambling**
   - Long, meandering responses
   - Includes unnecessary details
   - Lacks clear organization
   - Example: "Well, there was this project I was working on, and it started with..."

7. **Vague**
   - General statements without specifics
   - Unclear references
   - Avoids concrete examples
   - Example: "I was involved in a project that had several challenges..."

8. **Tangential**
   - Starts relevant but shifts focus
   - Draws unexpected parallels
   - Example: "Speaking of projects, have you ever tried organizing a group trip?"

9. **Contradictory**
   - Contains conflicting statements
   - Undermines main points
   - Example: "I'm excellent at managing projects and always finish on time, except..."

10. **Defensive**
    - Deflects responsibility
    - Blames others
    - Example: "The project didn't go as planned, but that wasn't my fault..."

### Setup
1. Create a `.env` file with your API keys:

OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

2. Install requirements:

pip install -r requirements.txt

### How it Works
1. **Response Generation**
   - Generates 3 responses per style per model (60 total)
   - Provides style-specific examples to guide generation
   - Uses identical prompts across models

2. **Human Evaluation Process**
   - Blind evaluation (evaluator doesn't know model source)
   - Rates alignment with intended style (1-5 scale)
   - Collects qualitative feedback

3. **Comparative Analysis**
   - Per-model performance across styles
   - Style-specific success rates
   - Cross-model comparisons

### Example Output

=== Evaluation Summary ===

Model: gpt-4
Style: complete
Average Rating: 4.67/5.0
Number of Samples: 3
Rating Distribution:
  4: * (1)
  5: ** (2)

Model: claude-3
Style: complete
Average Rating: 4.33/5.0
Number of Samples: 3
Rating Distribution:
  4: * (1)
  5: ** (2)
...

### Data Collection
Results in `evaluation_results.json` include:
- Raw responses and ratings
- Model identification
- Style categorization
- Human evaluator notes
- Statistical analysis

### Research Applications
This evaluation helps:
1. Validate AI models' ability to generate nuanced interview responses
2. Compare model performance across different response styles
3. Identify areas where models excel or struggle
4. Inform prompt engineering strategies
5. Support research in interview simulation systems