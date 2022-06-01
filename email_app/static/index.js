queue = []

 function updateVisual() {
    $("ol").empty();
    
    for(var i=0; i<queue.length; i++){
	var listItemElement = document.createElement("li");
	var textNode = document.createTextNode(queue[i][0]);
    listItemElement.appendChild(textNode);
    document.getElementById("list").appendChild(listItemElement);
	}
}

function flushList() {
	document.getElementById("name").value = "";
    document.getElementById("email").value = "";
    //document.getElementById("event_id").value = "";
}

function emailUsers() {
	$.ajax({
  type: "POST",
  url: "http://localhost:5000/",
  data: { 'email': queue[0][1], 'message': 'You have reached the front of the Queue! Please approach the front desk.'}
}).done(function( o ) {
   // do something
});

	for(var i=1; i<queue.length; i++){
	user = queue[i]
	$.ajax({
  type: "POST",
  url: "http://localhost:5000/",
  data: { 'email': user[1], 'message': 'There are '.concat(i.toString()).concat(' people remaining')}
}).done(function( o ) {
   // do something
});
}

}

function add() {
    // TODO: Show the queue on submission

    var name = document.getElementById("name").value.trim();
    var email = document.getElementById("email").value.trim();
    //var event_id = document.getElementById("event_id").value.trim();

    queue.push([name, email]);

    flushList();

    updateVisual();
}

function next() {
	emailUsers();

	queue.shift();

	flushList();

	updateVisual();
}
