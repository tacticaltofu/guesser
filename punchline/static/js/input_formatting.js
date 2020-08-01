$(document).ready(function() {
	$("input, textarea").addClass("form-control mb-1");
	$("input[name='title']").prop("placeholder", "title");
	$("textarea[name='setup']").prop("placeholder", "setup");
	$("input[name='punchline']").prop("placeholder", "punchline");
	$("input[name='username']").prop("placeholder", "username");
	$("input[name='email']").prop("placeholder", "email");
	$("input[name='password']").prop("placeholder", "password");
	$("input[name='password1']").prop("placeholder", "password");
	$("input[name='password2']").prop("placeholder", "confirm password");
});