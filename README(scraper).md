# TavernDAO-Bot-Scraper - api scrapers

Run the following command to install the required packages:
$ pip install -r requirements.txt

#Function
scrape summoners data 

#Requirements to run the scrapers:
api scraper : api key from RIOT GAMES DEVELOPER
myMMR scraper: None


#Running process:
1.The script would create a folder to store the data retrieved later.
2.The script would go on a data preprocessing process by remove duplicates of summoners names from the summoners' data into a set.
3.A set of summoners names(without duplicates) as a product of the preprocessing would be generated. 
4.The scraper would then take in the set to request data (myMMR or API) and generate the data in JSON format inside the folder that has been created in the beginning.  
    
     

#How to use? ( in terminal )
myMMR  -         python .\data_retrieval_myMMR.py {region}
riotapi -        python .\data_retrieval_LoL_{...}.py {region} {apiKEY}
