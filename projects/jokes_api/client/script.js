'use strict';

var apiUrl = 'http://localhost:5000/api/v1/jokes';
var apiUrl2 = 'http://localhost:5000/api/v1/jokes/';

// Populate the category select element
var selCat = document.getElementById('selCat');
var categories = ['all', 'chuck', 'neutral'];
for (var i = 0; i < categories.length; i++) {
    var option = document.createElement('option');
    option.text = categories[i];
    option.value = categories[i];
    selCat.add(option);
}

// Populate the language select element
var selLang = document.getElementById('selLang');
var languages = ['en', 'es', 'de'];
for (var i = 0; i < languages.length; i++) {
    var option = document.createElement('option');
    option.text = languages[i];
    option.value = languages[i];
    selLang.add(option);
}

var selNum = document.getElementById('selNum');
var categories = ['1', '2', '3', '5', '10'];
for (var i = 0; i < categories.length; i++) {
    var option = document.createElement('option');
    option.text = categories[i];
    option.value = categories[i];
    selNum.add(option);

}

// Add event listener to the form submit button
var btnAmuse = document.getElementById('btnAmuse');
btnAmuse.addEventListener('click', function(event) {
    event.preventDefault();
    var category = selCat.value;
    var language = selLang.value;
    var number = selNum.value;
    if (!number) {
        var jokesDiv = document.getElementById('jokes');
        jokesDiv.innerHTML = '<p>Please enter a value for number</p>';
        return;
    }
    if (!Number.isInteger(Number(number))) {
        var jokesDiv = document.getElementById('jokes');
        jokesDiv.innerHTML = '<p>Please enter a valid integer for Number</p>';
        return;
    }

    var url = apiUrl + '?category=' + category + '&language=' + language + '&number=' + number;
    fetch(url)
        .then(response => response.json())
        .then(function(data) {
            if (data.error) {
                var jokesDiv = document.getElementById('jokes');
                jokesDiv.innerHTML = '<p>' + data.error + '</p>';
            } else {
            var jokes = data.jokes;
            var jokesDiv = document.getElementById('jokes');
            jokesDiv.innerHTML = '';
            for (var i = 0; i < jokes.length; i++) {
                var jokeDiv = document.createElement('div');
                jokeDiv.innerHTML = '<p>' + jokes[i].joke + '</p>';
                jokesDiv.appendChild(jokeDiv);
            }}
        })
        .catch(function(error) {
            var jokesDiv = document.getElementById('jokes');
            jokesDiv.innerHTML = '<p>' + error.message + '</p>';
        });
});


// Add event listener to the form submit button
var btnAmuse2 = document.getElementById('btnAmuse2');
btnAmuse2.addEventListener('click', function(event) {
    event.preventDefault();
    var category = selCat.value;
    var language = selLang.value;
    var id = selid.value;
    if (!id) {
        var jokesDiv = document.getElementById('jokes');
        jokesDiv.innerHTML = '<p>Please enter a value for id</p>';
        return;
    }
    var url = apiUrl2 + language + '/' + category + '/' + id;
    fetch(url)
        .then(response => response.json())
        .then(function(data) {
            if (data.error) {
                var jokesDiv = document.getElementById('jokes');
                jokesDiv.innerHTML = '<p>' + data.error + '</p>';
            } else {
                var jokes = data.joke;
                var jokesDiv = document.getElementById('jokes');
                jokesDiv.innerHTML = '';
                jokesDiv.innerHTML = jokes;
            }
        })
        .catch(function(error) {
            var jokesDiv = document.getElementById('jokes');
            jokesDiv.innerHTML = '<p>' + error.message + '</p>';
        });
})