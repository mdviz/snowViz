__author__ = 'mdowd'

path = r"/Users/mdowd/Programming/mdviz/snowViz/snow.txt"
outpath = r"/Users/mdowd/Programming/mdviz/snowViz"
out_file = open( outpath +'/'+ "cleanSnow.csv", 'w')
import random

with open(path, "r") as f:
    lines = f.readlines()
runMe = 0

out_file.write("lat,lng,val\n")

for index, line in enumerate(lines):
    runMe +=1
    theLine = line.strip()
    try:
        if theLine[0].isdigit():
            myOut = theLine[0:14].strip().split(' ')
            if len(myOut)>2:
                myOut.remove('')
        
            lineString = ",".join(myOut)
            out_file.write(lineString + ","+ str(1000*random.random()) + "\n")
    except IndexError:
        print "no"


out_file.close()
