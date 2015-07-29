<?php
/* Set error reporting on */
error_reporting(E_ALL | E_STRICT);
ini_set("display_errors", "On");

/* Import the user information for the db */
require_once "./db_user.php";

class db {
    /* A small helper class to store all the needed variables of the db names. */
	public static $db = "akk";
	public static $dances_db = "dances";
	public static $users_db = "users";
	public static $songs_db = "songs";
	public static $songlists_db = "songlists";
	public static $artists_db = "artists";
	public static $playlists_db = "playlists";
	public static $notes_db = "notes";
}