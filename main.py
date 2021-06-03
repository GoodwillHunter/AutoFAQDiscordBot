"""
We present to you a discord bot that can help your community by answersing common questions from newcomers saving time of older members from answering repetitive questions.

The FAQ is managed automatically so its up-to-date as time passes eliminating the need for manually maintaining the FAQ.

Salient Features include
  * Automatic and up-to-date FAQ database.
  * Effective immediately after setup and gets better overtime xD.
  * You can use a private database too.
  * Can get as many related QA as you want.
  * Users can choose to not recieve answers for their questions (Older members might prefer to do so).
"""


import discord
import os
import datetime
from replit import db
import replit
import sys
import subprocess
from dateutil.parser import parse
import heapq
try:
  from Levenshtein import ratio
except:
  subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'python-levenshtein'])
  from Levenshtein import ratio


client = discord.Client()

"""
Important Links:
  Discord Bot tutorial: https://www.youtube.com/watch?v=SPTfmiYiuok&t=1s&ab_channel=freeCodeCamp.org
  https://replit.com/@BeauCarnes/Encourage-Bot

  discordpy documentation: https://discordpy.readthedocs.io/en/stable/api.html

  How to extract question and answer pairs from telegram chat using Python pandas? : https://www.numpyninja.com/post/how-to-extract-question-and-answer-pairs-from-telegram-chat-using-python-pandas

  Simple Question Answering (QA) Systems That Use Text Similarity Detection in Python : https://www.kdnuggets.com/2020/04/simple-question-answering-systems-text-similarity-python.html

  Identifying Clusters of Related Questions : https://www.kaggle.com/mithrillion/identifying-clusters-of-related-questions

  How to create your own Question-Answering system easily with python : https://towardsdatascience.com/how-to-create-your-own-question-answering-system-easily-with-python-2ef8abc8eb5


"""
question_words = set(["anyone", 'tell','can','what','where','when','how','which','who','why','suggest'])
# TODO: make utility functions for question_words


threshold = 0.5
#TODO: make last_answer channel independent
last_answer = None

bot_switch_off = False
bot_switch_user = {}

# Do RBAC for commands

def isQuestion(msg):
  # Detect if the msg is a question or not
  # return boolean
  msg = msg.lower()
  if any(word in msg for word in question_words):
      return True
  return False

def getAnswer(ques, arr):
  # phase 2
  # for a given question, find the answer
  # the answer could be a:
  #     Reply to the question
  #     Mention @quesUser in near following msgs.
  #     The very next msg
  pass

async def getChatHistory(channel):
  # get chat history of a given text channel
  # https://discordpy.readthedocs.io/en/stable/api.html#discord.TextChannel.history
  # print("getChatHistory called")
  temp = []
  if str(channel.id) not in db['created_at']:
    db['created_at'][str(channel.id)] = None
  if(db['created_at'][str(channel.id)] == None):
    async for message in channel.history(limit=None):
      temp.append(message)
  else:
    async for message in channel.history(limit=None, after=parse(db['created_at'][str(channel.id)])):
      temp.append(message)
  db['created_at'][str(channel.id)] = str(datetime.datetime.now())
  print("REAL TIME SET")
  arr = []
  n = len(temp)
  m = n-1
  for i in range(n):
    arr.append(temp[m])
    m -= 1

  return arr;


def add(question, answer):
  channel = str(question.channel.id)
  if(channel not in db):
    db[channel] = {}
  # adds question-answer pair into the database
  ques = question.content
  ques = ques.replace('?', '.')
  ques = ques.replace('!', '.')
  ques = ques.replace(';', '.')
  ques = ques.split(".")
  q = ""
  for x in ques:
    if(isQuestion(x)):
      q += x
      q += " "
  print(q)
  #print("A. "+answer.content)

  # max_score = 0
  # for ques2 in db[channel]:
  #   match = ratio(ques2, question.content)
  #   if(match>max_score):
  #     max_score = match
  # if(max_score < threshold):
  db[channel][q.lower()] = answer.content

async def generateFAQ(channel):
  # used self.last_generated- datetime
  # runs initially and then every 24 hrs
  # iterates through chat history and find question-answer pairs
  # put them in a database
  # print("generateFAQ called")
  channel1 = str(channel.id)
  unanswered_questions = {}
  if(channel1 not in db):
    db[channel1] = {}
  if("unanswered_questions" in db[channel1]):
    unanswered_questions = db[channel1]["unanswered_questions"]
  arr = await getChatHistory(channel)
  for msg in arr:
    if msg.author == client.user:
      continue
    if(isQuestion(msg.content)):
      unanswered_questions[msg.id] = msg
    if(msg.reference!=None and msg.reference.message_id in unanswered_questions and unanswered_questions[msg.reference.message_id].author!=msg.author):
      add(unanswered_questions[msg.reference.message_id], msg)
      unanswered_questions.pop(msg.reference.message_id)
  # db[channel1]["unanswered_questions"] = unanswered_questions

def generateFAQfromExisting(faq):
  # adds existing question-answers pair into the database
  # max score for these answers
  # TODO
  pass


# def getApproximateAnswer2(q):
#     max_score = 0
#     answer = ""
#     prediction = ""
#     for idx, row in data.iterrows():
#         score = ratio(row["Question"], q)
#         if score >= 0.9: # I'm sure, stop here
#             return row["Answer"], score, row["Question"]
#         elif score > max_score: # I'm unsure, continue
#             max_score = score
#             answer = row["Answer"]
#             prediction = row["Question"]
#     if max_score > 0.3: # threshold is lowered
#         return answer, max_score, prediction
#     return "Sorry, I didn't get you.", max_score, prediction

async def answer(ques):
  # find the matching question and confidence
  # if confidence > threshold, writes answer on the text channel
  # Phase 2: Get more than one related QA
  global last_answer 
  last_answer = ques
  channel = str(ques.channel.id)
  max_score = 0
  answer = ""
  prediction = ""
  for ques2 in db[channel]:
    match = ratio(ques2, ques.content)
    if(match>max_score):
      max_score = match
      answer = db[channel][ques2]
      prediction = ques2
  if(max_score >= threshold):
    await ques.channel.send("Related question: "+prediction)
    await ques.channel.send("Answer: "+answer)
    await last_answer.channel.send("To get more related QA, type '$more n', replace n with #questions")


async def answer_more(n=3):
  global last_answer
  if(last_answer==None):
    return
  channel1 = str(last_answer.channel.id)
  l1 = []
  for ques2 in db[channel1]:
    heapq.heappush(l1, (ratio(ques2, last_answer.content), ques2))
  l2 = heapq.nlargest(n+1, l1)
  l2.pop(0)
  for x in l2:
    await last_answer.channel.send("Related question: "+x[1])
    await last_answer.channel.send("Answer: "+db[channel1][x[1]])
    

def feedback(feedback):
  # Phase 2
  # handles feedback for answer output
  # adjusts score accordingly
  # TODO
  pass

def botReplySwitch(user):
  # switches bot reply for specific user
  # if no user provided, then acts as master on/off switch for the bot
  # TODO
  pass

def maintainDB():
  # Phase2
  # makes database more relevant
  # clusters similar questions
  # sorts based on importance
  pass

async def threshold_utility(msg, channel):
  global threshold
  if(msg[2]=="get"):
    await channel.send("threshold: "+str(threshold))
  if(msg[2]=="set"):
    temp = int(msg[3])
    if(temp>=0 and temp<=1):
      threshold = temp
    else:
      await channel.send("please send a valid value between 0 and 1")
async def database_utility(msg, channel):
  if(msg[2]=="show"):
    x = db[str(channel.id)]
    for q in x:
      await channel.send("Q. "+str(q))
      await channel.send("A. "+str(x[q]))
  if(msg[2]=="showall"):
      keys = db.keys()
      for x in keys:
        await channel.send("Channel: "+str(x))
        for q in db[x]:
          await channel.send("Q. "+str(q))
          #await channel.send("A. "+str(x[q]))
async def created_at_utility(msg, channel):
  if(msg[2]=="get"):
    await channel.send(db['created_at'][str(channel.id)])
  if(msg[2]=="set"):
    db['created_at'][str(channel.id)] = str(parse(msg[3]))

async def admin_utility(message):
  msg = message.content.split()
  channel = message.channel
  # format -> [$admin area task param1 param2...]
  if(msg[1]=="db"):
    await database_utility(msg, channel)
  elif(msg[1]=="threshold"):
    await threshold_utility(msg, channel)
  elif(msg[1]=="created_at"):
    await created_at_utility(msg, channel)

    

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  global bot_switch_off
  global bot_switch_user
  if(message.content.startswith("$switchall on")):
    bot_switch_off = False
  elif(message.content.startswith("$switchall off")):
    bot_switch_off = True
  elif(message.content.startswith("$switch on")):
    if(str(message.author.id) in bot_switch_user):
      bot_switch_user.pop(str(message.author.id))
  elif(message.content.startswith("$switch off")):
    if(str(message.author.id) not in bot_switch_user):
      bot_switch_user[str(message.author.id)] = "OFF"
  if(bot_switch_off or str(message.author.id) in bot_switch_user):
    return
  
  global db
  from replit import db
  if("private_db" not in db):
    db["private_db"] = {}
  if(message.content.startswith("$admin private_db reset")):
    if(str(message.channel.id) in db["private_db"]):
      db["private_db"].pop(str(message.channel.id))
  elif(message.content.startswith("$admin private_db set")):
    url = message.content.split()[3]
    db["private_db"][str(message.channel.id)] = url
  # print(type(message))
  
  if(str(message.channel.id) in db["private_db"]):
    db = replit.database.Database(db["private_db"][str(message.channel.id)])

  if message.author == client.user:
    return

  # print(db.keys())
  msg = message.content

  channel1 = str(message.channel.id)
  if("created_at" not in db):
    db["created_at"] = {}
    print("created_at not in db")
  
  if channel1 not in db['created_at']:
    print("channel1 not in db['created_at']")
    await generateFAQ(message.channel)
    print("FAQ refresh succesfull")
  if(channel1 not in db['created_at']):
    db['created_at'][channel1] = str(datetime.datetime(2000, 1, 1))
    print("PROXY TIME SET")
    print("channel1 not in db['created_at']")
    await generateFAQ(message.channel)
    print("FAQ refresh succesfull")
  # print(db['created_at'])
  if parse(db['created_at'][channel1])+datetime.timedelta(hours=24)<datetime.datetime.now():
    print("time expired")
    await generateFAQ(message.channel)
    print("FAQ refresh succesfull")
  
  
  if(isQuestion(msg)):
    await answer(message)
  
  if msg.startswith('$admin'):
    await admin_utility(message)
  
  if msg.startswith('$more'):
    temp = msg.split()
    n = 3
    if(len(temp)>1):
      n = int(temp[1])
    await answer_more(n)

  if msg.startswith('$generateFAQ'):
    # print("command recieved")
    
    if(channel1 in db):
      db.pop(channel1)
    db['created_at'].pop(str(message.channel.id))
    await generateFAQ(message.channel)
    print("FAQ reset successfull")
    await message.channel.send("FAQ reset successfull")

client.run(os.environ['TOKEN'])

# phase 3: Add super-admin commands that can export QA from all channels into a csv which will be used as test data for future algorithms