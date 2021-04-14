import torch
from PIL import Image
from torchvision import transforms
import os
from probabilities_to_decision import ImageNetProbabilitiesTo16ClassesMapping
import csv

models = ['alexnet', 'googlenet', 'vgg16', 'resnet50']
def evaluate(directory):
    for model_name in models:
        model = torch.hub.load('pytorch/vision:v0.9.0', model_name, pretrained=True)
        model.eval()

        with open('results/{}.csv'.format(model.__class__.__name__), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["subj", "trial", "object_response", "shape", "texture", "imagename"])
            trial = 1
            for cat in sorted(os.listdir(directory)):
                for filename in sorted(os.listdir("{}/{}".format(directory, cat))):
                    input_image = Image.open("{}/{}/{}".format(directory, cat, filename))
                    preprocess = transforms.Compose([
                        transforms.Resize(256),
                        transforms.CenterCrop(224),
                        transforms.ToTensor(),
                        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                    ])
                    input_tensor = preprocess(input_image)
                    input_batch = input_tensor.unsqueeze(0)

                    output = model(input_batch)

                    mapping = ImageNetProbabilitiesTo16ClassesMapping()

                    probabilities = torch.softmax(output, 1)
                    dec = mapping.probabilities_to_decision(probabilities.detach().numpy().flatten())
                    writer.writerow([model.__class__.__name__, trial, dec, cat, filename.split("-")[1].split(".")[0].rstrip('1234567890.'), filename])
                    trial += 1


if __name__ == '__main__':
    evaluate("cue-conflicts")
