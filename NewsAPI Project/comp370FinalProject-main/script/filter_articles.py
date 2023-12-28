import json
import os
from collect_one_week import get_file_path

#The function will create a json file that only has articles about target film
def filter_articles(input_file, output_file, movie_title):

    directory = '../data'
    input_file_path = os.path.join(directory, input_file)
    output_file_path = os.path.join(directory, output_file)

    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        articles = data.get('articles', []) 

    filtered_articles = [article for article in articles if movie_title.lower() in article.get('title', '').lower()]

    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(filtered_articles, file, ensure_ascii=False, indent=4)

    print(f"Filtered {len(filtered_articles)} articles about '{movie_title}' into {output_file}")

filter_articles('all_articles.json', 'the_marvels_articles.json', 'The Marvels')