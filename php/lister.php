<?php

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