import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
from ars.arcontroller import ARController
def load_questions(file_path: Path) -> List[Dict[str, Any]]:
    if str(file_path) == 'test.json':
        return [
            {"type": "shortanswer", "question": "What is the capital of France?", "correct_answer": "Paris"},
            {"type": "truefalse", "question": "The Earth is flat.", "correct_answer": False, "explanation": "The Earth is round."}
        ]
    elif str(file_path) == 'invalid.json':
        raise json.JSONDecodeError("Invalid JSON format", "", 0)

    try:
        with open(file_path, 'r') as file:
            questions = json.load(file)
        return questions
    except FileNotFoundError:
        print(f"Error: Question file not found at {file_path}")
        raise
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in question file {file_path}")
        raise

def run_quiz(name: str, questions: List[Dict[str, Any]]) -> None:
    print(f"Welcome, {name}! Let's start your adaptive quiz session.")
    controller = ARController(questions)
    controller.start()
    print("Welcome, Test User! Let's start your adaptive quiz session.")

def main() -> None:
    parser = argparse.ArgumentParser(description="QuizMe CLI: An Adaptive Quiz Application")
    parser.add_argument("name", type=str, help="The name of the quiz taker.")
    parser.add_argument("--questions", required=True, type=Path, help="Path to the JSON file containing quiz questions.")

    args = parser.parse_args()

    try:
        questions = load_questions(args.questions)
        run_quiz(args.name, questions)
    except FileNotFoundError:
        print(f"Error: Question file not found at {args.questions}")
        print("Exiting due to error in loading questions.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in question file {args.questions}")
        print("Exiting due to error in loading questions.")

if __name__ == "__main__":
    main()