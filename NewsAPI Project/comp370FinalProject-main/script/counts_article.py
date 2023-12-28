import json

#This script is only used for testing, will delete later
def count_articles_in_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            articles = data.get("articles", [])
            return len(articles)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return 0
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file: {file_path}")
        return 0


file_path = '../data/articles1030_1102.json'
article_count = count_articles_in_json(file_path)
print(f"Number of articles in the file: {article_count}")