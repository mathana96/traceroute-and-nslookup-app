"""
nslookup code from: (username)
http://stackoverflow.com/questions/12297500/python-module-for-nslookup

"""

import subprocess
import urllib
import json
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
    dest_name = "www.google.com"
    process = subprocess.Popen(["nslookup", dest_name], stdout=subprocess.PIPE)
    output = process.communicate()[0].split('\n')

    IPlist = []
    geolist = []

    for data in output:
        if 'Address' in data:
            IPlist.append(data.replace('Address: ',''))
    IPlist.pop(0)

    print(IPlist)

    for ip in IPlist:
        url = "http://ipinfo.io/" + ip + "/json"
        print(url)
        info = str(urllib.urlopen(url).read()) 
        data = json.loads(info) 
        if (("bogon" in data) == False):
            geolist.append(data)
    print(geolist)

    return render_template('nslookup.html', geolist=geolist)

if __name__ == '__main__':
    app.run(debug=True)
