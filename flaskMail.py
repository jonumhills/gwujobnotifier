import os
from flask import Flask, render_template
from flask_mail import Mail, Message

def send_mail(subject, recipients,mailTemplate, bcc=None, **kwargs):
    with app.app_context():
        msg = Message(subject=subject,
                      sender=app.config['MAIL_USERNAME'],
                      recipients=recipients,
                      bcc=bcc)
        msg.html = render_template(mailTemplate,**kwargs)
        mail.send(msg)
app = Flask(__name__)

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')    
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

