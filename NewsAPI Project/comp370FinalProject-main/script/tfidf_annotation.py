import argparse
import json
import math
import pandas as pd 
from collections import Counter

def extract_content(url, articles):
    for article in articles:
        if article['url'] == url:
            content = article.get('content')
            description = article.get('description')

            combined_text = f"{description} {content}" if description and content else content or description
            return combined_text.lower().split() if combined_text else []
    return []

def compute_tfidf(article, all_articles):
    # tfidf(t, d, D) = tfidf(word, article, all_articles)
    # TF = word frequency for each annotation topic in all articles with that specific annotation
    tf = {word: count / len(article) for word,count in Counter(article).items()}

    # DF = # of articles that contain each word
    df = Counter(word for doc in all_articles for word in set(doc))
    # IDF = log(total # of articles / # of articles with this specific annotation that contain the word)
    idf = {word: math.log(len(all_articles) / df[word] + 1) for word in df}

    tfidf = {word: tf.get(word, 0) * idf[word] for word in tf}

    return tfidf

def get_top_words(tfidf_scores, n=10):
    top_words = {}
    for category, scores in tfidf_scores.items():
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]
        top_words[category] = [word for word, score in sorted_scores]
    return top_words

def tfidf_scores(input_csv, output_json):
    # Concatenate all DataFrames along the rows
    df = pd.read_csv(input_csv)
    # Extract URLs and annotations

    with open('data/all_articles.json', 'r') as json_file:
        all_articles_data = json.load(json_file)
        articles = all_articles_data.get('articles', [])

    annotations_map = {1: 'Preview and Must-Watch Lists',
                   2: 'Commercial Performance',
                   3: 'Cast and Crew Focus',
                   4: 'Studio and Production Insights',
                   5: 'Critical Reviews and Analysis',
                   6: 'Comparative Film Studies'}
    
    tfidf_scores = {annotations_map[i]: {} for i in range(1,7)}

    for i, row in df.iterrows():
        url=row['URL']
        annotation=annotations_map.get(row['Annotation'])
        text = extract_content(url, articles)
        if text and annotation:
            scores = compute_tfidf(text, [extract_content(article['url'], articles) for article in articles])
            tfidf_scores[annotation].update(scores)

    top_words = get_top_words(tfidf_scores, n=10)

    with open(output_json, 'w') as output:
        json.dump(top_words, output, indent=2)


def main():
    #python tfidf_annotation.py -i data/all_annotated_articles.csv -o tfidf_results.json
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="All Annotated Article CSV file")
    parser.add_argument("-o", "--output", required=True, help="Output JSON TFIDF Results")
    args = parser.parse_args()

    tfidf_scores(args.input, args.output)


if __name__ == "__main__":
    main()