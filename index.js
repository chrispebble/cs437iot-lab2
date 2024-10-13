var server_port = 65432;
var server_addr = "192.168.1.80";   // the IP address of your Raspberry PI

function client(input){
    
    const net = require('net');
    // var input = document.getElementById("myName").value;

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${input}\r\n`);
    });
    
    // get the data from the server
    client.on('data', (data) => {
        document.getElementById("info_from_server").innerHTML = data;
        console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });

}

function command(cmd){

    // get the element from html
    // var name = document.getElementById("myName").value;
    // update the content in html
    document.getElementById("sending_to_server").innerHTML = cmd;
    // send the data to the server 
    // to_server(name);
    client(cmd);

}
