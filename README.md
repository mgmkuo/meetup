## Code for Insight project [TrySomethingNew](http://www.trynewthings.us/):
* meetup_api_wrapper : Tool to collect member profiles off Meetup's API
* webapp_files/site_files/extractData.py : Calculates user-similarity and items ranking
* webapp_files/site_files/model.py : Processes user input; Finds events related to recommendations

## About
*TrySomethingNew* is a webapp to help users find unexpected interests on MeetUp. The goal is to help users discover new hobbies and expand their interests. The tool uses collaborative filtering to recommend activities users may not have thought of.

## Methods
Meetup member profiles were collected through Meetup's API. About 41,000 profiles were used for this project. The webapp user first enters three interests and the kinds of activities they want to explore, ranging between those similar to their interests to those very different. Next, the model calculates how similar the tool user is to every member in the database. Then, for every interest in the database, the model computes a weighted average where the weight is the user-member similarity. The model also normalizes the weighted average by the frequency the interest shows up in the database to avoid popularity biases. Finally, the model ranks the hobbies based on the weighted averages. Whereas top recommendation systems presents the user the highest ranking hobbies, this model presents 5 hobbies with rankings that correspond to the degree the user wants to explore. The model queries and scrapes Meetup's site to find upcoming activities and active groups in those interest areas.

## Packages Used
* API: urllib.request, json
* Recommendation system: numpy, pandas, scipy.sparse, beautifulsoup
