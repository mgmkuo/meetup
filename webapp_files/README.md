**Files for running meetup hobby recommender app.**   

To run: `python run.py`   
Then, copy and paste url into browser.   


These are the core files:   
*dict_num2urlkey.json*: encoding key for hobbies   
*dict_urlkey2name.json*: key to convert meetup group url to group name   
*meetup_db_sparse.npz*: model file (table of hobbies of meetup members collected)   
*site_files/model.py*: Processes user input and finds events related to recommendations   
*site_files/extractData.py*: Calculates user-similarity and items ranking   

