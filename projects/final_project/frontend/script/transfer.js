var user_info = null;
var empty_player_divs = [1,2,3,4,5];
var player_div_number_player_index_object={
    1:-1,
    2:-1,
    3:-1,
    4:-1,
    5:-1,
}
var moneyRemaining = 50;

// Function to show the modal
 const showModal = (modalId) => {
     const modal = document.getElementById(modalId);
     if (modal) {
         modal.classList.remove('hidden');
         modal.setAttribute('aria-hidden', 'false');
     }
 };

 // Function to hide the modal
 const hideModal = (modalId) => {
     const modal = document.getElementById(modalId);
     if (modal) {
         modal.classList.add('hidden');
         modal.setAttribute('aria-hidden', 'true');
     }
 };

 document.addEventListener('click', (event) => {
     const toggleTarget = event.target.dataset.modalToggle;
     const hideTarget = event.target.dataset.modalHide;

     if (toggleTarget) {
         showModal(toggleTarget);
     }

     if (hideTarget) {
         hideModal(hideTarget);
     }
 });

 // Initialize an array to store goalkeeper player IDs
 let goalkeeperPlayerIds = [];

 // Fetch goalkeepers data
 fetch('http://supremepaudel.pythonanywhere.com/goalkeepers')
     .then(response => response.json())
     .then(goalkeepersData => {
         // Process and display goalkeeper data
         goalkeepersData.forEach(goalkeeper => {

         goalkeeperPlayerIds.push(goalkeeper.player_id);
         // Process and display goalkeeper data
         // This could involve creating HTML elements or updating a table, for example
         const playerContainer = document.createElement('div');
         playerContainer.className = 'mb-4 grid grid-cols-5 gap-2 text-center';

         // Info Button
         const infoButton = document.createElement('button');
         infoButton.textContent = 'Info';
         infoButton.className = 'text-blue-700 hover:underline cursor-pointer text-center';
         infoButton.dataset.modalToggle = 'info-modal'; // Set your modal ID
         infoButton.addEventListener('click', () => showKeeperInfo(goalkeeper));
         playerContainer.appendChild(infoButton);

         // College
         const playerCollege = document.createElement('div');
         playerCollege.textContent = goalkeeper.college;
         playerCollege.className = 'col-span-1 text-center'; // Added text-center
         playerContainer.appendChild(playerCollege);

         // Name
         const playerName = document.createElement('div');
         playerName.textContent = goalkeeper.name;
         playerName.className = 'col-span-1 text-center'; // Added text-center
         playerContainer.appendChild(playerName);

         // Price
         const playerPrice = document.createElement('div');
         playerPrice.textContent = `$${goalkeeper.price} m`;
         playerPrice.className = 'col-span-1 text-center'; // Added text-center
         playerContainer.appendChild(playerPrice);

                         // Add Button
         const addButton = document.createElement('button');
         addButton.textContent = 'Add';
         addButton.className = 'bg-green-500 text-white px-4 py-2 rounded';
         addButton.addEventListener('click', () => addPlayerToTeam(goalkeeper));
         playerContainer.appendChild(addButton);

         // Append the player container to the side column
         sideColumn.appendChild(playerContainer);
     });


         });

     // Fetch players data
     fetch('http://supremepaudel.pythonanywhere.com/players')
         .then(response => response.json())
         .then(playersData => {
         // Filter out players that are already goalkeepers
         const filteredPlayers = playersData.filter(player => {
             // Assuming there's a unique identifier like 'id' for each player
             return !goalkeeperPlayerIds.includes(player.id);
         });

                 // Process and display player data
                 filteredPlayers.forEach(player => {
                     // Process and display player data
                     // This could involve creating HTML elements or updating a table, for example
                     const playerContainer = document.createElement('div');
                     playerContainer.className = 'mb-4 grid grid-cols-5 gap-2 text-center';

                         // / Info Button
                     const infoButton = document.createElement('button');
                     infoButton.textContent = 'Info';
                     infoButton.className = 'text-blue-700 hover:underline cursor-pointer text-center';
                     infoButton.dataset.modalToggle = 'info-modal'; // Set your modal ID
                     infoButton.addEventListener('click', () => showPlayerInfo(player));
                     playerContainer.appendChild(infoButton);
         
                     // College
                     const playerCollege = document.createElement('div');
                     playerCollege.textContent = player.college;
                     playerCollege.className = 'col-span-1 text-center'; // Added text-center
                     playerContainer.appendChild(playerCollege);
         
                     // Name
                     const playerName = document.createElement('div');
                     playerName.textContent = player.name;
                     playerName.className = 'col-span-1 text-center'; // Added text-center
                     playerContainer.appendChild(playerName);
         
                     // Price
                     const playerPrice = document.createElement('div');
                     playerPrice.textContent = `$${player.price} m`;
                     playerPrice.className = 'col-span-1 text-center'; // Added text-center
                     playerContainer.appendChild(playerPrice);

                                     // Add Button
                     const addButton = document.createElement('button');
                     addButton.textContent = 'Add';
                     addButton.className = 'bg-green-500 text-white px-4 py-2 rounded';
                     addButton.addEventListener('click', () => addPlayerToTeam(player));
                     playerContainer.appendChild(addButton);
         
                     // Append the player container to the side column
                     sideColumn.appendChild(playerContainer);
                 });
             })

             .catch(error => console.error('Error fetching data:', error));

             const playerInfoContent = document.getElementById('player-info-content');

             function showKeeperInfo(goalkeeper) {
             // Populate modal with player information
             playerInfoContent.innerHTML = `
                     <div class="flex">
                 <div class="flex-1 pr-4">
                     <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                         Player Name: ${goalkeeper.name}
                     </p>
                     <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                         Team: ${goalkeeper.college}
                     </p>
                     <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                         Saves: ${goalkeeper.SV}
                     </p>
                     <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                         Save percentage: ${goalkeeper.SV_percentage}
                     </p>
                     <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                         Total Points for the season: ${goalkeeper.PTS}
                     </p>
                     <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                         Points per game: ${goalkeeper.PTS_G}
                     </p>
                 </div>
                 <div>
                     <img src="images/${goalkeeper.college.toLowerCase()}.png" alt="${goalkeeper.college} Logo" class="w-100 h-100 ml-auto">
                 </div>
             </div>
             `;

             // Show the info modal
             const infoModal = document.getElementById('info-modal');
             infoModal.classList.remove('hidden');
             }

             // const playerInfoContent = document.getElementById('player-info-content');

             function showPlayerInfo(player) {
             // Populate modal with player information
             playerInfoContent.innerHTML = `
                     <div class="flex">
                 <div class="flex-1 pr-4">
                     <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                         Player Name: ${player.name}
                     </p>
                     <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                         Team: ${player.college}
                     </p>
                     <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                         Goals Scored: ${player.G}
                     </p>
                     <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                         Assists: ${player.A}
                     </p>
                     <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                         Total Points for the season: ${player.PTS}
                     </p>
                     <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                         Points per game: ${player.PTS_G}
                     </p>
                 </div>
                 <div>
                     <img src="images/${player.college.toLowerCase()}.png" alt="${player.college} Logo" class="w-100 h-100 ml-auto">
                 </div>
             </div>
             `;
 
             // Show the info modal
             const infoModal = document.getElementById('info-modal');
             infoModal.classList.remove('hidden');
         }
         
                     // Apply Button Click Event
         const applyButton = document.getElementById('applyButton');
         applyButton.addEventListener('click', applyFilters);

         function applyFilters(event) {
         event.preventDefault(); // Prevent the default behavior of the button click event

         const selectedCollege = document.getElementById('collegeDropdown').value;
         const selectedPriceRange = document.getElementById('priceRangeDropdown').value;

         // Fetch and update the player list based on filters
         fetch(`http://supremepaudel.pythonanywhere.com/players?college=${selectedCollege}&price=${selectedPriceRange}`)
             .then(response => response.json())
             .then(filteredPlayers => {
                 
                 // Clear existing player list
                 const sideColumn = document.getElementById('sideColumn');
                 sideColumn.innerHTML = '';
                 reset_div_element(sideColumn);
             // Re-populate the player list with filtered data
                 filteredPlayers.forEach(player => {
                 const playerContainer = document.createElement('div');
                 playerContainer.className = 'mb-4 grid grid-cols-5 gap-2 text-center';

                 // Info Button
                 const infoButton = document.createElement('button');
                 infoButton.textContent = 'Info';
                 infoButton.className = 'text-blue-700 hover:underline cursor-pointer text-center';
                 infoButton.dataset.modalToggle = 'info-modal';
                 infoButton.addEventListener('click', () => showPlayerInfo(player));
                 playerContainer.appendChild(infoButton);

                 // College
                 const playerCollege = document.createElement('div');
                 playerCollege.textContent = player.college;
                 playerCollege.className = 'col-span-1 text-center';
                 playerContainer.appendChild(playerCollege);

                 // Name
                 const playerName = document.createElement('div');
                 playerName.textContent = player.name;
                 playerName.className = 'col-span-1 text-center';
                 playerContainer.appendChild(playerName);

                 // Price
                 const playerPrice = document.createElement('div');
                 playerPrice.textContent = `$${player.price} m`;
                 playerPrice.className = 'col-span-1 text-center';
                 playerContainer.appendChild(playerPrice);

                                 // Add Button
                 const addButton = document.createElement('button');
                 addButton.textContent = 'Add';
                 addButton.className = 'bg-green-500 text-white px-4 py-2 rounded';
                 addButton.addEventListener('click', () => addPlayerToTeam(player));
                 playerContainer.appendChild(addButton);

                 // Append the player container to the side column
                 sideColumn.appendChild(playerContainer);
             });
         })
         .catch(error => console.error('Error fetching filtered data:', error));
 }

         function addPlayerToTeam(player) {
            // only add if the array empty_player_divs is not empty
            if (empty_player_divs.length == 0){
                // alert : cannot add
                display_error_message("Cannot add player to the team");
                return;
            } else if (moneyRemaining - player.price < 0){
                display_error_message("Out of budget");
                return;
            }

            let div_id = empty_player_divs.pop()
            player_div_number_player_index_object[div_id] = player.id
            show_individual_player_info(div_id, player, json_is_player_object=true)
 }
         function submitDataToServer(){
            // if any divs empty: error
            if (empty_player_divs.length != 0){
                display_error_message("Incomplete number of players !");
            // if price above 50 million, error
            } else if (moneyRemaining < 0) {
                display_error_message("Out of Budget");
            } else {
                // get player id and username and token
                let ids = Object.values(player_div_number_player_index_object);
                let username = window.sessionStorage.getItem('username');
                let token = window.sessionStorage.getItem('token');
                // send post request with all those data
                send_info_to_backend(ids, username, token);
            }
        }

         function send_info_to_backend(ids, username, token){
            // if successful , show a new team saved message
            const headers = new Headers({
        "Content-Type": "application/x-www-form-urlencoded"
      });
      
            const urlencoded = new URLSearchParams({
        "username": username,
        "token": token,
        "player_ids": ids,
        "money_used": 50-moneyRemaining
      });
      
      const opts = {
        method: 'POST',
        headers: headers,
        body: urlencoded,
      };
      
        fetch(
        "http://supremepaudel.pythonanywhere.com/changeteam",
        opts
          )
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
            // invalid login attempt
            throw new Error('Something went wrong');
          })
          .then((responseJson) => {
            // alert saying new team has been saved

            // set username and new tokenID in session storage
            window.sessionStorage.setItem('username', responseJson.username);
            window.sessionStorage.setItem('token', responseJson.token);
            display_success_message("Team saved!")

          })
          .catch((error) => {
            display_error_message("Unable to save team!");
            console.log(error);
          });


         }

         function display_error_message(message){

            let error_div = document.querySelector("#errorMessage");
            error_div.innerHTML = `
  <div class="w-full md:w-1/3 mx-auto">
  <div class="flex flex-col p-5 rounded-lg shadow bg-white">
	<div class="flex flex-col items-center text-center">
	  <div class="inline-block p-4 bg-yellow-50 rounded-full">
		<svg class="w-12 h-12 fill-current text-yellow-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M12 5.99L19.53 19H4.47L12 5.99M12 2L1 21h22L12 2zm1 14h-2v2h2v-2zm0-6h-2v4h2v-4z"/></svg>
	  </div>
	  <h2 class="mt-2 font-semibold text-gray-800">${message}</h2>
	</div>

	<div class="flex items-center mt-3">
	  <button onclick="document.querySelector('#errorMessage').innerHTML ='';" class="flex-1 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 text-sm font-medium rounded-md">
		Cancel
	  </button>
	</div>
  </div>
</div>
`
}
         function display_success_message(message){
            let message_div = document.querySelector("#errorMessage");
            message_div.innerHTML = `<div class="w-full md:w-1/3 mx-auto">
            <div class="bg-green-600 py-4 px-6 rounded-l-lg flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="text-white fill-current" viewBox="0 0 16 16" width="20" height="20"><path fill-rule="evenodd" d="M13.78 4.22a.75.75 0 010 1.06l-7.25 7.25a.75.75 0 01-1.06 0L2.22 9.28a.75.75 0 011.06-1.06L6 10.94l6.72-6.72a.75.75 0 011.06 0z"></path></svg>
            </div>
            <div class="px-4 py-6 bg-white rounded-r-lg flex justify-between items-center w-full border border-l-transparent border-gray-200">
              <div>Team saved successfully!</div>
              <button onclick="document.querySelector('#errorMessage').remove();">
                <svg xmlns="http://www.w3.org/2000/svg" class="fill-current text-gray-700" viewBox="0 0 16 16" width="20" height="20"><path fill-rule="evenodd" d="M3.72 3.72a.75.75 0 011.06 0L8 6.94l3.22-3.22a.75.75 0 111.06 1.06L9.06 8l3.22 3.22a.75.75 0 11-1.06 1.06L8 9.06l-3.22 3.22a.75.75 0 01-1.06-1.06L6.94 8 3.72 4.78a.75.75 0 010-1.06z"></path></svg>
              </button>
            </div>
          </div>`
}
         function reset_div_element(element){
             element.innerHTML = `<h2 class="text-2xl font-bold mb-4">Player List</h2>

 <!-- Dropdowns and Apply Button -->
 <div class="mb-4 flex space-x-4">
     <!-- College Team Dropdown -->
     <select id="collegeDropdown" class="p-2 border rounded text-black">
         <option value="All">Select College</option>
         <option value="Luther">Luther</option>
         <option value="Loras">Loras</option>
         <option value="Coe">Coe</option>
         <option value="Nebraska Wesleyan">Nebraska Wesleyan</option>
         <option value="Simpson">Simpson</option>
         <option value="Wartburg">Wartburg</option>
         <option value="Buena Vista">Buena Vista</option>
         <option value="Dubuque">Dubuque</option>
         <option value="Central">Central</option>
         <!-- Add your college options dynamically if needed -->
     </select>

     <!-- Price Range Dropdown -->
     <select id="priceRangeDropdown" class="p-2 border rounded text-black">
         <option value="">Select Price</option>
         <option value="3">3m</option>
         <option value="5">5m</option>
         <option value="8">8m</option>
         <option value="11">11m</option>
         <option value="11">13m</option>
         <option value="15">15m</option>
         <!-- Add more options as needed -->
     </select>

     <!-- Apply Button -->
     <button id="applyButton" class="bg-blue-500 text-white px-4 py-2 rounded" onclick="applyFilters(event)">Apply</button>
 </div>`
         }

function show_individual_player_info(div_id, json, json_is_player_object=false){

        if (!json_is_player_object){
        document.querySelector(`#player${div_id}name`).innerText = json[`player${div_id}`].name;
        document.querySelector(`#player${div_id}price`).innerText = `$${json[`player${div_id}`].price}M`;
        document.querySelector(`#player${div_id}img`).setAttribute("src", `images/${json[`player${div_id}`].college}.png`);
        let button_element = document.querySelector(`#player${div_id}remove`);
        button_element.removeAttribute("class");
        button_element.setAttribute("class", "bg-sky-500 hover:bg-sky-700 px-4 py-2 rounded-md opacity-50 dark:text-black");
        button_element.addEventListener("click", ()=>{reset_player_div(div_id, json[`player${div_id}`].price)})

        player_div_number_player_index_object[div_id] = json[`player${div_id}`].id;
        moneyRemaining -= json[`player${div_id}`].price;
        document.querySelector("#money").innerText = `$${moneyRemaining}M`;
        } else {
        console.log(json);
        document.querySelector(`#player${div_id}name`).innerText = json.name;
        document.querySelector(`#player${div_id}price`).innerText = `$${json.price}M`;
        document.querySelector(`#player${div_id}img`).setAttribute("src", `images/${json.college}.png`);
        let button_element = document.querySelector(`#player${div_id}remove`);
        button_element.removeAttribute("class");
        button_element.setAttribute("class", "bg-sky-500 hover:bg-sky-700 px-4 py-2 rounded-md opacity-50 dark:text-black");
        button_element.addEventListener("click", ()=>{reset_player_div(div_id, json.price)})

        player_div_number_player_index_object[div_id] = json.id;
        moneyRemaining -= json.price;
        document.querySelector("#money").innerText = `$${moneyRemaining}M`;
}

}

function reset_player_div(div_id, price){
        let div_element = document.querySelector(`#player${div_id}div`);

        div_element.innerHTML = `<a href="#">
                        <h5 id="player${div_id}name" class="text-4xl font-semibold tracking-tight text-gray-900 dark:text-black">No player selected</h5>
                    </a>

                <a href="#">
                    <img id="player${div_id}img" class="p-1 rounded-t-lg" src="images/logo.png" alt="product image" style="width: 80%;
                    display: inline-block;"/>
                </a>
                <div class="px-5 pb-5">
                                   <div class="flex items-center mt-2.5 mb-5">
                    </div>
                    <div class="flex items-center justify-between">
                        <span id="player${div_id}price" class="text-3xl font-bold text-gray-900 dark:text-blue">0 points</span>
                        <button id="player${div_id}remove" class="bg-gray-300 px-4 py-2 rounded-md cursor-not-allowed opacity-50 dark:text-black">
                            Remove
                         </button>
                    </div>
            </div>`
        empty_player_divs.push(div_id);
        player_div_number_player_index_object[div_id] = -1;
        moneyRemaining += price;
        document.querySelector("#money").innerText = `$${moneyRemaining}M`;
}

function show_player_info(json){
    // player1div, player1img, player1name, player1points, player1stats
    for (let div_id = 1; div_id <= 5; div_id++){
        show_individual_player_info(div_id, json)
        empty_player_divs = empty_player_divs.filter(function(item) {
            return item !== div_id
        })
    }
}

async function fetch_user_team_info(username){

    try {
    var response = await fetch(`http://supremepaudel.pythonanywhere.com/user/${username}`);
    if (!response.ok){
        throw new Error('Invalid username');
    }
    let json = await response.json();
        // show player info in div 
        user_info = json;
        show_player_info(user_info);
    } catch (error) {
    // do not do anything
        console.log('error')

    }
}
window.onload = function(){

    // if the user is not signed in
    // take them to login page
    let username = window.sessionStorage.getItem('username');
    let token = window.sessionStorage.getItem('token');
    if (username == null || token == null || username == undefined || token == undefined){
        window.location.href = '/login.html'
    }

    document.querySelector("#submitDataToServer").addEventListener("click", submitDataToServer);
    // else fetch their team info
    fetch_user_team_info(username)
    // if server responds properly display that info
    // else nothing
}
