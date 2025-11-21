# api/index.py
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Load .env only in local development
if os.getenv("VERCEL") is None:
    load_dotenv()

app = Flask(__name__, template_folder='../templates')

GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")
if not GIPHY_API_KEY:
    raise RuntimeError("GIPHY_API_KEY is missing!")

# === All your routes exactly the same as before ===
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/advice')
def advice_page():
    return render_template('advice.html')

@app.route('/api/advice')
def get_advice():
    try:
        r = requests.get('https://api.adviceslip.com/advice', timeout=5)
        return jsonify(r.json())
    except:
        return jsonify({"slip": {"advice": "Keep going, you're doing great!"}})

@app.route('/giphy')
def giphy_page():
    query = request.args.get('q', '').strip()
    url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={query}&limit=20&rating=pg-13" if query \
          else f"https://api.giphy.com/v1/gifs/trending?api_key={GIPHY_API_KEY}&limit=20&rating=pg-13"
    try:
        gifs = requests.get(url, timeout=10).json().get('data', [])
    except:
        gifs = []
    return render_template('giphy.html', gifs=gifs, query=query)

@app.route('/bored')
def bored_page():
    return render_template('bored.html')

@app.route('/api/bored')
def get_activity():
    try:
        data = requests.get('https://bored-api.appbrewery.com/random', timeout=5).json()
        if 'activity' in data:
            return jsonify(data)
    except:
        pass
    return jsonify({
        "activity": "Deploying to Vercel successfully! 🎉",
        "type": "education",
        "participants": 1,
        "price": 0,
        "accessibility": 1.0
    })

# === THIS IS THE ONLY LINE YOU NEED FOR VERCEL ===
from mangum import Mangum
handler = Mangum(app)   # this makes it work serverless