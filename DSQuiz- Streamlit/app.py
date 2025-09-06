"""
GnanaVana - Data Science Quiz Application
A Streamlit web app for testing and improving your Data Science knowledge
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional
import time
from datetime import datetime

from models import QuizSession, QuizResult, Question
from quiz_repository import QuizRepository
import base64
import os


# Page configuration
st.set_page_config(
    page_title="GnanaVriksha - Data Science Quiz",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Twitch Purple theme with dark mode support
st.markdown("""
<style>
    :root {
        --twitch-purple: #9146FF;
        --twitch-purple-light: #B294FF;
        --twitch-purple-dark: #6441A5;
        --correct-green: #00D884;
        --incorrect-red: #EB4335;
        --warning-amber: #FBBC04;
    }
    
    /* Dark mode variables */
    [data-theme="dark"] {
        --card-bg: #262730;
        --card-border: #464753;
        --text-color: #FAFAFA;
        --secondary-bg: #1E1E1E;
        --question-bg: #363647;
    }
    
    /* Light mode variables */
    [data-theme="light"], :root {
        --card-bg: #FFFFFF;
        --card-border: #E1E5E9;
        --text-color: #262730;
        --secondary-bg: #F8F9FA;
        --question-bg: #F8F9FA;
    }
    
    .main-header {
        background: linear-gradient(135deg, var(--twitch-purple) 0%, var(--twitch-purple-dark) 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white !important;
    }
    
    .quiz-card {
        background: var(--card-bg) !important;
        color: var(--text-color) !important;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid var(--twitch-purple);
        border: 1px solid var(--card-border);
    }
    
    .quiz-card h2, .quiz-card h3, .quiz-card p, .quiz-card li {
        color: var(--text-color) !important;
    }
    
    .question-card {
        background: var(--question-bg) !important;
        color: var(--text-color) !important;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid var(--card-border);
    }
    
    .question-card h3, .question-card h4, .question-card p {
        color: var(--text-color) !important;
    }
    
    .stats-card {
        background: linear-gradient(135deg, var(--twitch-purple-light), var(--twitch-purple));
        color: white !important;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .stats-card h2, .stats-card h3, .stats-card p {
        color: white !important;
    }
    
    .metric-card {
        background: var(--card-bg) !important;
        color: var(--text-color) !important;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid var(--card-border);
    }
    
    /* Logo container styling */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1rem;
        padding: 0.5rem;
        border-radius: 10px;
        background: #FFFFFF;
        border: 1px solid #E1E5E9;
    }
    
    .logo-container img {
        max-width: 100px;
        height: auto;
    }
    
    /* Sidebar header styling */
    .sidebar-header {
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, var(--twitch-purple-light), var(--twitch-purple));
        padding: 1rem;
        border-radius: 10px;
        color: white !important;
    }
    
    .sidebar-header h2 {
        color: white !important;
        margin-bottom: 0.5rem;
        font-size: 1.8rem !important;
        font-weight: bold;
    }
    
    .sidebar-header p {
        margin-bottom: 0.3rem;
        color: white !important;
    }
    
    /* Ensure text visibility in all modes */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--text-color) !important;
    }
    
    /* Fix selectbox and form elements in dark mode */
    .stSelectbox > div > div {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
    }
    
    .stRadio > div {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
    }
    
    /* Auto-detect dark mode */
    @media (prefers-color-scheme: dark) {
        :root {
            --card-bg: #262730;
            --card-border: #464753;
            --text-color: #FAFAFA;
            --secondary-bg: #1E1E1E;
            --question-bg: #363647;
        }
    }
    
    /* Compact layout styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    .element-container {
        margin-bottom: 0.5rem;
    }
    
    /* Reduce spacing in forms */
    .stRadio > div {
        gap: 0.25rem;
    }
    
    /* Compact metrics - ensure they're not cut off */
    [data-testid="metric-container"] {
        padding: 0.5rem 0.25rem;
        margin-top: 0.5rem;
    }
    
    /* Fix quiz metrics visibility */
    .quiz-metrics {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def get_logo_base64():
    """Get logo as base64 string for embedding"""
    logo_path = "GnanaVana just logo.png"  # Keep original logo file name
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


def initialize_session_state():
    """Initialize session state variables"""
    if 'repository' not in st.session_state:
        st.session_state.repository = QuizRepository()
    
    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = None
    
    if 'quiz_results' not in st.session_state:
        st.session_state.quiz_results = []
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    if 'selected_field' not in st.session_state:
        st.session_state.selected_field = None
    
    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = None
    
    if 'selected_subtopic' not in st.session_state:
        st.session_state.selected_subtopic = None
    
    if 'quiz_start_time' not in st.session_state:
        st.session_state.quiz_start_time = None


def render_compact_header():
    """Render a compact header for main content area"""
    st.markdown("# GnanaVriksha Quiz", help="Master Data Science Through Interactive Quizzes")


def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        # Logo with proper styling
        logo_b64 = get_logo_base64()
        if logo_b64:
            st.markdown("""
            <div class="logo-container">
                <img src="data:image/png;base64,{}" alt="GnanaVana Logo">
            </div>
            """.format(logo_b64), unsafe_allow_html=True)
        
        # Main header in sidebar
        st.markdown("""
        <div class="sidebar-header">
            <h2>GnanaVriksha</h2>
            <p><em>Master Data Science Through Interactive Quizzes</em></p>
            <p style="font-size: 0.9em;">Test your knowledge, learn from explanations, and track your progress</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add explanation for GnanaVriksha
        st.markdown("""
        <div style="background-color: rgba(145, 70, 255, 0.1); padding: 0.5rem; border-radius: 5px; margin-bottom: 1rem; font-size: 0.85em;">
            <strong>About the Name:</strong><br>
            <em>GnanaVriksha</em> is a Sanskrit term meaning "Tree of Knowledge" or "Wisdom Tree" 
            (Gnana = Knowledge/Wisdom, Vriksha = Tree). It represents the ancient Indian concept 
            of knowledge growing and branching like a tree, where each topic builds upon previous learning.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### Navigation")
        
        if st.button("Home", use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()
        
        if st.button("Start Quiz", use_container_width=True):
            st.session_state.current_page = 'select_topic'
            st.rerun()
        
        if st.button("Results", use_container_width=True):
            st.session_state.current_page = 'results'
            st.rerun()
        
        if st.button("About", use_container_width=True):
            st.session_state.current_page = 'about'
            st.rerun()
        
        # Show current quiz progress if active
        if st.session_state.current_quiz:
            st.markdown("---")
            st.markdown("### Quiz Progress")
            progress = (st.session_state.current_quiz.current_question_index + 1) / st.session_state.current_quiz.total_questions
            st.progress(progress)
            st.write(f"Question {st.session_state.current_quiz.current_question_index + 1} of {st.session_state.current_quiz.total_questions}")
            st.write(f"Score: {st.session_state.current_quiz.correct_answers}/{st.session_state.current_quiz.current_question_index}")


def render_home_page():
    """Render the home page"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stats-card">
            <h3>Topics</h3>
            <h2>5+</h2>
            <p>Comprehensive Coverage</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card">
            <h3>Questions</h3>
            <h2>1000+</h2>
            <p>Practice Questions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-card">
            <h3>Difficulty</h3>
            <h2>3 Levels</h2>
            <p>Easy to Hard</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Compact topics overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Topics Covered:")
        st.markdown("""
        - **Machine Learning:** Linear Regression, Decision Trees, Random Forest, SVM, and more
        - **Deep Learning:** Neural Networks, CNNs, RNNs, Transformers
        - **Generative AI:** LLMs, GANs, Diffusion Models, RAG
        - **Computer Vision:** Image Processing, Feature Detection
        - **Natural Language Processing:** Text Processing, Word Embeddings, Sentiment Analysis
        """)
    
    with col2:
        st.markdown("### Features:")
        st.markdown("""
        - Progressive difficulty levels for structured learning
        - Detailed explanations for each answer option
        - Performance tracking and analytics
        - Randomized questions and answer options
        - 1000+ carefully curated questions
        - Multiple difficulty levels (Easy, Medium, Hard)
        """)
    
    if st.button("Start Your Learning Journey", type="primary", use_container_width=True):
        st.session_state.current_page = 'select_topic'
        st.rerun()


def render_topic_selection():
    """Render the topic selection page"""
    st.markdown("## Select Your Quiz Topic")
    
    # Load fields
    fields = st.session_state.repository.get_all_fields()
    
    if not fields:
        st.error("No quiz data found. Please check the quiz_data directory.")
        return
    
    # Field selection
    field_names = [field.name for field in fields]
    selected_field_name = st.selectbox("Select Field:", field_names)
    
    selected_field = next((f for f in fields if f.name == selected_field_name), None)
    if not selected_field:
        return
    
    st.session_state.selected_field = selected_field
    
    # Topic selection
    if selected_field.topics:
        topic_names = [topic.name for topic in selected_field.topics]
        selected_topic_name = st.selectbox("Select Topic:", topic_names)
        
        selected_topic = next((t for t in selected_field.topics if t.name == selected_topic_name), None)
        if not selected_topic:
            return
        
        st.session_state.selected_topic = selected_topic
        
        # Subtopic selection
        if selected_topic.subtopics:
            st.markdown("### Available Subtopics")
            st.markdown("*Subtopics are ordered by learning progression*")
            
            # Quiz settings first
            st.markdown("---")
            st.markdown("### Quiz Settings")
            
            col1, col2 = st.columns(2)
            with col1:
                num_questions = st.slider("Number of Questions", 5, 50, 20)
            
            with col2:
                shuffle_questions = st.checkbox("Shuffle Questions", value=True)
            
            st.markdown("---")
            
            # Display subtopics with enhanced options
            for i, subtopic in enumerate(selected_topic.subtopics):
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{subtopic.name}**")
                        st.markdown(f"*{subtopic.description[:100]}...*" if len(subtopic.description) > 100 else subtopic.description)
                    
                    with col2:
                        st.metric("Total Questions", subtopic.total_questions)
                        st.metric("Quiz Questions", min(num_questions, subtopic.total_questions))
                    
                    with col3:
                        if st.button(f"Start Quiz", key=f"quiz_{i}", type="primary"):
                            start_quiz(selected_field, selected_topic, subtopic, num_questions, shuffle_questions)
                            return
                
                st.markdown("---")


def start_quiz(field, topic, subtopic, num_questions=20, shuffle_questions=True):
    """Start a new quiz"""
    questions = st.session_state.repository.get_questions_for_subtopic(
        field.id, topic.id, subtopic.id, shuffle=shuffle_questions, limit=num_questions
    )
    
    if not questions:
        st.error("No questions found for this subtopic.")
        return
    
    # Clean up any existing quiz session state
    keys_to_remove = [key for key in st.session_state.keys() if key.startswith(('answer_submitted_', 'user_answer_', 'is_correct_'))]
    for key in keys_to_remove:
        del st.session_state[key]
    
    # Create quiz session
    st.session_state.current_quiz = QuizSession(
        field_id=field.id,
        topic_id=topic.id,
        subtopic_id=subtopic.id,
        questions=questions,
        current_question_index=0,
        user_answers=[None] * len(questions),
        correct_answers=0,
        total_questions=len(questions),
        is_completed=False
    )
    
    st.session_state.quiz_start_time = datetime.now()
    st.session_state.current_page = 'quiz'
    st.rerun()


def render_quiz_page():
    """Render the active quiz page"""
    if not st.session_state.current_quiz:
        st.error("No active quiz found.")
        st.session_state.current_page = 'select_topic'
        st.rerun()
        return
    
    quiz = st.session_state.current_quiz
    current_question = quiz.get_current_question()
    
    if not current_question:
        st.error("Invalid question.")
        return
    
    # Add some top spacing for quiz page
    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
    
    # Compact quiz header with proper spacing
    st.markdown('<div class="quiz-metrics">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        progress = (quiz.current_question_index + 1) / quiz.total_questions
        st.progress(progress)
    with col2:
        st.metric("Question", f"{quiz.current_question_index + 1}/{quiz.total_questions}", label_visibility="collapsed")
    with col3:
        st.metric("Correct", quiz.correct_answers, label_visibility="collapsed")
    with col4:
        st.metric("Score", f"{quiz.get_score_percentage():.1f}%", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Compact question display
    st.markdown(f"**Question {quiz.current_question_index + 1}** | Difficulty: {current_question.difficulty.value}")
    st.markdown(f"### {current_question.question}")
    
    # Answer options
    st.markdown("### Select your answer:")
    
    # Check if answer has been submitted for this question
    answer_key = f"answer_submitted_{quiz.current_question_index}"
    if answer_key not in st.session_state:
        st.session_state[answer_key] = False
    
    if not st.session_state[answer_key]:
        # Show form for answer submission
        with st.form(key=f"question_{quiz.current_question_index}"):
            selected_option = st.radio(
                "Options:",
                options=range(len(current_question.options)),
                format_func=lambda x: f"{chr(65 + x)}. {current_question.options[x]}",
                key=f"option_{quiz.current_question_index}"
            )
            
            submitted = st.form_submit_button("Submit Answer", type="primary", use_container_width=True)
            
            if submitted:
                # Process answer
                is_correct = quiz.answer_question(selected_option)
                st.session_state[answer_key] = True
                st.session_state[f"user_answer_{quiz.current_question_index}"] = selected_option
                st.session_state[f"is_correct_{quiz.current_question_index}"] = is_correct
                st.rerun()
    
    else:
        # Show feedback and navigation after answer submission
        user_answer = st.session_state.get(f"user_answer_{quiz.current_question_index}")
        is_correct = st.session_state.get(f"is_correct_{quiz.current_question_index}")
        
        # Compact feedback display
        col1, col2 = st.columns([3, 1])
        with col1:
            if is_correct:
                st.success(f"Correct! {chr(65 + user_answer)}. {current_question.options[user_answer]}")
            else:
                st.error(f"Incorrect! Your answer: {chr(65 + user_answer)}. {current_question.options[user_answer]}")
                st.info(f"Correct: {chr(65 + current_question.correct_option_index)}. {current_question.options[current_question.correct_option_index]}")
        
        with col2:
            # Navigation button
            if quiz.current_question_index < quiz.total_questions - 1:
                if st.button("Next Question", type="primary", use_container_width=True):
                    quiz.next_question()
                    st.rerun()
            else:
                if st.button("Finish Quiz", type="primary", use_container_width=True):
                    finish_quiz()
                    st.rerun()
        
        # Explanation section (expanded by default)
        with st.expander("Explanation", expanded=True):
            st.markdown(current_question.explanation)
            
            # Show option explanations if available
            if current_question.option_explanations:
                st.markdown("**Option Explanations:**")
                for i, explanation in enumerate(current_question.option_explanations):
                    if explanation:
                        st.markdown(f"**{chr(65 + i)}.** {explanation}")


def finish_quiz():
    """Finish the current quiz and show results"""
    if not st.session_state.current_quiz:
        return
    
    quiz = st.session_state.current_quiz
    quiz.is_completed = True
    
    # Calculate time taken
    time_taken = None
    if st.session_state.quiz_start_time:
        elapsed = datetime.now() - st.session_state.quiz_start_time
        time_taken = str(elapsed).split('.')[0]  # Remove microseconds
    
    # Get topic and subtopic names
    field = st.session_state.repository.get_field_by_id(quiz.field_id)
    topic = st.session_state.repository.get_topic_by_id(quiz.field_id, quiz.topic_id)
    subtopic = st.session_state.repository.get_subtopic_by_id(quiz.field_id, quiz.topic_id, quiz.subtopic_id)
    
    # Calculate difficulty breakdown
    difficulty_breakdown = {'EASY': 0, 'MEDIUM': 0, 'HARD': 0}
    incorrect_questions = []
    
    for i, question in enumerate(quiz.questions):
        if quiz.user_answers[i] != question.correct_option_index:
            incorrect_questions.append(question)
        else:
            difficulty_breakdown[question.difficulty.value] += 1
    
    # Create result
    result = QuizResult(
        field_name=field.name if field else "Unknown",
        topic_name=topic.name if topic else "Unknown",
        subtopic_name=subtopic.name if subtopic else "Unknown",
        score=quiz.correct_answers,
        total_questions=quiz.total_questions,
        percentage=quiz.get_score_percentage(),
        time_taken=time_taken,
        difficulty_breakdown=difficulty_breakdown,
        incorrect_questions=incorrect_questions
    )
    
    # Save result
    st.session_state.quiz_results.append(result)
    st.session_state.current_quiz = None
    st.session_state.current_page = 'quiz_result'


def render_quiz_result():
    """Render quiz results page"""
    if not st.session_state.quiz_results:
        st.error("No quiz results found.")
        return
    
    result = st.session_state.quiz_results[-1]  # Latest result
    
    st.markdown("## Quiz Completed!")
    
    # Score overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Final Score", f"{result.score}/{result.total_questions}")
    
    with col2:
        st.metric("Percentage", f"{result.percentage:.1f}%")
    
    with col3:
        st.metric("Time Taken", result.time_taken or "Unknown")
    
    with col4:
        grade = "A+" if result.percentage >= 90 else "A" if result.percentage >= 80 else "B" if result.percentage >= 70 else "C" if result.percentage >= 60 else "D"
        st.metric("Grade", grade)
    
    # Performance visualization
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = result.percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Quiz Performance"},
        delta = {'reference': 70},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#9146FF"},
            'steps': [
                {'range': [0, 50], 'color': "#FFCCCB"},
                {'range': [50, 80], 'color': "#FFFFCC"},
                {'range': [80, 100], 'color': "#90EE90"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    # Quiz details
    st.markdown(f"""
    <div class="quiz-card">
        <h3>Quiz Details</h3>
        <p><strong>Topic:</strong> {result.topic_name}</p>
        <p><strong>Subtopic:</strong> {result.subtopic_name}</p>
        <p><strong>Total Questions:</strong> {result.total_questions}</p>
        <p><strong>Correct Answers:</strong> {result.score}</p>
        <p><strong>Incorrect Answers:</strong> {result.total_questions - result.score}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Difficulty breakdown
    if result.difficulty_breakdown:
        df_difficulty = pd.DataFrame.from_dict(result.difficulty_breakdown, orient='index', columns=['Correct'])
        df_difficulty.index.name = 'Difficulty'
        
        fig = px.bar(df_difficulty, y=df_difficulty.index, x='Correct', 
                     title="Correct Answers by Difficulty",
                     color_discrete_sequence=['#9146FF'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Incorrect questions review
    if result.incorrect_questions:
        st.markdown("### Review Incorrect Questions")
        for i, question in enumerate(result.incorrect_questions):
            with st.expander(f"Question {i+1}: {question.question[:50]}..."):
                st.markdown(f"**Question:** {question.question}")
                st.markdown(f"**Correct Answer:** {chr(65 + question.correct_option_index)}. {question.options[question.correct_option_index]}")
                st.markdown(f"**Explanation:** {question.explanation}")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Take Another Quiz", type="primary", use_container_width=True):
            st.session_state.current_page = 'select_topic'
            st.rerun()
    
    with col2:
        if st.button("View All Results", use_container_width=True):
            st.session_state.current_page = 'results'
            st.rerun()


def render_results_page():
    """Render the results history page"""
    st.markdown("## Quiz Results History")
    
    if not st.session_state.quiz_results:
        st.info("No quiz results yet. Take a quiz to see your performance!")
        if st.button("Start Quiz", type="primary"):
            st.session_state.current_page = 'select_topic'
            st.rerun()
        return
    
    # Results summary
    total_quizzes = len(st.session_state.quiz_results)
    avg_score = sum(r.percentage for r in st.session_state.quiz_results) / total_quizzes
    total_questions = sum(r.total_questions for r in st.session_state.quiz_results)
    total_correct = sum(r.score for r in st.session_state.quiz_results)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Quizzes", total_quizzes)
    with col2:
        st.metric("Average Score", f"{avg_score:.1f}%")
    with col3:
        st.metric("Total Questions", total_questions)
    with col4:
        st.metric("Overall Accuracy", f"{(total_correct/total_questions)*100:.1f}%")
    
    # Results table
    results_data = []
    for i, result in enumerate(st.session_state.quiz_results):
        results_data.append({
            'Quiz #': i + 1,
            'Topic': result.topic_name,
            'Subtopic': result.subtopic_name,
            'Score': f"{result.score}/{result.total_questions}",
            'Percentage': f"{result.percentage:.1f}%",
            'Time': result.time_taken or "Unknown"
        })
    
    df = pd.DataFrame(results_data)
    st.dataframe(df, use_container_width=True)
    
    # Performance trend
    if len(st.session_state.quiz_results) > 1:
        scores = [r.percentage for r in st.session_state.quiz_results]
        fig = px.line(x=list(range(1, len(scores) + 1)), y=scores,
                      title="Performance Trend",
                      labels={'x': 'Quiz Number', 'y': 'Score (%)'})
        fig.update_traces(line_color='#9146FF')
        st.plotly_chart(fig, use_container_width=True)


def render_about_page():
    """Render the about page"""
    st.markdown("""
    <div class="quiz-card">
        <h2>About GnanaVriksha</h2>
        <p>
        GnanaVriksha is a comprehensive Data Science quiz platform designed to help learners test and 
        improve their knowledge across various topics in Data Science, Machine Learning, and AI.
        The name "GnanaVriksha" means "Tree of Knowledge" in Sanskrit, reflecting how learning branches 
        and grows from foundational concepts to advanced topics.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Mission")
    st.markdown("""
    To provide an interactive and engaging platform for Data Science enthusiasts to assess their knowledge,
    learn from detailed explanations, and track their progress in their learning journey. Like a tree of knowledge,
    GnanaVriksha helps learners build strong foundations and grow their understanding systematically.
    """)
    
    st.markdown("### Features")
    st.markdown("""
    - **Comprehensive Coverage:** Questions covering ML, DL, AI, Computer Vision, and NLP
    - **Progressive Learning:** Subtopics ordered by learning difficulty
    - **Detailed Explanations:** Learn from both correct and incorrect answers
    - **Performance Tracking:** Monitor your progress over time
    - **Randomized Questions:** Different experience each time
    - **Modern UI:** Clean, responsive design for optimal learning
    """)
    
    st.markdown("### How to Use")
    st.markdown("""
    1. Select a topic and subtopic from the quiz section
    2. Choose your quiz settings (number of questions, etc.)
    3. Answer questions and read the explanations
    4. Review your results and learn from mistakes
    5. Track your progress over time
    """)
    
    st.markdown("### Topics Covered")
    st.markdown("""
    - **Machine Learning:** Fundamentals, Supervised/Unsupervised Learning, Algorithms
    - **Deep Learning:** Neural Networks, CNNs, RNNs, Transformers
    - **Generative AI:** LLMs, GANs, Diffusion Models, RAG, Fine-tuning
    - **Computer Vision:** Image Processing, Feature Detection, Object Recognition
    - **Natural Language Processing:** Text Processing, Embeddings, Sentiment Analysis
    """)


def main():
    """Main application function"""
    initialize_session_state()
    render_sidebar()
    
    # Show compact header for all pages except quiz
    if st.session_state.current_page != 'quiz':
        render_compact_header()
    
    # Route to appropriate page
    if st.session_state.current_page == 'home':
        render_home_page()
    elif st.session_state.current_page == 'select_topic':
        render_topic_selection()
    elif st.session_state.current_page == 'quiz':
        render_quiz_page()
    elif st.session_state.current_page == 'quiz_result':
        render_quiz_result()
    elif st.session_state.current_page == 'results':
        render_results_page()
    elif st.session_state.current_page == 'about':
        render_about_page()


if __name__ == "__main__":
    main() 