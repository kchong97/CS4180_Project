import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


# Parse results
def analyse():
    for model in models:
        correct = 0
        incorrect = 0
        shape = 0
        texture = 0
        frequencies = {}

        if model == "Human":
            for human_result in os.listdir("results/human"):
                with open("results/human/{}".format(human_result)) as file:
                    file.readline()

                    for line in file.readlines():
                        data = line.split(",")
                        # Check if correct prediction for texture/shape
                        tex = data[7].split("-")[1].split(".")[0].rstrip('1234567890.')
                        if data[4] == data[5] or data[4] == tex:
                            correct += 1
                        else:
                            incorrect += 1

                        # Find the frequency of texture vs shape decisions, but only if shape != texture
                        if data[5] != tex:
                            if data[4] == data[5]:
                                if data[4] not in frequencies:
                                    frequencies[data[4]] = (0, 0)
                                frequencies[data[4]] = (frequencies[data[4]][0] + 1, frequencies[data[4]][1])
                                shape += 1
                            elif data[4] == tex:
                                if data[4] not in frequencies:
                                    frequencies[data[4]] = (0, 0)
                                frequencies[data[4]] = (frequencies[data[4]][0], frequencies[data[4]][1] + 1)
                                texture += 1
        else:
            with open('results/{}.csv'.format(model)) as file:
                # Skip header
                file.readline()
                for line in file.readlines():
                    data = line.split(",")
                    # Check if correct prediction for texture/shape
                    if data[2] == data[3] or data[2] == data[4]:
                        correct += 1
                    else:
                        incorrect += 1

                    # Find the frequency of texture vs shape decisions, but only if shape != texture
                    if data[3] != data[4]:
                        if data[2] == data[3]:
                            if data[2] not in frequencies:
                                frequencies[data[2]] = (0, 0)
                            frequencies[data[2]] = (frequencies[data[2]][0] + 1, frequencies[data[2]][1])
                            shape += 1
                        elif data[2] == data[4]:
                            if data[2] not in frequencies:
                                frequencies[data[2]] = (0, 0)
                            frequencies[data[2]] = (frequencies[data[2]][0], frequencies[data[2]][1] + 1)
                            texture += 1

        results[model] = {"correct": correct, "incorrect": incorrect, "shape": shape, "texture": texture, "ratio": frequencies}

def histograms():
    for model in results:
        for key, val in results[model]["ratio"].items():
            if key not in histogram_results:
                histogram_results[key] = {}
            histogram_results[key][model] = val[0] + val[1]
            if model == "Human":
                histogram_results[key][model] /= len(os.listdir("results/human"))
    for key in histogram_results:
        x = range(len(models))
        y = []
        col = []
        for model in models:
            if model not in histogram_results[key]:
                y.append(0)
            else:
                y.append(histogram_results[key][model])
            col.append(colors[model])
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
	# Replace limit with amount of images of a specific category
        plt.xlim(0, 600)
        plt.barh(x, width=y, color=col, height=1)
        plt.savefig("histograms/{}.png".format(key), bbox_inches='tight')
        plt.close()

# Plot results
def plot():
    plt.figure(figsize=(14, 14))
    for model in results:
        x = []
        y = []
        total_ratio = 0
        for key, val in results[model]["ratio"].items():
            x.append(val[1] / (val[0] + val[1]))
            y.append(cats.index(key))
            total_ratio += val[1] / (val[0] + val[1])
        plt.vlines(total_ratio / 16, -1, 16, linestyles='solid', colors=colors[model], linewidth=3, zorder=-10)
        plt.plot(x, y, markers[model], clip_on=False, markersize=20 - (models.index(model)), zorder=models.index(model), color=colors[model])

    # Plot other stuff
    plt.xlim(0, 1.0)
    plt.ylim(-0.5, 15.5)
    plt.yticks(range(16), [0 for _ in range(16)], rotation=0, fontsize=18)
    plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], fontsize=18)
    plt.hlines([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5], 0, 1, linestyles="dashed")
    plt.text(0.5, -2, 'Fraction of \'texture\' decisions', fontsize=20, ha='center', va='center')
    plt.annotate('', xy=(1, -1.5), xytext=(0, -1.5), ha='center', va='center', arrowprops={'width': 2}, annotation_clip=False, size=20)
    plt.text(0.5, 17, 'Fraction of \'shape\' decisions', fontsize=20, ha='center', va='center')
    plt.annotate('', xy=(0, 16.5), xytext=(1, 16.5), ha='center', va='center', arrowprops={'width': 2}, annotation_clip=False, size=20)
    plt.ylabel('Shape categories', fontsize=20, ha='center', va='center', labelpad=80)
    ax = plt.gca()
    ax.axes.yaxis.set_ticks([])
    ax.tick_params(length=15, width=2)

    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    for tick in ax2.yaxis.get_major_ticks():
        tick.label.set_fontsize(18)
    ax2.set_xticklabels(reversed([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]), fontsize=18)
    ax2.tick_params(length=15, width=2)

    for key in histogram_results:
        img = mpimg.imread('histograms/{}.png'.format(key))
        imagebox = OffsetImage(img, zoom=0.1)
        ab = AnnotationBbox(imagebox, (1.05, cats.index(key)), annotation_clip=False)
        ax.add_artist(ab)

        img2 = mpimg.imread('category/{}.png'.format(key))
        imagebox2 = OffsetImage(img2, zoom=0.3)
        ab2 = AnnotationBbox(imagebox2, (-0.04, cats.index(key)), annotation_clip=False)
        ax.add_artist(ab2)

    plt.savefig("final_figure.png")
    plt.show()


if __name__ == '__main__':
    results = {}
    histogram_results = {}
    # models = ["Human", "ResNet", "VGG", "GoogLeNet", "AlexNet"]
    models = ["ResNet", "VGG", "GoogLeNet", "AlexNet"]
    cats = ["bicycle", "clock", "chair", "bottle", "truck", "car", "bird", "oven", "elephant", "cat", "keyboard", "dog",
            "bear", "airplane", "knife", "boat"]
    markers = {"VGG": '^', "ResNet": 's', "GoogLeNet": 'o', "AlexNet": 'D', "Human": 'o'}
    colors = {"VGG": 'blue', "ResNet": 'grey', "GoogLeNet": 'turquoise', "AlexNet": 'purple', "Human": 'red'}

    analyse()
    histograms()
    plot()
