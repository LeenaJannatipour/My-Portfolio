import matplotlib.pyplot as plt
from matplotlib import gridspec
import json

def plt_results(tfidf_results):

    fig = plt.figure(figsize=(15,8))
    spec = gridspec.GridSpec(2, 3, width_ratios=[1,1,1], height_ratios=[1,1])

    for i, (category, word_score) in enumerate(tfidf_results.items()):
        ax = plt.subplot(spec[i])

        words, scores = zip(*word_score)

        ax.barh(words, scores)


        ax.set_title(category)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    with open('data/tfidf_scores.json', 'r') as json_file:
        tfidf_results = json.load(json_file)

    plt_results(tfidf_results)
