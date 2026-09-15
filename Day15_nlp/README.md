# 📰 ArticleLens NLP Studio

## 📌 Overview

ArticleLens NLP Studio is an interactive NLP application that processes and analyzes news articles. The project was developed as part of **Day 15 of the AIML 45-Day Curriculum** to understand the fundamentals of **Natural Language Processing and text preprocessing**.

The application allows users to enter or upload a news article and process it through different NLP steps.

## 🔄 NLP Workflow

```text
News Article
     ↓
Text Cleaning
     ↓
Lowercase Conversion
     ↓
Punctuation Removal
     ↓
Tokenization
     ↓
Stopword Removal
     ↓
Stemming
     ↓
Lemmatization
     ↓
Processed Text
```

## ✨ Features

* News article text input
* Text statistics
* Lowercase conversion
* Punctuation and special character removal
* Tokenization
* Stopword removal
* Stemming
* Lemmatization
* Word frequency analysis
* Extractive text summarization
* Named Entity Recognition (NER)
* Simple rule-based news category prediction
* NLTK and spaCy comparison
* Download analysis results as JSON

## 🛠️ Tech Stack

* Python
* Streamlit
* NLTK
* spaCy
* Regular Expressions

## 🎯 What I Learned

Through this project, I learned how raw text is processed and prepared for NLP applications. I understood important concepts such as tokenization, stopword removal, stemming, and lemmatization, and how they are used as part of an NLP preprocessing pipeline.

I also explored additional NLP concepts such as word frequency analysis, text summarization, Named Entity Recognition, and rule-based text classification.

## ▶️ Run the Project

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run main.py
```

## 📌 Conclusion

This project demonstrates a complete NLP text preprocessing workflow using a news article as input. The processed text can be used for further NLP applications such as text classification, search, sentiment analysis, and information extraction.
