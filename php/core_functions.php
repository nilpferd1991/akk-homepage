<?php
require_once './environ.php';
require_once './database.php';
require_once './password.php';

/* LIST */
/**
 * @param $term
 */
function list_artists($term) {
	print json_encode(query_array("SELECT artist_name FROM ".db::$artists_db." WHERE (artist_name LIKE :term)", array(":term" =>"%".$term."%")));
}

/**
 * @param $term
 */
function list_dances($term) {
	print json_encode(query_array("SELECT dance_name FROM ".db::$dances_db." WHERE (dance_name LIKE :term)", array(':term' => "%".$term."%")));
}

/**
 * @param $term
 */
function list_songs($term) {
	print json_encode(query_array("SELECT title FROM ".db::$songs_db." WHERE (title LIKE :term)", array(":term" => "%".$term."%")));
}

/**
 * @param $term
 */
function list_all($term) {
    $result = query_array("SELECT title FROM ".db::$songs_db. " WHERE (title LIKE :term)", array(":term" => "%".$term."%"));
    $result = array_merge($result, query_array("SELECT artist_name FROM ".db::$artists_db." WHERE (artist_name LIKE :term)", array(":term" =>"%".$term."%")));
    $result = array_merge($result, query_array("SELECT dance_name FROM ".db::$dances_db." WHERE (dance_name LIKE :term)", array(':term' => "%".$term."%")));

    print json_encode($result);
}

/* Search */
/**
 * @param $column
 * @param $term
 */
function print_songs($column, $term) {
	if($column == "artists") {
		$column_name = "artist_name";
	} else if($column == "songs") {
		$column_name = "title";
	} else if($column == "dances") {
		$column_name = "dance_name";
	}
	
	print json_encode(query_class("SELECT song_id, title, artist_id, artist_name, dance_id, dance_name 
			FROM ".db::$songs_db." AS ".db::$songs_db." 
			JOIN ".db::$artists_db." AS ".db::$artists_db." USING (artist_id) 
			JOIN ".db::$dances_db." AS ".db::$dances_db." USING (dance_id)
			WHERE ".$column_name." LIKE :term", array(":term" => "%".$term."%")));
}

/**
 * @param $term
 */
function print_all_songs($term) {
    print json_encode(query_class("SELECT song_id, title, artist_id, artist_name, dance_id, dance_name
			FROM ".db::$songs_db." AS ".db::$songs_db."
			JOIN ".db::$artists_db." AS ".db::$artists_db." USING (artist_id)
			JOIN ".db::$dances_db." AS ".db::$dances_db. " USING (dance_id)
			WHERE (title LIKE :term) OR (artist_name LIKE :term) OR (dance_name LIKE :term)", array(":term" => "%".$term."%")));
}

/* Deletion */
/**
 * @param $song_id
 */
function delete_song($song_id) {
    // TODO: Delete unused dances and artists!
	query_db("DELETE FROM ".db::$songs_db." WHERE song_id = :song_id", array(":song_id" => $song_id));
}

/* Adding */
/**
 * @param $title
 * @param $artist
 * @param $dance
 * @param $rating
 * @param $notes
 */
function add_song($title, $artist, $dance, $rating, $notes)
{
    $artist_id = get_or_add_artist($artist);
    $dance_id = get_or_add_dance($dance);
    $song_id = get_or_add_song($title, $artist_id, $dance_id);
    get_or_add_notes($song_id, $notes, $rating);
}

/**
 * @param $title
 * @param $artist_id
 * @param $dance_id
 * @return mixed
 */
function get_or_add_song($title, $artist_id, $dance_id)
{
    $old_song = get_song($title, $artist_id, $dance_id);

    if ($old_song == NULL) {
        query_db("INSERT INTO " . db::$songs_db . " (title, artist_id, dance_id)
                    VALUES (:title, :artist_id, :dance_id);",
            array(":title" => $title, ":artist_id" => $artist_id, ":dance_id" => $dance_id));
    }
    $song_id = get_song($title, $artist_id, $dance_id)->song_id;
    return $song_id;
}

/**
 * @param $artist_name the name of the artist
 * @return int the artist_id which is added or old
 */
function get_or_add_artist($artist_name)
{
    $artist = get_artist($artist_name);
    if ($artist == NULL) {
        add_artist($artist_name);
        $artist = get_artist($artist_name);
    }
    return $artist->artist_id;
}

/**
 * @param $dance_name the name of the dance
 * @return int the dance_id which is added or old
 */
function get_or_add_dance($dance_name)
{
    $dance = get_dance($dance_name);
    if ($dance == NULL) {
        add_dance($dance_name);
        $dance = get_dance($dance_name);
    }

    return $dance->dance_id;
}

/**
 * @param $notes the name of the artist
 */
function get_or_add_notes($song_id, $notes, $rating)
{
    $note_id = get_notes($song_id);
    if ($note_id == NULL) {
        add_notes($song_id, $notes, $rating);
    }
}

/**
 * @param $dancename
 */
function add_dance($dancename) {
	query_db("INSERT INTO ".db::$dances_db." (dance_name)
			VALUES (:dancename);",
			array(":dancename" => $dancename));
}

/**
 * @param $artistname
 */
function add_artist($artistname) {
	query_db("INSERT INTO ".db::$artists_db." (artist_name)
			VALUES (:artistname);",
			array(":artistname" => $artistname));
}

function add_notes($song_id, $notes, $rating) {
    query_db("INSERT INTO ".db::$notes_db." (song_id, note, date_created, user_id, rating)
        VALUES (:song_id, :notes, CURRENT_DATE(), 1, :rating);",
        array(":song_id" => $song_id, ":notes" => $notes, ":rating" => $rating));
}

/* Getter */
/**
 * @param $dancename
 * @return null
 */
function get_dance($dancename) {
	$result = query_db("SELECT * FROM ".db::$dances_db." WHERE dance_name = :dancename LIMIT 1;",
        array(":dancename" => $dancename));
	if($result) {
		return $result->fetch(PDO::FETCH_OBJ);
	} else {
		return NULL;
	}
}

/**
 * @param $song_id
 */
function print_song_information($song_id) {
    print json_encode(query_class("SELECT song_id, title, artist_name, dance_name
			FROM ".db::$songs_db." AS ".db::$songs_db."
			JOIN ".db::$artists_db." AS ".db::$artists_db." USING (artist_id)
			JOIN ".db::$dances_db." AS ".db::$dances_db. " USING (dance_id)
			WHERE (song_id LIKE :song_id)", array(":song_id" => "%".$song_id."%"))[0]);
}

/**
 * @param $artistname
 * @return null
 */
function get_artist($artistname) {
	$result = query_db("SELECT * FROM ".db::$artists_db." WHERE artist_name = :artistname LIMIT 1;", array(":artistname" => $artistname));
	if($result) {
		return $result->fetch(PDO::FETCH_OBJ);
	} else {
		return NULL;
	}
}

/**
 * @param $song_id the id of the song for which the notes are search for
 * @return null
 */
function get_notes($song_id) {
    $result = query_db("SELECT * FROM ".db::$notes_db." WHERE song_id = :song_id LIMIT 1;", array(":song_id" => $song_id));
    if($result) {
        return $result->fetch(PDO::FETCH_OBJ);
    } else {
        return NULL;
    }
}

/**
 * @param $title
 * @param $artist_id
 * @param $dance_id
 * @return null
 */
function get_song($title, $artist_id, $dance_id) {
    $result = query_db("SELECT * FROM ".db::$songs_db." WHERE (title LIKE :title) AND
                (artist_id = :artist_id) AND (dance_id = :dance_id) LIMIT 1",
                array(":title" => $title, ":artist_id" => $artist_id, "dance_id" => $dance_id));

    if($result) {
        return $result->fetch(PDO::FETCH_OBJ);
    } else {
        return NULL;
    }
}




/* UNUSED *********************************************/

/**
 * @param $username
 * @param $password
 */
function add_user($username, $password) {
	$result = create_hash_password($password);
	$salt = $result["salt"];
	$hash = $result["hash"];

	query_db("INSERT INTO ".db::$users_db." (user_name, password_hash, password_salt)
			VALUES (:username, :hash, :salt);",
			array(":username" => $username, ":salt" => $salt, ":hash" => $hash));
}

/**
 * @param $username
 * @param $test_password
 * @return bool
 */
function test_password($username, $test_password) {
	$result = query_db("SELECT password_hash FROM ".db::$users_db." WHERE user_name = :username LIMIT 1;", array(":username" => $username));
	$user = $result->fetch(PDO::FETCH_OBJ);

	if ($user != NULL) {
		$db_password_hash = $user->password_hash;
		$test_password_hash = crypt($test_password, $db_password_hash);

		return $db_password_hash == $test_password_hash;
	} else {
		return false;
	}
}

/**
 * @param $dancename
 */
function delete_dance($dancename) {
	query_db("DELETE FROM ".db::$dances_db." WHERE dance_name = :dancename", array(":dancename" => $dancename));
}


/**
 * @param $artistname
 */
function delete_artist($artistname) {
	query_db("DELETE FROM ".db::$artists_db." WHERE artist_name = :artistname", array(":artistname" => $artistname));
}