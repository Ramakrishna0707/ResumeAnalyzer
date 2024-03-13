from flask import Flask, render_template, request
from dotenv import load_dotenv
import openai
import PyPDF2
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # Set a maximum file size limit (1MB in this example)
openai.api_key = os.getenv('OPEN_API_KEY')  # Replace with your actual OpenAI API key

@app.route('/', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        resume_file = request.files['resume']
        if resume_file.filename.endswith('.pdf'):
            resume_content = parse_pdf_resume(resume_file)
            feedback = get_chatgpt_feedback(resume_content)
            return render_template('feedback.html', feedback=feedback)
        else:
            error = "Please upload a PDF resume file."
            return render_template('upload.html', error=error)
    return render_template('upload.html')

def parse_pdf_resume(file):
    pdf_reader = PyPDF2.PdfReader(file)
    resume_content = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        resume_content += page.extract_text()
    return resume_content

# def get_chatgpt_feedback(content):
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=f"Provide feedback on the following resume: {content}",
#         max_tokens=1024,
#         n=1,
#         stop=None,
#         temperature=0.7,
#     )
#     feedback = response.choices[0].text
#     return feedback


def get_chatgpt_feedback(content):
    messages = [
        {"role": "system", "content": "You are an AI assistant providing feedback on resumes."},
        {"role": "user", "content": f"Provide feedback on the following resume: {content}"},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    feedback = response["choices"][0]["message"]["content"]
    return feedback

if __name__ == '__main__':
    app.run(debug=True)