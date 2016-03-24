#!/usr/bin/python3
import argparse
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

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
        return response.read()
    pass            # error occured

argparser = argparse.ArgumentParser(description="""
    Download Debian.""")
argparser.add_argument("arch", type=str, help="""
    Architecture as given by 'uname -m'""")
argparser.add_argument("version", type=str, help="""
    Major kernel version in the form X.Y""")
argparser.add_argument("--pae", help="""
    Download extend physical address space version for i386""")

args = argparser.parse_args()

name = ""
archList = ["alpha", "amd64", "i386", "arm64", "armel", "armhf", "hppa", "m68k", 
            "mips", "mips64", "mips64el", "or1k", "powerpc", "powerpcspe", "ppc64", "ppc64el", "s390", "s390x", "sh4", "sparc", "sparc64", "x32"]
if args.arch in archList:
    if args.arch == 'i386' or args.arch == 'i686':
        if args.pae:
            name = "i386-pae"
        else:
            name = "i386"
    
    else if args.arch == 'x86_64':
        name = "amd64"
    else:
        name = "alpha"
else:
    pass        #non valid arch

if args.version:
    version = args.version


mainConfigFileURL = "https://anonscm.debian.org/cgit/kernel/linux.git/plain/debian/config/config"
mainConfigFile = download(mainConfigFileURL)

kernelarchList = ["arm", "mips", "powerpc", "s390", "sparc", "x86"]     #this will work
if args.arch in kernelarchList:
    kernelarchURL = "https://anonscm.debian.org/cgit/kernel/linux.git/plain/debian/config/kernelarch-"+args.arch+"/config"
    kernelarchFile = download(kernelarchURL)

# now for %arch/config
archConfigURL = name
