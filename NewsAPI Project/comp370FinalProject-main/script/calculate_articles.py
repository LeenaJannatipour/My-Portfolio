import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

def count_articles_by_movie(json_file, movie_list):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        articles = data.get('articles', [])

        article_counts = {}
        for movie in movie_list:
            count = 0
            for article in articles:
                title = article.get('title', '')
                description = article.get('description', '')

                if title and movie.lower() in title.lower():
                    count += 1
                elif description and movie.lower() in description.lower():
                    count += 1
            article_counts[movie] = count

        return article_counts


def plot_article_distribution(article_counts):
    labels = list(article_counts.keys())
    counts = list(article_counts.values())
    colors = plt.cm.viridis(np.linspace(0, 1, len(labels)))  # Generating a colormap

    fig, ax = plt.subplots()
    bars = plt.bar(labels, counts, color=colors)

    # Adding data labels on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval}', ha='center', va='bottom')

    # Set labels and title
    plt.xlabel('Movies')
    plt.ylabel('Number of Articles')
    plt.title('Article Count by Movie')

    # Format y-axis to show whole numbers only
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()



json_file = '../data/all_articles.json'
movie_list = ["The Marvels","The Hunger Games", "Napoleon","five nights at freddy's"]  # Replace with your list of movies
article_counts = count_articles_by_movie(json_file, movie_list)
plot_article_distribution(article_counts)