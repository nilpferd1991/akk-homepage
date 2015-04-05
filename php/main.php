<?php 
require './core_functions.php';

function fillIfValid($key) {
	if (isset($_GET[$key])) {
		return $_GET[$key];
	} else {
		return NULL;
	}
}

$param_action = fillIfValid("action");
$param_type = fillIfValid("type");
$param_term = fillIfValid("term");

if($param_action == "list") {
	if($param_type == "artists") {
		list_artists($param_term);
	} else if($param_type == "songs") {
		list_songs($param_term);
	} else if($param_type == "dances") {
		list_dances($param_term);
	}
}