#!/usr/bin/python3
import argparse
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def chunk_report(bytes_so_far, chunk_size, total_size):
    percent = float(bytes_so_far) / total_size
    percent = round(percent*100, 2)
    sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" % 
        (bytes_so_far, total_size, percent))

    if bytes_so_far >= total_size:
       sys.stdout.write('\n')
def chunk_read(response, chunk_size=8192, report_hook=None):
    aboutPage = response.info()
    total_size = aboutPage['Content-Length']
    total_size = int(total_size)
    bytes_so_far = 0

    while 1:
       chunk = response.read(chunk_size)
       bytes_so_far += len(chunk)
 
       if not chunk:
           break

       if report_hook:
           report_hook(bytes_so_far, chunk_size, total_size)

    return bytes_so_far

def download(url):
    print("Downloading " + url)
    req = Request(url)
    try:
        response = urlopen(req)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    else:
        aboutPage = response.info()
        chunk_read(response, report_hook=chunk_report)
        return response.read()
    pass            # error occured

argparser = argparse.ArgumentParser(description="""
    Download Liquorix.""")
argparser.add_argument("arch", type=str, help="""
    Architecture as given by 'uname -m'""")
argparser.add_argument("version", type=str, help="""
    Major kernel version in the form X.Y""")
argparser.add_argument("--pae", help="""
    Download extend physical address space version for i386""")

args = argparser.parse_args()

name = ""
if args.arch == 'i386' or args.arch == 'i686':
    if args.pae:
        name = "i386-pae"
    else:
        name = "i386"

if args.arch == 'x86_64':
    name = "amd64"

if args.version:
    version = args.version

top_url = "http://liquorix.net/sources/"
configFile = download(top_url + version + "/config." + name)
try:
    with open('myFile', 'wb') as my_file:    #name of file will be changed
        my_file.write(configFile)
except:
    print("error")
