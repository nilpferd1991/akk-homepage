<?php
require_once './environ.php';

$connected = False;
$connection = NULL;

/**
 * Open a new connection to the db server
 */
function connect_to_db() {
	global $connected, $connection;
	global $db_user, $db_host, $db_password;
	try {
		$connection = new PDO("mysql:dbname=" . db::$db . ";host=$db_host", "$db_user", "$db_password");
        $connection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	} catch (PDOException $e) {
		die("Connection failed: " . $e->getMessage());
	}  
	$connected = True;
}

/**
 * Send a query to the database
 * @param string $query query to send
 * @param null $variables the variables to use for the query
 * @return mixed the result of the query as a PDO::Statement.
 */
function query_db($query, $variables=NULL) {
	global $connected, $connection;
	
	if(!$connected) {
		connect_to_db();
	}
	
	try {
		$statement = $connection->prepare($query, array(PDO::ATTR_CURSOR => PDO::CURSOR_SCROLL));
		$statement->execute($variables);
		return $statement;
	} catch (PDOException $e) {
		die("Error in query: " . $e->getMessage());
	}
}

/**
 * Send a query to the database and fetch the results in a convenient way
 * @param string $query query to send
 * @param null $variables the variables to use for the query
 * @param int $fetch the PDO fetch property
 * @return mixed the result of the query as a PDO::fetchAll result.
 */
function query_with_fetch($query, $variables=NULL, $fetch) {
    $statement = query_db($query, $variables);
    try {
        $fetch_result = $statement->fetchAll($fetch);
    } catch(PDOException $e) {
        die("Error in result fetching: " . $e->getMessage());
    }
    return $fetch_result;
}

/**
 * Return the result of the query as an array
 * @param string $query query to send
 * @param null $variables the variables to use for the query
 * @return mixed the result of the query as an array.
 */
function query_array($query, $variables=NULL) {
    return query_with_fetch($query, $variables, PDO::FETCH_COLUMN);
}

/**
 * Return the result of the query as a string
 * @param string $query query to send
 * @param null $variables the variables to use for the query
 * @return string the result of the query as a string.
 */
function query_string($query, $variables=NULL) {
    return query_with_fetch($query, $variables, PDO::FETCH_BOTH);
}

/**
 * Return the result of the query as a class (for json)
 * @param string $query query to send
 * @param null $variables the variables to use for the query
 * @return mixed the result of the query as a class.
 */
function query_class($query, $variables=NULL) {
    return query_with_fetch($query, $variables, PDO::FETCH_CLASS);
}