# Import necessary libraries
from app_prompts import *
import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import base64
import json

# Set up the Streamlit app
st.set_page_config(page_title="Intelligent Resume Analyzer", page_icon=":robot_face:")

# Hide the Streamlit default footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Add custom CSS styles
st.markdown(
    """
    <style>
    .chat-message-user {
        background-color: #e0e0e0;
        border-radius: 20px;
        padding: 10px 20px;
        margin-bottom: 10px;
    }
    .chat-message-assistant {
        background-color: #f5f5f5;
        border-radius: 20px;
        padding: 10px 20px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Get the current working directory
cwd = os.getcwd()


def get_base64_jpg(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# Display developer information
with st.sidebar:
    st.markdown(
        f"""
        <div style="background-color: #282c34; padding: 16px; border-radius: 8px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); display: flex; align-items: center;">
            <img src="data:image/jpeg;base64,{get_base64_jpg(os.path.join(cwd, 'aa.jpg'))}" alt="Logo" style="width: 100px; height: 100px; margin-right: 12px;">
            <div>
                <p style="margin-bottom: 4px; color: #cccccc;"><strong>Developed by</strong> <a href="https://www.linkedin.com/in/harbhajan21/" target="_blank" style="color: #61dafb; text-decoration: none;">Harbhajan Singh</a></p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Get the Hugging Face Access Token from the user
GoogleGenerativeAI_token = st.sidebar.text_input("Google Generative AI Token", key="chatbot_api_key", type="password")

# Display helpful links
st.sidebar.write("[Get Google Generative AI Token](https://aistudio.google.com/app/apikey)")

def get_gemini_repsonse(input, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(resume_upload):
    reader = pdf.PdfReader(resume_upload)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

## Streamlit Application for Resume Evaluation
st.header("💬 Intelligent Resume Analyzer")
st.write("Enhance Your Job Application with Tailored Feedbacks with a cover letter sample.")

job_description = st.text_area("Enter the Job Description Details")
resume_upload = st.file_uploader("Upload Your Resume here!", type="pdf", help="Please provide your resume in PDF format.")


# Buttons for the app
# Create 3 columns
col1, col2, col3 = st.columns(3) 

with col1:
    analyze_match = st.button("Calculate Match Percentage")

with col2:
    resume_insights = st.button("Provide Resume Insights")

with col3:
    cover_letter = st.button("Write a Sample Cover Letter")
    
    
# Check if any button is clicked
button_clicked = analyze_match or resume_insights or cover_letter

# Disclaimer message
st.warning("Disclaimer: The information provided on this website is for educational purposes only. It is not intended to provide professional advice. Use it at your own risk. "
           + "\n" + "\nPlease note that the responses provided by the AI model are based on the information available in the resume and job description. While the model aims to provide accurate and relevant information, it may generate some hallucinated or fabricated details due to the nature of language models. We recommend cross-checking any specific details or claims with the original resume and job description content for accuracy.")

# Validate Google Generative AI Token
if button_clicked and not GoogleGenerativeAI_token:
    st.error("Please provide a valid Google Generative AI Token to proceed or the provided Google Generative AI Token is not valid")
else:
    # Logic for the buttons
    try:
        if analyze_match:
            if resume_upload is not None and GoogleGenerativeAI_token:
                text = input_pdf_text(resume_upload)
                response = get_gemini_repsonse(MetaPrompt, GoogleGenerativeAI_token)
                st.success("The Response for Match Percentage, Missing Keywords, and Final Thoughts is: ")
                st.write(response)
            else:
                st.write("Please upload the resume in pdf format and provide the Google Generative AI Token")
        elif resume_insights:
            if resume_upload is not None and GoogleGenerativeAI_token:
                pdf_content = input_pdf_text(resume_upload)
                response = get_gemini_repsonse(InputPrompt, GoogleGenerativeAI_token)
                st.success("The Response for Resume Insights is: ")
                st.write(response)
            else:
                st.write("Please upload the resume in pdf format and provide the Google Generative AI Token")
        elif cover_letter:
            if resume_upload is not None and GoogleGenerativeAI_token:
                pdf_content = input_pdf_text(resume_upload)
                response = get_gemini_repsonse(CoverLetterPrompt, GoogleGenerativeAI_token)
                st.success("The Response for Cover Letter is: ")
                st.write(response)
            else:
                st.write("Please upload the resume in pdf format and provide the Google Generative AI Token")
    except Exception as e:
        st.write(f"An error occurred: {e}")