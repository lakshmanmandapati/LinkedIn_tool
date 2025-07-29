# Personalized LinkedIn Post Generator (LLMOps Project)

This project is an **AI-powered Streamlit application** designed to help users generate engaging LinkedIn posts tailored to specific topics, lengths, and languages, all while mimicking a distinct writing style.  
It serves as an **end-to-end demonstration of an LLMOps pipeline**.

## Local Setup & Installation

Follow these steps to get the project running on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/lakshmanmandapati/LinkedIn_tool.git
cd LinkedIn-tool
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate 
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
> Ensure your `requirements.txt` includes **streamlit, pandas, langchain-core**, and your LLM library (e.g., `langchain-groq` if using Groq).

### 4. Prepare Data

```bash
mkdir data
```
Place your `student_tech_posts.json` file inside the **data** directory.

### 5. Configure LLM API Key (Groq)

Open **`llm_helper.py`** and ensure your LLM client is correctly initialized with your **Groq API key**.  
It's highly recommended to set this as an environment variable:

```bash
export GROQ_API_KEY="your_api_key_here"
```

### 6. Run Data Preprocessing

```bash
python process_posts.py
```
This will generate `processed_student_posts.json`.

## Running the Streamlit Application

### 1. Run the App

```bash
streamlit run main.py
```

### 2. Access

Open your web browser and go to the URL displayed in your terminal (usually:  
[http://localhost:8501](http://localhost:8501)).

## Usage

Once the application is running:

1. **Select Options** → Use the dropdowns to choose your desired **Topic**, **Length**, and **Language**.  
2. **Generate Post** → Click the **"Generate Post"** button.  
3. **View Output** → The generated LinkedIn post will appear below the button.  

## Project Structure

```bash
linkedin-post-generator/
├── data/
│   ├── student_tech_posts.json      # Raw input data for student persona
│   └── processed_student_posts.json # Processed data with metadata and unified tags
├── llm_helper.py                    # Handles LLM initialization and API calls
├── process_posts.py                 # Script for data preprocessing
├── few_shot.py                      # Class to load and filter processed posts for few-shot examples
├── post_generator.py                # Core logic for generating posts using few-shot LLM
├── main.py                          # Streamlit application entry point
└── requirements.txt                 # Python dependencies
```

## Architecture
![Arch](https://github.com/user-attachments/assets/703d2dda-6486-49f7-9bf4-3fe126b039c8)
