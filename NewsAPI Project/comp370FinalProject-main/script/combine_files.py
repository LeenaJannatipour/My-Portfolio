import json
import os
import csv

def combine_json_files(file_list, output_file):
    #This function is used for combining the JSON files
    combined_articles = []

    for file_path in file_list:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                articles = data.get("articles", [])  # Extract the articles list
                combined_articles.extend(articles)
        else:
            print(f"File not found: {file_path}")

    combined_data = {
        "status": "ok",
        "totalResults": len(combined_articles),
        "articles": combined_articles
    }

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(combined_data, file, indent=4)

    print(f"Combined JSON data written to {output_file}")


def combine_csv_files(file_list, output_file):
    combined_rows = []
    headers = None  # Initialize headers as None

    for file_path in file_list:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                current_headers = next(reader, None)  # Get the headers from the current file

                if current_headers:
                    if headers is None:
                        headers = current_headers  # Set headers if not already set
                    combined_rows.extend(row for row in reader)
        else:
            print(f"File not found: {file_path}")

    if headers is None:
        raise ValueError("No valid CSV files found in the provided file list.")

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write the headers
        writer.writerows(combined_rows)

    print(f"Combined CSV data written to {output_file}")


def json_task():
    file_list = ['../data/articles1030_1102.json', '../data/articles1103_1108.json', '../data/articles1109_1114.json','../data/articles1115_1120.json','../data/articles1120_1125.json']  # Replace with your actual file paths
    output_file = '../data/all_articles.json'
    combine_json_files(file_list, output_file)

def csv_task():
    file_list = ['../data/group_annotation/article_1.csv', '../data/group_annotation/article_2.csv', '../data/group_annotation/article_3.csv', '../data/group_annotation/article_4.csv'] 
    output_file = 'all_annotated_articles.csv' 
    combine_csv_files(file_list, output_file)


if __name__ == '__main__':
    # json_task()
    csv_task() 