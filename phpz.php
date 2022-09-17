<?php 
	include_once("db.php");

	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);

	//echo "<pre>";
	//echo print_r($_POST,true);
	//echo "</pre>";

	if (isset($_POST["exploration_date"]) && !empty($_POST["exploration_date"]) && 
			isset($_POST["guild_invite"]) && !empty($_POST["guild_invite"])){

		Storeinvite($_POST["exploration_date"], $_POST["guild_name"]);
	}

	function StoreInvite($exploration_date, $guild_invite){
		
		GLOBAL $con;
 		$sql = "SELECT guild_invite FROM invite_list WHERE guild_invite=?";
     	$st=$con->prepare($sql);
		$st->execute(array($guild_invite));
		$all=$st->fetchAll();
		if (count($all) == 1){
			http_response_code(200);
			echo "SERVER: 2, data already in db";
			exit();
        }
		else{
			GLOBAL $con;
			$sql = "INSERT INTO invite_list (exploration_date, guild_invite) VALUES (?, ?)";
			$st=$con->prepare($sql);
			$st->execute([$exploration_date, $guild_invite]);
			http_response_code(200);
			echo "SERVER: 1, request sucessfully processed";
			exit();
		}
	}

	//if data not valid
	echo "False, error 400";
	http_response_code(400);
	exit();
?>