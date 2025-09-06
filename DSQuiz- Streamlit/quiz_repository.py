"""
Quiz Repository for loading and managing quiz data
"""

import json
import os
from typing import Dict, List, Optional
import streamlit as st
from models import Field, Topic, Subtopic, Question, QuestionDifficulty


class QuizRepository:
    """Repository for managing quiz data"""
    
    def __init__(self, data_dir: str = "quiz_data"):
        self.data_dir = data_dir
        self._fields_cache: Optional[List[Field]] = None
        self._subtopics_cache: Dict[str, Subtopic] = {}
    
    @st.cache_data
    def _load_json_file(_self, file_path: str) -> dict:
        """Load JSON file with caching"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            st.error(f"Error loading {file_path}: {str(e)}")
            return {}
    
    def _parse_question(self, q_data: dict) -> Question:
        """Parse question data from JSON"""
        try:
            difficulty = QuestionDifficulty(q_data.get('difficulty', 'MEDIUM'))
        except ValueError:
            difficulty = QuestionDifficulty.MEDIUM
            
        return Question(
            id=q_data.get('id', ''),
            question=q_data.get('question', ''),
            options=q_data.get('options', []),
            correct_option_index=q_data.get('correctOptionIndex', 0),
            explanation=q_data.get('explanation', ''),
            option_explanations=q_data.get('optionExplanations', []),
            difficulty=difficulty,
            tags=q_data.get('tags', [])
        )
    
    def _parse_filename(self, filename: str) -> dict:
        """Parse filename to extract field, topic, and subtopic information"""
        # Format: FLD_DSC_TPC_MLG_150_STC_LRG.json
        parts = filename.replace('.json', '').split('_')
        
        if len(parts) < 7:
            return {}
            
        return {
            'field_id': f"{parts[0]}_{parts[1]}",  # FLD_DSC
            'topic_id': f"{parts[2]}_{parts[3]}",  # TPC_MLG
            'str_value': float(parts[4]) / 1000.0 if parts[4].isdigit() else 0.0,  # 150 -> 0.150
            'subtopic_id': f"{parts[5]}_{parts[6]}"  # STC_LRG
        }
    
    def load_subtopic_from_file(self, filename: str) -> Optional[Subtopic]:
        """Load a single subtopic from JSON file"""
        if filename in self._subtopics_cache:
            return self._subtopics_cache[filename]
            
        file_path = os.path.join(self.data_dir, filename)
        if not os.path.exists(file_path):
            return None
            
        data = self._load_json_file(file_path)
        if not data:
            return None
            
        # Parse questions
        questions = []
        for q_data in data.get('questions', []):
            question = self._parse_question(q_data)
            questions.append(question)
        
        # Create subtopic
        subtopic = Subtopic(
            id=data.get('subtopicId', ''),
            name=data.get('subtopicName', ''),
            topic_id=data.get('topicId', ''),
            field_id=data.get('fieldId', ''),
            str_value=data.get('str', 0.0),
            description=data.get('description', ''),
            total_questions=len(questions),
            file_name=filename,
            questions=questions
        )
        
        self._subtopics_cache[filename] = subtopic
        return subtopic
    
    @st.cache_data
    def get_all_fields(_self) -> List[Field]:
        """Get all available fields with their topics and subtopics"""
        if _self._fields_cache is not None:
            return _self._fields_cache
            
        fields_dict: Dict[str, Field] = {}
        topics_dict: Dict[str, Topic] = {}
        
        # Get all JSON files
        json_files = [f for f in os.listdir(_self.data_dir) if f.endswith('.json')]
        
        for filename in json_files:
            # Load the basic info from filename
            file_info = _self._parse_filename(filename)
            if not file_info:
                continue
                
            # Load the full data
            file_path = os.path.join(_self.data_dir, filename)
            data = _self._load_json_file(file_path)
            if not data:
                continue
                
            field_id = data.get('fieldId', '')
            topic_id = data.get('topicId', '')
            
            # Create field if not exists
            if field_id not in fields_dict:
                fields_dict[field_id] = Field(
                    id=field_id,
                    name=data.get('fieldName', ''),
                    description='',
                    topics=[]
                )
            
            # Create topic if not exists
            topic_key = f"{field_id}_{topic_id}"
            if topic_key not in topics_dict:
                topics_dict[topic_key] = Topic(
                    id=topic_id,
                    name=data.get('topicName', ''),
                    field_id=field_id,
                    description='',
                    subtopics=[]
                )
                fields_dict[field_id].topics.append(topics_dict[topic_key])
            
            # Load subtopic
            subtopic = _self.load_subtopic_from_file(filename)
            if subtopic:
                topics_dict[topic_key].subtopics.append(subtopic)
        
        # Sort subtopics by str_value within each topic
        for field in fields_dict.values():
            for topic in field.topics:
                topic.subtopics.sort(key=lambda x: x.str_value)
            
            # Sort topics in natural learning order
            field.topics.sort(key=lambda x: _self._get_topic_order(x.id))
        
        _self._fields_cache = list(fields_dict.values())
        return _self._fields_cache
    
    def _get_topic_order(self, topic_id: str) -> int:
        """Define natural learning order for topics"""
        topic_order = {
            'TPC_MLG': 1,  # Machine Learning - Start with fundamentals
            'TPC_DLG': 2,  # Deep Learning - Build on ML concepts
            'TPC_IMG': 3,  # Computer Vision - Specific application of DL
            'TPC_NLP': 4,  # Natural Language Processing - Another DL application
            'TPC_GAI': 5   # Generative AI - Advanced concepts
        }
        return topic_order.get(topic_id, 999)  # Unknown topics go to end
    
    def get_field_by_id(self, field_id: str) -> Optional[Field]:
        """Get field by ID"""
        fields = self.get_all_fields()
        for field in fields:
            if field.id == field_id:
                return field
        return None
    
    def get_topic_by_id(self, field_id: str, topic_id: str) -> Optional[Topic]:
        """Get topic by ID"""
        field = self.get_field_by_id(field_id)
        if field:
            for topic in field.topics:
                if topic.id == topic_id:
                    return topic
        return None
    
    def get_subtopic_by_id(self, field_id: str, topic_id: str, subtopic_id: str) -> Optional[Subtopic]:
        """Get subtopic by ID"""
        topic = self.get_topic_by_id(field_id, topic_id)
        if topic:
            for subtopic in topic.subtopics:
                if subtopic.id == subtopic_id:
                    return subtopic
        return None
    
    def get_questions_for_subtopic(self, field_id: str, topic_id: str, subtopic_id: str, 
                                 shuffle: bool = True, limit: Optional[int] = None) -> List[Question]:
        """Get questions for a specific subtopic"""
        subtopic = self.get_subtopic_by_id(field_id, topic_id, subtopic_id)
        if not subtopic:
            return []
            
        questions = subtopic.questions.copy()
        
        if shuffle:
            import random
            random.shuffle(questions)
            # Also shuffle individual question options
            questions = [q.shuffle_options() for q in questions]
        
        if limit:
            questions = questions[:limit]
            
        return questions 