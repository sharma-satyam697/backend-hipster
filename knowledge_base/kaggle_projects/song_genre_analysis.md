## Song Genre Analysis Using Doc2Vec (Kaggle Project)

This project focused on classifying songs into genres based on their lyrics using **natural language processing (NLP)** and the **Doc2Vec** model. The dataset used consisted of over **28,000 songs**, each annotated with metadata such as artist name, track name, release date, and genre, along with detailed lyrical content and linguistic sentiment scores. 

---

### 📊 Dataset Overview
The dataset contained the following key features:
- **28372** total rows (songs)
- **7 unique genres**: pop, country, blues, rock, jazz, reggae, hip hop
- Other fields included lyrical sentiment indicators (e.g., sadness, romantic), audio features (e.g., danceability, loudness), and metadata (e.g., artist_name, release_date)
- **No null values** were present in the dataset

---

### 🧹 Data Preprocessing
To ensure high model accuracy and cleaner textual input, the lyrics were preprocessed through several steps:
- **Contraction Expansion**: Replaced contractions like "won't" with "will not", using regex rules.
- **Sampling**: Extracted a random sample from the dataset for faster experimentation.
- **Language Filtering**: Used the `langdetect` package to retain only English lyrics.
- **Symbol Cleaning**: Removed extra punctuation and symbols between words using regex.

```python
def expand_contractions_filter_1(text):
    contractions = {
        r"won't": "will not",
        r"can't": "can not",
        r"n't": " not",
        r"'re": " are",
        r"'s": " is",
        r"'d": " would",
        r"'ll": " will",
        r"'ve": " have"
    }
    for pattern, replacement in contractions.items():
        text = re.sub(pattern, replacement, text)
    return text
```

---

### 🧠 Model Development with Doc2Vec
The model was built using **Gensim's Doc2Vec** implementation. Each song's lyrics were tokenized and tagged with its corresponding genre.

```python
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

def word_to_vec(input_list, output_list, vector_size=150, min_count=5, epochs=40):
    tagged_data = [TaggedDocument(words=inp, tags=[out]) for inp, out in zip(input_list, output_list)]
    model = Doc2Vec(vector_size=vector_size, min_count=min_count, epochs=epochs)
    model.build_vocab(tagged_data)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    return model
```

The final model was trained with:
- **Vector size**: 8000
- **Epochs**: 30
- **min_count**: 5 (to filter rare words)

---

### 🔮 Genre Prediction
Genre for new lyrics was predicted using similarity between the inferred vector and existing genre tags:

```python
def Predict_genre(model, text):
    text_vector = infer_vector(model, text)
    return model.dv.most_similar([text_vector], topn=1)[0][0]
```

Example prediction:
```python
text = "How many roads must a man walk down before you call him a man..."
Predict_genre(model, text)
```

---

### 📈 Visualization & Insights
The dataset revealed interesting trends in genre distribution:
- **Pop** and **Country** music were dominant, accounting for **44%** of the entire dataset.
- Blues, Rock, Jazz, and Reggae had moderate representation.
- Hip Hop had the lowest share.

Two charts illustrated this insight:
1. A **line plot** showing song counts per genre
2. A **pie chart** highlighting each genre's percentage

![Genre Distribution](./86ce86a1-10b7-41d1-b1ae-a2fce21f0647.png)

---

### ✅ Conclusion
This project demonstrates my ability to perform text preprocessing, build embedding-based models, and analyze genre trends from large-scale textual datasets. It also highlights the usefulness of Doc2Vec in capturing semantic meaning from lyrics and making genre predictions based purely on textual content.
