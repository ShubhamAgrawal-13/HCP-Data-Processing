
#input subject id list
import os
from sys import argv

if(len(argv) != 2):
	print("Please provide subject ids list file")
	os._exit(0)

file = open(str(argv[1]), 'r')
list_ids = file.readlines()
file.close()

for idd in list_ids:
	try:
		subject_id = str(idd).strip()
		cmd = 'python download_data.py --subject='+ subject_id +' --out_dir="."'
		print(cmd)
		print("Downloading : subject_id = ", subject_id)
		os.system(cmd)
		print("Completed : subject_id = ", subject_id)
		print("\n\n\n")
	except:
		print("Error Occurred")
