# Fin_Nlp_bot

## Installation and launch
(Python v11)
Just copy to terminal:

```bash
cd .\Fin_Nlp_bot\ 
pip install -r requirements.txt
cd BackEnd 
uvicorn main:app --reload 
```

---

## Требования к проекту

### 1. Project topic by options

**Variant-36** NLP-chat-bot - understanding a question

### 2. Using Python

The main logic of the project should be implemented in the Python language. The use of third-party libraries is allowed.

Yes, only Python for logic and some packs (library):

- `fastapi`
- `os`
- `re`
- `math`
- `uvicorn`
- `collections`
- `supabase`
- `python-dotenv`
- `pydantic`
- `dotenv`

### 3. User Interface

Web application

### 4. The logic of the chatbot

**Tokenize:**
```python
def tokenize(text: str) -> list[str]:
    text = text.lower()
    tokens = re.findall(r'[а-яёa-z]+', text)
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 2]
```

Calculating the local importance of a word within one specific text:
```python
def compute_tf(tokens: list[str]) -> dict:
    tf = defaultdict(int)
    for token in tokens: tf[token] += 1
    total = len(tokens) if tokens else 1
    return {k: v / total for k, v in tf.items()}
```

Same to document (all text and questions FAQ):
```python
def compute_idf(documents: list[list[str]]) -> dict:
    n = len(documents)
    idf = defaultdict(float)
    all_words = set(w for doc in documents for w in doc)
    for word in all_words:
        doc_count = sum(1 for doc in documents if word in doc)
        idf[word] = math.log((n + 1) / (doc_count + 1)) + 1
    return idf
```

Give Vector:
```python
def tfidf_vector(tokens: list[str], idf: dict) -> dict:
    tf = compute_tf(tokens)
    return {word: tf[word] * idf.get(word, 1.0) for word in tokens}
```

Finds the intersection of words in vectors and calculates the cosine of the angle between them in a multidimensional space (through the dot product and the norm of the vectors):
```python
def cosine_similarity(vec1: dict, vec2: dict) -> float:
    common = set(vec1) & set(vec2)
    if not common: return 0.0
    dot = sum(vec1[w] * vec2[w] for w in common)
    norm1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    norm2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
    if norm1 == 0 or norm2 == 0: return 0.0
    return dot / (norm1 * norm2)
```

### 5. Error handling
<img width="860" height="442" alt="image" src="https://github.com/user-attachments/assets/31a8ae8a-f924-4ed6-8eeb-dac37eb3fb88" />

**User chat:**
```python
def respond(self, user_input: str) -> str:
    tokens = tokenize(user_input)
    if not tokens: return "Not understand Question"
    user_vec = tfidf_vector(tokens, self.idf)
    best_score, best_idx = 0.0, -1
    for i, faq_vec in enumerate(self.vectors):
        score = cosine_similarity(user_vec, faq_vec)
        if score > best_score:
            best_score, best_idx = score, i
    if best_score >= self.threshold:
        return f"Answer for question: ''{self.questions[best_idx]}'' - " + self.answers[best_idx]
    return "-------Not found similar question--------"
```

**Terminal if server die:**

![image](https://github.com/user-attachments/assets/d082d1c8-cc94-4457-9747-1c6068224433)

### 6. Data storage

**Server Supobase**

<img width="1548" height="754" alt="image" src="https://github.com/user-attachments/assets/9ef19722-c8ac-4d41-9ae5-d0a41c0280cb" />

<img width="848" height="256" alt="image" src="https://github.com/user-attachments/assets/1764bb6a-c07d-4944-b863-a1655cec8644" />

### 7. Design and ease of use

<img width="1892" height="858" alt="image" src="https://github.com/user-attachments/assets/2778600a-a5bf-423b-be9b-5175cc979bfe" />
<img width="1844" height="904" alt="image" src="https://github.com/user-attachments/assets/73bc6473-d62a-4d84-8bd6-f06f069e93b5" />
<img width="1858" height="904" alt="image" src="https://github.com/user-attachments/assets/95719054-cddf-482e-a13f-86f2b148d46b" />

