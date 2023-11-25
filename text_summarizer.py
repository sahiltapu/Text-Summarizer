import nltk
import heapq
from flask import Flask

# nltk.download('punkt')
# nltk.download('stopwords')

app = Flask(__name__)

def preprocess_text(text):
    # Tokenize the text into sentences and words
    sentence_list = nltk.sent_tokenize(text)
    word_list = nltk.word_tokenize(text)
    
    # Initializing stop words
    stopwords = nltk.corpus.stopwords.words('english')
    
    # Removing stopwords from the word list
    filtered_words = [word for word in word_list if word.lower() not in stopwords]
    
    return sentence_list, filtered_words

def calculate_word_frequencies(words):
    frequency_map = {}
    
    for word in words:
        if word not in frequency_map:
            frequency_map[word] = 1
        else:
            frequency_map[word] += 1
    
    max_frequency = max(frequency_map.values())
    
    for word in frequency_map:
        frequency_map[word] = frequency_map[word] / max_frequency
    
    return frequency_map

def calculate_sentence_scores(sentence_list, frequency_map):
    sent_score = {}
    
    for sent in sentence_list:
        for word in frequency_map:
            if word in frequency_map and len(sent.split(" ")) < 35:
                if sent not in sent_score:
                    sent_score[sent] = frequency_map[word]
                else:
                    sent_score[sent] += frequency_map[word]
    
    return sent_score

def generate_summary(sent_score, num_sentences=10):
    # Finding the top sentences based on scores
    summary = heapq.nlargest(num_sentences, sent_score, key=sent_score.get)
    
    return summary

def main():
    text = '''Although "tree" is a term of common parlance, there is no universally recognised precise definition of what a tree is, either botanically or in common language.[1][2] In its broadest sense, a tree is any plant with the general form of an elongated stem, or trunk, which supports the photosynthetic leaves or branches at some distance above the ground.[3] Trees are also typically defined by height,[4] with smaller plants from 0.5 to 10 m (1.6 to 32.8 ft) being called shrubs,[5] so the minimum height of a tree is only loosely defined.[4] Large herbaceous plants such as papaya and bananas are trees in this broad sense.[2][6]

A commonly applied narrower definition is that a tree has a woody trunk formed by secondary growth, meaning that the trunk thickens each year by growing outwards, in addition to the primary upwards growth from the growing tip.[4][7] Under such a definition, herbaceous plants such as palms, bananas and papayas are not considered trees regardless of their height, growth form or stem girth. Certain monocots may be considered trees under a slightly looser definition;[8] while the Joshua tree, bamboos and palms do not have secondary growth and never produce true wood with growth rings,[9][10] they may produce "pseudo-wood" by lignifying cells formed by primary growth.[11] Tree species in the genus Dracaena, despite also being monocots, do have secondary growth caused by meristem in their trunk, but it is different from the thickening meristem found in dicotyledonous trees.[12]

Aside from structural definitions, trees are commonly defined by use; for instance, as those plants which yield lumber.[13]

Overview
"Saplings" redirects here. For the novel, see Saplings (novel). For the film, see The Saplings. For the episode, see Saplings (Weeds).
The tree growth habit is an evolutionary adaptation found in different groups of plants: by growing taller, trees are able to compete better for sunlight.[14] Trees tend to be tall and long-lived,[15] some reaching several thousand years old.[16] Several trees are among the oldest organisms now living.[17] Trees have modified structures such as thicker stems composed of specialised cells that add structural strength and durability, allowing them to grow taller than many other plants and to spread out their foliage. They differ from shrubs, which have a similar growth form, by usually growing larger and having a single main stem;[5] but there is no consistent distinction between a tree and a shrub,[18] made more confusing by the fact that trees may be reduced in size under harsher environmental conditions such as on mountains and subarctic areas. The tree form has evolved separately in unrelated classes of plants in response to similar environmental challenges, making it a classic example of parallel evolution. With an estimated 60,000-100,000 species, the number of trees worldwide might total twenty-five per cent of all living plant species.[19][20] The greatest number of these grow in tropical regions; many of these areas have not yet been fully surveyed by botanists, making tree diversity and ranges poorly known.[21]'''
    
    # Check if the input text is empty or contains only spaces
    if text.isspace() or not text:
        print("Text is empty. Nothing to summarize.")
        return
    
    sentence_list, filtered_words = preprocess_text(text)
    frequency_map = calculate_word_frequencies(filtered_words)
    sent_score = calculate_sentence_scores(sentence_list, frequency_map)
    summary = generate_summary(sent_score, num_sentences=10)
    
    for sentence in summary:
        print(sentence)

if __name__ == "__main__":
    main()
