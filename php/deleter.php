<?php

/**
 * Delete a given song from the database.
 * @param int $song_id The song to delete.
 */
function delete_song($song_id) {
    // TODO: Delete unused dances and artists?
    query_db("DELETE FROM ".db::$notes_db." WHERE song_id = :song_id;
	          DELETE FROM ".db::$songs_db." WHERE song_id = :song_id", array(":song_id" => $song_id));
}

/**
 * @param $dance_name
 */
function delete_dance($dance_name) {
    query_db("DELETE FROM ".db::$dances_db." WHERE dance_name = :dance_name", array(":dance_name" => $dance_name));
}


/**
 * @param $artist_name
 */
function delete_artist($artist_name) {
    query_db("DELETE FROM ".db::$artists_db." WHERE artist_name = :artist_name", array(":artist_name" => $artist_name));
}