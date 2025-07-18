import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter

# Set page config
st.set_page_config(
    page_title="Text Sentiment Analyzer",
    page_icon="💬",
    layout="wide"
)

# Title
st.title("💬 Text Sentiment Analyzer")
st.markdown("*Analyze the sentiment and characteristics of your text*")

# Simple sentiment word lists (for demo purposes)
positive_words = {
    'amazing', 'awesome', 'brilliant', 'excellent', 'fantastic', 'good', 'great', 
    'happy', 'love', 'perfect', 'wonderful', 'best', 'incredible', 'outstanding',
    'superb', 'delighted', 'pleased', 'satisfied', 'beautiful', 'nice'
}

negative_words = {
    'awful', 'bad', 'terrible', 'horrible', 'worst', 'hate', 'disgusting',
    'disappointing', 'sad', 'angry', 'frustrated', 'annoying', 'boring',
    'ugly', 'stupid', 'ridiculous', 'pathetic', 'useless', 'failed', 'disaster'
}

def analyze_sentiment(text):
    """Simple sentiment analysis based on word counts"""
    words = re.findall(r'\b\w+\b', text.lower())
    
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
    total_words = len(words)
    
    if positive_count > negative_count:
        sentiment = "Positive 😊"
        score = (positive_count - negative_count) / max(total_words, 1)
    elif negative_count > positive_count:
        sentiment = "Negative 😔"
        score = (negative_count - positive_count) / max(total_words, 1)
    else:
        sentiment = "Neutral 😐"
        score = 0
    
    return {
        'sentiment': sentiment,
        'score': abs(score),
        'positive_words': positive_count,
        'negative_words': negative_count,
        'total_words': total_words,
        'word_list': words
    }

# Text input
st.subheader("📝 Enter Your Text")
user_text = st.text_area(
    "Type or paste your text here:",
    placeholder="Enter some text to analyze its sentiment...",
    height=150
)

if user_text:
    # Analyze the text
    results = analyze_sentiment(user_text)
    
    # Display results
    st.subheader("📊 Analysis Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Sentiment", results['sentiment'])
    
    with col2:
        st.metric("Sentiment Score", f"{results['score']:.3f}")
    
    with col3:
        st.metric("Positive Words", results['positive_words'])
    
    with col4:
        st.metric("Negative Words", results['negative_words'])
    
    # Word frequency analysis
    if results['word_list']:
        st.subheader("🔤 Word Frequency Analysis")
        
        word_freq = Counter(results['word_list'])
        top_words = dict(word_freq.most_common(10))
        
        if top_words:
            # Create a simple bar chart
            fig, ax = plt.subplots(figsize=(10, 6))
            words = list(top_words.keys())
            counts = list(top_words.values())
            
            bars = ax.bar(words, counts, color='skyblue')
            ax.set_title('Top 10 Most Frequent Words')
            ax.set_xlabel('Words')
            ax.set_ylabel('Frequency')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Color positive/negative words
            for i, word in enumerate(words):
                if word in positive_words:
                    bars[i].set_color('lightgreen')
                elif word in negative_words:
                    bars[i].set_color('lightcoral')
            
            st.pyplot(fig)
            plt.close()
    
    # Text statistics
    st.subheader("📈 Text Statistics")
    
    sentences = len(re.split(r'[.!?]+', user_text.strip()))
    characters = len(user_text)
    characters_no_spaces = len(user_text.replace(' ', ''))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Words", results['total_words'])
    
    with col2:
        st.metric("Sentences", sentences)
    
    with col3:
        st.metric("Characters", characters)
    
    with col4:
        st.metric("Chars (no spaces)", characters_no_spaces)
    
    # Show detected sentiment words
    detected_positive = [word for word in results['word_list'] if word in positive_words]
    detected_negative = [word for word in results['word_list'] if word in negative_words]
    
    if detected_positive or detected_negative:
        st.subheader("🎯 Detected Sentiment Words")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if detected_positive:
                st.success("**Positive Words Found:**")
                st.write(", ".join(detected_positive))
        
        with col2:
            if detected_negative:
                st.error("**Negative Words Found:**")
                st.write(", ".join(detected_negative))

else:
    st.info("👆 Please enter some text above to begin analysis")

# Sample texts for testing
st.subheader("📋 Try These Sample Texts")

col1, col2 = st.columns(2)

with col1:
    if st.button("Load Positive Sample"):
        st.experimental_set_query_params(
            sample="I absolutely love this amazing product! It's fantastic and works perfectly. The design is beautiful and the quality is outstanding. Highly recommended!"
        )

with col2:
    if st.button("Load Negative Sample"):
        st.experimental_set_query_params(
            sample="This is terrible and disappointing. The quality is awful and it's completely useless. I hate everything about it. Worst purchase ever!"
        )

# Footer
st.markdown("---")
st.markdown("💡 *This is a demo app using simple word-based sentiment analysis for portfolio purposes*") 