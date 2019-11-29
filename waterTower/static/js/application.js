$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    //receive details from server
    socket.on('newnumber', function(msg) {
        number = msg.number.toString();
        numbers_string = '<h4>' + msg.number.toString() + '</h4>';
        crop = "crop";
        style = "";
        value = "80";

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
            style = `style="background-image: url('/static/imgs/fondo2dead.png')"`;
        }else if (number < 0.1){
            value = "0";
            crop = "cropdead";
            style = `style="background-image: url('/static/imgs/fondo2dead.png')"`;
        }

        if (msg.MV001 == 2){
            MV001 = "off";
        }else if (msg.MV001 == 1){
            MV001 = "on";
        }
        console.log(MV001);

        if (msg.P201 == 2){
            P201 = "off";
        }else if (msg.P201 == 1){
            P201 = "on";
        }
        console.log(P201);

        number = Math.trunc(msg.number * 1000); 
        css = `
            <div id="fondo" ` + style + ` class="col-md-2 col-md-offset-2">
            <div id="torre" >
                <img src="static/imgs/water` + value.toString() + `.png" width="100%" >
            </div>
            <div id="bomba1" >
                <img src="static/imgs/pump_` + MV001.toString() + `.png" width="100%" >
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