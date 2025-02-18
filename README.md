# Open-Bench

## Overview
A framework for evaluating LLM-based conversational agents through role-played interactions, using carefully designed personas and questionnaires to assess conversation quality and authenticity.

## Agents

### Agent A (Interviewer/Host/Salesperson)
- Leads the conversation by asking questions
- Supports multiple scenarios:
  - Job interviews
  - Podcast interviews
  - B2B negotiations
- Maintains conversation flow with:
  - Question quotas
  - Context awareness
  - Topic tracking
- Uses public information to guide questioning

### Agent B (Interviewee/Guest/Buyer)
- Responds based on detailed persona scripts
- Follows behavior patterns:
  - Normal: factual responses
  - Slight: minor embellishments
  - Extensive: fabricated stories
- Maintains consistency with:
  - Previous responses
  - Script boundaries
  - Behavioral patterns
- Tracks disclosed information

### Agent C (Evaluator)
- Analyzes conversations post-completion
- Performs two-step evaluation:
  1. Retrieves relevant conversation pieces
  2. Answers questionnaire based on evidence
- Computes metrics:
  - Answer accuracy
  - Response completeness
  - Behavior pattern recognition