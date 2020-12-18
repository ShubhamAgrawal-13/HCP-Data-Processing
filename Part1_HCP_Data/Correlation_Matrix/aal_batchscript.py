import os
f1=open("listdata.txt","r")
# f1=open("listsmall.txt","r")

'''
 rfMRI_REST1_LR
   rfMRI_REST1_LR_hp2000_clean.nii.gz
  rfMRI_REST2_LR
      rfMRI_REST2_LR_hp2000_clean.nii.gz
'''
lis=f1.readlines()
for i1 in lis:
	i=i1.strip()
	# print(i)
	cmd="python3 correlation_matrix_using_aal.py "+i+" 1"
	# cmd="python3 correlation_matrix_using_schaefer.py "+i+" 1"
	if  os.path.isdir(i+"/rfMRI_REST1_LR"):
		os.system(cmd)
	
	cmd="python3 correlation_matrix_using_aal.py "+i+" 2"
	# cmd="python3 correlation_matrix_using_schaefer.py "+i+" 2"
	if  os.path.isdir(i+"/rfMRI_REST2_LR"):
		os.system(cmd)
