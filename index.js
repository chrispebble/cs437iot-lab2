var server_port = 65432;
var server_addr = "192.168.1.80";   // the IP address of Raspberry Pi

function client(input) {
    const net = require('net');

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${input}`);
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

function command(cmd) {
    // update the content in HTML
    document.getElementById("sending_to_server").innerHTML = cmd;
    // send the data to the server 
    client(cmd);
}

// Function to automatically request status update
function requestStatusUpdate() {
    console.log('Requesting status update...');
    // You can modify 'status' to whatever message your server expects for status requests
    client('status');
}

// Set up an interval to send status requests every 5 seconds
setInterval(requestStatusUpdate, 5000);
