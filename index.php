<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>ts3sniff</title>
	<meta name="description" content="teamspeak3 log analyzer">
	<meta name="author" content="Karri Väänänen">
	<meta name="viewport" content="width=device-width, initial-scale=1">

	<link href='//fonts.googleapis.com/css?family=Raleway:400,300,600' rel='stylesheet' type='text/css'>

	<link rel="stylesheet" href="bower_components/skeleton/css/normalize.css">
	<link rel="stylesheet" href="bower_components/skeleton/css/skeleton.css">
	<link rel="stylesheet" href="style.css">

</head>
<body>

  <div class="section">
    <div class="container">
      <div class="row">
	    <h3>Latest connections by hour</h3>
		<a href="connected.png"><img class="u-max-full-width" src="connected.png" alt="Connections"  /></a>
		<p class="updatedate"><?php echo "Updated on ".date("F d Y H:i:s (e)",filemtime("connected.png")); ?></p>
      </div>
	  <div class="row">
	    <h3>Latest disconnections by hour</h3>
		<a href="disconnected.png"><img class="u-max-full-width" src="disconnected.png" alt="Connections"  /></a>
		<p class="updatedate"><?php echo "Updated on ".date("F d Y H:i:s (e)",filemtime("disconnected.png")); ?></p>
      </div>
    </div>
  </div>
  
  <div class="section">
    <div class="container">
	  <h3>Overview</h3>
      <div class="row overview-table">
		<?php include('overview.html'); ?>
		<p class="updatedate"><?php echo "Updated on ".date("F d Y H:i:s (e)",filemtime("overview.html")); ?></p>
	    <p><a href="output.txt">output</a></p>
	  </div>
    </div>
  </div>

  <hr />
  
  <div class="section footer">
    <div class="container">
      <div class="row">
	    <p>ts3sniff</p>
	  </div>
    </div>
  </div>

</body>
</html>
