from __future__ import print_function
import socket
import struct
import sys
import os
import webbrowser
import json
import urllib
from flask import Flask, render_template
app = Flask(__name__)



@app.route("/")
def main():
    dest_name = 'google.com'	
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
    
#     reverseDNS(IPlist)


# def reverseDNS(IPlist):
    IPlist = list(set(IPlist))
    print(IPlist)
    geolist = []
    for ip in IPlist:
        url = "http://ipinfo.io/" + ip + "/json"
        print(url)
        info = str(urllib.urlopen(url).read()) 
        data = json.loads(info) 
        if (("bogon" in data) == False):
            geolist.append(data['loc'])
    geolist = list(set(geolist))
    print(geolist)
    return render_template('template.html', list=geolist)



if __name__ == '__main__':
    app.run(debug=True)
