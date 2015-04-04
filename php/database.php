<?php
include './environ.php';

$connected = False;
$connection = NULL;

function connect_to_db() {
	global $connected, $connection;
	global $db, $db_user, $db_host, $db_password;
	try {
		$connection = new PDO("mysql:dbname=$db;host=$db_host", "$db_user", "$db_password");
	} catch (PDOException $e) {
		echo "Connection failed: " . $e->getMessage();
	}  
	$connected = True;
}

function query_db($query, $variables) {
	global $connected, $connection;
	
	if(!$connected) {
		connect_to_db();
	}
	
	try {
		$statement = $connection->prepare($query, array(PDO::ATTR_CURSOR => PDO::CURSOR_SCROLL));
		$statement->execute($variables);
		return $statement;
	} catch (PDOException $e) {
		echo "Error in query: " . $e->getMessage();
	}
}

function query_array($query, $variables=NULL) {
	$statement = query_db($query, $variables);
	return $statement->fetchAll(PDO::FETCH_COLUMN);
}

function query_string($query, $variables=NULL) {
	$statement = query_db($query, $variables);
	return $statement->fetchAll();
}

function query_class($query, $variables=NULL) {
	$statement = query_db($query, $variables);
	return $statement->fetchAll(PDO::FETCH_CLASS);
}