# -*- coding: utf-8 -*-
import os
consumer_key=os.environ.get('CK')
consumer_secret=os.environ.get('CS')
access_token=os.environ.get('AT')
access_token_secret=os.environ.get('ATS')
myuserid=os.environ.get('MYUSERID')

### 定義部 ###

import pytesseract
import io
import requests
from PIL import Image


import redis
client=redis.from_url(
        url=os.environ.get('REDIS_URL'),
        decode_responses=True,
    )


from twython import Twython, TwythonError

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
)

### 主題部 ###

def main():
  responses = twitter.get_mentions_timeline(count=30)     
  
  for r in responses:
    medium=[]
    id=r['id_str']
    if r['user']['id_str'] !=myuserid : continue
    try:
      medium=r['entities']['media']
    except:
      continue
    if id not in client.smembers('twitterid'):
      for media in medium:
        response = requests.get(media['media_url'])
        image_bytes = io.BytesIO(response.content)
        img = Image.open(image_bytes)
        pytesseract.pytesseract.tesseract_cmd = 'tesseract'
        t = pytesseract.image_to_string(img, lang="pri") 
        twitter.update_status(status=t, in_reply_to_status_id=id, auto_populate_reply_metadata=True)
        client.sadd('twitterid',id)
        print('replyed:'+id)

main()

### web用API ###

from flask import Flask
app = Flask(__name__)
@app.route("/")
def index():
  main()
  str="Princess Awakened!"
  return str

app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
