/* jshint esversion: 8 */
/* jshint node: true */
/* jshint browser: true */
'use strict';


/**
 * Greet user by name
 * 
 * @param {string} name visitor's name
 * @param {string} selector element to use for display
 */
function greet(name, selector) {
    const greetingElement = document.querySelector(selector);
    greetingElement.textContent = `Welcome, ${name}!`;
}


/**
 * Check if a number is prime
 * 
 * @param {number} number number to check
 * @return {boolean} result of the check
 */
function isPrime(number) {
    if (number <= 1) return false;
    if (number <= 3) return true;
    if (number % 2 === 0 || number % 3 === 0) return false;

    for (let i = 5; i * i <= number; i += 6) {
        if (number % i === 0 || number % (i + 2) === 0) {
            return false;
        }
    }

    return true;
}


/**
 * Print whether a number is prime
 * 
 * @param {number} number number to check
 * @param {string} selector element to use for display
 */
function printNumberInfo(number, selector) {
    const numberInfoElement = document.querySelector(selector);
    const isPrimeMessage = isPrime(number) ? 'is prime' : 'is not prime';
    numberInfoElement.textContent = `${number} ${isPrimeMessage}`;
}



/**
 * Generate an array of prime numbers
 * 
 * @param {number} number number of primes to generate
 * @return {number[]} an array of `number` prime numbers
 */
function getNPrimes(number) {
    const primes = [];
    let currentNumber = 2;

    while (primes.length < number) {
        if (isPrime(currentNumber)) {
            primes.push(currentNumber);
        }
        currentNumber++;
    }

    return primes;
}


/**
 * Print a table of prime numbers
 * 
 * @param {number} number number of primes to display
 * @param {string} selector element to use for display
 */
function printNPrimes(number, selector) {
    const tableBody = document.querySelector(`${selector} tbody`);
    const primes = getNPrimes(number);

    tableBody.innerHTML = ''; 

    primes.forEach((prime) => {
        const row = document.createElement('tr');
        const cell = document.createElement('td');
        cell.textContent = prime;
        row.appendChild(cell);
        tableBody.appendChild(row);
    });
}


/**
 * Display warning about missing URL query parameters
 * 
 * @param {Object} urlParams URL parameters
 * @param {string} selector element to use for display
 */
function displayWarnings(urlParams, selector) {
    
}

const urlParams = new URLSearchParams(window.location.search);
const name = urlParams.get('name') || 'student';
const number = parseInt(urlParams.get('number')) || 330;

window.onload = function () {
    // TODO: Initialize the following variables

    this.displayWarnings(urlParams, "#warnings");
    greet(name, "#greeting");
    printNumberInfo(number, "#numberInfo");
    printNPrimes(number, "table#nPrimes");
};
