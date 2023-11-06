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
            unique_jokes = set()
            while len(jokes) < int(num_jokes):
                joke = pyjokes.get_joke(language=language, category=category)
                if joke not in unique_jokes:
                    unique_jokes.add(joke)
                    jokes.append(joke)
        except Exception as e:
            error_message = str(e)
            return render_template('base.html', languages=languages, categories=categories, numbers=numbers,  error_message=error_message, )

        return render_template('jokes.html', language=language, category=category, number=numbers, jokes=jokes)

    

if __name__ == "__main__":
    app.run(debug=True)

def send_joke(
    language: str = "en", category: str = "all", number: int = 1) -> List[str]:
    """Return a list of unique jokes"""
    if language == "es" and category == "chuck":
        return ["No kidding!"]
    else:
        
        all_jokes = pyjokes.get_jokes(language=language, category=category)
        jokes = random.sample(all_jokes, min(number, len(all_jokes)))
    
    return jokes
    

