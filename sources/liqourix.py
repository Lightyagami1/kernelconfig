#!/usr/bin/python3
import argparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

def download(url):
    print("Downloading " + url)
    req = Request(url)
    try:
        response = urlopen(req)
    except error.HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    else:
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
        name = "i1386"

if args.arch == 'x86_64':
    name = "amd64"

if args.version:
    version = args.version

top_url = "http://liquorix.net/sources/"
configFile = download(top_url + version + "/config." + name)
