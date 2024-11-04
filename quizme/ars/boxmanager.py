from datetime import timedelta
from typing import List, Dict, Optional
from .box import Box
from .qtype.question import Question  # Explicitly import Question for type hinting
class BoxManager:
    def __init__(self):
        self._boxes: List[Box] = [
            Box("Missed Questions", timedelta(seconds=60)),
            Box("Unasked Questions", timedelta(seconds=0)),
            Box("Correctly Answered Once", timedelta(seconds=180)),
            Box("Correctly Answered Twice", timedelta(seconds=360)),
            Box("Known Questions", timedelta.max)
        ]
        self._question_location: Dict[str, int] = {}

    def add_new_question(self, question: Question) -> None:
        
        self._boxes[1].add_question(question)
        self._question_location[str(question.id)] = 1

    def move_question(self, question: Question, answered_correctly: bool) -> None:
        
        current_index = self._question_location.get(str(question.id))
        if current_index is None:
            return  

        new_index = 0  
        if answered_correctly:
            if current_index == 0:
                new_index = 2  
            else:
                new_index = min(current_index + 1, len(self._boxes) - 1)
        
       
        self._boxes[current_index].remove_question(question)
        self._boxes[new_index].add_question(question)
        self._question_location[str(question.id)] = new_index
        self._log_box_counts()

    def get_next_question(self) -> Optional[Question]:
        for box in self._boxes[:-1]:  
            question = box.get_next_priority_question()
            if question:
                return question
        return None

    def _log_box_counts(self) -> None:
        for box in self._boxes:
            print(f"{box.name}: {len(box)} questions")