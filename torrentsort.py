import os, glob, re, shutil, difflib

# list sibling directories
directories = []
for dir in os.listdir(".."):
	if os.path.isdir(os.path.join("..",dir)):
		directories.append(dir)

# file extensions of interest
fileext = (".mp4",".avi",".srt",".mkv", ".py")

# simple method to show what's being moved
def printmovemessage(filename, foldername):
	print ("moved ", filename, " to ", foldername)

# search this directory for files
for downloadedfile in glob.glob('./**/*', recursive=True):
	# match file extension
	if downloadedfile.endswith(tuple(fileext)) and os.path.isfile(downloadedfile):
		# skip this file
		if downloadedfile.endswith(".py"):
			print ("jumped over snake pit successfully")
		else:
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
	# avoid wrongly moving subdirectories and delete unwanted files
	elif os.path.isfile(downloadedfile):
		print ("this is ", downloadedfile)
		destt = '/home/kostas/Templates/Trash'
		shutil.move(downloadedfile, destt)

# remove empty directories
for dir in os.listdir("."):
	if os.path.isdir(dir):
		os.rmdir(dir)
