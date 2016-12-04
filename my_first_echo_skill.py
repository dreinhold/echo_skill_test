from flask import Flask
from flask_ask import Ask, statement, question, session

import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app,"/reddit_reader")

def get_headlines():
    user_pass_dict = {'user': 'YOUR_REDDIT_USER_NAME', 
                      'passwd': 'YOUR_REDDIT_PASSWORD', 
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'Alexa Test'})
    sess.post('https://www.reddit.com/api/login', data = user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/programming/.json?limit=3'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    title_info = ""
    count = 0
    count_name = ['top post', '2nd to top post', '3rd to the top post']
    for i in titles:
        title_info += "The {} on reddit programming is {}........".format(count_name[count], i)
        count+=1
    return title_info

@app.route('/')
def homepage():
    return "hi there"

@ask.launch
def start_skill():
    welcome_message = 'Hello there,, would you like the top reddit post for r programming?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    return statement(headlines)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Im not sure why you asked me'
    return statement(bye_text)


if __name__ == '__main__':
    app.run(debug=True)
