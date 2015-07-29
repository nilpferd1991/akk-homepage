<?php

require_once "./getter.php";

/**
 * Add a dance
 * @param string $dance_name
 */
function add_dance($dance_name) {
    query_db("INSERT INTO ".db::$dances_db." (dance_name)
			VALUES (:dancename);",
        array(":dance_name" => $dance_name));
}

/**
 * Add n artist
 * @param string $artist_name
 */
function add_artist($artist_name) {
    query_db("INSERT INTO ".db::$artists_db." (artist_name)
			VALUES (:artist_name);",
        array(":artist_name" => $artist_name));
}

/**
 * Add notes and ratings to a song
 * @param int $song_id
 * @param string $notes
 * @param int $rating
 */
function add_notes($song_id, $notes, $rating) {
    query_db("INSERT INTO ".db::$notes_db." (song_id, note, date_created, user_id, rating)
        VALUES (:song_id, :notes, CURRENT_DATE(), 1, :rating);",
        array(":song_id" => $song_id, ":notes" => $notes, ":rating" => $rating));
}

/**
 * Add a song to the database
 * @param string $title
 * @param string $artist
 * @param string $dance
 * @param int $rating
 * @param string $notes
 */
function add_song($title, $artist, $dance, $rating, $notes)
{
    $artist_id = get_or_add_artist($artist);
    $dance_id = get_or_add_dance($dance);
    $song_id = get_or_add_song($title, $artist_id, $dance_id);
    get_or_add_notes($song_id, $notes, $rating);
}


/**
 * @param string $artist_name the name of the artist
 * @return int the artist_id which is added or old one
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
 * @param string $dance_name the name of the dance
 * @return int the dance_id which is added or old one
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
 * @param int $song_id the song id to look for
 * @param string $notes the notes which are added if not there already
 * @param int $rating
 */
function get_or_add_notes($song_id, $notes, $rating)
{
    $note_id = get_notes($song_id);
    if ($note_id == NULL) {
        add_notes($song_id, $notes, $rating);
    }
}
