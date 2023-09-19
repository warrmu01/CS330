/* jshint esversion: 8 */
/* jshint browser: true */
'use strict';

var outputScreen;
var clearOnEntry;
var expression;

/**
 * Display a digit on the `outputScreen`
 * 
 * @param {number} digit digit to add or display on the `outputScreen`
 */
function enterDigit(digit) {
  document.querySelector("#result").innerText += digit;
  expression += digit;
}

/**
 * Clear `outputScreen` and set value to 0
 */
function clear_screen() {
  document.querySelector("#result").innerText = "0" ;
  expression =  ' ' ;
  clearOnEntry = true;
}

/**
 * Evaluate the expression and display its result or *ERROR*
 */
function eval_expr() {
  try {
    var result = eval(expression);
    document.querySelector("#result").innerText = result;
    expression = result.toString();
    clearOnEntry = false;
  } catch (error) {
    document.querySelector("#result").innerText= 'ERROR';
    expression = ' ';
    
    clearOnEntry = true;
  }
}

/**
 * Display an operation on the `outputScreen`
 * 
 * @param {string} operation to add to the expression
 */
function enterOp(operation) {
    document.querySelector("#result").innerText += operation;
    expression += operation;
  }

window.onload = function () {
  outputScreen = document.querySelector("#result")
   clear_screen();
};
