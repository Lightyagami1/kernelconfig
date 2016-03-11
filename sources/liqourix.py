#!/usr/bin/python3
import argparse
from urllib import request

def download(url):
    print("Downloading " + url)
    with request.urlopen(url) as response:
        return response.read()

argparser = argparse.ArgumentParser(description="""
    Download Liquorix.""")
argparser.add_argument("arch", type=str, help="""
    Architecture as given by 'uname -m'""")
argparser.add_argument("version", type=str, help="""
    Major kernel version in the form X.Y""")
argparser.add_argument("--pae", help="""
    Download high memory support version for i386""")

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
    print(version,args.arch)


base = "http://liquorix.net/sources/"
configFile = download(base + version + "/config." + name)
