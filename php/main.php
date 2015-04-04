<?php 
require './core_functions.php';

function print_titles() {
	print json_encode(query_db("SELECT * FROM `lieder` RIGHT JOIN `taenze` ON `lieder`.Tanz = `taenze`.ID"));
}

print json_encode(print_artists());