/* jshint esversion: 8 */
/* jshint browser: true */
'use strict';

var outputScreen;
var clearOnEntry;


/**
 * Display a digit on the `outputScreen`
 * 
 * @param {number} digit digit to add or display on the `outputScreen`
 */
function enterDigit(digit) {
    if (clearOnEntry) {
        outputScreen.textContent = '';
        clearOnEntry = false;
    }
    outputScreen.textContent += digit;
    expression += digit;
}


/**
 * Clear `outputScreen` and set value to 0
 */
function clear_screen() {
    outputScreen.textContent = '';
    expression = '';
    clearOnEntry = true;
}


/**
 * Evaluate the expression and display its result or *ERROR*
 */
function eval_expr() {
    try {
        var result = eval(expression);
        if (isNaN(result) || result === Infinity) {
            outputScreen.textContent = 'ERROR';
        } else {
            outputScreen.textContent = result;
        }
        expression = result.toString();
        clearOnEntry = true;
    } catch (error) {
        outputScreen.textContent = 'ERROR';
        expression = '';
        clearOnEntry = true;
    }
}


/**
 * Display an operation on the `outputScreen`
 * 
 * @param {string} operation to add to the expression
 */
function enterOp(operation) {
    if (clearOnEntry) {
        outputScreen.textContent = '';
        clearOnEntry = false;
    }
    outputScreen.textContent += operation;
    expression += operation;
}


window.onload = function () {
    outputScreen = document.querySelector("#result");
    clearOnEntry = true;
};
