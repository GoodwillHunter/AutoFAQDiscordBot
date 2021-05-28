"""
We present to you a discord bot that can help your community by answersing common questions from newcomers saving time of older members from answering repetitive questions.

The FAQ is managed automatically so its up-to-date as time passes eliminating the need for manually maintaining the FAQ.

Salient Features include
  * Automatic and up-to-date FAQ database.
  * Effective immediately after setup and gets better overtime xD.
  * Can initialsize with existing FAQ set.
  * Incorporates feedback for induvisual question-answer pairs.
  * Users can choose to not recieve answers for their questions (Older members might prefer to do so).
"""


import discord
import os
import datetime
from replit import db
import sys
import subprocess
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

#TDOD: Make created_at channel wise and add to db
created_at = None
threshold = 0.5
# TODO: Make utility functions for threshold

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
  global created_at
  async for message in channel.history(limit=None, after=created_at):
    temp.append(message)
  created_at = datetime.datetime.now()
  arr = []
  n = len(temp)
  m = n-1
  for i in range(n):
    arr.append(temp[m])
    m -= 1

  return arr;

def add(question, answer):
  # TODO: Divide the question sentence wise and only add question part.
  channel = str(question.channel)
  if(channel not in db):
    db[channel] = {}
  # adds question-answer pair into the database
  print("Q. "+question.content)
  print("A. "+answer.content)
  max_score = 0
  for ques2 in db[channel]:
    match = ratio(ques2, question.content)
    if(match>max_score):
      max_score = match
  if(max_score < threshold):
    db[channel][question.content.lower()] = answer.content

async def generateFAQ(channel):
  # used self.last_generated- datetime
  # runs initially and then every 24 hrs
  # iterates through chat history and find question-answer pairs
  # put them in a database
  # print("generateFAQ called")
  channel1 = str(channel)
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
  channel = str(ques.channel)
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
    await ques.channel.send("Hey, your friendly FAQ Bot here. Here is a related question asked befor: "+prediction)
    await ques.channel.send("Here is the answer: "+answer)

def feedback(feedback):
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

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  # if created_at + 24 hrs > datetime.now
  #   await generateFAQ(message.channel)
  global created_at
  # if(created_at==None or created_at+datetime.timedelta(hours=24)<datetime.datetime.now()):
  #   await generateFAQ(message.channel)
  if message.author == client.user:
    return

  msg = message.content

  if(isQuestion(msg)):
    await answer(message)

  if msg.startswith('$generateFAQ'):
    # print("command recieved")
    channel1 = str(message.channel)
    if(channel1 in db):
      db.pop(channel1)
    created_at = None
    await generateFAQ(message.channel)
    print("FAQ reset successfull")
    await message.channel.send("FAQ reset successfull")

client.run(os.environ['TOKEN'])