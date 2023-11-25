from flask import Flask, render_template, request
from text_summarizer import preprocess_text, calculate_word_frequencies, calculate_sentence_scores, generate_summary

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    if request.method == 'POST':
        text = request.form['text'].strip() 
        if text and not text.isspace():
            sentence_list, filtered_words = preprocess_text(text)
            frequency_map = calculate_word_frequencies(filtered_words)
            sent_score = calculate_sentence_scores(sentence_list, frequency_map)
            num_sentences = int(request.form.get('numSentences', 10))
            summary = generate_summary(sent_score, num_sentences=num_sentences) 
    elif request.method == 'GET':
        summary = None  # Set summary to None when the page is loaded or refreshed
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
