from flask import Flask, render_template, request
import pandas as pd
import faiss
import pickle
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# Load the brain and the memory
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
index = faiss.read_index('security_bot.index')
kb_df = pd.read_pickle('knowledge_base.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    query = request.form['user_query']
    
    # 1. Convert user query to vector
    query_vector = model.encode([query.lower()])
    
    # 2. Search FAISS for the top 1 closest answer
    distances, indices = index.search(query_vector, k=1)
    
    # 3. Get the result
    match_index = indices[0][0]
    bot_answer = kb_df['answer'].iloc[match_index]
    matched_question = kb_df['question'].iloc[match_index]
    
    return render_template('index.html', 
                           question=query, 
                           answer=bot_answer, 
                           matched=matched_question)

if __name__ == '__main__':
    app.run(debug=True)