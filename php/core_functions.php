<?php
require_once './environ.php';
require_once './database.php';
require_once './password.php';
require_once './getter.php';
require_once './adder.php';
require_once './lister.php';
require_once './deleter.php';
require_once './printer.php';
require_once './updater.php';



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
