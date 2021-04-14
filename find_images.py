import os

zips_required = set()

for f in os.listdir("image_names"):
    with open("image_names/{}".format(f)) as file:
        for l in file.readlines():
            zips_required.add((f.rstrip(".txt"), l.split("_")[0]))

for a, b in sorted(zips_required):
    print((a, b))

# for f in os.listdir("cue-conflicts"):
#     for ff in os.listdir("cue-conflicts/{}".format(f)):
#         if "airplanes" in ff:
#             os.rename("cue-conflicts/{}/{}".format(f, ff), "cue-conflicts/{}/{}".format(f, ff.replace("airplanes", "airplane")))