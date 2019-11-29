$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number" + msg.number);
        number = msg.number.toString();
        numbers_string = '<h4>' + msg.number.toString() + '</h4>';
        if (number > 0.7) {
            numbers_string = numbers_string + '<img src="static/imgs/water.jpg" alt="Water Tower">'
        }
        $('#log').html(numbers_string);
    });

});