import socket, utils, network, tinyweb, re
import machine
from utime import sleep

def run(ssid, password):
    # Define an access point, name it and then make it active
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    # Wait until it is active
    while ap.active == False:
        pass

    print("Access point active")
    # Print out IP information
    print(ap.ifconfig())

    # Start up a tiny web server
    app = tinyweb.webserver()

    # Serve a simple Hello World! response when / is called
    # and turn the LED on/off using toggle()
    @app.route('/')
    async def index(request, response):
        # Start HTTP response with content-type text/html
        await response.start_html()
        # Send actual HTML page
        #await response.send(utils.read_html('ap.html'))
        await response.send_file('ap.html')
    
    @app.route('/getWiFi/<fn>', method='GET')
    def user(req, resp, fn):
        await resp.start_html()
        data = req.query_string.decode()
        ssid, password = data.split('&')
        ssid = ssid.split('=')[-1]
        password = password.split('=')[-1]
        print(ssid, password)
        with open('secrets.txt', 'w') as f:
            f.write(f'{ssid}\n{password}')
        machine.reset()

    # Run the web server as the sole process
    app.run(host="0.0.0.0", port=80)
