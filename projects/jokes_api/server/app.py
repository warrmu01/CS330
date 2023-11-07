#!/usr/bin/env python3
"""
jokes api
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pyjokes

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/v1/jokes', methods=['GET'])
def get_jokes():
    category = request.args.get('category')
    language = request.args.get('language')
    number = int(request.args.get('number'))
    if category == 'chuck' and language == 'es':
        return jsonify({'error': 'No jokes available for category "chuck" and language "es"'}), 404
    jokes = pyjokes.get_jokes(category=category, language=language)
    if not jokes:
        return jsonify({'error': 'Invalid category or language'}), 404
    if number > len(jokes):
        return jsonify({'error': 'Number of jokes requested exceeds the total number of jokes available'}), 404
    random_jokes = []
    for i in range(number):
        random_jokes.append({'joke': pyjokes.get_joke(category=category, language=language)})
    return jsonify({'jokes': random_jokes})

@app.route('/api/v1/jokes/<string:language>/<string:category>/<int:id>', methods=['GET'])
def get_joke(language, category, id):
    if category == 'chuck' and language == 'es':
        return jsonify({'error': 'No jokes available for category "chuck" and language "es"'}), 404
    jokes = pyjokes.get_jokes(category=category, language=language)
    if not jokes:
        return jsonify({'error': 'Invalid category or language'}), 404
    if id >= len(jokes):
        return jsonify({'error': 'Joke ID not found'}), 404
    return jsonify({'id': id, 'joke': jokes[id]})


if __name__ == '__main__':
    app.run(debug=True)
