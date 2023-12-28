from newsapi import NewsApiClient
import json
import os

API_KEY ="7b595b26853642c4a2cecb2fe18224a6" 
MOVIES = ["The Marvels","The Hunger Games", "Napoleon","five nights at freddy's"]
# Create a query string with 'OR' between movie titles
MOVIES_QUERY_STRING = " OR ".join([f'"{movie}"' for movie in MOVIES])

def get_file_path(file_name, directory):
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file_name)
    return file_path

def collect_news():
    newsapi = NewsApiClient(api_key=API_KEY)
    
    # /v2/everything
    articles= newsapi.get_everything(q=MOVIES_QUERY_STRING,
                                      from_param='2023-11-21',
                                      to='2023-11-26',
                                      language='en',
                                      sort_by='relevancy')
    
    
    file_name = 'articles.json'

    # Write the array to a JSON file
    with open(file_name, 'w') as json_file:
        json.dump(articles, json_file)

    print(f'The array has been stored in {file_name}')
    return articles

        
if __name__ == '__main__':
    collect_news()
    




