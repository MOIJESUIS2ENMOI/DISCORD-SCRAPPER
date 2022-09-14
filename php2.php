<?php 
	include_once("db.php");

	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);

	echo "<pre>";
	echo print_r($_POST,true);
	echo "</pre>";

	if (isset($_POST["exploration_date"]) && !empty($_POST["exploration_date"]) &&
	        isset($_POST["guild_name"]) && !empty($_POST["guild_name"]) &&
	   		isset($_POST["guild_invite"]) && !empty($_POST["guild_invite"]) &&
	  		isset($_POST["expiration_date"]) && !empty($_POST["expiration_date"]) &&
	   		isset($_POST["guild_members_count"]) && !empty($_POST["guild_members_count"]) &&
	  		isset($_POST["guild_members_online"]) && !empty($_POST["guild_members_online"]) &&
	 		isset($_POST["guild_id"]) && !empty($_POST["guild_id"]) &&
	   		isset($_POST["guild_icon"]) && !empty($_POST["guild_icon"]) &&
	   		isset($_POST["guild_banner"]) && !empty($_POST["guild_banner"]) && 
	   		isset($_POST["guild_description"]) && !empty($_POST["guild_description"]) && 
	   		isset($_POST["verification_level"]) && !empty($_POST["verification_level"])&& 
	   		isset($_POST["invite_channel_id"]) && !empty($_POST["invite_channel_id"]) && 
	   		isset($_POST["invite_channel_name"]) && !empty($_POST["invite_channel_name"])&&
	   		isset($_POST["inviter_id"]) && !empty($_POST["inviter_id"]) &&
	   		isset($_POST["inviter_name"]) && !empty($_POST["inviter_name"]) &&
	   		isset($_POST["inviter_avatar"]) && !empty($_POST["inviter_avatar"])){

		StoreData($_POST["exploration_date"], $_POST["guild_name"], $_POST["guild_invite"], $_POST["expiration_date"], $_POST["guild_members_count"], $_POST["guild_members_online"], $_POST["guild_id"], $_POST["guild_icon"], $_POST["guild_banner"], $_POST["guild_description"], $_POST["verification_level"], $_POST["invite_channel_id"], $_POST["invite_channel_name"], $_POST["inviter_id"], $_POST["inviter_name"], $_POST["inviter_avatar"]);
	}

	function StoreData($exploration_date, $guild_name, $guild_invite, $expiration_date, $guild_member_count, $guild_members_online, $guild_id, $guild_icon, $guild_banner, $guild_description, $verification_level, $invite_channel_id, $invite_channel_name, $inviter_id, $inviter_name, $inviter_avatar){
		
		GLOBAL $con;
		$sql = "INSERT INTO server_list (exploration_date, guild_name, guild_invite, expiration_date, guild_member_count, guild_members_online, guild_id, guild_icon, guild_banner, guild_description, verification_level, invite_channel_id, invite_channel_name, inviter_id, inviter_name, inviter_avatar) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
		$st=$con->prepare($sql);
		$st->execute([$exploration_date, $guild_name, $guild_invite, $expiration_date, $guild_member_count, $guild_members_online, $guild_id, $guild_icon, $guild_banner, $guild_description, $verification_level, $invite_channel_id, $invite_channel_name, $inviter_id, $inviter_name, $inviter_avatar]);
		http_response_code(200);
		exit();
	}

	//if username or password is null (not set)
	echo "False, error 400";
	http_response_code(400);
	exit();
?>