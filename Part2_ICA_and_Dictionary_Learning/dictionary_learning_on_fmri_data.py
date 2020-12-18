from nilearn import datasets

rest_dataset = datasets.fetch_development_fmri(n_subjects=5)
func_filenames = rest_dataset.func  # list of 4D nifti files for each subject

# print basic information on the dataset
print('First functional nifti image (4D) is at: %s' % rest_dataset.func[0])

from nilearn.decomposition import DictLearning
dict_learning = DictLearning(n_components=20,
                             memory="nilearn_cache", memory_level=2,
                             verbose=1,
                             random_state=0,
                             n_epochs=1,
                             mask_strategy='template')

print('[Example] Fitting dicitonary learning model')
dict_learning.fit(func_filenames)
print('[Example] Saving results')
# Grab extracted components umasked back to Nifti image.
# Note: For older versions, less than 0.4.1. components_img_
# is not implemented. See Note section above for details.
dictlearning_components_img = dict_learning.components_img_
dictlearning_components_img.to_filename('dict_learning.nii.gz')

from nilearn.plotting import plot_prob_atlas
plot_prob_atlas(dictlearning_components_img,
                title='All DictLearning components', output_file="dict_learning_atlas.png")

from nilearn.image import iter_img
from nilearn.plotting import plot_stat_map, show

j=0
import os
os.system("mkdir dict_learning_images")

for i, cur_img in enumerate(iter_img(dictlearning_components_img)):
	ofile="dict_learning_images/img_"+str(j)+".png"
	j=j+1
	plot_stat_map(cur_img, display_mode="z", title="Comp %d" % i,
                  cut_coords=1, colorbar=False, output_file=ofile)


os.system("python merge_images.py dict_learning_images/ dict")
