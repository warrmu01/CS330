/* jshint esversion: 8 */
/* jshint browser: true */
"use strict";

var team = ["Aardvark", "Beaver", "Cheetah", "Dolphin", "Elephant", "Flamingo", "Giraffe", "Hippo"];
var priority = ["Low", "Normal", "Important", "Critical"];

/**
 * Add a new task to the list
 * 
 * Validate form, collect input values, and add call `addRow` to add a new row to the table
 */
function addTask() {
    const titleInput = document.getElementById("title").value;
    const assignedToInput = document.getElementById("assignedTo").value;
    const priorityInput = document.getElementById("priority").value;
    const dueDateInput = document.getElementById("dueDate").value;
 
    if (!titleInput || !assignedToInput || !priorityInput || !dueDateInput) {
        showFeedbackMessage("Fill out all required fields.");
        return; 
    }
 
    let vals = [titleInput, assignedToInput, priorityInput, dueDateInput];
 
    addRow(vals, "taskList");
 
    document.getElementById("newTask").reset();
 
    showFeedbackMessage("Task added successfully.", "success");
 }
 
 /**
 * Display a feedback message
 * 
 * @param {string} message The message to display
 * @param {string} type (optional) The type of message (e.g., "success", "error")
 */
 function showFeedbackMessage(message, type = "error") {
    const feedbackMessage = document.getElementById("feedbackMessage");
 
    feedbackMessage.textContent = "Fill out title and due date"; 
    feedbackMessage.className = type;
 
    setTimeout(function () {
        feedbackMessage.textContent = "";
        feedbackMessage.className = "";
    }, 3000);
 }

/**
 * Add a new row to the table
 * 
 * @param {string[]} valueList list of task attributes
 * @param {Object} parent DOM node to append to
 */

function addRow(valueList, tbodyId) {

    let tbody = document.getElementById('newrow');

    let row = document.createElement("tr");

    let checkboxCell = document.createElement("td");
    let checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkboxCell.appendChild(checkbox);
    row.appendChild(checkboxCell);

    for (let i = 0; i < valueList.length; i++) {
        let cell = document.createElement("td");
        cell.textContent = valueList[i];

        if (i === 2) {

            switch (valueList[i]) {
                case "Low":
                    row.classList.add("low");
                    break;
                case "Normal":
                    row.classList.add("normal");
                    break;
                case "Important":
                    row.classList.add("important");
                    break;
                case "Critical":
                    row.classList.add("critical");
                    break;
            }
        }

        row.appendChild(cell);
    }

    tbody.appendChild(row);
}

/**
 * Remove a table row corresponding to the selected checkbox
 * 
 * https://stackoverflow.com/questions/26512386/remove-current-row-tr-when-checkbox-is-checked
 */
function removeRow() {

    let checkboxes = document.querySelectorAll('#taskList tbody input[type="checkbox"]:checked');

    checkboxes.forEach(function (checkbox) {
        let row = checkbox.closest('tr');
        if (row) {
            row.remove();
        }
    });
}

/**
 * Remove all table rows
 * 
 */
function selectAll() {
    let tableBody = document.querySelector('#taskList tbody');

    while (tableBody.firstChild) {
        tableBody.removeChild(tableBody.firstChild);
    }
}

/**
 * Add options to the specified element
 * 
 * @param {string} selectId `select` element to populate
 * @param {string[]} sList array of options
 */
function populateSelect(selectElementId, sList) {
    let selectElement = document.querySelector(selectElementId);
    for (let opt of sList) {
        let optElem = document.createElement("option");
        optElem.setAttribute("option", opt);
        optElem.innerHTML = opt;
        selectElement.appendChild(optElem);
    }
}

// 

window.onload = function () {
    populateSelect(("#assignedTo"), team);
    populateSelect(("#priority"), priority);

    const checkboxes = document.querySelectorAll('#taskList tbody input[type="checkbox"]');

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            if (this.checked) {
                removeRow();
            }
        });
    });
}

