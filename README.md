# AutoFAQ Discord Bot
We present to you a discord bot that can help your community by answering common questions from newcomers saving time for older members and improving the onboarding experience. 

The FAQ is managed automatically, so it's up-to-date as time passes, eliminating the need for manually maintaining the FAQ.

Salient Features include
  * Automatic and up-to-date FAQ database. (Refreshes every 24 hrs)
  * Effective immediately after setup and gets better overtime xD.
  * You can use a private database too.
  * Can get as many related QA as you want.
  * Users can choose not to receive answers for their questions (Older members might prefer to do so).

## Motivation
As one of the early members of a growing discord community, we usually face the problem of answering the same questions multiple times as new people join. We cannot expect the new members to go through countless chat history also. This slows down the process of onboarding and puts a natural limit on a growing online community.

But what if we can automate the task of sorting through the chat history to find the relevant questions and related answers. That's exactly what this project is trying to achieve. 

Put simply, this bot is the receptionist to your nascent network union. I was encouraged to make this bot by a challenge from [@balajis](https://twitter.com/balajis) new project, [1729.com](https://1729.com/).

## Installation
Simply invite the bot to join your server from the following link and you are good to go xD.

https://discord.com/api/oauth2/authorize?client_id=847806364453830728&permissions=76800&scope=bot

### Further Customisation 
Though the bot's UX is made to work flawlessly from the get go, here are a few things you can do to improve the experience. 

#### Turn bot reply ON/OFF
There might be some channels where you don't want the bot to answers questions for you. To turn off the bot for a specific channel, just message ```$switchall off``` on your channel chat.
To turn the replies back on, message ```$switchall on```.

You can also turn replies on/off just for yourself too (if you are an older member, you might prefer to do so). Just message ```$switch off``` in the chat. To turn them back on, message ```$switch on```.

#### Private Database
You might want to have a private database for your community to keep the data secure. This is also encouraged for larger communities to improve performance. To use a private database, you can follow these simple steps:

1. Go to repl.it and create a new repl.
2. Open python in your repl shell and ```import os```.
3. Copy the repl db url by typing ```os.environ["REPLIT_DB_URL"]``` .
4. In your channel chat, type ```$admin private_db set <REPLIT_DB_URL>```.

Note: Private databases are set up channel-wise; thus, you have to repeat step 4 on every channel in your discord server.
Conversely, you can use the same database for multiple servers too.

#### Reset FAQ
For some reason, you might want to hard reset the question/answer database for your channel. You can do so by typing ```$generateFAQ``` in your channel chat.

## Usage
The bot is made to work flawlessly in the background. Simply ask a question, and the bot will find a relevant question (if present) and the corresponding answer.

You can get more related questions by typing ```$more <n>``` in the chat. For example ```$more 3``` will give you three more related question and answer.

## Contributing
Please stay tuned. We will open the repo for open-source contribution soon.