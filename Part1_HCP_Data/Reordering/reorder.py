from sys import argv
import os


#ssh mtechproject@10.2.24.246
#ls | sort -r | grep "[0-9][0-9][0-9][0-9][0-9][0-9]$" | wc -l'
#995174 not present

curr_path = os.getcwd()

if(len(argv) != 2):
	print("Please provide subject ids list file")
	os._exit(0)

file = open(str(argv[1]), 'r')
list_ids = file.readlines()
file.close()

for idd in list_ids:
	try:
		subject_id = str(idd).strip()

		# path1=curr_path + '/' + subject_id  + '/MNINonLinear/Results/rfMRI_REST1_LR'
		# if os.path.isdir(path1):
		# 	cmd = 'mv '+ path1 +" " + curr_path + '/' + subject_id
		# 	print(cmd)
		# 	os.system(cmd)

		# path2=curr_path + '/' + subject_id  + '/MNINonLinear/Results/rfMRI_REST2_LR'
		# if os.path.isdir(path2):
		# 	cmd = 'mv '+ path2 +" " + curr_path + '/' + subject_id
		# 	print(cmd)
		# 	os.system(cmd)

		cmd = 'rm -r '+ curr_path + '/' + subject_id  + '/MNINonLinear/'
		print(cmd)
		if os.path.isdir(curr_path + '/' + subject_id  + '/MNINonLinear/'):
			os.system(cmd)
	except:
		print("Error Occurred")

