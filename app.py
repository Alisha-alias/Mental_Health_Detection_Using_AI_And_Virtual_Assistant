from flask import Flask, render_template, request
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import csv

app = Flask(__name__)

# Load the dataset
df = pd.read_csv("Mental_Health_FAQ.csv")

# Load the SentenceTransformer model
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Preprocess function to clean and tokenize text
def preprocess(text):
    # Add your preprocessing steps here (e.g., lowercasing, removing punctuation)
    return text.lower()

def read_responses_from_csv(file_path):
    responses = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            intent = row['intent'].lower()
            response_list = row['response'].split('."')
            responses[intent] = response_list
    return responses

# Load responses from CSV
responses = read_responses_from_csv("Mental_Health_FAQ.csv")

def get_responses(user_input, threshold=0.5):
    user_input = preprocess(user_input)

    # Check for direct match in the dataset
    if user_input in responses:
        return responses[user_input]

    # Convert user input and intents to embeddings
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    intent_embeddings = model.encode(df['intent'].apply(preprocess), convert_to_tensor=True)

    # Calculate cosine similarity
    similarity_scores = util.pytorch_cos_sim(user_embedding, intent_embeddings)[0]

    # Get similar intents
    similar_intents_indices = similarity_scores.argsort(descending=True)
    
    similar_responses = []
    for index in similar_intents_indices:
        if similarity_scores[index] > threshold:
            # Convert index to integer before using it to access the DataFrame
            index = int(index)
            response = df.at[df.index[index], 'response']
            similar_responses.append(response)
        else:
            break  # Break if similarity falls below the threshold

    return similar_responses if similar_responses else ["I'm sorry!!! I'm not trained to respond to that question."]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cont')
def cont():
    return render_template('cont.html')

@app.route('/comparison')
def comparison():
    return render_template('comparison.html')

@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        # Handle the form submission logic here
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Add your logic for processing the form data here (e.g., create a new user)
        # For simplicity, let's assume the sign-up is successful without validation

        # Redirect to the login page
        return redirect(url_for('login'))

    return render_template('sign.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle the form submission logic here
        email = request.form['email']
        password = request.form['password']

        # Check if the email exists in the users dictionary
        if email in users and users[email]['password'] == password:
            # Add more advanced authentication logic as needed
            # For simplicity, let's assume the login is successful

            # Redirect to the indexc page (change the route as needed)
            return redirect(url_for('indexc'))

    # Render the login page for GET requests or failed login attempts
    return render_template('login.html')

@app.route('/index1')
def index1():
    return render_template('index1.html')

@app.route('/indexc')
def indexc():
    return render_template('indexc.html')

@app.route('/slider')
def slider():
    return render_template('slider.html')

@app.route('/songs')
def songs():
    return render_template('songs.html')

@app.route('/Tictactoe')
def Tictactoe():
    return render_template('Tictactoe.html')

@app.route('/who')
def who():
    return render_template('who.html')



@app.route("/get_response", methods=["POST"])
def get_bot_response():
    user_input = request.form["user_input"]
    bot_responses = get_responses(user_input)
    return render_template("indexc.html", user_input=user_input, bot_responses=bot_responses)

from waitress import serve
from app import app  # Assuming your Flask app instance is named 'app' and is defined in app.py

if __name__ == '__main__':
    serve(app, port=3000)

