

from flask import Flask
import os
from twilio.rest import Client
from dotenv import load_dotenv

from google.cloud import firestore

#test change
# load env variables from .env file
load_dotenv() 
# connect db
db = firestore.Client(project='clean-house-337521')

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World! '

@app.route('/yes')
def confirm():
    # do something in the db

    # return thank you
    return 'Thank you for doing the task'

@app.route('/no')
def no():
    # mark in db

    return 'Well go do it'

@app.route('/adduser')
def adduser():
    doc_ref = db.collection(u'users').document(u'larswiersholm')
    doc_ref.set({
        u'first': u'Lars',
        u'last': u'Wiersholm',
        u'born': 1992
    })
    return "201"


@app.route('/reset')
def reset():
    doc_ref = db.collection(u'users').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })
    return "200"

@app.route('/run_reminders')
def run_reminders():
    # this is what the cron hits to kick off reminders

    # figure out what reminders we need to send by checking db
    users_ref = db.collection(u'users')
    docs = users_ref.stream()

    print('users: ')
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

    # send the reminders with twilio: 
    # To set up environmental variables, see http://twil.io/secure

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']

    client = Client(account_sid, auth_token)

    client.api.account.messages.create(
        to="+15408787650",
        from_="+12563443615",
        body="Hello from twilio!")
    
    return "Sent message to lars"



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)