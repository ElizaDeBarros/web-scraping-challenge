# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# stablish a mongo connection
mongo = PyMongo(app, uri='mongodb://localhost:27017/mars.app')

# create route that renders index.html template
@app.route("/")
def index():
    # find one record of data from the mongo db
    mars_collection = mongo.db.mars_collection.find_one()
    return render_template("index.html", mars_collection=mars_collection)


# create router that imports scrape_mars.py and calls the scrape function
@app.route("/scrape")
def scrape():
    
    # Pull data from dictionary created by scrape_mars.py
    mars_data = scrape_mars.scrape()
    
    # Update the collection with most recent data
    mars_collection = mongo.db.mars_collection
    mars_collection.update({}, mars_data, upsert=True)
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)
