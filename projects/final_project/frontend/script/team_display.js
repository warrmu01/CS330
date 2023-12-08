var user_info=null;

function draw_chart(chrt, player){

      var chartId = new Chart(chrt, {
         type: 'radar',
         data: {
            labels: ["Goals", "Assists","Shots", "Points", "Price"],
            datasets: [{
               label: "Player stats",
               data: [player.G, player.A,player.SH, player.PTS, player.price],
               backgroundColor: ['white'],
               pointBackgroundColor: ['yellow', 'aqua', 'pink', 'lightgreen', 'lightblue'],
               borderColor: ['white'],
               borderWidth: 1,
               pointRadius: 5,
            }],
         },
         options: {
            responsive: false,
            elements: {
               line: {
                  borderWidth: 3
               }
            },
            scale: {
                gridLines: {
                  color: ['black', 'red', 'orange', 'yellow', 'green', 'blue', 'indigo']
                }
              }
         },
      });
}
function display_person_data(person_id){
    let player = user_info[`player${person_id}`];
                        // Populate modal with player information
    const playerInfoContent = document.getElementById('player-info-content');
    // show their radar chart with stats
    playerInfoContent.innerHTML = `
            <div class="flex">
        <div class="flex-1 pr-4">
            <canvas id="chartId" aria-label="chart" height="300" width="580"></canvas>
            <p class="text-5xl text-base leading-relaxed text-gray-500 dark:text-gray-400" style="text-align: center;">
                ${player.name}
            </p>
        </div>
        <div>
            <img src="images/${player.college.toLowerCase()}.png" alt="${player.college} Logo" class="w-100 h-100 ml-auto">
        </div>
    </div>
    `;
    const infoModal = document.getElementById('info-modal');
    infoModal.classList.remove('hidden');

    let chart_element = document.querySelector("#chartId").id;
    draw_chart(chart_element, player);
}

function show_player_info(json){
    // player1div, player1img, player1name, player1points, player1stats
    for (let div_id = 1; div_id <= 5; div_id++){
        document.querySelector(`#player${div_id}name`).innerText = json[`player${div_id}`].name;
        document.querySelector(`#player${div_id}points`).innerText = `${json[`player${div_id}`].PTS} points`;
        document.querySelector(`#player${div_id}img`).setAttribute("src", `images/${json[`player${div_id}`].college}.png`);
        let button_element = document.querySelector(`#player${div_id}stats`);
        button_element.removeAttribute("class");
        button_element.setAttribute("class", "bg-sky-500 hover:bg-sky-700 px-4 py-2 rounded-md opacity-50 dark:text-black");
        button_element.addEventListener("click", ()=>{display_person_data(div_id)})
    }
    // show total points and budget left
    document.querySelector("#playerDetails").innerHTML += ` <br /> <p class='text-base'>Money used : ${user_info.used_money}M out of ${user_info.total_budget}M</p>`
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

    //show name on playerDetails
    document.querySelector("#playerDetails").innerHTML = `${username}'s team`
    // else fetch their team info
    fetch_user_team_info(username)
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

    // if server responds properly display that info
    // else nothing
}
