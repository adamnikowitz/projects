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

# 📰 LLM-RAG-PDFs

This project pulls data from a folder of PDF files, uses **RAG (Retrieval-Augmented Generation)** to integrate them into an **LLM model** and uses a **Gradio chatbot** interface to allow you to ask questions about the information within the PDFs.

## 🔧 Project Overview

- **Python Libraries**: Uses **PyMuPDF** to pull data from PDF files.
- **Retrieval-Augmented Generation**: Built with **Langchain** library to split text, convert to chunks, and store as vectors within a **Chroma** database
- **LLM Models**: Made with Open AI's **ChatGPT 40-mini** and fed through a **Gradio** chatbot in order to interfact with the text.

---

# 🤖  LLM-Subreddit-Summarizer

This project pulls uses a **Reddit API** to pull top comments from the top posts on a subreddit and uses an open-source LLM, **Ollama 3.2**, to provide summaries of the comments.

## 🔧 Project Overview

- **Python Libraries**: Uses **Praw**,  a wrapper library that allows you to connect to the Reddit API
- **LLM Models**: Made with Meta's **Ollama 3.2** open source LLM

  ## 🚀 Next Steps

- Sentiment analysis or additional analysis through **RAG (Retrieval-Augmented Generation)** process to embed text within LLM models for conversational interactions.
