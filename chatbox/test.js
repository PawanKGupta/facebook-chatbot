
function sendMessage(serversidemessage){

   
var sendFromServerValue = "Message from Server:" + serversidemessage;
var sendValue =  document.getElementById("sendfromclient").value; 

/* Server Side Dynamic Div */
 var server = document.createElement("li");
 server.id = "testserver";
 var textservernode = document.createTextNode(sendFromServerValue);
 server.appendChild(textservernode);
 document.getElementById("myList").appendChild(server); 


/* Clinet Side Dynamic Div */

 var client = document.createElement("li");
 client.id = "testclient";
 var textnode = document.createTextNode("User:" + sendValue);
 client.appendChild(textnode);
 document.getElementById("myList").appendChild(client); 
}



