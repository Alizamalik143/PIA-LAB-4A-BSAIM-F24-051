from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# The API endpoint for random jokes
JOKE_API_URL = "https://official-joke-api.appspot.com/random_joke"

@app.route('/', methods=['GET', 'POST'])
def index():
    joke_data = None
    error_message = None

    # If the user clicks the "Get Joke" button (POST request)
    if request.method == 'POST':
        try:
            response = requests.get(JOKE_API_URL)
            if response.status_code == 200:
                joke_data = response.json()
            else:
                error_message = "Oops! Couldn't grab a joke right now."
        except Exception as e:
            error_message = f"Connection error: {e}"

    return render_template('index.html', joke=joke_data, error=error_message)

if __name__ == '__main__':

    app.run(debug=True)