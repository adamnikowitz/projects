## **🚀 LeetCode-Tutor-AI**
This project creates an intelligent AI-powered coding tutor that generates personalized programming problems, executes code safely in Docker containers, and provides detailed feedback to help users improve their coding interview skills.

### **🔧 Project Overview**
* **Problem Generation**: Uses **OpenAI GPT-4** to create diverse coding problems with randomized topics and difficulty levels.
* **Code Execution**: Safely runs user solutions in isolated **Docker containers** with automatic package installation.
* **AI Agents**: Built with **CrewAI** framework featuring specialized agents for problem generation, code execution, and code review.
* **Memory System**: Tracks user progress, difficulty preferences, and learning patterns in **JSON-based storage**.
* **Adaptive Learning**: Adjusts problem difficulty based on user feedback and maintains learning history.
* **Web Interface**: Interactive **Gradio** app with proper workflow - problem first, then code submission and feedback.

# ⚾ Baseball-Model

This project demonstrates an end-to-end machine learning pipeline from acquiring unstructured data through developing a model to predict pitcher strikouts and deploying it though FastAPI to serve a simple web app.

## 🔧 Project Overview

- **Data Ingestion**: Pulls live data from an external API.
- **Data Pipelines**: Built using **MySQL** and **Python** to clean and prepare the data.
- **Model Training**: Uses machine learning to predict outcomes.
- **Scheduling**: Automated with **Prefect** for regular execution.
- **Deployment**: A **FastAPI** app serves predictions via a simple web interface.

## 🚀 Next Steps

- Add new data sources and engineer additional features.
- Integrate **MLflow** for experiment tracking and model monitoring.
- Containerize the app with **Docker**.
- Deploy to a **cloud platform** (TBD).

---
<br><br>


# 📰 LLM-RAG-PDFs

This project pulls data from a folder of PDF files, uses **RAG (Retrieval-Augmented Generation)** to integrate them into an **LLM model** and uses a **Gradio chatbot** interface to allow you to ask questions about the information within the PDFs.

## 🔧 Project Overview

- **Python Libraries**: Uses **PyMuPDF** to pull data from PDF files.
- **Retrieval-Augmented Generation**: Built with **Langchain** library to split text, convert to chunks, and store as vectors within a **Chroma** database
- **LLM Models**: Made with Open AI's **ChatGPT 40-mini** and fed through a **Gradio** chatbot in order to interfact with the text.

---
<br><br>


# 🤖  LLM-Subreddit-Summarizer

This project pulls uses a **Reddit API** to pull top comments from the top posts on a subreddit and uses an open-source LLM, **Ollama 3.2**, to provide summaries of the comments.

## 🔧 Project Overview

- **Python Libraries**: Uses **Praw**,  a wrapper library that allows you to connect to the Reddit API
- **LLM Models**: Made with Meta's **Ollama 3.2** open source LLM

  ## 🚀 Next Steps

- Sentiment analysis or additional analysis through **RAG (Retrieval-Augmented Generation)** process to embed text within LLM models for conversational interactions.

---
<br><br>


# 🤝 Prisoner's Dilemma Tournament

A simulation of the Iterated Prisoner’s Dilemma featuring multiple adaptive strategies created from both closed and open source LLM models to see how well each model can build a strategy from a given base class and multi-shot prompting.

## 🔧 Project Overview

- **Game Mechanics**: Simulates repeated rounds of the classic Prisoner's Dilemma between multiple AI agents.
- **Strategies Implemented**:
  - `Win-Stay-Lose-Shift`
  - `Adaptive Tit-for-Tat`
  - `Forgiving Tit-for-Tat`
  - `Pattern Detection`
  - `Random Strategy` (added by me because the LLMs were playing too rationally)
- **Scoring**: Agents accumulate points based on classic payoff rules.
- **Visualization**: Results are graphed using **Matplotlib**, including:
  - Line graph showing scores over time
  - Final rankings by total score

## 🛠️ Technologies Used

- Python
- Object-Oriented Programming (OOP)
- Matplotlib for graphing
- (Optional) Jupyter Notebooks for step-by-step visualization

## 🚀 Future Ideas

- Add genetic algorithms to evolve strategies
- Allow user input to participate as a player
- Web interface with **Gradio** or **FastAPI**
- Export results to CSV or database
