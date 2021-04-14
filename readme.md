### Reproduction ImageNet-trained CNNs are biased towards texture paper reproduction
This repository contains the code used in the reproduction, it builds on top of some existing functionality provided by Geirhos et al. in [this repository](https://github.com/rgeirhos/texture-vs-shape).

The code is split into two chunks, `evaluate.py` and `analyse.py`. The code requires the `probabilities_to_decision.py` and the scripts in the `helper` folder from the repository of Geirhos et al.

#### Evaluate
This script takes as input some cue-conflict images with the names having a specific format and evaluates several pretrained models on these images. The result is then stored with indications of predicted category, shape category, and texture category.

The format for the name of the images is as follows `{x}-{y}.JPEG`, the extension does not matter, the important part is that `{x}` is the shape category and `{y}` is the texture category of the image. Both `{x}` and `{y}` can have a number appended to it to distinguish images with the same shape-texture combination. 

#### Analyse
This script takes csv files resulting from `evaluate.py` and creates a figure similar to Figure 4 of the paper in Geirhos et al. 


