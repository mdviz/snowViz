__author__ = 'mdowd'
import urllib
from os import listdir

#response = urllib.urlopen('http://www1.ncdc.noaa.gov/pub/data/snowmonitoring/fema/02-2008-dlysnfl.txt')

path = r"/Users/mdowd/Programming/mdviz/snowViz/test.txt"
outpath = r"/Users/mdowd/Programming/mdviz/snowViz"
cleanOutPath = r"/Users/mdowd/Programming/mdviz/snowViz/cleaned"
rawDataPath = r'/Users/mdowd/Programming/mdviz/snowViz/rawData'
yearRange = (2006,2014)

def collectData():
    for year in xrange(yearRange[0], yearRange[1]+1):
        for mon in xrange(1,13):
            strYear = str(year)
            strMon = str(mon).zfill(2)
            print strYear, strMon
            urlPart1 = "http://www1.ncdc.noaa.gov/pub/data/snowmonitoring/fema/"
            urlPart3 = "-dlysnfl.txt"
            urllib.urlretrieve (urlPart1 + strMon + "-" + strYear + urlPart3, outpath +"/"+ strYear + "_" + strMon + ".txt")

def processFile(path, month, year):
    out_file = open(cleanOutPath + "/" + "c_" + month + "_" + year + ".csv", 'w')
    days = 31
    
    with open(path, "r") as f:
        lines = f.readlines()
    runMe = 0
    
    headerString = '  lat     lng  COOP# StnID State City/Station Name               County                     Elev      Jan 1      Jan 2      Jan 3      Jan 4      Jan 5      Jan 6      Jan 7      Jan 8      Jan 9      Jan10      Jan11      Jan12      Jan13      Jan14      Jan15      Jan16      Jan17      Jan18      Jan19      Jan20      Jan21      Jan22      Jan23      Jan24      Jan25      Jan26      Jan27      Jan28      Jan29      Jan30      Jan31'
    headers = []
    
    columnIndices = [1,7, 15, 22, 27, 34, 65, 92, 100]
    
    #Get the text headers
    for i in range(len(columnIndices)-1):
        h =  headerString[columnIndices[i]:columnIndices[i+1]-1].strip()
        headers.append(h)
    
    #create the number of day headers always assume 31, and control for months with fewer days
    for i in xrange(1,days+1):
        headers.append(str(month) + "_" + str(i).zfill(2))
    headers.append("TotalSnow")
    
    
    out_file.write(','.join(headers)+"\n")
    for index, line in enumerate(lines):
        runMe +=1
        try:
            #if the line is a digit it is a data row
            if line[1].isdigit():
                #Get the tract data
                part = []
                for i in range(len(columnIndices)-1):
                    piece =  line[columnIndices[i]:columnIndices[i+1]-1].strip()
                    #print piece + "*"
                    part.append(piece)
                    
                #get the snow data
                part2 = line[columnIndices[-1]:].split(" ")
                #clear out the empty spaces - artifact of data
                part2 = [x for x in part2 if x!='']
                #clear out the newline characters
                part2 = [x.replace('\n','')  if '\n' in x else x for x in part2]
                #change -9999's to -1's to make data smaller
                part2 = ['-1' if x=='-9999.000' else x for x in part2]
                while (len(part2) < 31):
                    part2.append('0')
                #check if there are any valid snow values in the row
                #if there are no valid values we will not keep the row
                test = [x for x in part2 if x!='-9999.000']
                test = [x for x in test if float(x)>0 ]
                test = [x for x in test if x!='-9999.000\n']
                test = [x for x in test if x!='0.000\n']

                
                #print "len of test", len(test), test
                if len(test) > 0:
                    totalSnow = 0
                    for i in part2:
                        if '\n' in i:
                            i.replace("\n", "")
                        if float(i) > 0:
                            totalSnow += float(i)
                    total =  part + part2 + [str(totalSnow)+'\n']
                    print total
                    lineString = ",".join(total)
                    out_file.write(lineString)
        except IndexError:
            continue
        #if runMe > 6:
        #    break
    out_file.close()


def cleanData(dataPath):
    f = listdir(dataPath)
    for i, file in enumerate(f):
        print i, str(file)
        M = file.split("_")[1].split(".")[0] 
        Y = file.split("_")[0]  
        #print "M", str(M), "Y", str(Y)
        processFile(dataPath + "/" + file, M, Y)