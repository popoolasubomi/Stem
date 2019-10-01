#Speech Outputs
import subprocess
def say(text):
    subprocess.call(['say', text])

#Speech Inputs
import speech_recognition as sr
def Listen():
    global transcript
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=0)
    with mic:
        recognizer.adjust_for_ambient_noise(mic)
        audio = recognizer.listen(mic)
        try:
            transcript = recognizer.recognize_google(audio) 
            return transcript
        except:
            transcript_fail = "I Couldn't understand you"
            return transcript_fail

#Accessing app            
import os
def appAccess():
    global transcript
    transcript = ' '.join(transcript)
    open_loc = transcript.index('open')
    start = open_loc + 5
    app = transcript[start:].title()
    try:
        d = '/Applications'
        apps = list(map(lambda x: x.split('.app')[0], os.listdir(d)))
        os.system('open ' +d+'/%s.app' %app.replace(' ','\ '))
    except:
        say('Sorry, I do not have access to that app')
      
#Accessing from web pages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
def search_google():
    global transcript
    transcript = ' '.join(transcript)
    search_loc = transcript.index('search')
    start = search_loc + 6
    query = transcript[start:]
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get('http://www.google.com')
    search = browser.find_element_by_name('q')
    search.send_keys(query)
    search.send_keys(Keys.RETURN)

#English Dictionary
def meaning():
    global transcript
    transcript = ' '.join(transcript)
    define_loc = transcript.index('define')
    start = define_loc + 7
    try:
        transcript = transcript[start:]
        mean = wordnet.synsets(transcript)[0].definition()
        say(mean)
    except:
        print(transcript)
        say("I couldn't find the definition")

#Basic Calculator
from word2number import w2n
def BasicMaths():
    global transcript
    transcript = ''.join(transcript)
    print(transcript)
    solve_loc = transcript.index('solve')
    start = solve_loc + 5
    newTranscript = transcript[start:]
    newTranscript = newTranscript.replace('plu', '+')
    newTranscript = newTranscript.replace('minu', '-')
    newTranscript = newTranscript.replace('divid', '/')
    newTranscript = newTranscript.replace('multiply', '*')
    newTranscript = newTranscript.replace('divi', '/')
    newTranscript = newTranscript.replace('times', '*')
    newWord, num_word_list = '', []
    for x in newTranscript:
        if x in ['+','-','/','*']:
            num_word_list.append(newWord.strip())
            newWord = ''
        else:
            newWord += x
    num_word_list.append(newWord.strip())
    for x in num_word_list:
        newTranscript = newTranscript.replace(x, str(w2n.word_to_num(x)))
    say(str(eval(newTranscript)))
    
#Playing music
from playsound import playsound
from random import *
def musicPlayer():
    song = choice(['Suge.mp3'])
    path = '/Users/subomipopoola/Downloads/' + song
    playsound(path)
    
#Getting weather data
import requests
def checkWeather():
    say('what city')
    transcript3 = Listen()
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(transcript3, '0790a7f882c3dbf771b733d3846a14e8')
    r = requests.get(url)
    r = r.json()
    print(r['main'])
    for x,y in r['main'].items():
        say(x + str(y))
               
#Getting time and date
from datetime import datetime, date
def getTime():
    now = datetime.now()
    say("the time is " + now.strftime("%H %M %p"))

def getDate():
    today = date.today()
    say("todays date is " + today.strftime('%B %d, %Y'))

from nltk.corpus import *
from nltk.stem import PorterStemmer
ps = PorterStemmer()
def relevantWords(transcript):
     return [x for x in transcript if x not in stopwords.words('english')]
def Stemmer(transcript):
    return ps.stem(transcript) 
def Synonym(transcript):
    try:
        return [x.lemma_names() for x in wordnet.synsets(transcript) if x.lemma_names() != None][0]
    except:
        pass

def NonCommandOperation():
    global Question, transcript, all_similars
    f_obj = open('memory.json')  
    Question = json.load(f_obj)
    check1 = False
    wordLists = all_similars
    for num in range(len(wordLists)):
        wordLists[num] = sorted(wordLists[num])
    for Keys, Values in Question.items():
        if Values in wordLists:
            check1 = True
            say(Keys)
    if check1 == False:
        return Learn()
 
def CommandOperation():
    global transcript, relevant_words, mainCommand
    wordLists = relevant_words
    if mainCommand == 'search':
        search_google()
    elif mainCommand == 'solve':
        BasicMaths()
    elif mainCommand == 'open':
        appAccess()
    elif mainCommand == 'time':
        getTime()
    elif mainCommand == 'date':
        getDate()
    elif mainCommand == 'define':
        meaning()
    elif mainCommand == 'play':
        musicPlayer()
    elif mainCommand == 'weather':
        checkWeather()
    elif mainCommand == 'understand' or mainCommand == 'stop':
        pass
    elif mainCommand == 'destroy':
        Destroy()

import json
def Learn():
    global relevant_words, all_similars, Question
    relevant_word = sorted([Stemmer(words) for words in relevant_words])
    say("That has not been added to my memory, you tell me")
    transcript2 = Listen()
    if  'stop' not in transcript2:
        Question[transcript2] = relevant_word
        cobj = open('memory.json', 'w')  
        json.dump(Question, cobj)
        say('Thank you')
   
def Destroy(): 
    lobj = open('memory.json', 'w')
    json.dump({"hi, I'm stem. I am built mainly with the use of advanced natural language processing and speech recognition for the sole aim to serve humans":['introduc'],
           'Shoobomi is my creator':['creat'],'Shooobomi is my creator':['creator'],'Shoooobomi is my creator':['master'], "Hey":['hey'], "heyy":['hello'], "I am stem":['name'], "New Jersey":['live'],
           'I can define words, solve basic maths, play songs, access webpages, open apps, tell time and date, and also learn about you':[],'Yes?':['stem'], 'I am 3 days old':['old']}, lobj) 
    say('memory formated')      
    
def Stem():
    global all_similars, transcript, relevant_words, mainCommand, commands
    transcript = Listen().lower()
    try:
        print(transcript)
        transcript = ' '.join(transcript.split("'"))
        transcript = transcript.split(' ')
        commands = ['search', 'solve', 'open', 'time', 'date', 'define', 'destroy', 'shutdown', 'understand', 'stop', 'play','weather']
        mainTranscript = transcript
        relevant_words = relevantWords(mainTranscript)
      
        for command in commands:
            if command in mainTranscript:
                mainCommand = command
                return CommandOperation()
                break
        similar_words = [Synonym(words) for words in relevant_words]
        total, index1, index2 = 1, 0, 0
        for lists in similar_words:
          total *= len(lists)
        all_similars = [[] for _ in range(total)]
        for lists in similar_words:
          for num in range(total):
            if index2 == len(similar_words[index1]):
              index2 = 0
            all_similars[num].append(Stemmer(similar_words[index1][index2]))
            index2 += 1
          index1 += 1
          index2 = 0
        return NonCommandOperation()
    except:
        print(f)
        pass
        
    

