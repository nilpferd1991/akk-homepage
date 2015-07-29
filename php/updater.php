<?php
require_once "./adder.php";

/**
 * Update a song to the given information
 * @param int $song_id
 * @param string $title
 * @param string $artist
 * @param string $dance
 * @param string $rating
 * @param string $notes
 */
function update_song($song_id, $title, $artist, $dance, $rating, $notes) {
    $artist_id = get_or_add_artist($artist);
    $dance_id = get_or_add_dance($dance);

    query_db("UPDATE ".db::$songs_db." SET
                song_id=:song_id,
                title=:title,
                artist_id=:artist_id,
                dance_id=:dance_id
              WHERE (song_id=:song_id)", array(":song_id" => $song_id, ":title" => $title,
        ":artist_id" => $artist_id, ":dance_id" => $dance_id));

    query_db("UPDATE ".db::$notes_db." SET
                song_id=:song_id,
                note=:notes,
                rating=:rating
              WHERE (song_id=:song_id)", array(":song_id" => $song_id, ":rating" => $rating, ":notes" => $notes));
}