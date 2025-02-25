import streamlit as st
from dotenv import load_dotenv
import os
import openai
# Load environment variables from .env file
load_dotenv()

# Access the API key
openai_api_key = os.getenv("OPENAI_API_KEY")

from utils import extract_text_from_resume
import streamlit.components.v1 as components

# Set your OpenAI API key securely (e.g., via Streamlit secrets)
import streamlit as st
import openai

# Access the API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]


def generate_portfolio(resume_text, user_preferences):
    """
    Use OpenAI API to generate a static HTML portfolio website.
    The prompt instructs the model to create modern, responsive HTML code.
    """
    prompt = (
        "Based on the following resume content:\n\n"
        f"{resume_text}\n\n"
        "and the following design preferences:\n"
        f"{user_preferences}\n\n"
        "Generate a complete, modern, responsive, and professional static HTML portfolio website code. "
        "The code should include all necessary HTML, inline CSS (or minimal external CSS), and JavaScript if needed. "
        "Make sure it is well-structured and commented."
    )
    
    response = openai.Completion.create(
        engine="text-davinci-003",  # or another model endpoint
        prompt=prompt,
        max_tokens=1500,
        temperature=0.7,
        n=1,
        stop=None
    )
    html_code = response.choices[0].text.strip()
    return html_code

def main():
    st.title("Portfolio Generator")
    st.write("Upload your resume to generate a personalized portfolio website.")

    # Upload resume file (PDF or TXT)
    uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
    user_preferences = st.text_area("Enter your design preferences (e.g., color scheme, layout ideas):", "")

    if uploaded_file is not None:
        # Determine file type and extract text accordingly
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension == "pdf":
            resume_text = extract_text_from_resume(uploaded_file)
        elif file_extension == "txt":
            resume_text = uploaded_file.read().decode("utf-8")
        else:
            st.error("Unsupported file type. Please upload a PDF or TXT file.")
            return

        st.subheader("Extracted Resume Text (Preview)")
        st.text(resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)

        if st.button("Generate Portfolio"):
            with st.spinner("Generating your portfolio..."):
                html_code = generate_portfolio(resume_text, user_preferences)
            st.success("Portfolio generated successfully!")
            
            st.subheader("Generated HTML Code")
            st.code(html_code, language="html")
            
            st.subheader("Portfolio Preview")
            # Render the generated HTML in an iframe-like component
            components.html(html_code, height=600, scrolling=True)
            
            st.download_button(
                label="Download Portfolio HTML",
                data=html_code,
                file_name="portfolio.html",
                mime="text/html"
            )

if __name__ == "__main__":
    main()
