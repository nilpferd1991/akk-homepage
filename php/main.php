<?php 
include 'database.php';

function print_titles() {
	print json_encode(query_db("SELECT * FROM `lieder` RIGHT JOIN `taenze` ON `lieder`.Tanz = `taenze`.ID"));
}

function print_artists() {
	print json_encode(query_db("SELECT `Interpret` FROM `lieder` GROUP BY `Interpret`"));
}

function print_dances() {
	print json_encode(query_db("SELECT `Tanz` FROM `taenze` GROUP BY `Tanz`"));
}

function insert_dance($dance_name) {
	//$dance_name_escaped = mysql_real_escape_string($dance_name);
	query_db("INSERT INTO `taenze` (`ID`, `Tanz`) VALUES ('', '$dance_name')
				SELECT '$dance_name' WHERE NOT EXISTS (
					SELECT * FROM `taenze` WHERE `Tanz` = '$dance_name'
			)");
	return query_db("SELECT `ID` FROM `taenze` WHERE `Tanz` = '$dance_name';");
}

insert_dance("Test");
print_dances();
?>