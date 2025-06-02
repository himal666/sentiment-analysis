import flask
from flask import request, jsonify
from textblob import TextBlob
import csv
from collections import Counter
import matplotlib.pyplot as plt
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import nltk

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta hhtp-equiv="X-UA-Compatible" content="IE=EDGE" />
    <meta name="viewport" content="width=device-xidth, initial-scale=1.0" />
    <title>SENTIMENT ANALYSIS</title>
  </head>

  <body id="body">
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Cairo&family=Neucha&family=Parisienne&family=Poppins:wght@200;300;400;500;600&family=Roboto:wght@300;400&display=swap");

      html,
      body,
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      body {
        width: 100%;
        min-height: 100vh;
        background-image: linear-gradient(
            115deg,
            rgba(58, 58, 158, 0.8),
            rgba(136, 136, 206, 0.7)
          ),
          url("https://images.pexels.com/photos/5833843/pexels-photo-5833843.jpeg?cs=srgb&dl=pexels-alphatradezone-5833843.jpg&fm=jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        font-family: "Cairo", sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 50px 0;
        color: white;
      }

      header {
        width: 100%;
        height: 180px;
        color: white;
      }

      header h1,
      header p {
        text-align: center;
      }

      h1 {
        font-size: 3rem;
      }

      header p {
        font-size: 2rem;
        margin: 0 10px;
      }

      form {
        font-size: 1.6rem;
        background: hsl(297deg 1% 3% / 39%);
        width: 80%;
        padding: 20px 35px;
        border-radius: 25px;
        margin: auto;
      }

      .input-group {
        margin-top: 20px;
      }

      input[type="text"],
      input[type="email"],
      input[type="number"],
      select {
        width: 100%;
        height: 40px;
        border-radius: 15px;
        border: none;
        padding-left: 10px;
      }

      textarea {
        resize: none;
        width: 100%;
        border-radius: 15px;
        border: none;
        padding: 10px 10px;
      }

      input[type="submit"] {
        background-color: white;
        text-align: center;
        width: 100%;
        height: 40px;
        border-radius: 15px;
        border: none;
        font-size: 1.3rem;
        transition: 0.8s;
      }

      input[type="submit"]:hover {
        background-color: rgba(136, 136, 206, 0.7);
        letter-spacing: 2px;
        color: white;
      }

      @media (max-width: 1172px) {
        header {
          margin-bottom: 10px;
        }
      }

      @media (max-width: 1066px) {
        header {
          margin-bottom: 50px;
        }
      }

      @media (max-width: 845px) {
        header p {
          height: 100px;
          display: none;
        }
      }
    </style>
    <main id="main">
      <div id="container">
        <header style="text-align: center">
          <h1 id="title">AMITY University Online</h1>
          <h1 id="description">MBA: Business Analytics</h1>

          <br /><br />
        </header>
        <h2 id="description" style="text-align: center">
          Project: Sentiment Analysis on Product Reviews
        </h2>
        <h2 id="description" style="text-align: center">
          Designed by:
          <li>Himal Asawa - A9920123009930(el)</li>
        </h2>
        <form id="survey-form" action="login">
          <input type="submit" value="Proceed Further" id="submit" />
        </form>
      </div>
    </main>
  </body>
</html>
'''

@app.route('/login', methods=['GET'])
def login():
    return '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <style>
      * {
        margin: 0;
        padding: 0;
        outline: none;
      }

      :root {
        --main-color: #fff;
        --second-color: #347deb;
        --box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
        --facebook-color: rgb(60, 90, 154);
        --google-color: rgb(220, 74, 61);
      }

      html {
        height: 100%;
      }
      body {
        background-image: linear-gradient(310deg, #df98fa, #9055ff);
        font-family: sans-serif;
      }

      #container {
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        background-color: var(--main-color);
        width: 1200px;
        height: 800px;
        border-radius: 10px;
        display: grid;
        grid-template-columns: repeat(2, 50%);
        box-shadow: var(--box-shadow);
        transition-duration: 1s;
      }

      #left,
      #right {
        margin: auto;
        width: 95%;
        height: 96%;
        border-radius: 10px;
      }

      #left {
        background-image: url("https://images.unsplash.com/photo-1615400014497-55726234cccb?crop=entropy&cs=srgb&fm=jpg&ixid=MnwxNDU4OXwwfDF8cmFuZG9tfHx8fHx8fHx8MTYxNzg4Njg0Ng&ixlib=rb-1.2.1&q=85");
        background-size: cover;
        background-position: center;
        box-shadow: var(--box-shadow);
      }
      #welcome,
      #lorem {
        margin: 20px;
        text-shadow: var(--box-shadow);
      }
      #welcome {
        font-size: 75px;
        font-weight: 300;
        margin-top: 330px;
        text-shadow: var(--box-shadow);
      }

      #login {
        padding-top: 35%;
        text-align: center;
        text-transform: uppercase;
        font-weight: 100;
        text-shadow: var(--box-shadow);
      }
      .client-info {
        display: block;
        margin: 20px auto;
        width: 60%;
        height: 50px;
        border: solid #999 1px;
        border-radius: 5px;
        text-indent: 15px;
        transition: all 200ms;
        box-shadow: var(--box-shadow);
      }
      .client-info:focus {
        width: 80%;
      }
      label {
        position: absolute;
        margin: -76px 130px;
        font-size: 12px;
        white-space: nowrap;
        background: #fff;
        padding: 0 5px;
        color: #999;
        transition: all 200ms;
        text-shadow: var(--box-shadow);
      }
      #email:focus ~ label[for="email"] {
        margin: -76px 70px;
      }
      #password:focus ~ label[for="password"] {
        margin: -76px 70px;
      }
      #submit {
        border: none;
        background-color: #9055ff;
        color: white;
        width: 60%;
      }
      #submit:hover {
        background-color: #df98fa;
      }

      .social {
        background-color: #fff;
        display: block;
        margin: 10px auto;
        width: 70%;
        height: 50px;
        border: none;
        border-radius: 5px;
        text-transform: uppercase;
        transition-duration: 200ms;
        box-shadow: var(--box-shadow);
        text-shadow: var(--box-shadow);
      }
      #facebook {
        border: solid var(--facebook-color) 1px;
        color: var(--facebook-color);
      }
      #facebook:hover {
        background-color: var(--facebook-color);
        color: white;
      }
      #google {
        border: solid var(--google-color) 1px;
        color: var(--google-color);
      }
      #google:hover {
        background-color: var(--google-color);
        color: white;
      }

      @media (max-width: 1250px) {
        #container {
          width: 600px;
          display: block;
        }
        #left {
          display: none;
        }
        #right {
          margin-top: 16px;
          background-image: url("https://images.unsplash.com/photo-1615400014497-55726234cccb?crop=entropy&cs=srgb&fm=jpg&ixid=MnwxNDU4OXwwfDF8cmFuZG9tfHx8fHx8fHx8MTYxNzg4Njg0Ng&ixlib=rb-1.2.1&q=85");
          background-size: cover;
          background-position: center;
          box-shadow: var(--box-shadow);
        }
      }

      @media (max-height: 850px) {
        #container {
          width: 1000px;
          height: 600px;
        }
        #login {
          padding-top: 20%;
        }
        #welcome {
          margin-top: 240px;
          font-size: 60px;
        }
        #lorem {
          font-size: 15px;
        }
      }
    </style>
    <div id="container">
      <div id="left">
        <h1 id="welcome">Welcome</h1>
        <p id="lorem" style="margin-right: 100px">
          Sentiment analysis is contextual mining of text which identifies and
          extracts subjective information in source material, and helping a
          business to understand the social sentiment of their brand, product or
          service while monitoring online conversations.
        </p>
      </div>
      <div id="right">
        <h1 id="login" style="padding: 100px 0px 42px 0px">
          choose the option
        </h1>
        <br />
        <a href="http://127.0.0.1:5000/Text_Sentiment">
          <input
            type="submit"
            id="submit"
            class="client-info"
            value="Text Input"
            style="font-size: larger" />
        </a>
        <a href="http://127.0.0.1:5000/review_sentiment">
          <input
            type="submit"
            id="submit"
            class="client-info"
            value="File Upload"
            style="font-size: larger" />
        </a>
      </div>
    </div>
  </body>
</html>
'''


# allow both GET and POST requests
# allow both GET and POST requests
@app.route('/Text_Sentiment', methods=['GET', 'POST'])
def Text_Sentiment():
    # handle the POST request
    if request.method == 'POST':
        language = str(request.form.get('language'))
        analysis = TextBlob(language)
        Sentiment = analysis.sentiment
        if analysis.sentiment[0]>0:
            Reaction = 'positive'
        elif analysis.sentiment[0]<0:
            Reaction =  'Negative'
        else:
            Reaction = 'Nuetral'
        return '''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Document</title>
                </head>
                <body>
                <style>
                *{
                margin: 0;
                padding: 0;
                outline: none;
                }

                :root {
                --main-color: #fff;
                --second-color: #347deb;
                --box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
                --facebook-color: rgb(60, 90, 154);
                --google-color: rgb(220, 74, 61);
                }

                html {
                height: 100%;
                }
                body {
                background-image: linear-gradient(310deg, #df98fa, #9055ff);
                font-family: sans-serif;
                }

                #container {
                position: absolute;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
                background-color: var(--main-color);
                width: 1200px;
                height: 800px;
                border-radius: 10px;
                display: grid;
                grid-template-columns: repeat(2, 50%);
                box-shadow: var(--box-shadow);
                transition-duration: 1s;
                }

                #left, #right {
                margin: auto;
                width: 95%;
                height: 96%;
                border-radius: 10px;
                }

                #left {
                background-image: url("https://images.unsplash.com/photo-1615400014497-55726234cccb?crop=entropy&cs=srgb&fm=jpg&ixid=MnwxNDU4OXwwfDF8cmFuZG9tfHx8fHx8fHx8MTYxNzg4Njg0Ng&ixlib=rb-1.2.1&q=85");
                background-size: cover;
                background-position: center;
                box-shadow: var(--box-shadow);
                }
                #welcome, #lorem {
                margin: 20px;
                text-shadow: var(--box-shadow);
                }
                #welcome {
                font-size: 75px;
                font-weight: 300;
                margin-top: 330px;
                text-shadow: var(--box-shadow);
                }

                #login {
                padding-top: 35%;
                text-align: center;
                text-transform: uppercase;
                font-weight: 100;
                text-shadow: var(--box-shadow);
                }
                .client-info {
                display: block;
                margin: 20px auto;
                width: 60%;
                height: 50px;
                border: solid #999 1px;
                border-radius: 5px;
                text-indent: 15px;
                transition: all 200ms;
                box-shadow: var(--box-shadow);
                }
                .client-info:focus {
                width: 80%;
                }
                label {
                position: absolute;
                margin: -76px 130px;
                    font-size: 12px;
                    white-space: nowrap;
                    background: #fff;
                    padding: 0 5px;
                    color: #999;
                transition: all 200ms;
                text-shadow: var(--box-shadow);
                }
                #email:focus ~ label[for="email"] {
                margin: -76px 70px;
                }
                #password:focus ~ label[for="password"] {
                margin: -76px 70px;
                }
                #submit {
                border: none;
                background-color: #9055ff;
                color: white;
                width: 60%;
                }
                #submit:hover {
                background-color: #df98fa;
                }

                .social {
                background-color: #fff;
                display: block;
                margin: 10px auto;
                width: 70%;
                height: 50px;
                border: none;
                border-radius: 5px;
                text-transform: uppercase;
                transition-duration: 200ms;
                box-shadow: var(--box-shadow);
                text-shadow: var(--box-shadow);
                }
                #facebook {
                border: solid var(--facebook-color) 1px;
                color: var(--facebook-color);
                }
                #facebook:hover {
                background-color: var(--facebook-color);
                color: white;
                }
                #google {
                border: solid var(--google-color) 1px;
                color: var(--google-color);
                }
                #google:hover {
                background-color: var(--google-color);
                color: white;
                }

                @media (max-width: 1250px) {
                
                #container {
                    width: 600px;
                    display: block;
                }
                #left {
                    display: none;
                }
                #right {
                    margin-top: 16px;
                    background-image: url("https://images.unsplash.com/photo-1615400014497-55726234cccb?crop=entropy&cs=srgb&fm=jpg&ixid=MnwxNDU4OXwwfDF8cmFuZG9tfHx8fHx8fHx8MTYxNzg4Njg0Ng&ixlib=rb-1.2.1&q=85");
                    background-size: cover;
                    background-position: center;
                    box-shadow: var(--box-shadow);
                }
                
                }

                @media (max-height: 850px) {
                
                #container {
                    width: 1000px;
                    height: 600px;
                }
                #login {
                    padding-top: 20%;
                }
                #welcome {
                    margin-top: 240px;
                    font-size: 60px;
                }
                #lorem {
                    font-size: 15px;
                }
                
                }
                </style>
                <div id="container">
                    <div id="left">
                        <h1 id="welcome">Welcome</h1>
                        <p id="lorem" style="margin-right: 100px;">
                        Sentiment analysis is contextual mining of text which identifies and extracts subjective information in source material, and helping a business to understand the social sentiment of their brand, product or service while monitoring online conversations.
                        </p>
                    </div>
                    <div id="right">
                        <form method="POST">
                            <h2 id="login">Input a text to get the Sentiment</h2><br>
                            <input id="email" class="client-info" name="language">
                            <label for="email">Sentence</label>
                            <input type="submit" id="submit" class="client-info">
                        </form>
                        <h6 class="client-info" style="text-align: center;font-size: 13px;">'''+ str(Sentiment) +'''</h6>
                        <h6 class="client-info" style="text-align: center;font-size: 16px;">'''+ str(Reaction) +'''</h6>
                    </div>
                    </div>
                    '''
                    
                
                
                
    # otherwise handle the GET request
    return '''
           <style>
                *{
                margin: 0;
                padding: 0;
                outline: none;
                }

                :root {
                --main-color: #fff;
                --second-color: #347deb;
                --box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
                --facebook-color: rgb(60, 90, 154);
                --google-color: rgb(220, 74, 61);
                }

                html {
                height: 100%;
                }
                body {
                background-image: linear-gradient(310deg, #df98fa, #9055ff);
                font-family: sans-serif;
                }

                #container {
                position: absolute;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
                background-color: var(--main-color);
                width: 1200px;
                height: 800px;
                border-radius: 10px;
                display: grid;
                grid-template-columns: repeat(2, 50%);
                box-shadow: var(--box-shadow);
                transition-duration: 1s;
                }

                #left, #right {
                margin: auto;
                width: 95%;
                height: 96%;
                border-radius: 10px;
                }

                #left {
                background-image: url("https://images.unsplash.com/photo-1615400014497-55726234cccb?crop=entropy&cs=srgb&fm=jpg&ixid=MnwxNDU4OXwwfDF8cmFuZG9tfHx8fHx8fHx8MTYxNzg4Njg0Ng&ixlib=rb-1.2.1&q=85");
                background-size: cover;
                background-position: center;
                box-shadow: var(--box-shadow);
                }
                #welcome, #lorem {
                margin: 20px;
                text-shadow: var(--box-shadow);
                }
                #welcome {
                font-size: 75px;
                font-weight: 300;
                margin-top: 330px;
                text-shadow: var(--box-shadow);
                }

                #login {
                padding-top: 35%;
                text-align: center;
                text-transform: uppercase;
                font-weight: 100;
                text-shadow: var(--box-shadow);
                }
                .client-info {
                display: block;
                margin: 20px auto;
                width: 60%;
                height: 50px;
                border: solid #999 1px;
                border-radius: 5px;
                text-indent: 15px;
                transition: all 200ms;
                box-shadow: var(--box-shadow);
                }
                .client-info:focus {
                width: 80%;
                }
                label {
                position: absolute;
                margin: -76px 130px;
                    font-size: 12px;
                    white-space: nowrap;
                    background: #fff;
                    padding: 0 5px;
                    color: #999;
                transition: all 200ms;
                text-shadow: var(--box-shadow);
                }
                #email:focus ~ label[for="email"] {
                margin: -76px 70px;
                }
                #password:focus ~ label[for="password"] {
                margin: -76px 70px;
                }
                #submit {
                border: none;
                background-color: #9055ff;
                color: white;
                width: 60%;
                }
                #submit:hover {
                background-color: #df98fa;
                }

                .social {
                background-color: #fff;
                display: block;
                margin: 10px auto;
                width: 70%;
                height: 50px;
                border: none;
                border-radius: 5px;
                text-transform: uppercase;
                transition-duration: 200ms;
                box-shadow: var(--box-shadow);
                text-shadow: var(--box-shadow);
                }
                #facebook {
                border: solid var(--facebook-color) 1px;
                color: var(--facebook-color);
                }
                #facebook:hover {
                background-color: var(--facebook-color);
                color: white;
                }
                #google {
                border: solid var(--google-color) 1px;
                color: var(--google-color);
                }
                #google:hover {
                background-color: var(--google-color);
                color: white;
                }

                @media (max-width: 1250px) {
                
                #container {
                    width: 600px;
                    display: block;
                }
                #left {
                    display: none;
                }
                #right {
                    margin-top: 16px;
                    background-image: url("https://images.unsplash.com/photo-1615400014497-55726234cccb?crop=entropy&cs=srgb&fm=jpg&ixid=MnwxNDU4OXwwfDF8cmFuZG9tfHx8fHx8fHx8MTYxNzg4Njg0Ng&ixlib=rb-1.2.1&q=85");
                    background-size: cover;
                    background-position: center;
                    box-shadow: var(--box-shadow);
                }
                
                }

                @media (max-height: 850px) {
                
                #container {
                    width: 1000px;
                    height: 600px;
                }
                #login {
                    padding-top: 20%;
                }
                #welcome {
                    margin-top: 240px;
                    font-size: 60px;
                }
                #lorem {
                    font-size: 15px;
                }
                
                }
                </style>
                <div id="container">
                <div id="left">
                    <h1 id="welcome">Welcome</h1>
                    <p id="lorem" style="margin-right: 100px;">
                    Sentiment analysis is contextual mining of text which identifies and extracts subjective information in source material, and helping a business to understand the social sentiment of their brand, product or service while monitoring online conversations.
                    </p>
                </div>
                <div id="right">
                    <form method="POST">
                        <h2 id="login">Input a text to get the Sentiment</h2><br>
                        <input id="email" class="client-info" name="language">
                        <label for="email">Sentence</label>
                        <input type="submit" id="submit" class="client-info">
                    </form>
                </div>
                </div>
           '''

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/review_sentiment', methods=['GET', 'POST'])
def review_sentiment():
    if request.method == 'POST':
        rowno = str(request.form.get('rowno'))
        file = request.files['file']
        file.save(secure_filename(file.filename))
        a = 0
        b = 0
        c = 0
        lst = []
        infile = file.filename
        Dict = []
        with open(infile, 'r') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                l = []
                rowno = int(rowno)
                sentence = row[rowno]
                analysis = TextBlob(sentence)
                print("\n",sentence)
                Sentiment = analysis.sentiment
                if analysis.sentiment[0]>0:
                    print('positive')
                    e = "positive"
                    lst.append(e)
                    a += 1
                elif analysis.sentiment[0]<0:
                    print('Negative')
                    e = "negative"
                    lst.append(e)
                    b += 1
                else:
                    print('Nuetral')
                    e = "nuetral"
                    lst.append(e)
                    c += 1
                l.append(sentence)
                l.append(e)
                l.append(Sentiment)
                l.append("<br>")
                Dict.append(l)
        print("\n Positive sentiments =",a)
        print("\n Negative sentiments =",b)
        print("\n Nuetral sentiments =",c)
        print(lst)
        w = Counter(lst)
        print(w)
        plt.figure()
        plt.bar(w.keys(),w.values())
        plt.savefig(file.filename +"_"+ str(rowno)+'.png')
        Dict = ((str(Dict)).replace("[","")).replace("]","")
        return '''<div id="container">
                <div id="left">
                    <h1 id="welcome">Output</h1>
                    <p id="lorem" style="margin-right: 100px;">'''+Dict+'''</p>
                    <p>'''+ str(lst) +'''</p>
                    <p>'''+ str(w) +'''</p>
                    <h5>File is Downloaded with name : ('''+ file.filename +"_"+ str(rowno)+'.png' +''') in your System</h5>
                </div>'''
    return '''
           <style>
                *{
                margin: 0;
                padding: 0;
                outline: none;
                }

                :root {
                --main-color: #fff;
                --second-color: #347deb;
                --box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
                --facebook-color: rgb(60, 90, 154);
                --google-color: rgb(220, 74, 61);
                }

                html {
                height: 100%;
                }
                body {
                background-image: linear-gradient(310deg, #df98fa, #9055ff);
                font-family: sans-serif;
                }

                #container {
                position: absolute;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
                background-color: var(--main-color);
                width: 1200px;
                height: 800px;
                border-radius: 10px;
                display: grid;
                grid-template-columns: repeat(2, 50%);
                box-shadow: var(--box-shadow);
                transition-duration: 1s;
                }

                #left, #right {
                margin: auto;
                width: 95%;
                height: 96%;
                border-radius: 10px;
                }

                #left {
                background-image: url("https://images.unsplash.com/photo-1615400014497-55726234cccb?crop=entropy&cs=srgb&fm=jpg&ixid=MnwxNDU4OXwwfDF8cmFuZG9tfHx8fHx8fHx8MTYxNzg4Njg0Ng&ixlib=rb-1.2.1&q=85");
                background-size: cover;
                background-position: center;
                box-shadow: var(--box-shadow);
                }
                #welcome, #lorem {
                margin: 20px;
                text-shadow: var(--box-shadow);
                }
                #welcome {
                font-size: 75px;
                font-weight: 300;
                margin-top: 330px;
                text-shadow: var(--box-shadow);
                }

                #login {
                padding-top: 35%;
                text-align: center;
                text-transform: uppercase;
                font-weight: 100;
                text-shadow: var(--box-shadow);
                }
                .client-info {
                display: block;
                margin: 20px auto;
                width: 60%;
                height: 50px;
                border: solid #999 1px;
                border-radius: 5px;
                text-indent: 15px;
                transition: all 200ms;
                box-shadow: var(--box-shadow);
                }
                .client-info:focus {
                width: 80%;
                }
                label {
                position: absolute;
                margin: -76px 130px;
                    font-size: 12px;
                    white-space: nowrap;
                    background: #fff;
                    padding: 0 5px;
                    color: #999;
                transition: all 200ms;
                text-shadow: var(--box-shadow);
                }
                #email:focus ~ label[for="email"] {
                margin: -76px 70px;
                }
                #password:focus ~ label[for="password"] {
                margin: -76px 70px;
                }
                #submit {
                border: none;
                background-color: #9055ff;
                color: white;
                width: 60%;
                }
                #submit:hover {
                background-color: #df98fa;
                }

                .social {
                background-color: #fff;
                display: block;
                margin: 10px auto;
                width: 70%;
                height: 50px;
                border: none;
                border-radius: 5px;
                text-transform: uppercase;
                transition-duration: 200ms;
                box-shadow: var(--box-shadow);
                text-shadow: var(--box-shadow);
                }
                #facebook {
                border: solid var(--facebook-color) 1px;
                color: var(--facebook-color);
                }
                #facebook:hover {
                background-color: var(--facebook-color);
                color: white;
                }
                #google {
                border: solid var(--google-color) 1px;
                color: var(--google-color);
                }
                #google:hover {
                background-color: var(--google-color);
                color: white;
                }

                @media (max-width: 1250px) {
                
                #container {
                    width: 600px;
                    display: block;
                }
                #left {
                    display: none;
                }
                #right {
                    margin-top: 16px;
                    background-image: url("https://images.unsplash.com/photo-1615400014497-55726234cccb?crop=entropy&cs=srgb&fm=jpg&ixid=MnwxNDU4OXwwfDF8cmFuZG9tfHx8fHx8fHx8MTYxNzg4Njg0Ng&ixlib=rb-1.2.1&q=85");
                    background-size: cover;
                    background-position: center;
                    box-shadow: var(--box-shadow);
                }
                
                }

                @media (max-height: 850px) {
                
                #container {
                    width: 1000px;
                    height: 600px;
                }
                #login {
                    padding-top: 20%;
                }
                #welcome {
                    margin-top: 240px;
                    font-size: 60px;
                }
                #lorem {
                    font-size: 15px;
                }
                
                }
                </style>
                <div id="container">
                <div id="left">
                    <h1 id="welcome">Welcome</h1>
                    <p id="lorem" style="margin-right: 100px;">
                    Sentiment analysis is contextual mining of text which identifies and extracts subjective information in source material, and helping a business to understand the social sentiment of their brand, product or service while monitoring online conversations.
                    </p>
                </div>
                <div id="right">
                    <form method="POST" enctype=multipart/form-data>
                        <h2 id="login">Input CSV file containing reviews</h2><br>
                        <input type="file" id="myFile" name="file" style="margin-left:95;">
                        <input id="email" class="client-info" name="rowno">
                        <label for="email">Review's column no.</label>
                        <input type="submit" id="submit" class="client-info">
                    </form>
                </div>
                </div>
           '''
app.run()