import random
from typing import List

import pyjokes
from flask import Flask, render_template, request

app = Flask(__name__)

languages = ["en", "es", "de"]
categories = ["neutral", "all", "chuck"]
numbers = [1, 5, 10]

@app.route("/", methods=["GET"])
def index():
    """Render the template with form"""
    return render_template('base.html', languages=languages, categories=categories, numbers=numbers)


@app.route("/", methods=["POST"])
def index_jokes():
        """Render the template with jokes"""
        language = request.form.get('language')
        category = request.form.get('category')
        num_jokes = request.form.get('number')
        
        jokes = []
        try:
            for _ in range(int(num_jokes)):
                joke = pyjokes.get_joke(language=language, category=category)
                jokes.append(joke)
        except Exception as e:
            error_message = str(e)
            return render_template('base.html', languages=languages, categories=categories, numbers=numbers,  error_message=error_message, )

        return render_template('jokes.html', language=language, category=category, number=numbers, jokes=jokes)

    

if __name__ == "__main__":
    app.run(debug=True)

def send_joke(
    language: str = "en", category: str = "all", number: int = 1) -> List[str]:
    """Return a list of jokes"""
    if language == "es" and category == "chuck":
        return ["No kidding!"]
    else:
        jokes = []
        for x in range(number):
            joke = pyjokes.get_joke(language=language, category=category)
            jokes.append(joke)
    
    return jokes

