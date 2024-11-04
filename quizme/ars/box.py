"""Module for the Box class in the Adaptive Review System."""

from datetime import datetime, timedelta
from typing import List, Optional
from .qtype.question import Question  
class Box:
    
    def __init__(self, name: str, priority_interval: timedelta):
        
        self._name = name
        self._questions: List[Question] = []
        self._priority_interval = priority_interval

    @property
    def name(self) -> str:
        return self._name

    @property
    def priority_interval(self) -> timedelta:
        return self._priority_interval
    def add_question(self, question: Question) -> None:
        if question not in self._questions:
            self._questions.append(question)

    def remove_question(self, question: Question) -> None:
        
        if question in self._questions:
            self._questions.remove(question)

    def get_next_priority_question(self) -> Optional[Question]:
       
        now = datetime.now()
        sorted_questions = sorted(self._questions, key=lambda q: q.last_asked or datetime.min)
        for question in sorted_questions:
            if (now - (question.last_asked or datetime.min)) >= self._priority_interval:
                return question
        return None

    def __len__(self) -> int:
        
        return len(self._questions)

    def __str__(self) -> str:

        return f"Box(name='{self._name}', questions_count={len(self._questions)})"