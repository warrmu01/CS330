"use strict";

var myFootlockerModel = new Footlocker();
var myFootlockerView = new FootlockerView(myFootlockerModel);

/**
 * Populate select
 * @param {Selector idx} selectElementId 
 * @param {Options} options 
 */
function populateSelect(selectElementId, options) {
    let selectElement = document.querySelector(selectElementId);
    for (let opt of options) {
        let optElem = document.createElement("option");
        optElem.setAttribute("value", opt);
        optElem.innerHTML = opt;
        selectElement.appendChild(optElem);
    }
}

/**
 * Add a pair of shoes to the footlocker
 * @returns if the form is invalid
 * 
 * 
 * 
 */
function addPair() {
    if (!document.querySelector("#New_Order").checkValidity()) {
        return;
    }

    let order = localStorage.getItem("myOrder");
    order = order ? JSON.parse(order) : [];

    let foodSelect = document.querySelector("#sel_food");
    let size = document.querySelector("#sel_quantity").value;
    let price = document.querySelector("#sel_price").value;

    if (foodSelect.selectedIndex === -1) {
        console.error("No food option selected.");
        return;
    }

    let food = foodSelect.options[foodSelect.selectedIndex].value;

    let newPair = {
        "food": food,
        "size": size,
        "price": price
    };

    order.push(newPair);
    localStorage.setItem("myOrder", JSON.stringify(order));

    myFootlockerModel.add(newPair);
    loadOutfits();
}
function loadOutfits() {
    let order = localStorage.getItem("myOrder");
    order = order ? JSON.parse(order) : [];
    let orderDiv = document.querySelector("#newrow");
    orderDiv.innerHTML = "";
    for (let Food of order) {
            let row = document.createElement("tr");

            let checkboxCell = document.createElement("td");
            let checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkboxCell.appendChild(checkbox);
            
            let foodCell = document.createElement("td");
            let sizeCell = document.createElement("td");
            let priceCell = document.createElement("td");
    
            foodCell.textContent = Food.food;
            sizeCell.textContent = Food.size;
            priceCell.textContent = Food.price;


            row.appendChild(checkboxCell);
            row.appendChild(foodCell);
            row.appendChild(sizeCell);
            row.appendChild(priceCell);

    
            orderDiv.appendChild(row);
        }
    }

function clearAll() {
    localStorage.removeItem("myOrder");
    loadOutfits();
}
function removeCheckedRows() {
    let checkboxes = document.querySelectorAll("#newrow input[type='checkbox']");
    let order = localStorage.getItem("myOrder");
    order = order ? JSON.parse(order) : [];

    let newOrder = [];

    for (let i = 0; i < checkboxes.length; i++) {
        if (!checkboxes[i].checked) {
            newOrder.push(order[i]);
        }
    }

    localStorage.setItem("myOrder", JSON.stringify(newOrder));

    loadOutfits();
}

window.onload = function (params) {
    populateSelect("#sel_food", ["Chicken", "Fried Rice", "Tacos", "Nachos"]);
}

