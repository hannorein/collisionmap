import csv
import random
import os
import urllib2
import urllib
import time
import xml.etree.ElementTree as ET
def cfracs(fs,deli):
    nfs = []
    for f in fs:
        n = f.split(deli)
        for k in n:
            nfs.append(k)
    return nfs

with open('tpsoperations_tweets.csv.1', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if "cycl" in row[2].lower():
            if "motorc" not in row[2].lower():
                if "collision" == row[2].lower()[0:9]:
                    line= row[2][10:].strip().replace("\n", ",")
                    fracs = line.split(",")
                    fracs1 = cfracs(fracs,"..")
                    fracs2 = cfracs(fracs1,"-")
                    fracs3 = cfracs(fracs2,"report")
                    ad = fracs3[0] + ", Toronto"

                    found = 0
                    with open("locations.txt","r") as fl:
                        for ll in fl:
                            cl = ll.split(",")
                            if cl[0]+","+cl[1]==ad:
                                found = 1
                                break
                    if found == 0:
                        time.sleep(0.2)
                        uad = urllib.urlencode({"address": ad+", Toronto"})
                        url = "http://maps.google.com/maps/api/geocode/xml?"+uad
                        response = urllib2.urlopen(url)
                        html = response.read()
                        root = ET.fromstring(html)
                        stars = root.findall(".//location/lat")
                        if len(stars)>0:
                           lat = float(stars[0].text)
                        stars = root.findall(".//location/lng")
                        if len(stars)>0:
                           lng = float(stars[0].text)
                        with open("locations.txt","a+") as fl:
                            fl.write(ad+",%.9f,%.9f\n"%(lat,lng))
                    with open("locations.txt","r") as fl:
                        for ll in fl:
                            cl = ll.strip().split(",")
                            if cl[0]+","+cl[1]==ad:
                                print cl[2]+";"+ cl[3]+";"+ row[1]+";"+ row[2].strip().replace("\n", ",").replace(";",",").replace("\"","")
                                break
                    
