"""
Data models for GnanaVana Quiz Application
Mirrors the Android app's data structure
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
import random


class QuestionDifficulty(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


@dataclass
class Question:
    """Represents a multiple-choice question in GnanaVana"""
    id: str
    question: str
    options: List[str]
    correct_option_index: int
    explanation: str
    option_explanations: List[str]
    difficulty: QuestionDifficulty
    tags: List[str]
    
    def shuffle_options(self) -> 'Question':
        """Returns a shuffled version of this question with options in random order"""
        shuffled_indices = list(range(len(self.options)))
        random.shuffle(shuffled_indices)
        
        shuffled_options = [self.options[i] for i in shuffled_indices]
        shuffled_explanations = []
        if len(self.option_explanations) == len(self.options):
            shuffled_explanations = [self.option_explanations[i] for i in shuffled_indices]
        else:
            shuffled_explanations = self.option_explanations
            
        new_correct_index = shuffled_indices.index(self.correct_option_index)
        
        return Question(
            id=self.id,
            question=self.question,
            options=shuffled_options,
            correct_option_index=new_correct_index,
            explanation=self.explanation,
            option_explanations=shuffled_explanations,
            difficulty=self.difficulty,
            tags=self.tags
        )


@dataclass
class Subtopic:
    """Represents a Subtopic (Leaf) in the GnanaVana knowledge hierarchy"""
    id: str
    name: str
    topic_id: str
    field_id: str
    str_value: float  # Subtopic Rank for ordering
    description: str
    total_questions: int
    file_name: str
    questions: List[Question]


@dataclass
class Topic:
    """Represents a Topic (Branch) in the GnanaVana knowledge hierarchy"""
    id: str
    name: str
    field_id: str
    description: str
    subtopics: List[Subtopic]


@dataclass
class Field:
    """Represents a Field (Tree) in the GnanaVana knowledge hierarchy"""
    id: str
    name: str
    description: str
    topics: List[Topic]


@dataclass
class QuizSession:
    """Represents an active quiz session"""
    field_id: str
    topic_id: str
    subtopic_id: str
    questions: List[Question]
    current_question_index: int
    user_answers: List[Optional[int]]
    correct_answers: int
    total_questions: int
    is_completed: bool
    
    def get_current_question(self) -> Optional[Question]:
        """Get the current question"""
        if 0 <= self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None
    
    def answer_question(self, answer_index: int) -> bool:
        """Answer the current question and return if correct"""
        if self.current_question_index < len(self.questions):
            self.user_answers[self.current_question_index] = answer_index
            current_question = self.questions[self.current_question_index]
            is_correct = answer_index == current_question.correct_option_index
            if is_correct:
                self.correct_answers += 1
            return is_correct
        return False
    
    def next_question(self) -> bool:
        """Move to next question, return True if there are more questions"""
        self.current_question_index += 1
        if self.current_question_index >= len(self.questions):
            self.is_completed = True
            return False
        return True
    
    def get_score_percentage(self) -> float:
        """Get the score as a percentage"""
        if self.total_questions > 0:
            return (self.correct_answers / self.total_questions) * 100
        return 0.0


@dataclass
class QuizResult:
    """Represents quiz results"""
    field_name: str
    topic_name: str
    subtopic_name: str
    score: int
    total_questions: int
    percentage: float
    time_taken: Optional[str]
    difficulty_breakdown: dict
    incorrect_questions: List[Question] 