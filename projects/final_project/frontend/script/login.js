function process_login_data(){

    let username = document.querySelector("#username").value;
    let password = document.querySelector("#password").value;
    send_info_to_backend(username, password);

}

function display_error_message(){

  let error_div = document.querySelector("#errorMessage");
  error_div.innerHTML = `
  <div class="w-full md:w-1/3 mx-auto">
  <div class="flex flex-col p-5 rounded-lg shadow bg-white">
	<div class="flex flex-col items-center text-center">
	  <div class="inline-block p-4 bg-yellow-50 rounded-full">
		<svg class="w-12 h-12 fill-current text-yellow-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M12 5.99L19.53 19H4.47L12 5.99M12 2L1 21h22L12 2zm1 14h-2v2h2v-2zm0-6h-2v4h2v-4z"/></svg>
	  </div>
	  <h2 class="mt-2 font-semibold text-gray-800">Incorrect username/password</h2>
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
async function send_info_to_backend(username, password){

    const headers = new Headers({
        "Content-Type": "application/x-www-form-urlencoded"
      });
      
      const urlencoded = new URLSearchParams({
        "username": username,
        "password": password
      });
      
      const opts = {
        method: 'POST',
        headers: headers,
        body: urlencoded,
      };
      
    fetch(
        "http://supremepaudel.pythonanywhere.com/login",
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
            document.querySelector("#errorMessage").innerHTML = "";

            // set username and tokenID in session storage
            window.sessionStorage.setItem('username', responseJson.username);
            window.sessionStorage.setItem('token', responseJson.token);
            // redirect to home page
            window.location.href = '/team.html'


          })
          .catch((error) => {
            display_error_message();
          });
}

window.onload = function() {
    

    // Check if user is already logged in
    // if logged in already redirect them to their team
    
    let user = window.sessionStorage.getItem('username')
    let token = window.sessionStorage.getItem('token');
    if (user != null && token != null){
      window.location.href = '/team.html'
    }
    // else get login info and send info to backend
    let button = document.querySelector("#login_button");
    button.addEventListener("click", process_login_data)
}
