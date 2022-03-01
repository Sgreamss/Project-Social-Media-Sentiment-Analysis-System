import snscrape.modules.twitter    as twitterScraper
import json
import csv
import datetime

#write json สร้าง tweet = [] ก่อน แล้ว append data
#f = open("tweets.json","w")
#j = json.dumps(tweets)
#f.write(j)

#since:2020-07-20  return tweet newer than this date
#until:2020-07-20  return tweet older than this date
#tweet.user.username , tweet.content , tweet.date, tweet.user.location ,tweet.likeCount,tweet.retweetCount
#lang:en  near:Bangkok

tweets = []
fields = ['Review','Date']
n = int(input("Enter number of tweet to scrape: "))
inp = input("Enter scrape input: ")

if inp.lower() == 'user':
    user_input = input("Enter User name: ")
    scraper = twitterScraper.TwitterUserScraper(user_input,False)
elif inp.lower() =='search':
    search_input = input("Enter search input: ")
    scraper = twitterScraper.TwitterSearchScraper(search_input+" lang:th")
elif inp.lower() == 'hashtag':
    hashtag_input = input("Enter hashtag to search: ")
    scraper = twitterScraper.TwitterHashtagScraper(hashtag_input+" lang:th")



for i, tweet in  enumerate(scraper.get_items()):
    if i>n :
        break
    print(f"{i} content: {tweet.content} \n language: {tweet.lang} \n location: {tweet.user.location}")
    #tweets.append(f"{tweet.content} ")
    date = datetime.datetime.strftime(tweet.date,"%Y-%d-%m %H:%M:%S+%f")
    d1 = date.split(" ")
    
    tweets.append([f"{tweet.content}",f"{d1[0]}"] )


#f = open("tweets.json","w",encoding='utf8')
#j = json.dumps(tweets,ensure_ascii=False)500
#f.write(j)

with open('static/tweets.csv','w',encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    writer.writerows(tweets)




