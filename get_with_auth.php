<?php
# GET an object from an ENCODE server

#Uses Requests library from https://github.com/rmccue/Requests
include('../Requests/library/Requests.php');
Requests::register_autoloader();

# Force return from the server in JSON format
$headers = array('Content-Type' => 'application/json', 'Accept' => 'application/json');

#This URL locates the ENCODE biosample with accession number ENCBS000AAA
$url = "<server>/biosamples/ENCBS000AAA/?frame=object"; // <-Replace this with appropriate server

# Authentication is only required to GET unreleased objects
$authid = "access_key"; // <-Replace this with your access_key
$authpw = "secret_access_key"; // <-Replace this with your secret_access_key
$auth = array('auth' => array($authid, $authpw));

# GET the object
$request = Requests::get($url, $headers,  $auth);

#Extract the JSON object
$json =$request->body;

#Print the object
var_dump(json_decode($json));

?>