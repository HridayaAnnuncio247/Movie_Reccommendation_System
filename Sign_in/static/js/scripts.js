//we are using jquery here

//signup form
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



//setting_up.html stuff
let selected_movies = [];
//the carousel with the different genres
if (document.querySelector('.genrecard')){
	const track = document.querySelector('.track');
	const left_arrow = document.querySelector('.left-arrow');
	const right_arrow = document.querySelector('.right-arrow');
	const card_width = document.querySelector('.genrecard').offsetWidth;
	const all_cards = document.querySelectorAll('.genrecard')
	const total_cards = all_cards.length;
	const track_width = card_width * total_cards;
	const base = "https://image.tmdb.org/t/p/w500"
	let offset = 0;

	//when the right arrow is clicked, the track should start from a different genere.
	//offset keeps account of which point of the track should the display start at.
	//a feature called translateX is added to the css of the track to place the offset correctly.
	right_arrow.addEventListener('click', function(){
		if (offset < track_width - card_width*5){
			offset += card_width;
			//track shifted to the left by offset number of pixels because of "-". we need to go left so that a new genre to the right can be displayed and the leftmost can be hidden.
			track.style.transform = `translateX(-${offset}px)`; 
		}
	});

	left_arrow.addEventListener('click', function(){
		if (offset >= card_width){
			offset -= card_width;
			//track shifted to the left by offset number of pixels because of "-". we need to go left so that a new genre to the right can be displayed and the leftmost can be hidden.
			track.style.transform = `translateX(-${offset}px)`; 
		}
	});

	all_cards.forEach(function(card_){
		card_.addEventListener('click', function(){
			console.log(card_.dataset.title)
			$("#moviegrid").empty();
			$.ajax({
					url: `/user/settingup/?genre=${card_.dataset.title}`, //from routes.py gets the json movies
					type: "GET",
					dataType: "json",
					success: function(movies){
						console.log(movies)
						movies.forEach(function(movie){
							var $card = $("<div>").addClass("moviecard");

							$card.html(
								`<img src = "${base + movie.poster_path}" alt= "${movie.title}" width = "200">
								<p>${movie.title}</p>
								<input type="checkbox" value="${movie._id}"  class = "movie_checkbox">`
								);
							$("#moviegrid").append($card);		
							$card.find(".movie_checkbox").on("change", function(){
									if ($(this).is(":checked")){
										selected_movies.push($(this).val());
									}
									else{
										selected_movies = selected_movies.filter(movie=>movie!=$(this).val());
									}
									
							});
						})
					},
					error: function(resp){
						console.log(resp);
					}
				});	


		});
		});
}
//the movie grid stuff
/*if ($("#moviegrid").length){ // only runs for setting_up.html where the id moviegrid actually exists
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
*/


$("#done").click(function(e){
	$.ajax({
		url:"/user/userpreferences", // the flask route it is sending th request to
		type: "POST", //POST cuz we are seding signup details to the server
		data: JSON.stringify({"selected_movies":selected_movies}), //the actual data being sent
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

