<?php


/**
 * @param string $artist_name
 * @return null
 */
function get_artist($artist_name) {
    $result = query_db("SELECT * FROM ".db::$artists_db." WHERE artist_name = :artistname LIMIT 1;", array(":artistname" => $artist_name));
    if($result) {
        return $result->fetch(PDO::FETCH_OBJ);
    } else {
        return NULL;
    }
}

/**
 * @param int $song_id the id of the song for which the notes are search for
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
 * @param string $title
 * @param int $artist_id
 * @param int $dance_id
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


/**
 * @param string $dancename
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
 * Add a song to the database if it is not already there.
 * @param string $title The title to look for or add
 * @param int $artist_id The artist id to look for or add
 * @param int $dance_id The dance id to look for or ad
 * @return int the song id we added (or that was already there)
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