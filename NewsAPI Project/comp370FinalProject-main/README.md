# comp370FinalProject

google doc: https://docs.google.com/document/d/1pWsTaOmGaiKQVxaKho8py3PTFfjUyr12Yf6W9wDzT_I/edit?usp=sharing

overleaf (for submission): 
AAAI format 
Overleaf link https://www.overleaf.com/4663495762hyxyknsjmrqb#66384f

(with this link u can edit) ^^^

 
Approach to collect articles: 
1. Since the task requires to compare the visibility and reception relative to other movies that have 
come out at a similar time, we should choose movies that has a similar popularity and release date.
Then we use NewAPI to collect 500 hundred articles that contains movies in our movie list.

To ensure that we are not biased towards 


Scripts:
1. filter_articles: It will filtered the articles that only mentions 'The Marvels' and create another json
file for the 'The Marvels'
2. article_info_csv: It will extract the title and url of  'The Marvels ' article into a csv file, please add
the annotation at the last column 


Analysis Part:
1. We can compare the numbers of article talks about 'The Marvels' over the total number of the articles 
to cimpare the converage volume
2. We extract the articles that only talks about the 'The Marvels' for open coding and developping topics 


The Categories of the Article:
1. Preview and Must-Watch Lists
2. Commercial Performance.
3. Cast and Crew Focus
4. Studio and Production Insights
5. Critical Reviews and Analysis
6. Comparative Film Studies
7. Trailers and First Looks
8. Awards and Accolades
9. Behind-the-Scenes and Production
10. Audience Reactions and Fan Perspectives.


Note:
1. Please use article_info_csv.py after 500 articles is collected
2. note that the max articles can collected per account is 90 per day
3. Please check if the list is updated after using the collect_articles.py
