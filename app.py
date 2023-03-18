from flask import Flask, render_template, request
from main import pdf
from Functions import recorder, audio_transcript

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    text = request.form['text']
    pdf_name = pdf(text)
    if(pdf_name == -1):
        return render_template('home.html', pdf_name='The ticker is wrong')
    return render_template('process_text.html', pdf_name=pdf_name)

@app.route('/process_text2')
def process_text2():
    recorder()
    text = audio_transcript()
    print(text)
    pdf_name = pdf(text)
    if(pdf_name == -1):
        return render_template('home.html', pdf_name='The ticker is wrong')
    return render_template('process_text.html', pdf_name=pdf_name)


if __name__ == '__main__':
    app.run(debug=True)