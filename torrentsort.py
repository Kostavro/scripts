#!/usr/bin/python3.6
import os, glob, re, shutil, difflib, subprocess, sys

# list sibling directories
siblingdirectories = []
for dir in os.listdir(".."):
	if os.path.isdir(os.path.join("..",dir)):
		siblingdirectories.append(dir)

# file extensions of interest
fileext = (".mp4",".avi",".srt",".mkv")

#file extensions that are going to be deleted
fileextdel = (".jpg",".nfo",".txt",".png")

# simple method to show what's being moved
def printmovemessage(filename, type, foldername):
	print ("moving ", type, " ", filename, " to ", foldername,"\n")

# method to determine if a file/folder is a series file/folder
def isitseries(filename):
	# search the filename for substring like S**E** (e.g. S01E01 - meaning Series01Episode01)
	regexmatch = re.search(r'[sS][0-9]{1,2}[eE][0-9]{1,2}.{1,}',filename)
	# remove the S**E** from the filename for better matching using the difflib library
	filenameminusseries = re.sub(r'[sS][0-9]{1,2}[eE][0-9]{1,2}.{1,}','',filename)
	# get the closest matching sibling directory name
	best_match = difflib.get_close_matches(filenameminusseries,siblingdirectories,1,0.6)
	print ('Best match is directory: ',best_match)
	for sdir in siblingdirectories:
		if best_match and regexmatch:
			itseries = 'yes'
			matched_dir = best_match[0]
		elif not best_match and regexmatch:
			itseries = 'regexmatched'
			matched_dir = 'UnsortedSeries'
		elif best_match and not regexmatch:
			itseries = 'diffmatched'
			matched_dir = 'Unsorted'
		elif not best_match and not regexmatch:
			itseries = 'no'
			matched_dir = 'MOVIES'
		else:
			itseries = 'no'
			matched_dir = 'MOVIES'
	return itseries, matched_dir

# method to determine if a file is a sample file
def isitsample(filename):
	samplematch = re.search(r'[sS][aA][mM][pP][lL][eE].{1,}',filename)
	if samplematch:
		itssample = 'yes'
	else:
		itssample = 'no'
	return itssample

# method to determine what to do with a file of interest	
def whatdowithfile(filename):
	slashes = filename.count('/')
	if slashes == 1:
		filename1, filenameE = filename.split('/')
	elif slashes == 2:
		filename1, filename2, filenameE = filename.split('/')
	elif slashes == 3:
		filename1, filename2, filename3, filenameE = filename.split('/')
	elif slashes == 4:
		filename1, filename2, filename3, filename4, filenameE = filename.split('/')
	else:
		filenameE = filename
		print ('this file has too many slashes, it won\'t match well')
	# remove weird characters and strings that we do not want for better matching
	removechars = ['.','_','WEB-DL','-','[',']',' ','720p','1080p','(',')','eason','pisode','x264','AC3','XviDVD','x265','BRRip','HDRip','WEBRip']
	for ch in removechars:
		filenameE = filenameE.replace(ch,'')
	print ('The string has been cleaned to: ',filenameE)
	# call the isitseries function
	(seriesbool, seriesdir) = isitseries(filenameE)
	# is this file a series file?
	if seriesbool == 'yes':
		dest = "../"+seriesdir
		shutil.move(filename, dest)
		printmovemessage(filenameE, "SERIES FILE", seriesdir)
		#os.remove(filename)
	# is this file a series file but no sibling directory exists?
	elif seriesbool == 'regexmatched':
		dest = "../"+seriesdir
		shutil.move(filename, dest)
		printmovemessage(filenameE, "ORPHAN SERIES FILE", "UnsortedSeries")
		#os.remove(filename)
	# is this file a series file (probably)?
	elif seriesbool == 'diffmatched':
		dest = "../"+seriesdir
		shutil.move(filename, dest)
		printmovemessage(filenameE, "PROBABLY UNSORTED SERIES FILE", "Unsorted")
		#os.remove(filename)
	# if all above fail then we have a movie file
	else:
		dest = "../"+seriesdir
		shutil.move(filename, dest)
		printmovemessage(filenameE, "MOVIES FILE", "MOVIES")
		#os.remove(filename)
	
# search this directory for files
for downloadedfile in glob.glob('./**/*', recursive=True):
	print ('\n\n************************************************************')
	print('Deciding what to do with: ',downloadedfile,'\n')
	## start decision making here ##
	# 1] skip all python files
	if downloadedfile.endswith(".py"):
		print ("jumped over snake pit successfully")
	# 2] delete "sample" clips and directories
	elif isitsample(downloadedfile) == 'yes':
		if os.path.isfile(downloadedfile):
			printmovemessage(downloadedfile, "SAMPLE FILE", "null")
			os.remove(downloadedfile)
		elif os.path.isdir(downloadedfile):
			printmovemessage(downloadedfile, "SAMPLE DIRECTORY", "null")
			shutil.rmtree(downloadedfile)
	# 3] delete files with an extension in fileextdel
	elif downloadedfile.endswith(tuple(fileextdel)) and os.path.isfile(downloadedfile):
	    destt = '../Trash'
	    printmovemessage(downloadedfile, "UNWANTED EXTENSION", "Trash")
	    shutil.move(downloadedfile, destt)
	    #os.remove(downloadedfile)
	# 4] examine files with extension of interest
	elif downloadedfile.endswith(tuple(fileext)) and os.path.isfile(downloadedfile):
		whatdowithfile(downloadedfile)
	# 5] delete empty folders
	elif os.path.isdir(downloadedfile) and not os.listdir(downloadedfile):
		printmovemessage(downloadedfile, "EMPTY FOLDER", "null")
		os.rmdir(downloadedfile)
	# 6] examine remaining directories
	elif os.path.isdir(downloadedfile) and os.listdir(downloadedfile):
		for subfile in os.listdir(downloadedfile):
			# are the subfiles empty directories?
			if os.path.isdir(subfile) and not os.listdir(subfile):
				printmovemessage(subfile, "EMPTY FOLDER", "null")
				os.rmdir(subfile)
			# are the subfiles non empty directories?
			elif os.path.isdir(subfile) and os.listdir(subfile):
				for subsubfile in os.listdir(subfile):
					# are the sub-sub files files?
					if os.path.isfile(subsubfile):
						whatdowithfile(subsubfile)
					# are the sub-sub files empty directories?
					elif os.path.isdir(subfile) and not os.listdir(subfile):
						printmovemessage(subfile, "EMPTY FOLDER", "null")
						os.rmdir(subfile)
					# are the sub-sub files non empty directories?
					elif os.path.isdir(subfile) and os.listdir(subfile):
						printmovemessage(downloadedfile, "NON EMPTY DIRECTORY", "null")
						shutil.rmtree(downloadedfile)
	# 7] move the remaining files to the Trash directories
	elif os.path.isfile(downloadedfile):
		destt = '../Trash'
		printmovemessage(downloadedfile, "REMAINING FILES", "Trash")
		shutil.move(downloadedfile, destt)
		#os.remove(downloadedfile)
	print('************************************************************')

# run the script again for deep clean
repeat = input("Would you like to run again? (y/n) ")						
if repeat == 'y':
    os.execv(sys.executable, ['python3.6'] + sys.argv)