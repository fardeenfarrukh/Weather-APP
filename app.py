from flask import Flask, render_template, request, jsonify, url_for
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')
BASE_URL = "http://api.weatherapi.com/v1/current.json"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    if city:
        params = {
            'key': API_KEY,
            'q': city
        }
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'location': data['location']['name'],
                'temperature': data['current']['temp_c'],
                'condition': data['current']['condition']['text'],
                'icon': data['current']['condition']['icon'],
                'humidity': data['current']['humidity'],
                'wind_speed': data['current']['wind_kph']
            }
            return render_template('index.html', weather=weather_data)
        else:
            error_message = "City not found or API error!"
            return render_template('index.html', error=error_message)
    else:
        error_message = "Please enter a city!"
        return render_template('index.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
