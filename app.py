from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Securely load the GIPHY API key
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

# Optional: fallback if key is missing (helps during development)
if not GIPHY_API_KEY:
    raise RuntimeError("GIPHY_API_KEY not found in .env file! Add it and restart.")

# ==================== HOME / DASHBOARD ====================
@app.route('/')
def index():
    return render_template('index.html')

# ==================== ADVICE SLIP ====================
@app.route('/advice')
def advice_page():
    return render_template('advice.html')

@app.route('/api/advice')
def get_advice():
    try:
        r = requests.get('https://api.adviceslip.com/advice', timeout=5)
        return jsonify(r.json())
    except:
        return jsonify({"slip": {"id": 0, "advice": "Everything will be okay in the end. If it's not okay, it's not the end."}})

# ==================== GIPHY ====================
@app.route('/giphy')
def giphy_page():
    query = request.args.get('q', '').strip()

    if query:
        url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={query}&limit=20&rating=pg-13&lang=en"
    else:
        url = f"https://api.giphy.com/v1/gifs/trending?api_key={GIPHY_API_KEY}&limit=20&rating=pg-13"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raises exception for bad status
        gifs = response.json().get('data', [])
    except requests.exceptions.RequestException:
        gifs = []

    return render_template('giphy.html', gifs=gifs, query=query)

# ==================== BORED API (reliable mirror) ====================
@app.route('/bored')
def bored_page():
    return render_template('bored.html')

@app.route('/api/bored')
def get_activity():
    try:
        response = requests.get('https://bored-api.appbrewery.com/random', timeout=5)
        data = response.json()
        if 'activity' in data:
            return jsonify(data)
    except:
        pass

    # Fallback
    return jsonify({
        "activity": "Take a few deep breaths and enjoy the moment 🌿",
        "type": "relaxation",
        "participants": 1,
        "price": 0,
        "accessibility": 1.0,
        "link": ""
    })

if __name__ == '__main__':
    app.run(debug=True)