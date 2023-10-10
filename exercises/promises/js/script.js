async function getData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    } catch (error) {
        console.error("Error fetching data: ", error);
        return null; 
    }
}
async function get_individual(num, all_numbers) {
    all_numbers.innerHTML = "";

    for (let i = num - 1; i <= num + 1; i++) {
        const data = await getData(`http://numbersapi.com/${i}`);
        
        const numberContainer = document.createElement("div");
        numberContainer.className = "numbercontainer"; 
        
        const numberValueDiv = document.createElement("div");
        numberValueDiv.className = "numbervalues"; 
        numberValueDiv.innerHTML = `${i}`;
        
        const triviaDiv = document.createElement("div");
        triviaDiv.className = "trivia"; 
        triviaDiv.innerHTML = `${data}`; 
        
        numberContainer.appendChild(numberValueDiv);
        numberContainer.appendChild(triviaDiv);

        all_numbers.appendChild(numberContainer);
    }
}

async function get_batch(num, all_numbers) {
    all_numbers.innerHTML = "";

    const promises = [];

    for (let i = num - 1; i <= num + 1; i++) {
        promises.push(getData(`http://numbersapi.com/${i}`));
    }

    try {
        const results = await Promise.all(promises);

        results.forEach((data, index) => {
            const numberDiv = document.createElement("div");
            numberDiv.className = "numbercontainer"; 
            
            const numberValueDiv = document.createElement("div");
            numberValueDiv.className = "numbervalues"; 
            numberValueDiv.innerHTML = `${num + index - 1}`;
            
            const triviaDiv = document.createElement("div");
            triviaDiv.className = "trivia"; 
            triviaDiv.innerHTML = `${data}`;
            
            numberDiv.appendChild(numberValueDiv);
            numberDiv.appendChild(triviaDiv);

            all_numbers.appendChild(numberDiv);
        });
    } catch (error) {
        console.error("Error fetching data: ", error);
    }
}

async function clickedon() {
    let num = parseInt(document.querySelector('#number').value);
    let all_numbers = document.querySelector('#number_info');

    if (document.querySelector('#batch').checked) {
        get_batch(num, all_numbers);
    } else {
        get_individual(num, all_numbers);
    }
}