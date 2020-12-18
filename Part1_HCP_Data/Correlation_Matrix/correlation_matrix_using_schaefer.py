import numpy as np
import pandas as pd
from nilearn import image as nlimg
from nilearn import datasets as nldatasets
import nilearn.plotting as nlplt
from sys import argv
import os

if(len(argv)!=3):
        print('Enter Subject ID')
        os._exit(0)

from nilearn import datasets
dataset = datasets.fetch_atlas_schaefer_2018()
# dataset = datasets.fetch_atlas_harvard_oxford('sub-maxprob-thr50-1mm')
atlas_filename = dataset.maps
labels = dataset.labels

print(len(labels))

from nilearn.input_data import NiftiLabelsMasker
masker = NiftiLabelsMasker(labels_img=atlas_filename, standardize=True)

suffix=""
outputsuffix=""

if argv[2]=='1':
        suffix  = "/rfMRI_REST1_LR/rfMRI_REST1_LR_hp2000_clean.nii.gz"
        outputsuffix="/rfMRI_REST1_LR/SCHAEFER"
else:
        suffix  = "/rfMRI_REST2_LR/rfMRI_REST2_LR_hp2000_clean.nii.gz"
        outputsuffix="/rfMRI_REST2_LR/SCHAEFER"

os.system("mkdir ./"+argv[1]+"/"+outputsuffix)

file_name = str("./") + str(argv[1]) + suffix
print(file_name)

fmri_file_1 = file_name
time_series_1 = masker.fit_transform(fmri_file_1)


from nilearn.connectome import ConnectivityMeasure
from nilearn import plotting as nlplt
from copy import deepcopy

correlation_measure_1 = ConnectivityMeasure(kind='correlation')
correlation_matrix_1 = correlation_measure_1.fit_transform([time_series_1])[0]
import numpy
a = numpy.asarray(correlation_matrix_1)
print(a.shape)


# output_filename = + "_correlation_matrix.csv"
# nlplt.plot_matrix(correlation_matrix_1, figure=(10, 9), labels=labels,
                     # vmax=1.0, vmin=-1.0, reorder=True)



output_filename = "./"+argv[1] +outputsuffix +"/correlation_matrix.csv"
numpy.savetxt(output_filename, a, delimiter=",")


display=nlplt.plot_matrix(correlation_matrix_1, figure=(10, 9), labels=labels,
                     vmax=1.0, vmin=-1.0, reorder=True)

output_image = "./"+argv[1] +outputsuffix +"/correlation_matrix.png"
v1=display.get_figure()
v1.savefig(output_image)

output_labels="./"+argv[1] +outputsuffix +"/labels.txt"
f1=open(output_labels,'w')
for i in labels:
  f1.write(i.decode("utf-8") +"\n")
f1.close()
