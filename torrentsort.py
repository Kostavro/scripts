# Current problems:
# 	1. directory matching gives false results
# Suggested solutions:
#	1. wrap in functions, so that you can fully explore directories

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

# search this directory for files and directories
for downloadedfile in glob.glob('./**/*', recursive=True):
	similardiryes = False #boolean var for 3)
	#samplematch = re.search(r'[sS][aA][mM][pP][lL][eE].{1,}',downloadedfile)
	# 1) delete "sample" directories and files
	if fnmatch.fnmatch(downloadedfile,'*sample*'):
		if os.path.isfile(downloadedfile):
			printmovemessage("sample file "+downloadedfile, "deleted")
			os.remove(downloadedfile)
		elif os.path.isdir(downloadedfile):
			printmovemessage("sample directory "+downloadedfile, "deleted")
			shutil.rmtree(downloadedfile)
	# 2) skip this file
	elif downloadedfile.endswith(".py") or downloadedfile.endswith(".sh"):
		print ("jumped over snake pit successfully")
	# 3) examine non empty folders
	elif os.path.isdir(downloadedfile) and os.listdir(downloadedfile):
		for sdir in directories:
			# match with siblings and pick series directories (because they may contain non recognizable files)
			if difflib.SequenceMatcher(None,downloadedfile, sdir).ratio() > 0.25:
				for subfile in os.listdir(downloadedfile):
					sourcef = downloadedfile+"/"+subfile
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
	# 4) examine files of interest (according to file extensions)
	elif downloadedfile.endswith(tuple(fileext)) and os.path.isfile(downloadedfile):
		# i) pick series files
		regexmatch = re.search(r'[sS][0-9]{1,2}[eE][0-9]{1,2}.{1,}',downloadedfile)
		if regexmatch:
			# a) if similarly named directory exists then move the series file there
			for sdir in directories:
				if difflib.SequenceMatcher(None,downloadedfile, sdir).ratio() > 0.2:
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
		# ii) logically, the rest files are movie related and moved to the MOVIES directory
		else:
			destm = '/home/kostas/Templates/MOVIES'
			shutil.copy(downloadedfile, destm)
			printmovemessage(downloadedfile, "MOVIES - hope it's a good one!")
			os.remove(downloadedfile)	
	# logically, everything that remains is unwanted and moved to the Trash directory
	elif os.path.isfile(downloadedfile):
		destt = '/home/kostas/Templates/Trash'
		printmovemessage(downloadedfile, "Trash - empty the trash sometime eh!")
		shutil.copy(downloadedfile, destt)
		os.remove(downloadedfile)

# remove empty directories
for sdir in os.listdir("."):
	if os.path.isdir(sdir) and not os.listdir(sdir):
		try:
			printmovemessage(sdir, "deleted directories")
			os.rmdir(sdir)
		except OSError as ex:
			if ex.errno == errno.ENOTEMPTY:
				print (sdir, " is not empty")
		
