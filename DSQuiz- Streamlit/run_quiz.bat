@echo off
echo Starting GnanaVriksha Data Science Quiz Platform...
echo Tree of Knowledge - Master Data Science Through Interactive Quizzes
echo.

REM Activate virtual environment
call DSQuiz\Scripts\activate

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Launch the application
echo Launching application...
echo Open your browser to http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
streamlit run app.py

pause 