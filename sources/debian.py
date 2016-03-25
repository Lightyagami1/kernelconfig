#!/usr/bin/python3
# debian uses multiple config files, in a particular order given at https://anonscm.debian.org/cgit/kernel/linux.git/tree/debian/config/README. There are many inconsistency within the subdirectories
import argparse
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from configparser import SafeConfigParser


def fileSaver(fileName, finalName):
    try:
        with open(finalName, 'wb') as my_file:    #name of file will be changed
            my_file.write(fileName)
            my_file.close()
    except:
        pass    # will make a empty file, not a big deal as in the end I will delete all files and only keep the main config file which is sure to be present.


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
    pass            # error occured, now it will have NoneType

def isComment(line):
    return line[0] == "#" or line.length() == 0 or line.startwith("\\#")

argparser = argparse.ArgumentParser(description="""
    Download Debian kernel config files""")
argparser.add_argument("arch", type=str, help="""
    Architecture as given by 'uname -m'""")
argparser.add_argument("version", type=str, help="""
    Major kernel version in the form X-Y""")    #example jessie-backport
argparser.add_argument("-f", "--flavour", help="""
    Download extend physical address space version for i386""")

args = argparser.parse_args()

name = ""
archList = ["alpha", "amd64", "i386", "arm64", "armel", "armhf", "hppa", "m68k", 
            "mips", "mips64", "mips64el", "or1k", "powerpc", "powerpcspe", "ppc64", "ppc64el", "s390", "s390x", "sh4", "sparc", "sparc64", "x32"]
if args.arch in archList:
    pass
else:
    print("non valid architecture")
    raise SystemExit

if args.version != "master":
    versionAddition = "?h="+args.version
else:
    versionAddition = ""

# this is base config file
mainConfigFileURL = "https://anonscm.debian.org/cgit/kernel/linux.git/plain/debian/config/config"+versionAddition
mainConfigFile = download(mainConfigFileURL)  ##remember to uncomment this
fileSaver(mainConfigFile, "ConfigFile.config")

kernelarchList = ["arm", "mips", "powerpc", "s390", "sparc", "x86"]     #this will work
if args.arch in kernelarchList:
    kernelarchURL = "https://anonscm.debian.org/cgit/kernel/linux.git/plain/debian/config/kernelarch-"+args.arch+"/config"+versionAddition
    kernelarchFile = download(kernelarchURL)
    fileSaver(kernelarchFile, "kernelarch.config")

# now for %arch/config
if args.arch in archList:
    archConfigURL = "https://anonscm.debian.org/cgit/kernel/linux.git/plain/debian/config/"+args.arch+"/config"+versionAddition
    archConfigFile = download(archConfigURL)
    fileSaver(archConfigFile, "archConfig.config")

# for %arch/config.%flavour and for %arch/config
if (args.arch in archList) & (args.flavour != None):
    if args.arch == "i386":
        if args.flavour == "pae":
            args.flavour = "686-pae"
        else:
            args.flavour = "686"
    archConfigFlavourURL = "https://anonscm.debian.org/cgit/kernel/linux.git/plain/debian/config/"+args.arch+"/config."+args.flavour+versionAddition
    archConfigFlavourFile = download(archConfigFlavourURL)
    fileSaver(archConfigFlavourFile, "archConfigFlavour.config")

#featureset-%featureset/config  #not sure what they do so leave them right now
#if args.featureset:
    #featuresetURL = "https://anonscm.debian.org/cgit/kernel/linux.git/plain/debian/config/featureset-rt/config"+versionAddition
    #featuresetFile = download(featuresetURL)

# %arch/featureset/config and %arch/featureset/config.%flavour are left for now

### now Have to merge these multiple config files in same order

secondfile = ["kernelarch.config", "archConfig.config", "archConfigFlavour.config"]
BASE = open("ConfigFile.config", "r+")
if args.arch not in kernelarchList:
    secondfile.remove("kernelarch.config")

for i in secondfile:
    f = open(i, "r")
    try:
        if len(f.read()) == 0:
            secondfile.remove(i)
        else:
            addingConfigFiles(BASE, f)
    finally:
        f.close()


def addingConfigFiles(base, top):
    if isComment(i):
        pass
#can now use functionlaty of settings.py of kernelconfig to manage these multiple files
