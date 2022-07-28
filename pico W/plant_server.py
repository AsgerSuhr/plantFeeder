import socket, utils, network, tinyweb, re
from machine import Pin
from utime import sleep

def run(net):
    # setting up pumps
    pump_01 = Pin(5, Pin.OUT)
    pump_02 = Pin(4, Pin.OUT)
    pump_03 = Pin(3, Pin.OUT)
    pump_04 = Pin(2, Pin.OUT)
    pump_01.value(1)
    pump_02.value(1)
    pump_03.value(1)
    pump_04.value(1)
    
    pumps = {'1':pump_01,
             '2':pump_02,
             '3':pump_03,
             '4':pump_04}

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
        await response.send_file('website.html')
    
    @app.route('/getPump/<data>', method='GET')
    def user(req, resp, data):
        await resp.start_html()
        data = req.query_string.decode()
        print(data)
        pump, ml = data.split('=')
        pump_nr = pump.split('+')[1]
        t = utils.flow(int(ml))
        html = utils.read_html('wateringPlant.html')
        html = html.replace('{nr}', pump_nr)
        html = html.replace('{delay}', str(int(t)+5))
        html = html.replace('{ip}', net.ifconfig()[0])
        await resp.send(html)
        pumps[pump_nr].value(0)
        sleep(t)
        pumps[pump_nr].value(1)

    # Run the web server as the sole process
    app.run(host="0.0.0.0", port=80)