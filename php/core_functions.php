<?php
require './environ.php';
require './database.php';
require './password.php';

function add_user($username, $password) {
	global $users_db;

	$result = create_hash_password($password);
	$salt = $result["salt"];
	$hash = $result["hash"];

	query_string("INSERT INTO $users_db (name, password_hash, password_salt)
			VALUES (:username, :hash, :salt);",
			array(":username" => $username, ":salt" => $salt, ":hash" => $hash));
}

function test_password($username, $test_password) {
	global $users_db;

	$result = query_db("SELECT password_hash FROM $users_db WHERE user_name = :username LIMIT 1;", array(":username" => $username));
	$user = $result->fetch(PDO::FETCH_OBJ);

	if ($user != NULL) {
		$db_password_hash = $user->password_hash;
		$test_password_hash = crypt($test_password, $db_password_hash);

		return $db_password_hash == $test_password_hash;
	} else {
		return false;
	}
}

function print_dances() {
	global $dances_db;
	return query_array("SELECT dance_name FROM $dances_db");
}

function add_dance($dancename) {
	global $dances_db;

	query_db("INSERT INTO $dances_db (dance_name)
			VALUES (:dancename);",
			array(":dancename" => $dancename));
}

function delete_dance($dancename) {
	global $dances_db;

	query_db("DELETE FROM $dances_db WHERE dance_name = :dancename", array(":dancename" => $dancename));
}

function get_dance($dancename) {
	global $dances_db;
	$result = query_db("SELECT * FROM $dances_db WHERE dance_name = :dancename LIMIT 1;", array(":dancename" => $dancename));
	if($result) {
		return $result->fetch(PDO::FETCH_OBJ);
	} else {
		return NULL;
	}
}

function print_artists() {
	global $artists_db;
	return query_array("SELECT artist_name FROM $artists_db");
}


function add_artist($artistname) {
	global $artists_db;

	query_db("INSERT INTO $artists_db (artist_name)
			VALUES (:artistname);",
			array(":artistname" => $artistname));
}

function delete_artist($artistname) {
	global $artists_db;

	query_db("DELETE FROM $artists_db WHERE artist_name = :artistname", array(":artistname" => $artistname));
}

function get_artist($artistname) {
	global $artists_db;
	$result = query_db("SELECT * FROM $artists_db WHERE artist_name = :artistname LIMIT 1;", array(":artistname" => $artistname));
	if($result) {
		return $result->fetch(PDO::FETCH_OBJ);
	} else {
		return NULL;
	}
}


function print_songs() {
	global $songs_db, $artists_db, $dances_db;
	return query_class("SELECT song_id, title, artist_name, dance_name FROM $songs_db AS $songs_db JOIN $artists_db AS $artists_db USING (artist_id) JOIN $dances_db AS $dances_db USING (dance_id)");
}

function add_song($title, $artist_name, $dance_name) {
	global $songs_db, $artists_db, $dances_db;

	query_db("INSERT INTO $songs_db (title, artist_id, dance_id)
			VALUES (:title, (
				SELECT artist_id FROM $artists_db WHERE artist_name = :artistname LIMIT 1
			), (
				SELECT dance_id FROM $dances_db WHERE dance_name = :dancename LIMIT 1
			));",
			array(":title" => $title, ":artistname" => $artist_name, ":dancename" => $dance_name));
}

function delete_song($song_id) {
	global $songs_db;

	query_db("DELETE FROM $songs_db WHERE song_id = :song_id", array(":song_id" => $song_id));
}