from nilearn import datasets

rest_dataset = datasets.fetch_development_fmri(n_subjects=5)
func_filenames = rest_dataset.func  # list of 4D nifti files for each subject

# print basic information on the dataset
print('First functional nifti image (4D) is at: %s' % rest_dataset.func[0])

from nilearn.decomposition import CanICA

canica = CanICA(n_components=20,
                memory="nilearn_cache", memory_level=2,
                verbose=10,
                mask_strategy='template',
                random_state=0)

canica.fit(func_filenames)
# Retrieve the independent components in brain space. Directly
# accesible through attribute `components_img_`.
canica_components_img = canica.components_img_
# components_img is a Nifti Image object, and can be saved to a file with
# the following line:
canica_components_img.to_filename('ica.nii.gz')
from nilearn.plotting import plot_prob_atlas
plot_prob_atlas(canica_components_img, title='All ICA components', output_file="ica_atlas.png")

from nilearn.image import iter_img
from nilearn.plotting import plot_stat_map, show

j=0
import os
os.system("mkdir ica_images")
for i, cur_img in enumerate(iter_img(canica_components_img)):
    ofile="ica_images/img_"+str(j)+".png"
    j=j+1
    plot_stat_map(cur_img, display_mode="z", title="IC %d" % i,
                  cut_coords=1, colorbar=False,output_file=ofile)


os.system("python merge_images.py ica_images/ ica")
