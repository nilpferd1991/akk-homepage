<?php
require_once './environ.php';
require_once './database.php';
require_once './password.php';

function add_user($username, $password) {
	$result = create_hash_password($password);
	$salt = $result["salt"];
	$hash = $result["hash"];

	query_string("INSERT INTO db::$users_db (name, password_hash, password_salt)
			VALUES (:username, :hash, :salt);",
			array(":username" => $username, ":salt" => $salt, ":hash" => $hash));
}

function test_password($username, $test_password) {
	$result = query_db("SELECT password_hash FROM db::$users_db WHERE user_name = :username LIMIT 1;", array(":username" => $username));
	$user = $result->fetch(PDO::FETCH_OBJ);

	if ($user != NULL) {
		$db_password_hash = $user->password_hash;
		$test_password_hash = crypt($test_password, $db_password_hash);

		return $db_password_hash == $test_password_hash;
	} else {
		return false;
	}
}

/* LIST */
function list_artists($term) {
	print json_encode(query_array("SELECT artist_name FROM " . db::$artists_db . " WHERE artist_name LIKE '%$term%'"));
}

function list_dances($term) {
	print json_encode(query_array("SELECT dance_name FROM " . db::$dances_db . " WHERE dance_name LIKE '%$term%'"));
}

function list_songs($term) {
	print json_encode(query_array("SELECT title FROM " . db::$songs_db . " WHERE title LIKE '%$term%'"));
}



function print_dances() {
	return query_array("SELECT dance_name FROM db::$dances_db");
}

function add_dance($dancename) {
	query_db("INSERT INTO db::$dances_db (dance_name)
			VALUES (:dancename);",
			array(":dancename" => $dancename));
}

function delete_dance($dancename) {
	query_db("DELETE FROM db::$dances_db WHERE dance_name = :dancename", array(":dancename" => $dancename));
}

function get_dance($dancename) {
	$result = query_db("SELECT * FROM db::$dances_db WHERE dance_name = :dancename LIMIT 1;", array(":dancename" => $dancename));
	if($result) {
		return $result->fetch(PDO::FETCH_OBJ);
	} else {
		return NULL;
	}
}

function print_artists() {
	return query_array("SELECT artist_name FROM db::$artists_db");
}


function add_artist($artistname) {
	query_db("INSERT INTO db::$artists_db (artist_name)
			VALUES (:artistname);",
			array(":artistname" => $artistname));
}

function delete_artist($artistname) {
	query_db("DELETE FROM db::$artists_db WHERE artist_name = :artistname", array(":artistname" => $artistname));
}

function get_artist($artistname) {
	$result = query_db("SELECT * FROM db::$artists_db WHERE artist_name = :artistname LIMIT 1;", array(":artistname" => $artistname));
	if($result) {
		return $result->fetch(PDO::FETCH_OBJ);
	} else {
		return NULL;
	}
}


function print_songs() {
	return query_class("SELECT song_id, title, artist_name, dance_name FROM db::$songs_db AS db::$songs_db JOIN db::$artists_db AS db::$artists_db USING (artist_id) JOIN db::$dances_db AS db::$dances_db USING (dance_id)");
}

function add_song($title, $artist_name, $dance_name) {
	query_db("INSERT INTO db::$songs_db (title, artist_id, dance_id)
			VALUES (:title, (
				SELECT artist_id FROM db::$artists_db WHERE artist_name = :artistname LIMIT 1
			), (
				SELECT dance_id FROM db::$dances_db WHERE dance_name = :dancename LIMIT 1
			));",
			array(":title" => $title, ":artistname" => $artist_name, ":dancename" => $dance_name));
}

function delete_song($song_id) {
	query_db("DELETE FROM db::$songs_db WHERE song_id = :song_id", array(":song_id" => $song_id));
}