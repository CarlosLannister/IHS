$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    //receive details from server
    socket.on('newnumber', function(msg) {
        number = msg.number.toString();
        numbers_string = '<h4>' + msg.number.toString() + '</h4>';
        crop = "crop";

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
        }else if (number > 1.1){ //Water Tank Limit
            value = "over";
        }else if (number < 0.1){
            value = "0";
            crop = "cropdead";
        }

        if (msg.MV101 == 0){
            MV101 = "off";
        }else{
            MV101 = "on";
        }

        if (msg.P201 == 0){
            P201 = "off";
        }else{
            P201 = "on";
        }

        number = Math.trunc(msg.number * 1000); 
        css = `
            <div id="torre" >
                <img src="static/imgs/water` + value.toString() + `.png" width="100%" >
            </div>
            <div id="bomba1" >
                <img src="static/imgs/pump_` + MV101.toString() + `.png" width="100%" >
            </div>
            <div id="bomba2" >
                <img src="static/imgs/pump_` + P201.toString() + `.png" width="100%" >
            </div>
            <div id="huerto" >
                <img src="static/imgs/`+ crop.toString() + `.png" width="100%" >
            </div>
            <div id="value1" >   
                <h3> Water level:
        ` +  number.toString() +  " liters</h3> </div>";
            
        $('#log').html(css);
    });

});