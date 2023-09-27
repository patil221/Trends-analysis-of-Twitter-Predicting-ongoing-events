from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import sys
import tweepy
import json
from table import *
from PIL import ImageTk,Image
import matplotlib.pyplot as plt
from textblob import TextBlob 
import re 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="pass",
  database="twitterDb"
)
class TrendAnalysisClassTextBlob():
    def __init__(self , master):
        self.master = master
         
        
        master.configure(background='white')
        master.geometry("%dx%d+0+0" % (700, 600))
        #master.geometry("700x600")        
        #master.resizable(0, 0)
        
        #==============================FRAMES=========================================

        Form = Frame(master,highlightbackground="black", highlightcolor="black", highlightthickness=2,height=600, width=700)
        Form.configure(bg="white")
        Form.pack(side=TOP)
        
        label = Label(Form,bg="white")
        label.grid(row=0)
        image = ImageTk.PhotoImage(Image.open("welcome2.jpg"))
        label.config(image = image)
        label.image = image
   
        self.lbl_Trend_Name = Label(Form,bg="white",fg="Red", text = "Analysis of Trend", font=('arial', 14))
        self.lbl_Trend_Name.grid(row=3)
        
        self.table_Tweets = Table(Form, ["Tweet No", "Tweet Text","Score","Polarity"], column_minwidths=[None, None, None, None])
        self.table_Tweets.grid(row=4,padx=10)
        
        self.btn_Home = Button(Form, bg="green",fg="white", text=" Exit ", width=35, command=self.backtoHome)
        self.btn_Home.grid(row=7,pady=10)
        
        
        
        trend_name=""
        with open('temp.txt') as f:
             for line in f:
                        trend_name=line
             self.lbl_Trend_Name['text']="Analysis of Trend: "+trend_name       
         
        #Autentication
        consumer_key = '7NoaT2HJ7FLe1Pqk7pCYmsxMN'
        consumer_secret = 'vKAV1o8b37V0bWVthV0Co95BeQStkUTPKfmAupA0ua8ttDNANR'
        access_token = '767678312693002241-qUKuqor9lDJjcQLrlXzstGXArMV0Rx9'
        access_token_secret = 'A4ViIm2crVp9DDivvxVcg6VIRGbUqMmeCyjbH94DHVxqR'

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        cnt=1
        index=0
        T = [[]]
        posCount=0
        negCount=0
        for tweet in tweepy.Cursor(api.search,q=trend_name,
                           lang="en").items(7):
            tweet_text=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())                
            
            
            analysis = TextBlob(tweet_text) 
            polarity="Negative"
            if analysis.sentiment.polarity > 0: 
               polarity="Positive"
               posCount+=1               
            elif analysis.sentiment.polarity == 0: 
               polarity="Neutral"
               #print('Neutral')
            else: 
               negCount+=1
            
            T.insert(index,[cnt,tweet_text,analysis.sentiment.polarity,polarity])
            index=index+1
            cnt=cnt+1
            
        
        self.table_Tweets.set_data(T)
        labels = 'Positive', 'Negative'
        sizes = [posCount, negCount]
        explode = (0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()
        
    def backtoHome(self):
            self.master.withdraw()    