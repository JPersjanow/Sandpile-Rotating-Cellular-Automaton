import imageio
import os

filenames = os.listdir("animation")
filenames_sorted = sorted(filenames, key=lambda x: int(x.split("_")[0]))
print(filenames_sorted)
filenamse_dir = []
for i in filenames_sorted:
    filenamse_dir.append("animation\\" + i)

print(filenamse_dir)

with imageio.get_writer('animation\\sandpile.gif', mode='I') as writer:
    for filename in filenamse_dir:
        image = imageio.imread(filename)
        writer.append_data(image)