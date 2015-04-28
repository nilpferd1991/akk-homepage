<?php
error_reporting(E_ALL | E_STRICT);
ini_set("display_errors", "On");

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
	} else if($param_type == "search") {
        list_all($param_term);
    }
} else if ($param_action == "search") {
    if($param_type == "search") {
        print_all_songs($param_term);
    } else {
        print_songs($param_type, $param_term);
    }
}