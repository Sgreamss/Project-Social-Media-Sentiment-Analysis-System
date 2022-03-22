
from flask import Flask,render_template,request

import snscrape.modules.twitter as twitterScraper
import csv
import datetime

import os
from clean_predict import clean
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit')
def submitForm():
    datestart = ''
    datestartstring = ''
    datestop = ''
    datestopstring =''
    scape = request.args.get('scrape')
    # number = request.args.get('number')
    datestart = request.args.get('datestart')
    datestop = request.args.get('datestop')
    tinput = request.args.get('textinput')

    if datestart != '':
        datestartstring = " since:"+datestart
    if datestop != '':
        datestopstring = " until:"+datestop

    tweets = []
    fields = ['Review','Date','Name']

    n = int(100)
    tweetcount = 0
    inp = scape

    
    if inp.lower() =='search':
        search_input = tinput
        scraper = twitterScraper.TwitterSearchScraper(search_input+" lang:th"+datestartstring+datestopstring)
    elif inp.lower() == 'hashtag':
        hashtag_input = tinput
        scraper = twitterScraper.TwitterHashtagScraper(hashtag_input+" lang:th"+datestartstring+datestopstring)

    for i, tweet in  enumerate(scraper.get_items()):
        if i>=n :
            break
    
        tweetcount+=1
        date = datetime.datetime.strftime(tweet.date,"%Y-%d-%m %H:%M:%S+%f")
        d1 = date.split(" ")
        tweets.append([f"{tweet.content}",f"{d1[0]}",f"{tinput}"] )

    with open('static/tweets.csv','w',encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerows(tweets)
    
    if(os.path.exists('static/tweets.csv')):
        clean()
        df = pd.read_csv('static/tweets.csv')
        
        dfshow = df.head(10)
        example_list = dfshow.values.tolist()
        # palette = { c:'green' if c =='pos' else 'red' if c =='neg' else 'blue' for c in df.predict.unique()}
        # a = plt.subplots(figsize = (10,8))
        # a = df.groupby(['Month','predict'], sort=False, as_index=False).agg(count=('Month','count'))
        # sns.lineplot(data=a , x='Month', y="count", hue='predict', marker= "o" , palette=palette)
        # imagepath = os.path.join('static','image'+'.png')
        # plt.savefig(imagepath)

        palette = { c:'green' if c =='pos' else 'red' if c =='neg' else 'blue' for c in df.predict.unique()}

        month_count =  df.groupby('Month')

        if(len(list(month_count.groups.keys())) == 1) :
            a = sns.countplot(data = df, x ='Month' , hue='predict' , palette=palette)
            sns.set_theme(style="darkgrid")
            a.set(xlabel='Number of sentiment' , ylabel='Rating')
            imagepath = os.path.join('static','image'+'.png')
            plt.savefig(imagepath)
            plt.clf()
        else:
            a = plt.subplots(figsize = (20,7))
            a = sns.set_theme(style="darkgrid")
            a = df.groupby(['Month','predict'], sort=False, as_index=False).agg(Rating=('Month','count'))
            a = sns.lineplot(data=a , x='Month', y="Rating", hue='predict', marker= "o" , palette = palette)
            imagepath = os.path.join('static','image'+'.png')
            plt.savefig(imagepath)
            plt.clf()

        data = {"tweetCount":tweetcount,"image":imagepath,"exampleTweet":example_list}


    return render_template("image.html",data = data)

@app.route('/image')
def image():
    return render_template("image.html")


if __name__ == "__main__":
    app.run(debug=True)

