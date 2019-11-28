$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number" + msg.number);
        numbers_string = '';
        numbers_string = '<h4>' + msg.number.toString() + '</h4>';
        $('#log').html(msg.number);
    });

});