from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import requests
from bs4 import BeautifulSoup
import json
import pymongo
import certifi
from sendMail import mail
import os
from dotenv import load_dotenv
from flaskMail import app,send_mail
from datetime import datetime

load_dotenv()
mongouri = os.getenv('MONGO_URI')
jobLink = os.getenv('GWU_NONFWS_JOBLINK')

app = Flask(__name__)
scheduler = BackgroundScheduler()

def sendMsg(messageHtml):
   recipients = ['gwunonfwsnotifier@gmail.com']
   subject = 'New Job Posted | Non-FWS '
   html_body = 'emailTemplate.html'
   context = {
         'Jobs' : messageHtml,
         'JobLink' : jobLink,
      }
   bcc = []
   with open('emailId.txt', 'r') as file:
        for email in file:    
            bcc.append(email.strip())

      # Send email
   send_mail(subject, recipients, html_body, bcc, **context)
   print("Mails sent at: "+str(datetime.now()))
   
def scrapeJobs():
    # Your job scraping logic here
    print("Running scrapeJobs...")
    try:
      print("Scraping jobs...")
      response = requests.get(jobLink)
      jobs = []
      jobsJson = json.dumps({})
      jDFromMDB = []
      # Check if the request was successful
      if response.status_code == 200:
          # Parse the HTML content of the page with BeautifulSoup
          soup = BeautifulSoup(response.content, 'html.parser')

          # Find all elements with class 'job-item'
          job_items = soup.find_all(class_='job-item')



          # Iterate over each job item and extract information
          for job_item in job_items:
              # Find all job titles within the job item
              title_elements = job_item.find_all(class_='job-title')
              job_titles = [title_element.get_text(strip=True) for title_element in title_elements]

              # Find all job descriptions within the job item
              description_elements = job_item.find_all(class_='job-description')
              job_descriptions = [description_element.get_text(strip=True) for description_element in description_elements]


              if job_descriptions:
                  for job_description in job_descriptions:
                      jbDict = {"Job Description": job_description, "Job Title": job_titles[0], "No of Positions": job_titles[1], "Department": job_titles[3], "Job Type": job_titles[4], "Closing Date": job_titles[5]}
                      jobs.append(jbDict)

              else:
                  print("No job descriptions found")

            
          #Get data from MongoDB
          try:
            # Create a new client and connect to the server
            client = pymongo.MongoClient(mongouri, tlsCAFile=certifi.where())
            print("MongoDB connection successfull")
            # print(client.list_database_names())
            db = client["jobs"]

            # Specify the collection name
            collection_name = "gwu"
            collection = db[collection_name]

            documents = collection.find()

            documentsList = list(documents)
            for i in documentsList:
                jDFromMDB.append(i['Job Description'])
          except Exception as e:
            print(e)

      else:
          print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

      jobsJson = json.dumps(jobs)
      notifyJobs = []
      messageHtml = ''
      for i in jobs:
         #make it not in
         if i["Job Description"]  in jDFromMDB:
            notifyJobs.append(i)
      collection.delete_many({})
      collection.insert_many(json.loads(jobsJson))  
      if len(notifyJobs) > 0 :
         for job in notifyJobs:
            messageHtml = messageHtml+"<div> \
            <h2> Job Details </h2> \
            <ul> \
            <li><b>Job Title:</b> "+ job['Job Title'] + " </li> \
            <li><b>No of Positions:</b>"+ job['No of Positions'] + "</li> \
            <li><b>Department:</b>"+ job['Department'] + "</li> \
            <li><b>Job Type:</b>"+ job['Job Type'] + "</li> \
            <li><b>Closing Date:</b>"+ job['Closing Date'] + "</li>\
            <li><b>Job Description:</b>"+job['Job Description']+ "</li> \
            </ul>\
            </div>"
      sendMsg(messageHtml)

    except Exception as e:
      print("error:",e)
      print(f"Error scraping jobs: {e}")

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"})

if __name__ == '__main__':
    # Schedule scrapeJobs to run every hour
    scheduler.add_job(func=scrapeJobs, trigger="interval", minutes=1)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    app.run(host='0.0.0.0', port=5001)
