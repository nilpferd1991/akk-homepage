<?php
/**
 * @param $column
 * @param $term
 */
function print_songs($column, $term) {
    $column_name = "";

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
 * Return all songs which have $term in their names, artist names or dance names.
 * @param string $term The piece to look for.
 */
function print_all_songs($term) {
    print json_encode(query_class("SELECT song_id, title, artist_id, artist_name, dance_id, dance_name
			FROM ".db::$songs_db." AS ".db::$songs_db."
			JOIN ".db::$artists_db." AS ".db::$artists_db." USING (artist_id)
			JOIN ".db::$dances_db." AS ".db::$dances_db. " USING (dance_id)
			WHERE (title LIKE :term) OR (artist_name LIKE :term) OR (dance_name LIKE :term)", array(":term" => "%".$term."%")));
}

/**
 * @param int $song_id
 */
function print_song_information($song_id) {
    print json_encode(query_class("SELECT song_id, title, artist_name, dance_name, note, rating
			FROM ".db::$songs_db." AS ".db::$songs_db."
			JOIN ".db::$artists_db." AS ".db::$artists_db." USING (artist_id)
			JOIN ".db::$dances_db." AS ".db::$dances_db. " USING (dance_id)
			JOIN ".db::$notes_db." AS ".db::$notes_db. " USING (song_id)
			WHERE (song_id LIKE :song_id)", array(":song_id" => "%".$song_id."%"))[0]);
}