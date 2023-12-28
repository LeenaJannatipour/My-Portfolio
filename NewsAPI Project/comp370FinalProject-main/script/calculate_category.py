import csv
import os
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np


import csv
import matplotlib.pyplot as plt
from collections import Counter

def count_articles_by_category(csv_file):
    # Updated mapping of annotation numbers to category names
    category_map = {
        '1': 'Previews, Trailers, and Must-Watch Lists',
        '2': 'Commercial Performance',
        '3': 'Cast and Crew Focus',
        '4': 'Studio and Production Insights',
        '5': 'Critical Reviews and Analysis',
        '6': 'Comparative Film Studies',
        '7': 'Previews, Trailers, and Must-Watch Lists',
        '0': 'Spam Streaming Link',
        '8': 'Irrelevant'
    }

    combined_categories = Counter()

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            annotation = row['Annotation']
            category = category_map.get(annotation, 'Unknown')
            combined_categories[category] += 1

    # Combine counts for categories 1 and 7
    if 'Previews, Trailers, and Must-Watch Lists' in combined_categories:
        combined_categories['Previews, Trailers, and Must-Watch Lists'] /= 2

    return combined_categories

def plot_category_distribution(category_counts):
    categories = list(category_counts.keys())
    counts = list(category_counts.values())

    # Generating a color map with a unique color for each bar
    colormap = ListedColormap(plt.cm.get_cmap('tab10').colors)
    colors = colormap.colors[:len(categories)]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, counts, color=colors)

    # Adding the count above each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval}', ha='center', va='bottom')

    plt.xlabel('Categories')
    plt.ylabel('Number of Articles')
    plt.title('Article Distribution by Category')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def process_data_for_proportions(csv_file, target_movie):
    # Updated mapping of annotation numbers to category names
    category_map = {
        '1': 'Previews, Trailers, and Must-Watch Lists',
        '2': 'Commercial Performance',
        '3': 'Cast and Crew Focus',
        '4': 'Studio and Production Insights',
        '5': 'Critical Reviews and Analysis',
        '6': 'Comparative Film Studies',
        '7': 'Previews, Trailers, and Must-Watch Lists',
        '0': 'Irrelevant',
        '8': 'Spam Streaming Link'
    }

    # Define the order of categories
    ordered_categories = [
        'Previews, Trailers, and Must-Watch Lists',
        'Commercial Performance',
        'Cast and Crew Focus',
        'Studio and Production Insights',
        'Critical Reviews and Analysis',
        'Comparative Film Studies',
        'Irrelevant',
        'Spam Streaming Link'
    ]

    category_counts = {category: {'target': 0, 'others': 0} for category in ordered_categories}
    total_counts = {'target': 0, 'others': 0}

    # Process the CSV file
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            annotation = row['Annotation']
            category = category_map.get(annotation, 'Unknown')
            if category not in category_counts:
                continue

            if target_movie.lower() in row['Title'].lower():
                category_counts[category]['target'] += 1
                total_counts['target'] += 1
            else:
                category_counts[category]['others'] += 1
                total_counts['others'] += 1

    # Calculate proportions
    proportions = {
        category: {
            'target': category_counts[category]['target'] / total_counts['target'] if total_counts['target'] > 0 else 0,
            'others': category_counts[category]['others'] / total_counts['others'] if total_counts['others'] > 0 else 0
        } for category in ordered_categories if category in category_counts
    }

    return proportions, ordered_categories

def plot_proportions(proportions, categories):
    target_props = [proportions[cat]['target'] for cat in categories]
    others_props = [proportions[cat]['others'] for cat in categories]

    x = np.arange(len(categories))  # Label locations
    width = 0.35  # Width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, target_props, width, label='Target Movie')
    rects2 = ax.bar(x + width/2, others_props, width, label='Other Movies')

    
    def add_bar_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    add_bar_labels(rects1)
    add_bar_labels(rects2)

    ax.set_ylabel('Proportions')
    ax.set_title('Proportions of Articles by Category')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha="right")
    ax.legend()

    plt.tight_layout()
    plt.show()


def process_data_for_proportions_2(csv_file, movie_list):
    category_map = {
        '1': 'Previews, Trailers, and Must-Watch Lists',
        '2': 'Commercial Performance',
        '3': 'Cast and Crew Focus',
        '4': 'Studio and Production Insights',
        '5': 'Critical Reviews and Analysis',
        '6': 'Comparative Film Studies',
        '7': 'Previews, Trailers, and Must-Watch Lists',
        '0': 'Irrelevant',
        '8': 'Spam Streaming Link'
    }

    # Define the order of categories
    ordered_categories = [
        'Previews, Trailers, and Must-Watch Lists',
        'Commercial Performance',
        'Cast and Crew Focus',
        'Studio and Production Insights',
        'Critical Reviews and Analysis',
        'Comparative Film Studies',
        'Irrelevant',
        'Spam Streaming Link'
    ]
    category_counts = {category: {movie: 0 for movie in movie_list} for category in ordered_categories}
    total_counts = {movie: 0 for movie in movie_list}

    # Process the CSV file
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            annotation = row['Annotation']
            category = category_map.get(annotation, 'Unknown')
            if category not in category_counts:
                continue

            for movie in movie_list:
                if movie.lower() in row['Title'].lower():
                    category_counts[category][movie] += 1
                    total_counts[movie] += 1
                    break  # Assume each article belongs to one movie only

    # Calculate proportions
    proportions = {category: {movie: category_counts[category][movie] / total_counts[movie] if total_counts[movie] > 0 else 0 for movie in movie_list} for category in ordered_categories}

    return proportions, ordered_categories


def plot_proportions_2(proportions, categories, target_movie, other_movies):
    x = np.arange(len(categories))  # Label locations
    width = 0.35  # Width of the bars

    for other_movie in other_movies:
        target_props = [proportions[cat][target_movie] for cat in categories]
        other_props = [proportions[cat][other_movie] for cat in categories]

        # Create a new figure for each comparison plot
        fig, ax = plt.subplots(figsize=(10, 6))

        rects1 = ax.bar(x - width/2, target_props, width, label=target_movie)
        rects2 = ax.bar(x + width/2, other_props, width, label=other_movie)

        # Add labels and title
        ax.set_ylabel('Proportions')
        ax.set_title(f'{target_movie} vs {other_movie}')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha="right")
        ax.legend()

        # Add bar labels
        def add_bar_labels(bars):
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.2f}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        add_bar_labels(rects1)
        add_bar_labels(rects2)

        plt.tight_layout()
        plt.show()

def plot_2():
    csv_file = '../data/all_annotated_articles.csv'
    target_movie = 'The Marvels'
    proportions, categories = process_data_for_proportions(csv_file, target_movie)
    plot_proportions(proportions, categories)

def plot_3():
    csv_file = '../data/all_annotated_articles.csv'
    target_movie = 'The Marvels'
    other_movies = ["The Hunger Games", "Napoleon","five nights at freddy's"]
    proportions, categories = process_data_for_proportions_2(csv_file, [target_movie] + other_movies)
    plot_proportions_2(proportions, categories, target_movie, other_movies)


if __name__ == '__main__':
    # plot_2()
    plot_3()

