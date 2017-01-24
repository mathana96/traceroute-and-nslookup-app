#!/usr/bin/python

"""
Phllip Calvin's python-traceroute.py, from http://gist.github.com/502451
based on Leonid Grinberg's traceroute, from
http://blog.ksplice.com/2010/07/learning-by-doing-writing-your-own-traceroute-in-8-easy-steps/

Autogen html code adapted from a posting at 
http://stackoverflow.com/questions/21437386/launch-html-code-in-browser-that-is-generated-by-beautifulsoup-straight-from-p

Embed html into python
http://stackoverflow.com/questions/29734208/how-can-i-connect-my-python-script-with-my-html-file

Use a public API
https://www.youtube.com/watch?v=X4VBfiuIBJY
"""
from __future__ import print_function
import socket
import struct
import sys
import os
import webbrowser
import json
import urllib



def main(dest_name):
    dest_addr = socket.gethostbyname(dest_name)
    port = 33434
    max_hops = 30
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    IPlist = []


    while True:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        
        # Build the GNU timeval struct (seconds, microseconds)
        timeout = struct.pack("ll", 5, 0)
        
        # Set the receive timeout so we behave more like regular traceroute
        recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)
        
        recv_socket.bind(("", port))
        print(" %d  " % ttl)
        send_socket.sendto("", (dest_name, port))
        curr_addr = None
        curr_name = None
        finished = False
        tries = 1
        while not finished and tries > 0:
            try:
                _, curr_addr = recv_socket.recvfrom(512)
                finished = True
                curr_addr = curr_addr[0]
                # try:
                #     curr_name = socket.gethostbyaddr(curr_addr)[0]
                # except socket.error:
                #     curr_name = curr_addr
            except socket.error as (errno, errmsg):
                tries = tries - 1
                print("* ")
        
        send_socket.close()
        recv_socket.close()
        
        if not finished:
            pass

        if curr_addr is not None:
            IPlist.append(curr_addr)
            # print(*IPlist, sep='\n')
 

        ttl += 1
        if curr_addr == dest_addr or ttl > max_hops:
            break
    
    reverseDNS(IPlist)

def reverseDNS(IPlist):
    list(set(IPlist))
    print(IPlist)
    for ip in IPlist:
        url = "http://ipinfo.io/" + ip + "/json"
        print(url)
        info = str(urllib.urlopen(url).read()) 
        data = json.loads(info) 
        if (("bogon" in data) == False):
            geolist.append(data['loc'])
            # print("Country: " + data['country'])

    map(geolist)

# def data_to_html_table(data):
#     html = '<table><tbody>'
#     for item in data:
#         html += '<tr><td>' + str(item) + '</td></tr>'
#     html += '</tbody></table>'
#     return html

# print data_to_html_table(data)
#         # else:
        #     print("Country: " + data['country'])

def map(geolist):
    # glist = geolist
    html = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Simple Map</title>
        <meta name="viewport" content="initial-scale=1.0">
        <meta charset="utf-8">
        <style>
          /* Always set the map height explicitly to define the size of the div
           * element that contains the map. */
          #map {
            height: 100%;
          }
          /* Optional: Makes the sample page fill the window. */
          html, body {
            height: 100%;
            margin: 0;
            padding: 0;
          }
        </style>
      </head>
      <body>
        <div id="map"></div>
        <script>
          var map;
          function initMap() {
            var middle = {lat: 53.2734, lng: -7.778};

            map = new google.maps.Map(document.getElementById('map'), {
              center: middle,
              zoom: 4
            });
          """
    for geo in geolist:
        lat, lng = geo.split(",")
        num = 1
        html += "var " + position + " = " + "new google.maps.LatLng(" + str(lat) + ", " + str(lng) + ");" + " var " + position + " marker = new google.maps.Marker({position: " + str(geo) + " location, map: map, title: \"Hello world\"});"
          

    html += """
          }
        </script>
        <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAK_JiBbgnyNYXXwaFWAyIPkVFL80a-NAc&callback=initMap"
        async defer></script>
      </body>
    </html>
          
            """
    path = os.path.abspath('results.html')
    url = 'file://' + path

    with open(path, 'w') as f:
        f.write(html)
        webbrowser.open(url)

# def main(): 
#     ip = raw_input("Enter the IP: ") 
#     url = "http://tamilhackers.net/ip?ip=" + ip 
#     info = str(urllib.urlopen(url).read()) 
#     data = json.loads(info) 
#     isValid = True 
#     if (data['status'] == 404): 
#         isValid = False print("Invalid IP!") 
#     else: 
#         display(data)

# def display(data): 
#     print("\nResult\n------\n") 
#     print("IP: " + data['ip']) 
#     print("ISP: " + data['isp']) 
#     print("ORG: " + data['org']) 
# print("Country: " + data['country']) print("City: " + data['city']) print("Region: " + data['region']) print("TimeZone: " + data['timezone']) print("ZipCode: " + data['zip']) print("Country Code: " + data['countryCode']) print("Latitude: " + data['latitude']) print("Longitude: " + data['longitude']) print("Currency Code: " + data['currencyCode'])



if __name__ == "__main__":
    main('google.com')




# html = '<html> ...  generated html string ...</html>'
# path = os.path.abspath('results.html')
# url = 'file://' + path

# with open(path, 'w') as f:
#     f.write(html)
# webbrowser.open(url)