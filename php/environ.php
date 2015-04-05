<?php
error_reporting(E_ALL | E_STRICT);
ini_set("display_errors", "On");

require_once "./db_user.php";

class db {
	public static $db = "akk";
	public static $dances_db = "dances";
	public static $users_db = "users";
	public static $songs_db = "songs";
	public static $songlists_db = "songlists";
	public static $artists_db = "artists";
	public static $playlists_db = "playlists";
	public static $notes_db = "notes";
}