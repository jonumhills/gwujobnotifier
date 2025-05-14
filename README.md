# GWU-JobNotifier
The GWU Job Posting Notification System is designed to streamline the process of notifying students about new job postings on the George Washington University (GWU) website. As soon as a job is posted, registered students will receive email notifications, ensuring they stay updated with the latest opportunities

# Architecture
![JobNotifierArchitecture](https://github.com/jonumhills/gwujobnotifier/blob/main/JobNotifierArchitecture.png)


#To run and deploy in Heroku
1. Fork the repository in your github and use vs code to make edits in local.
2. Create Heroku Account and buy Dynos to run a server.
3. Create a new email (preferably gmail) only for sending out job notifications.
4. Create APP Name and APP Password for the above email over https://myaccount.google.com/apppasswords, Use this app password as your SMTP password.
5. Add the created gmail and above password to MAIL_USERNAME, MAIL_PASSWORD in the env
6. Create MongoDB Database with Collection name "gwu" and with following fields
    "Job Description": string <br>
    "Job Title": string <br>
    "No of Positions": string <br> 
    "Department": string <br>
    "Job Type": string <br>
    "Closing Date": string <br>
7. Choose connection string for python driver from mongodb and add it to env MONGO_URI
8. Now deploy the gwujobnotifier folder to heroku by following https://devcenter.heroku.com/articles/getting-started-with-python#set-up


