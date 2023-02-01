##############################################################
#
# INPUT - bibles original bible corpus from Cysouw, 
# OUTPUTS - (to stdout) - all the filenames, ISO lang codes as per header (sometimes conflict w/ filename), year, and title
# OUTPUTS - to outDirectory - bibles without the header and verse info. 
# Currently it grabs the new testament only since that has wider coverage than old+new
#
##############################################################

import re,sys,glob
import pandas as pd
import glob, os, path, gzip,bz2, random
import unicodedata2

print sys.argv
input_directory = ['bibles']
outDirectory = 'parsed'
output_filename = 'bibles_parsed_info.txt'
extension ="txt"
verseStart 	= 40001001
verseEnd 	= 66022021
path = os.getcwd() #set path to current directory

#read in files
fileList = []
for dir in input_directory:
	fileList.extend(glob.glob(os.path.join(path,dir,'*'+extension)))


header = "\t".join(['filename', 'numVerses', 'proposed_language_name', 'proposed_ISO', 'year', 'script', 'title'])
print header

for curFile in fileList:
	inputfile = open(curFile,'r')
	
	outputfile = open(outDirectory+'/'+os.path.basename(curFile)[0:-4]+'_parsed.txt','w')

	allText = inputfile.readlines()
	textToWrite=[]
	someChars = []
	headerKey = headerValue = proposed_language_name = proposed_ISO = year = title = 'NA'
	for numLine,curLine in enumerate(allText):
		if '#' in curLine and numLine<12:  #probably in the header 
			curLine = re.sub('\s+', ' ', curLine)
			try:
				headerKey,headerValue = curLine.split(":")[0:2] #URLs have colons too 
			except:
				pass #can happen if there are hashtagged versenumbers in the beginning which some files have
			headerKey = re.sub('#\s', '', headerKey)
			if 'name' in headerKey and 'language' in headerKey:
				proposed_language_name = headerValue
			elif 'ISO' in headerKey:
				proposed_ISO = headerValue
			elif 'year_short' in headerKey:
				year = headerValue.split('/')[0]
				if year=='':
					year='NA'
			elif 'title' in headerKey:
				title = headerValue
			else:
				pass
		else: #we're in the body
			verseNum = verseText = ''
			try:
				verseNum,verseText = curLine.split('\t')
				unicodeVerseText = unicode(verseText,'utf-8')
				someChars.append(random.sample(unicodeVerseText,1)[0])
			except:
				pass #can happen if there's a stray newline
			try:
				verseNum = int(re.sub('#', '', verseNum))
			except:
				pass
				#print '### Integer conversion failed: ', os.path.basename(curFile), verseNum, curLine
			if verseNum >= verseStart and verseNum <= verseEnd:
				textToWrite.append(verseText)

			numVerses = len(textToWrite)

	scriptGuesses = [unicodedata2.script_cat(curChar) for curChar in someChars]
	scriptGuesses = [scriptGuess[0] for scriptGuess in scriptGuesses if scriptGuess[0]!="Common"]
	mostCommonScriptGuess = max(set(scriptGuesses), key=scriptGuesses.count)

	print "\t".join([os.path.basename(curFile)[0:-4], str(numVerses), proposed_language_name, proposed_ISO, year, mostCommonScriptGuess, "\""+title+"\""])
	
	for i in textToWrite:
		outputfile.write(i)

	inputfile.close()
	outputfile.close()
