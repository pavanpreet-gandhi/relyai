# RelyAI

> **Note:** This project is no longer maintained.

## Overview

RelyAI is a prototype application that leverages large language models to summarize financial news, developed as a proof of concept for an entrepreneurship course. It was developed in under 48 hours and is not intended for production use.

## Features

- Automated financial news summarization
- Clean minimal codebase
- Clean, scrollable user interface
- Customizable stock ticker focus (currently defaults to AAPL)

## Setup

### Installation

1. Clone the repository
2. Create a Python virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the backend server:
   ```
   python src/backend.py
   ```

2. Launch the frontend:
   ```
   streamlit run src/frontend.py
   ```

3. Navigate to the URL provided by Streamlit (typically `http://localhost:8501`)

The application is currently configured to retrieve news for Apple Inc. (AAPL) but can be modified in backend.py to track different securities.