import json
import csv
import os

"""
This script is used for dividing the articles into 4 csv file for each group mumber to annotate
"""
def create_csv_files_from_json(json_file, output_directory, csv_filenames, articles_per_file=125):
    # Load articles from the JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        articles = data.get('articles', [])

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Check if the number of CSV filenames is sufficient
    if len(csv_filenames) < 4:
        raise ValueError("Insufficient number of CSV filenames provided.")

    # Divide articles into groups of 50 and create CSV files
    for i, csv_filename in enumerate(csv_filenames[:4]):  # Limit to first four filenames
        group_articles = articles[i * articles_per_file:(i + 1) * articles_per_file]
        csv_file_path = os.path.join(output_directory, csv_filename)

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Source', 'Title', 'URL', 'Annotation'])

            for article in group_articles:
                source_name = article['source']['name']
                title = article['title']
                url = article['url']
                annotation = ''  # Initially empty
                writer.writerow([source_name, title, url, annotation])

        print(f"Articles group {i + 1} written to {csv_file_path}")


json_file = '../data/all_articles.json'  # Replace with the path to your JSON file
output_directory = '../data/group_annotation'  # Replace with your desired output directory
csv_filenames = ['article_1.csv', 'article_2.csv', 'article_3.csv', 'article_4.csv']  # List of CSV filenames
create_csv_files_from_json(json_file, output_directory, csv_filenames)