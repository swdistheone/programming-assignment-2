"""Module for the TrueFalse quiz item class in the Adaptive Review System."""

from typing import Union
from .question import Question
class TrueFalse(Question):

    def __init__(self, question: str, answer: bool, explanation: str = ""):
       
        if not isinstance(answer, bool):
            raise ValueError("The answer must be a boolean (True or False).")
        super().__init__(question, answer)
        self._explanation = explanation

    def ask(self) -> str:
        super().ask()
        return f"{self._question} (True/False)"

    def check_answer(self, answer: str) -> bool:
        normalized_answer = answer.strip().lower()
        if normalized_answer in ["true", "t"]:
            user_answer = True
        elif normalized_answer in ["false", "f"]:
            user_answer = False
        else:
            raise ValueError("Answer must be 'True' or 'False'.")
        return user_answer == self._answer

    def incorrect_feedback(self) -> str:
        feedback = "Incorrect."
        if self._explanation:
            feedback += " " + self._explanation
        return feedback