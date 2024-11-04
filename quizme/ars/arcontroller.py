"""Core module for running the Adaptive Review System (ARS) session."""

from typing import List, Dict, Any
from .boxmanager import BoxManager
class ARController:
    def __init__(self, question_data: List[Dict[str, Any]]):
        self._box_manager = BoxManager()
        self._initialize_questions(question_data)

    def _initialize_questions(self, question_data: List[Dict[str, Any]]) -> None:
        for q_data in question_data:
            question_type = q_data.get("type")
            try:
                if question_type == "shortanswer":
                    from .qtype.shortanswer import ShortAnswer
                    question = ShortAnswer(
                        q_data["question"],
                        q_data["correct_answer"],
                        q_data.get("case_sensitive", False)
                    )
                elif question_type == "truefalse":
                    from .qtype.truefalse import TrueFalse
                    question = TrueFalse(
                        q_data["question"],
                        q_data["correct_answer"],
                        q_data.get("explanation", "")
                    )
                else:
                    print(f"Unsupported question type: {question_type}. Skipping this question.")
                    continue
                self._box_manager.add_new_question(question)
            except KeyError as e:
                field_name = e.args[0]
                print(f"Missing required field for question: '{field_name}'. Skipping this question.")

    def start(self) -> None:
        print("Type 'q' at any time to quit the session.")

        while True:
            question = self._box_manager.get_next_question()
            if not question:
                print("All questions have been reviewed. Session complete!")
                break

            print(question.ask())
            user_answer = input("Your answer: ")
            if user_answer.strip().lower() == 'q':
                break

            try:
                correct = question.check_answer(user_answer)
            except ValueError:
                print("Invalid input: Answer must be 'True' or 'False'.")
                continue

            if correct:
                print("Correct!")
            else:
                print(question.incorrect_feedback())
            self._box_manager.move_question(question, correct)
        print("Thank you, goodbye!")