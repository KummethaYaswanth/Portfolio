# 🧠 GnanaVriksha - Data Science Quiz Platform

A comprehensive Streamlit web application for testing and improving your Data Science knowledge through interactive quizzes.

**About the Name:** *GnanaVriksha* is a Sanskrit term meaning "Tree of Knowledge" or "Wisdom Tree" (Gnana = Knowledge/Wisdom, Vriksha = Tree). It represents the ancient Indian concept of knowledge growing and branching like a tree, where each topic builds upon previous learning.

![GnanaVriksha Logo](GnanaVana%20just%20logo.png)

## ✨ Features

- **Comprehensive Coverage**: 1000+ questions across Machine Learning, Deep Learning, Generative AI, Computer Vision, and NLP
- **Progressive Learning**: Subtopics ordered by learning difficulty for structured progress
- **Interactive Quizzes**: Multiple choice questions with immediate feedback
- **Detailed Explanations**: Learn from both correct and incorrect answers
- **Performance Tracking**: Monitor your progress over time with analytics
- **Modern UI**: Clean, responsive design with purple theme
- **Randomized Content**: Different experience each time with shuffled questions and options
- **Performance Analytics**: Detailed results with charts and breakdowns

## 📚 Topics Covered

### Machine Learning
- Linear Regression, Logistic Regression
- Decision Trees, Random Forest
- Support Vector Machines (SVM)
- K-Means Clustering, Hierarchical Clustering
- Naive Bayes, K-Nearest Neighbors
- Gradient Boosting, Feature Engineering
- Model Evaluation, Time Series Analysis

### Deep Learning
- Neural Network Basics
- Convolutional Neural Networks (CNNs)
- Recurrent Neural Networks (RNNs)
- Transformers

### Generative AI
- Large Language Models (LLMs)
- Prompt Engineering
- Generative Adversarial Networks (GANs)
- Diffusion Models
- Retrieval Augmented Generation (RAG)
- Fine-tuning
- RLHF (Reinforcement Learning from Human Feedback)
- Multi-Modal AI
- AI Ethics

### Computer Vision
- Image Fundamentals
- Image Feature Extraction
- Feature Detection

### Natural Language Processing
- Text Preprocessing
- Word Embeddings
- Sentiment Analysis

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd DSQuiz-Streamlit
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv DSQuiz
   DSQuiz\Scripts\activate
   
   # macOS/Linux
   python -m venv DSQuiz
   source DSQuiz/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to that URL

## 🎯 How to Use

1. **Start**: Click "Start Quiz" from the home page or sidebar
2. **Select Topic**: Choose your field, topic, and subtopic
3. **Configure**: Set number of questions and other preferences
4. **Take Quiz**: Answer questions and get immediate feedback
5. **Learn**: Read detailed explanations for each answer
6. **Review**: Check your results and performance analytics
7. **Track Progress**: View your quiz history and improvements

## 📁 Project Structure

```
DSQuiz-Streamlit/
├── app.py                          # Main Streamlit application
├── models.py                       # Data models (Question, Quiz, etc.)
├── quiz_repository.py              # Data loading and management
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── GnanaVana just logo.png         # Logo image
├── quiz_data/                      # Quiz question data
│   ├── FLD_DSC_TPC_MLG_150_STC_LRG.json
│   ├── FLD_DSC_TPC_DLG_100_STC_NNB.json
│   └── ... (more quiz files)
├── run_quiz.bat                    # Windows launcher
├── run_quiz.sh                     # macOS/Linux launcher
├── .streamlit/config.toml          # Streamlit configuration
└── DSQuiz/                         # Virtual environment
```

## 🎨 Design Features

- **Purple Theme**: Consistent Twitch purple color scheme (#9146FF)
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Clean cards, gradients, and animations
- **Data Visualization**: Charts and graphs for performance tracking
- **Intuitive Navigation**: Easy-to-use sidebar and page routing

## 📊 Performance Features

- **Streamlit Caching**: Optimized data loading with `@st.cache_data`
- **Efficient Storage**: In-memory session state management
- **Fast Navigation**: Minimal page reloads with smart state management

## 🔧 Technical Implementation

### Data Models
- Object-oriented design with dataclasses
- Type hints for better code reliability
- Enum for question difficulties

### Repository Pattern
- Centralized data access through QuizRepository
- Caching for improved performance
- Error handling for robust operation

### State Management
- Streamlit session state for quiz progress
- Persistent results across navigation
- Clean separation of concerns

## 📈 Analytics Features

- **Real-time Progress**: Live updates during quiz
- **Performance Metrics**: Score, percentage, time tracking
- **Difficulty Analysis**: Breakdown by question difficulty
- **Trend Visualization**: Performance over time
- **Detailed Review**: Incorrect questions with explanations

## 🎓 Educational Benefits

- **Immediate Feedback**: Learn from mistakes instantly
- **Comprehensive Explanations**: Understand why answers are correct/incorrect
- **Progressive Difficulty**: Build knowledge systematically
- **Spaced Repetition**: Review incorrect questions
- **Performance Tracking**: Monitor learning progress

## 🛠️ Customization

The application is designed to be easily customizable:

- **Add New Topics**: Simply add new JSON files to `quiz_data/`
- **Modify Questions**: Edit existing JSON files
- **Change Theme**: Update CSS variables in `app.py`
- **Add Features**: Extend with new pages or functionality

## 📱 Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## 🔒 Data Privacy

- No personal data collection
- Local session storage only
- No external API calls for quiz data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is for educational purposes. Please respect the quiz content and attribution.

## 🎯 Future Enhancements

- User accounts and progress persistence
- Adaptive difficulty based on performance
- Team challenges and leaderboards
- Mobile app version
- Integration with learning management systems
- Export results to PDF
- Social sharing features

## 📞 Support

For issues or questions:
1. Check the FAQ section
2. Review the troubleshooting guide
3. Open an issue on the repository
4. Contact the development team

---

**Happy Learning! 🚀**

Master Data Science concepts through interactive quizzes and detailed explanations with GnanaVriksha - your Tree of Knowledge! 