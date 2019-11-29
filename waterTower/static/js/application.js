$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number" + msg.number);
        number = msg.number.toString();
        numbers_string = '<h4>' + msg.number.toString() + '</h4>';

        if (number > 0.1 && number < 0.2){
            value = "20";
        }else if (number > 0.2 && number < 0.3){
            value = "30";
        }else if (number > 0.3 && number < 0.4){
            value = "40";
        }else if (number > 0.4 && number < 0.5){
            value = "50";
        }else if (number > 0.5 && number < 0.6){
            value = "60";
        }else if (number > 0.6 && number < 0.7){
            value = "70";
        }else if (number > 0.7 && number < 0.8){
            value = "80";
        }else if (number > 0.9 && number < 1){
            value = "90";
        }else if (number < 0.1){
            value = "0";
        }

        number = Math.trunc(msg.number * 1000); 
        css = `
            <div id="torre" >
                <img src="static/imgs/water` + value.toString() + `.png" width="100%" >
            </div>
            <div id="bomba1" >
                <img src="static/imgs/pump_off.png" width="100%" >
            </div>
            <div id="bomba2" >
                <img src="static/imgs/pump_on.png" width="100%" >
            </div>
            <div id="huerto" >
                <img src="static/imgs/crop.png" width="100%" >
            </div>
            <div id="value1" >   
                <h3> Water level:
        ` +  number.toString() +  " liters</h3> </div>";
            
        $('#log').html(css);
    });

});