import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

# 1. Sample Dataset
data = {
    'text': [
        'Free entry in 2 a weekly comp to win FA Cup final tickets',
        'Hi, how are you doing today?',
        'WINNER!! As a valued network customer you have been selected to receivea £900 prize reward!',
        'Had your mobile 11 months or more? U R entitled to Update to the latest colour mobiles with camera for Free!',
        'I gonna be home soon and i dont want to talk about this stuff anymore tonight',
        'SIX chances to win CASH! From 100 to 20,000 pounds txt> CSH11 and send to 87575.',
        'Urgent! Please call 09061743818 from landline. Your complimentary 4* Ibiza Holiday or £10,000 cash await collection!',
        'I am fine, thank you for asking.'
    ],
    'label': ['spam', 'ham', 'spam', 'spam', 'ham', 'spam', 'spam', 'ham']
}

df = pd.DataFrame(data)

# 2. Features and Labels
X = df['text']
y = df['label']

# 3. Vectorization (Converting text to numbers)
cv = CountVectorizer(stop_words='english')
X = cv.fit_transform(X)

# 4. Model Training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = MultinomialNB()
clf.fit(X_train, y_train)

# 5. Save the model and vectorizer to disk
pickle.dump(clf, open('spam_model.pkl', 'wb'))
pickle.dump(cv, open('vectorizer.pkl', 'wb'))

print("Model Trained and Saved successfully!")