import os.path
from PIL import Image

import os
from sys import argv

if(len(argv) != 3):
    print("Please provide subject ids list file")
    os._exit(0)
 
files = os.listdir(str(argv[1]))
output_file = ""
if(argv[2]=="dict"):
    output_file = "dict_output.png"
else:
    output_file = "ica_output.png"

image_files = []
list_temp=[]
for image in files:
    temp = image.split("_")
    temp2 = temp[1].split(".")
    list_temp.append([int(temp2[0]), image])

list_temp.sort()

for i in list_temp:
    image_files.append(argv[1] + "/" + i[1])

n_files = len(image_files)
print(image_files)
target_img = None
n_targets = 0
collage_saved = False
for n in range(n_files):
    img = Image.open(image_files[n])
    img.thumbnail((200, 200))
 
    if n % 64 == 0:
        # create an empty image for a collage
        target_img = Image.new("RGB", (1000, 800))
        n_targets += 1
        collage_saved = False
 
    # paste the image at the correct position
    i = int(n / 4)
    j = n % 4
    target_img.paste(img, (200*i, 200*j))
 
    if (n + 1) % 4 == 0 and target_img is not None:
        # save a finished 8x8 collage
        target_img.save(output_file.format(n_targets))
        collage_saved = True
 
# save the last collage

if not collage_saved:
    target_img.save(output_file.format(n_targets))
