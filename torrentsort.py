import os, glob, re, shutil, difflib

# list sibling directories
directories = []
for dir in os.listdir(".."):
	if os.path.isdir(os.path.join("..",dir)):
		directories.append(dir)

# file extensions of interest
fileext = (".mp4",".avi",".srt",".mkv")

# simple method to show what's being moved
def printmovemessage(filename, foldername):
	print ("moved ", filename, " to ", foldername)

# search this directory for files
for downloadedfile in glob.glob('./**/*', recursive=True):
	samplematch = re.search(r'[sS][aA][mM][pP][lL][eE].{1,}',downloadedfile)
	# skip this file
	if downloadedfile.endswith(".py"):
		print ("jumped over snake pit successfully")
	# delete "sample" clips
	elif samplematch:
		if os.path.isfile(downloadedfile):
			printmovemessage(downloadedfile, "null")
			os.remove(downloadedfile)
	# examine non empty folders
	elif os.path.isdir(downloadedfile) and os.listdir(downloadedfile):
		for dir in directories:
			# match with siblings and pick series directories (because they may contain non recognizable files)
			if difflib.SequenceMatcher(None,downloadedfile, dir).ratio() > 0.20:
				for subfile in os.listdir(downloadedfile):
					sourcef = downloadedfile+"/"+subfile
					# only grab files of interest and delete the rest
					if subfile.endswith(tuple(fileext)):
						destd = "../"+dir
						shutil.copy(sourcef, destd)
						printmovemessage(sourcef, destd)
						os.remove(sourcef)
					else:
						printmovemessage(sourcef, "null")
						os.remove(sourcef)
				break		
	# examine files of interest
	elif downloadedfile.endswith(tuple(fileext)) and os.path.isfile(downloadedfile):
		# pick series files
		regexmatch = re.search(r'[sS][0-9]{1,2}[eE][0-9]{1,2}.{1,}',downloadedfile)
		if regexmatch:
			# if desired directory exists move the file there
			for dir in directories:
				if difflib.SequenceMatcher(None,downloadedfile, dir).ratio() > 0.5:
					dest = "../"+dir
					shutil.copy(downloadedfile, dest)
					printmovemessage(downloadedfile, dir)
					os.remove(downloadedfile)
					break
			# if desired directory doesn't exist move the file to the Unsorted directory
			if os.path.isfile(downloadedfile):
				dest = "/home/kostas/Templates/Unsorted"
				shutil.copy(downloadedfile, dest)
				printmovemessage(downloadedfile, "Unsorted")
				os.remove(downloadedfile)
			# the rest are movie related and moved to the MOVIES directory
			elif os.path.isfile(downloadedfile):
				destm = '/home/kostas/Templates/MOVIES'
				shutil.copy(downloadedfile, destm)
				printmovemessage(downloadedfile, "MOVIES")
				os.remove(downloadedfile)
	# delete unwanted files
	elif os.path.isfile(downloadedfile):
		print ("this is ", downloadedfile)
		destt = '/home/kostas/Templates/Trash'
		printmovemessage(downloadedfile, "Trash")
		shutil.move(downloadedfile, destt)

# remove empty directories
for dir in os.listdir("."):
	if os.path.isdir(dir) and not os.listdir(dir):
		try:
			printmovemessage(dir, "deleted directories")
			os.rmdir(dir)
		except OSError as ex:
			if ex.errno == errno.ENOTEMPTY:
				print (dir, " is not empty")
		
