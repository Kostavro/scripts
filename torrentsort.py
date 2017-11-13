# Current problems:
# 	1. still getting some bad matching from difflib, but getting closer now
# Suggested solutions:
#	1. when moving files from ifdir function maybe call iffile function instead

import os, glob, re, shutil, difflib, fnmatch

# list sibling directories
directories = []
for sdir in os.listdir(".."):
	if os.path.isdir(os.path.join("..",sdir)):
		directories.append(sdir)

# file extensions of interest
fileext = (".mp4",".avi",".srt",".mkv")

# simple method to show what's being moved
def printmovemessage(filename, foldername):
	print ("moved ", filename, " to ", foldername)

downloads = []
# search this directory for files and directories
for downloadedfile in glob.glob('./**/*', recursive=True):
	downloads.append(downloadedfile)

# removing samples
def ifsample(downloadedfile):
	if os.path.isfile(downloadedfile):
		printmovemessage(downloadedfile, "deleted samples")
		os.remove(downloadedfile)
	elif os.path.isdir(downloadedfile):
		printmovemessage(downloadedfile, "deleted samples")
		shutil.rmtree(downloadedfile)

### MAIN ###
def ifdir(downloadeddir):
	# 1) remove sample directories
	if fnmatch.fnmatch(downloadeddir,'*sample*'):
		ifsample(downloadeddir)
	else:
		for sdir in directories:
			# match with siblings and pick series directories (because they may contain non recognizable files)
			if difflib.SequenceMatcher(None,downloadeddir, sdir).ratio() > 0.25:
				for subfile in os.listdir(downloadeddir):
					sourcef = downloadeddir+"/"+subfile
					# only grab files of interest and delete the rest
					if subfile.endswith(tuple(fileext)):
						# move these files to this directory for easier sorting
						destd = "./"
						shutil.copy(sourcef, destd)
						printmovemessage(sourcef, destd)
						os.remove(sourcef)
					else:
						if os.path.isfile(subfile):
							printmovemessage("file "+sourcef, "null")
							os.remove(sourcef)
						elif os.path.isdir(subfile):
							printmovemessage("tree "+sourcef, "null")
							shutil.rmtree(subfile)
				break	
	
def iffile(downloadedfile):
	similardiryes = False #boolean var for 3)
	# 1) remove sample files
	if fnmatch.fnmatch(downloadedfile,'*sample*'):
		ifsample(downloadedfile)
	# 2) skip scripts
	elif downloadedfile.endswith(".py") or downloadedfile.endswith(".sh"):
		print ("jumped over snake pit successfully")
	elif downloadedfile.endswith(tuple(fileext)):
		# i) pick series files
		regexmatch = re.search(r'[sS][0-9]{1,2}[eE][0-9]{1,2}.{1,}',downloadedfile)
		if regexmatch or fnmatch.fnmatch(downloadedfile, '*episode*') or fnmatch.fnmatch(downloadedfile, '*Episode*'):
			# a) if similarly named directory exists then move the series file there
			for sdir in directories:
				if difflib.SequenceMatcher(None,os.path.basename(downloadedfile), sdir).ratio() > 0.25:
					dest = "../"+sdir
					shutil.copy(downloadedfile, dest)
					printmovemessage(downloadedfile, sdir+" (because similar dirs)")
					os.remove(downloadedfile)
					similardiryes = True
					break
			# b) if similarly named directory doesn't exist move the series file to the Unsorted directory
			if not similardiryes:
				dest = "/home/kostas/Templates/Unsorted"
				shutil.copy(downloadedfile, dest)
				printmovemessage(downloadedfile, "Unsorted - sort it out later!")
				os.remove(downloadedfile)
		# ii) logically, the remaining files are movie related and moved to the MOVIES directory
		else:
			destm = '/home/kostas/Templates/MOVIES'
			shutil.copy(downloadedfile, destm)
			printmovemessage(downloadedfile, "MOVIES - hope it's a good one!")
			os.remove(downloadedfile)
	# logically, everything else is unwanted and moved to the Trash directory (safety net)
	else:
		destt = '/home/kostas/Templates/Trash'
		printmovemessage(downloadedfile, "Trash - empty the trash sometime eh!")
		shutil.copy(downloadedfile, destt)
		os.remove(downloadedfile)

### END ###

for downloadedfile in downloads:
	if os.path.isdir(downloadedfile):
		ifdir(downloadedfile)
	elif os.path.isfile(downloadedfile):
		iffile(downloadedfile)
	else:
		print ("wtf is this? ", downloadedfile)

# remove empty directories
for sdir in os.listdir("."):
	if os.path.isdir(sdir) and not os.listdir(sdir):
		try:
			printmovemessage(sdir, "deleted directories")
			shutil.rmtree(sdir)
		except OSError as ex:
			if ex.errno == errno.ENOTEMPTY:
				print (sdir, " is not empty")
		
