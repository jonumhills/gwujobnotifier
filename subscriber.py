from flask import Flask, request, jsonify
import jwt
import os
import datetime
from flaskMail import app,send_mail

app = Flask(__name__)
app.config['SECRET_JWT_KEY'] = 'Nakkan_Ley_IG'
SUBSCRIBER_FILE = "subscriber.txt"

@app.route('/subscribe', methods=['POST'])
def subscribe():
    """
    Subscribe a user by adding their email to the subscriber list.
    """
    email = str(request.json.get('email'))
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    # # Generate JWT token valid for 1 hour
    # token = jwt.encode({
    #     'email': email,
    #     'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    # }, app.config['SECRET_JWT_KEY'], algorithm='HS256')
    # print(f"Generated JWT token: {token}")
    # Check if file exists and email is already subscribed

    if os.path.exists(SUBSCRIBER_FILE):
        with open(SUBSCRIBER_FILE, 'r') as file:
            existing_emails = {line.strip().lower() for line in file}
        if email in existing_emails:
            return jsonify({"message": "Email is already subscribed"}), 200
        
    with open(SUBSCRIBER_FILE, 'a') as file:
        file.write(email + '\n')
    # confirm_link = f"http://localhost:5000/confirm?token={token}"
    # subject="Subscription Confirmation"
    # recipients=[email]
    # html_body='subscribeConfirmation.html'
    # context = {
    #      'SubscribeLink' : str(confirm_link),
    #   }
    # bcc = []
    # send_mail(subject, recipients, html_body, bcc, **context)
    # print(f"Subscription email sent to {email}")

    return jsonify({"message": "Subscription successful"}), 200


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """
    Unsubscribe a user by removing their email from the subscriber list.
    """
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    email = email.strip().lower()

    if not os.path.exists(SUBSCRIBER_FILE):
        return jsonify({"error": "Subscriber list not found"}), 404

    with open(SUBSCRIBER_FILE, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    if email not in lines:
        return jsonify({"message": "Email is not subscribed"}), 200

    with open(SUBSCRIBER_FILE, 'w') as file:
        for line in lines:
            if line != email:
                file.write(line + '\n')

    return jsonify({"message": "Unsubscription successful"}), 200


@app.route('/subscribers', methods=['GET'])
def get_subscribers():
    """
    Get the list of all subscribers.
    """
    if not os.path.exists(SUBSCRIBER_FILE):
        return jsonify({"subscribers": []}), 200

    with open(SUBSCRIBER_FILE, 'r') as file:
        subscribers = [line.strip() for line in file.readlines()]

    return jsonify({"subscribers": subscribers}), 200

if __name__ == '__main__':
    app.run(debug=True)