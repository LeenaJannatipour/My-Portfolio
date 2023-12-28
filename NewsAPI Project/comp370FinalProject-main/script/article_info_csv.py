import json
import csv
from collect_news import get_file_path


#The funciton create a csv file that cotain the title and description for annotation
def info_csv(json_file, csv_file):
    directory = '../data'
    json_file_path = get_file_path(json_file,directory)
    csv_file_path = get_file_path(csv_file,directory)

    with open(json_file_path, 'r',encoding='utf-8') as file:
        articles = json.load(file)
    
    with open(csv_file_path,'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # writer.writerow(['Source','Title','Description', 'Published At', 'Annotation'])
        writer.writerow(['Source','Title','url', 'Annotation'])

        for article in articles:
            source_name = article['source']['name']
            title = article['title']
            # description = article['description']
            # published_at = article['publishedAt']
            url = article['url']
            annotation = ''
            writer.writerow([source_name, title, url, annotation])


    print(f"Data for annotation has been written to {csv_file}")
