$(document).ready(function() {
	$("input").addClass("form-control mb-1");
	$("input[name='punchline']").prop("placeholder", "Can you guess the punchline?");
	$("input[name='username']").prop("placeholder", "username");
	$("input[name='email']").prop("placeholder", "email");
	$("input[name='password1']").prop("placeholder", "password");
	$("input[name='password2']").prop("placeholder", "confirm password");
});