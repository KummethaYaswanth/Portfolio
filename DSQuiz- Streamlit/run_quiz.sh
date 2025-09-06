#!/bin/bash

echo "Starting GnanaVriksha Data Science Quiz Platform..."
echo "Tree of Knowledge - Master Data Science Through Interactive Quizzes"
echo ""

# Activate virtual environment
source DSQuiz/bin/activate

# Check if streamlit is installed
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Launch the application
echo "Launching application..."
echo "Open your browser to http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""
streamlit run app.py 