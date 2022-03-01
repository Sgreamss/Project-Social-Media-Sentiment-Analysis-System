
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
    scape = request.args.get('scrape')
    number = request.args.get('number')
    tinput = request.args.get('textinput')

    tweets = []
    fields = ['Review','Date']

    n = int(number)
    inp = scape

    if inp.lower() == 'user':
        user_input = tinput
        scraper = twitterScraper.TwitterUserScraper(user_input,False)
    elif inp.lower() =='search':
        search_input = tinput
        scraper = twitterScraper.TwitterSearchScraper(search_input+" lang:th")
    elif inp.lower() == 'hashtag':
        hashtag_input = tinput
        scraper = twitterScraper.TwitterHashtagScraper(hashtag_input+" lang:th")

    for i, tweet in  enumerate(scraper.get_items()):
        if i>n :
            break
    
    
        date = datetime.datetime.strftime(tweet.date,"%Y-%d-%m %H:%M:%S+%f")
        d1 = date.split(" ")
        tweets.append([f"{tweet.content}",f"{d1[0]}"] )

    with open('static/tweets.csv','w',encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerows(tweets)
    
    if(os.path.exists('static/tweets.csv')):
        clean()
        df = pd.read_csv('static/tweets.csv')
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

        


    return render_template("image.html", image = imagepath)

@app.route('/image')
def image():
    return render_template("image.html")


if __name__ == "__main__":
    app.run(debug=True)

