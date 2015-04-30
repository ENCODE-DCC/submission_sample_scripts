<?php
# GET an object from an ENCODE server

#Uses Requests library from https://github.com/rmccue/Requests
include('../Requests/library/Requests.php');
Requests::register_autoloader();

# Force return from the server in JSON format
$headers = array('Content-Type' => 'application/json', 'Accept' => 'application/json');

#This URL locates the ENCODE biosample with accession number ENCBS000AAA
$url = "<server>/biosamples/ENCBS000AAA/?frame=object"; // <-Replace this with appropriate server

# GET the object
$request = Requests::get($url, $headers);

#Extract the JSON object
$json =$request->body;

#Print the object
var_dump(json_decode($json));

?>