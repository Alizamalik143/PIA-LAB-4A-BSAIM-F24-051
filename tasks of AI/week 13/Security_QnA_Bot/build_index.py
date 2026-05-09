import pandas as pd
import re
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# 1. Our "Knowledge Base" (The data the bot will use to answer)
data = {
    'question': [
        "What is a phishing attack?",
        "How to identify a spam email?",
        "What is two-factor authentication?",
        "What should I do if I click a suspicious link?",
        "How do I report a scam?"
    ],
    'answer': [
        "Phishing is a type of social engineering where attackers deceive users into revealing sensitive info.",
        "Look for poor grammar, mismatched URLs, and urgent requests for personal information.",
        "2FA adds a second layer of security to your accounts, requiring a code in addition to your password.",
        "Disconnect from the internet immediately, scan for malware, and change your account passwords.",
        "You can report scams to your email provider and official government cybercrime departments."
    ]
}

df = pd.DataFrame(data)

# 2. Text Cleaning Function
def clean_text(text):
    text = re.sub(r'[^A-Za-z\s]', '', text)
    return text.lower().strip()

# 3. Embedding using Hugging Face (MiniLM)
print("Loading MiniLM model...")
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
# We embed the 'questions' because that's what users will match against
embeddings = model.encode(df['question'].apply(clean_text).tolist())

# 4. Storing in FAISS
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# 5. Save everything for the Flask app
faiss.write_index(index, 'security_bot.index')
df.to_pickle('knowledge_base.pkl')
print("Successfully created FAISS index and saved knowledge base!")