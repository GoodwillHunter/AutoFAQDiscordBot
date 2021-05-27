"""
We present to you a discord bot that can help your community by answersing comman questions from newcomers saving time of older members from answering repetitive questions.

The FAQ is managed automatically so its up-to-date as time passes eliminating the need for manually maintaining the FAQ.

Salient Features include
  * Automatic and up-to-date FAQ database.
  * Effective immediately after setup and gets better overtime xD.
  * Can initialsize with existing FAQ set.
  * Incorporates feedback for induvisual question-answer pairs.
  * Users can choose to not recieve answers for their questions (Older members might prefer to do so).
"""


import discord

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


def isQuestion(msg):
  # Detect if the msg is a question or not
  # return boolean
  pass

def getAnswer(ques):
  # for a given question, find the answer
  # the answer could be a:
  #     Reply to the question
  #     Mention @quesUser in near following msgs.
  #     The very next msg
  pass

def getChatHistory():
  # get chat history of a given text channel
  # https://discordpy.readthedocs.io/en/stable/api.html#discord.TextChannel.history
  pass

def add(question, answer):
  # adds question-answer pair into the database
  pass

def generateFAQ():
  # used self.last_generated- datetime
  # runs initially and then every 24 hrs
  # iterates through chat history and find question-answer pairs
  # put them in a database
  pass

def generateFAQfromExisting(faq):
  # adds existing question-answers pair into the database
  # max score for these answers
  pass

def maintainDB():
  # Phase2
  # makes database more relevant
  # clusters similar questions
  # sorts based on importance
  pass

def answer(ques):
  # find the matching question and confidence
  # if confidence > threshold, writes answer on the text channel
  pass

def feedback(feedback):
  # handles feedback for answer output
  # adjusts score accordingly
  pass

def botReplySwitch(user):
  # switches bot reply for specific user
  # if no user provided, then acts as master on/off switch for the bot
  pass