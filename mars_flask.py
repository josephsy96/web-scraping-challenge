from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os


#Set working directory so Python 3.7.4 doesn't glitch my file (NOTE: Bobby & Nika you know what I'm talking about, lol)
os.chdir("/Users/josephyi/Documents/web-scraping-challenge/")

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017//mars_app")

@app.route('/')
def mars_index():
