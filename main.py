from flask import Flask, render_template, request
from text_summarizer import preprocess_text, calculate_word_frequencies, calculate_sentence_scores, generate_summary

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    if request.method == 'POST':
        text = request.form['text'].strip()  # Remove leading and trailing spaces
        if text and not text.isspace():  # Check if the text is not empty and not just spaces
            sentence_list, filtered_words = preprocess_text(text)
            frequency_map = calculate_word_frequencies(filtered_words)
            sent_score = calculate_sentence_scores(sentence_list, frequency_map)
            summary = generate_summary(sent_score, num_sentences=10) 
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
