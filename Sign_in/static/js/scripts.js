//we are using jquery here
$("form[name=signup_form]").submit(function(e){ //e is the event. .submit used instead of .click() cuz it will include clicks plus other forms of submition like clicking on enter
	var $form = $(this);
	var $error = $form.find(".error"); //currently takes the <p> element in the form cuz its the only element with the error class
	var data = $form.serialize(); //bundles up all the fields from the form to send it to the backend i.e.  user/signup route
	//jquery ajax is a way for your frontend to talk to the backend(Flask) without reloading the page.
	$.ajax({  //function that sends an HTTP request behind the scenes
		url:"/user/signup/", // the flas route it is sending th request to
		type: "POST", //POST cuz we are seding signup details to the server
		data: data, //the actual data being sent
		dataType: "json", //tells jquery  "I expect the server to respond with JSON" so it automatically parses it for you
		success: function(resp){ // this runs if request succeeds. "resp" is the flask route returned
			console.log(resp);
			window.location.href="/setting_up/"; //go to that user's dashboard after signing up
		},
		error: function(resp){ //if something goes wrong, this function runs and will most probs show 200? lie error 200 or 404
			console.log(resp); // this doesn't show anything on the webpage though
			$error.text(resp.responseJSON.error).removeClass("error--hidden"); //text of <p> in form should be the alue of the key called error
			}
		});


	e.preventDefault(); //prevents stuff being submitted to a different pg etc
})

//login form
$("form[name=login_form]").submit(function(e){ //e is the event.
	var $form = $(this);
	var $error = $form.find(".error"); //currently takes the <p> element in the form cuz its the only element with the error class
	var data = $form.serialize(); //bundles up all the fields from the form to send it to the backend i.e.  user/signup route
	//jquery ajax is a way for your frontend to talk to the backend(Flask) without reloading the page.
	$.ajax({  //function that sends an HTTP request behind the scenes
		url:"/user/login", // the flask route it is sending th request to
		type: "POST", //POST cuz we are seding signup details to the server
		data: data, //the actual data being sent
		dataType: "json", //tells jquery  "I expect the server to respond with JSON" so it automatically parses it for you
		success: function(resp){ // this runs if request succeeds. "resp" is the flask route returned
			console.log(resp);
			window.location.href="/dashboard/"; //go to that user's dashboard after signing up
		},
		error: function(resp){ //if something goes wrong, this function runs and will most probs show 200? lie error 200 or 404
			console.log(resp); // this doesn't show anything on the webpage though
			$error.text(resp.responseJSON.error).removeClass("error--hidden"); //text of <p> in form should be the alue of the key called error
			}
		});


	e.preventDefault(); //prevents stuff being submitted to a different pg etc
})

if ($("#moviegrid").length){ // only runs for setting_up.html where the id moviegrid actually exists
	var base = "https://image.tmdb.org/t/p/w500"
	$.ajax({
		url: "/user/settingup/", //from routes.py gets the json movies
		type: "GET",
		dataType: "json",
		success: function(movies){
			movies.forEach(function(movie){
				var $card = $("<div>").addClass("moviecard");

				$card.html(
					`<img src = "${base + movie.poster_path}" alt= "${movie.title}" width = "200">
					<p>${movie.title}</p>
					<button data-title = "${movie.title}">${movie.vote_average}</button>`
					);
				$("#moviegrid").append($card);
			})
		},
		error: function(resp){
			console.log(resp);
		}
	});	
}


$("#done").click(function(e){
	$.ajax({
		//url:"/user/login", // the flask route it is sending th request to
		//type: "POST", //POST cuz we are seding signup details to the server
		//data: data, //the actual data being sent
		//dataType: "json", //tells jquery  "I expect the server to respond with JSON" so it automatically parses it for you
		success: function(resp){ // this runs if request succeeds. "resp" is the flask route returned
			console.log(resp);
			window.location.href="/dashboard/"; //go to that user's dashboard after signing up
		},
		error: function(resp){ //if something goes wrong, this function runs and will most probs show 200? lie error 200 or 404
			console.log(resp); // this doesn't show anything on the webpage though
			$error.text(resp.responseJSON.error).removeClass("error--hidden"); //text of <p> in form should be the alue of the key called error
			}
	});

})

