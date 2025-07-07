import firebase_admin
from firebase_admin import credentials
# from google.oauth2 import service_account
# import google
import requests
import json


PROJECT_ID = 'hussain-6daca'
BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']



# https://fcm.googleapis.com/v1/projects/myproject-b5ae1/messages:send


def _get_access_token():
  """Retrieve a valid access token that can be used to authorize requests.

  :return: Access token.
  """
  cred = credentials.Certificate("service-account.json")
  default_app = firebase_admin.initialize_app(cred)
#   credentials = service_account.Credentials.from_service_account_file(
#     'service-account.json', scopes=SCOPES)
#   request = google.auth.transport.requests.Request()
#   credentials.refresh(request)
  
  return default_app.credential.get_access_token().access_token




def sendMessage(topic,title , body):
  headers = {
  'Authorization': 'Bearer ' + _get_access_token(),
  'Content-Type': 'application/json; UTF-8',
  }
  url = FCM_URL 
  body = {
  "message": {
    "topic": 'news',
    "notification": {
      "title": title,
      "body": body
    },
    "data": {
      "story_id": "story_12345"
    },
    "android": {
      "notification": {
   
        "body": body
      }
    },
    "apns": {
      "payload": {
        "aps": {
          "category" : "NEW_MESSAGE_CATEGORY"
        }
      }
    }
  }
  } 

  resp = requests.post(FCM_URL, data=json.dumps(body), headers=headers)
  print(resp)



