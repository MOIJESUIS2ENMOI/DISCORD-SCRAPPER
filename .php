<?php 
	include_once("db.php");

	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);

	//echo "<pre>";
	//echo print_r($_POST,true);
	//echo "</pre>";

		
GLOBAL $con;
$sql = "SELECT exploration_date, guild_invite FROM invite_list";
$st=$con->prepare($sql);
$st->execute();
$all=$st->fetchAll();
if (count($all) > 1){
	echo $all[0]['guild_invite'];
	http_response_code(200);
	echo "SERVER: 1, data already in db";
	exit();
}
else {
	http_response_code(200);
	echo "SERVER: 1, no data in db";
	exit();
}

?>