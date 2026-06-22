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
$(document).ready(function(){
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
								<p>${movie.title}</p>`
								);
							$("#moviegrid").append($card);		
							$card.on("click", function(){
								 	$card.toggleClass("setting_up_likes");
									if ($(this).hasClass("setting_up_likes")){
										selected_movies.push(movie._id);

									}
									else{
										selected_movies = selected_movies.filter(m=>m!=movie._id);
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
		url:"/user/userpreferences/", // the flask route it is sending th request to
		type: "POST", //POST cuz we are sending movie details to the server
		contentType: "application/json", //cuz we are sending to flask
		data: JSON.stringify({"selected_movies":selected_movies}), //the actual data being sent
		//dataType: "json", //what we want from flask.tells jquery  "I expect the server to respond with JSON" so it automatically parses it for you
		success: function(resp){ // this runs if request succeeds. "resp" is the flask route returned
			console.log(resp);
			window.location.href="/dashboard/"; //go to that user's dashboard after signing up
		},
		error: function(resp){ //if something goes wrong, this function runs and will most probs show 200? lie error 200 or 404
			console.log(resp); // this doesn't show anything on the webpage though
			//$error.text(resp.responseJSON.error).removeClass("error--hidden"); //text of <p> in form should be the alue of the key called error
			}
	});

});
})



$(document).ready(function(){

	console.log("dashboard JS loaded");
	console.log(document.querySelector('#dashboard_recommendations'));
if (document.querySelector('#dashboard_recommendations')){
	let movie_ids = [];
	let rewards = [];
	const base = "https://image.tmdb.org/t/p/w500";
	console.log("in dashboard recommendations")
	$("#dashboard_recommendations").empty();

$.ajax({
					url: `/user/dashboard/`, //from routes.py gets the json movies
					type: "GET",
					dataType: "json",
					success: function(movies){
						console.log("inside the ajax printnng list of movies")
						console.log(movies)
						movies.forEach(function(movie){
							var $card = $("<div>").addClass("moviecard");

							$card.html(
								`<img src = "${base + movie.poster_path}" alt= "${movie.title}" width = "200">
								<p>${movie.title}</p>
								<div class = "movie-actions">
								 <button class="like_btn" value="${movie._id}"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path>
    </svg></button>
    							<button class="dislike_btn" value="${movie._id}"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"></path>
    </svg></button>
    </div>`
								);
							$("#dashboard_recommendations").append($card);	
							$card.find(".like_btn").on("click", function(){
												$card.removeClass("disliked");
											    $card.toggleClass("liked");
											    //only last button clicked for the movies and rewards is selected
											    if (movie_ids.some(item => item === $(this).val())){
											    	let idx = movie_ids.indexOf($(this).val());
											    	movie_ids.splice(idx, 1);
											    	rewards.splice(idx, 1);											  
											    }
											    if ($card.hasClass("liked")){
												    movie_ids.push($(this).val());
												    rewards.push(1);
												}

											});	
							$card.find(".dislike_btn").on("click", function(){
												$card.removeClass("liked");
											    $card.toggleClass("disliked");
											    if (movie_ids.some(item => item === $(this).val())){
											    	let idx = movie_ids.indexOf($(this).val());
											    	movie_ids.splice(idx, 1);
											    	rewards.splice(idx, 1);											  
											    }							  
											    if ($card.hasClass("disliked")){
												    movie_ids.push($(this).val());
												    rewards.push(-1);
												}
											});	
						})
					},
					error: function(resp){
						console.log(resp);
					}
				});	
		$("#update").click(function(e){
		$.ajax({
		url:"/user/update_userpreferences/", // the flask route it is sending th request to
		type: "POST", //POST cuz we are sending movie details to the server
		contentType: "application/json", //cuz we are sending to flask
		data: JSON.stringify({"movie_ids":movie_ids, "rewards":rewards}), //the actual data being sent
		//dataType: "json", //what we want from flask.tells jquery  "I expect the server to respond with JSON" so it automatically parses it for you
		success: function(resp){ // this runs if request succeeds. "resp" is the flask route returned
			console.log(resp);
			window.location.href="/dashboard/"; //go to that user's dashboard after signing up
		},
		error: function(resp){ //if something goes wrong, this function runs and will most probs show 200? lie error 200 or 404
			console.log(resp); // this doesn't show anything on the webpage though
			//$error.text(resp.responseJSON.error).removeClass("error--hidden"); //text of <p> in form should be the alue of the key called error
			}
	});

});
		}
	})