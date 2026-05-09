from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the saved model and vectorizer
model = pickle.load(open('spam_model.pkl', 'rb'))
cv = pickle.load(open('vectorizer.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        message = request.form['message']
        data = [message]
        vect = cv.transform(data).toarray()
        prediction = model.predict(vect)
        return render_template('index.html', prediction=prediction[0])

if __name__ == '__main__':
    app.run(debug=True)