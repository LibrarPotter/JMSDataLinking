#Working!
#access each article individually
#intakes fulltext, strips the XML tags, uses RE to find links and text before the links, writes a file 
#with link text and the text before the links, keeping the Vol# and Article filename with the link.
#vol223 is the first one we are intersted in

import os
from lxml import etree
from io import StringIO, BytesIO
import re
import csv
import Tkinter
import tkFileDialog

#choose folder where data is located
root = Tkinter.Tk()
root.withdraw()
mainPath = tkFileDialog.askdirectory(parent = root)
print mainPath

#select file to save CSV output to

csvOutput = tkFileDialog.asksaveasfilename()
print csvOutput

#realmainPath = "C:\Users\Megan\Documents\LibDataResearch\IouliProject\Volumes"
#mainPath = "C:\Users\Megan\Desktop\\Test\\Nest" #main test file
#csvOutput = "C:\Users\Megan\Desktop\\test\\test.csv"


openFile = open(csvOutput, "wb")
wr = csv.writer(openFile)
wr.writerow(["article","volume","pre_link_text","link_text"]) #writes the heading row. Must be outside loop.

#print mainPath
listOfVolumes = os.listdir(mainPath)


#This allows you to loop through each volume folder
for vol in listOfVolumes:
    path = mainPath+"/"+vol 
    #print path
    articles = os.listdir(path)
    for article in articles: #access each article
        #print path
        filePath = path+"/"+article #use this to open each file
        print vol
        print article
        print filePath
        
        try:
            #remove XML tags leaving only text
            tree = etree.parse(filePath)
            justText = etree.tostring(tree, encoding='utf8', method='text')
            #print(justText)   
            
            print "Before RegEx"
            justLinks = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', justText)
            toGetNewLines = re.compile('.{,250}http', re.DOTALL)
            preLinks = re.findall(toGetNewLines, justText) #grabs 250 characters before link
            print "After RegEx"
            #print preLinks
            tupleList = zip(preLinks, justLinks) #zips lists together to allow for double iteration
            for linkText in tupleList:
                #print vol
                #print article
                print linkText
                print len(linkText)
                print "each link"
                #this is used to remove litteral \t and \n which works because this code is written in Jupyter
                t1 = re.compile("([^/\n+|/\t+])") #use negatives to return everything except \n and \t up to 250 characters from the right side of the string
                t2 = re.findall(t1, linkText[0])
                print t2
                print len(t2)
                s = "";                
                textForTest = s.join(t2)
                print textForTest
            
                try:
                    #wr.writerow([article, vol, linkText[0], linkText[1]])
                    wr.writerow([article, vol, textForTest, linkText[1]])
                except:
                    print "Error writing to doc.csv"
                    
        #if there's an error parsing the XML, skip all the steps and this will be printed instead
        except:
            print "Error parsing XML on article: "+article
            print "Article: "+article+" has been skipped"
            pass
        
            
    print "Next Volume!"

    
openFile.close()
