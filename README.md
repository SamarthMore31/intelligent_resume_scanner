Intelligent Resume Scanner
An automated, AI-powered tool to parse, score, and rank candidate resumes against a job description, helping to streamline the initial phase of the recruitment process.

About The Project
Recruiters often spend hours manually sifting through hundreds of resumes for a single job opening. This project automates that initial screening process by intelligently ranking candidates, allowing hiring managers to focus their time on the most qualified applicants.

The application leverages a sophisticated hybrid scoring model that combines traditional keyword matching with modern semantic analysis to provide a nuanced and accurate evaluation of each candidate.

Key Features
Interactive Web Interface: A user-friendly web app built with Streamlit for easy uploading of job descriptions and resumes.

Intelligent Parsing: Uses spaCy for Natural Language Processing to accurately extract key information from PDF resumes, including:

Candidate Name & Email

Work Experience

Education History

Advanced Hybrid Ranking: Ranks candidates using a weighted score that combines two methods:

Keyword Score: Measures the presence of specific, required skills.

Semantic Score: Uses a pre-trained AI model to analyze the contextual similarity between the resume and the job description.

Exportable Results: The final ranked list of candidates can be downloaded as a CSV file directly from the web app.

Command-Line Interface: Includes a main.py script for users who prefer to run the analysis from the terminal.

Technology Stack
Frontend: Streamlit

Backend & NLP: Python, spaCy, Pandas

AI / Machine Learning: Sentence-Transformers (Hugging Face), PyTorch

PDF Parsing: PyMuPDF

Setup and Installation
Follow these steps to set up the project locally.

Clone the Repository

Bash

git clone https://github.com/YourGitHubUsername/intelligent-resume-scanner.git
cd intelligent-resume-scanner
Create and Activate a Virtual Environment

Bash

# For Windows
python -m venv venv
.\venv\Scripts\Activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
Install Dependencies
Install all the required packages using the requirements.txt file.

Bash

pip install -r requirements.txt
Download the spaCy Language Model
The application requires an English language model from spaCy.

Bash

python -m spacy download en_core_web_sm
Usage
You can run the project in two ways:

1. Using the Streamlit Web App (Recommended)
This is the easiest and most interactive way to use the application.

Run the following command in your terminal:

Bash

streamlit run app.py
Open your web browser and navigate to the local URL provided (usually http://localhost:8501).

Follow the on-screen instructions to upload a job description and resumes, then click "Rank Candidates" to see the results.

2. Using the Command-Line Script
This method is useful for automated processing and will save the output to a CSV file.

Place your job description in a file at data/job_description.txt.

Place all candidate resumes (PDFs) inside the data/resumes/ folder.

Run the script from your terminal:

Bash

python main.py
The final report will be saved at results/ranking_output.csv.

Configuration
You can customize the skills that the scanner looks for by editing the SKILL_DB list located in the following file:
utils/skill_extractor.py

Simply add or remove skills (in lowercase) to tailor the scanner to different job roles and industries.
