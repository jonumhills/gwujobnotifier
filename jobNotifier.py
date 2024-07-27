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

load_dotenv()
mongouri = os.getenv('MDB')

app = Flask(__name__)
scheduler = BackgroundScheduler()

def scrapeJobs():
    # Your job scraping logic here
    print("Running scrapeJobs...")
    try:
      print("Scraping jobs...")
      # URL of the webpage you want to scrape
      url = 'https://gwu-studentemployment.peopleadmin.com/postings/search?utf8=%E2%9C%93&query=&query_v0_posted_at_date=&1387%5B%5D=5&commit=Search'
      # Send a GET request to the URL
      response = requests.get(url)
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


              # Print the job titles and descriptions
              # if job_titles:
              #     print("Job Titles:")
              #     # for i in  range(len(job_titles)):
              #         # print(f"- {job_titles[i]}")

              # else:
              #     print("No job titles found")

              if job_descriptions:
                  # print("Job Descriptions:")
                  for job_description in job_descriptions:
                      # print(f"- {job_description}")
                      # jobs[job_description] = {"JOB TITLE":job_titles[0],
                      #                         "NO OF POS":job_titles[1],
                      #                         "DEPT":job_titles[3],
                      #                         "JOB TYPE":job_titles[4],
                      #                         "CLOSING DATE":job_titles[5]}
                      jbDict = {"Job Description": job_description, "Job Title": job_titles[0], "No of Positions": job_titles[1], "Department": job_titles[3], "Job Type": job_titles[4], "Closing Date": job_titles[5]}
                      jobs.append(jbDict)

              else:
                  print("No job descriptions found")

            
          #Get data from MongoDB
          try:
            # Create a new client and connect to the server
            client = pymongo.MongoClient(mongouri, tlsCAFile=certifi.where())
            print("Did the connection")
            print(client.list_database_names())
            db = client["jobs"]

            # Specify the collection name
            collection_name = "gwu"
            collection = db[collection_name]

            # Query the collection
            # You can use find() to get all documents or add a query filter
            # For example, to get all documents:
            documents = collection.find()

            documentsList = list(documents)
            for i in documentsList:
                jDFromMDB.append(i['Job Description'])
            # print("-----Data from MongoDB-----")
            # print(jDFromMDB)
            # print("---------------------------")
          except Exception as e:
            print(e)

      else:
          print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

      jobsJson = json.dumps(jobs)
    #   print("------Data from Website------")
    #   print(jobsJson)
    #   print("-----------------------------")
      notifyJobs = []
      for i in jobs:
         if i["Job Description"] not in jDFromMDB:
            notifyJobs.append(i)
      collection.delete_many({})
      collection.insert_many(json.loads(jobsJson))  
      if len(notifyJobs) > 0 :
         print("Notify")
         mail(notifyJobs)
      # print(type(jobs))
      # print(next(iter(jobs.items())))  # Print a newline for better readability
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
