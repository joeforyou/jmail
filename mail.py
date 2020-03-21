#!/usr/bin/env python3
import smtplib, config
from render import render_str
from trivia import get_random_question

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.ehlo()
# Login as my Gmail user.
username=config.email['username']
password=config.email['password']
s.login(username,password)

replyto=config.email['reply']
sendto=config.email['recipients'] # The list to send to.

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Daily Jeopardy Question for " + datetime.now().strftime('%m-%d')
msg['From'] = replyto
msg['To'] = replyto

# Get the trivia question to put into email template.
json = get_random_question()
month = '{:%B}'.format(datetime.now()).lower()
link =  config.spreadsheet['link'] + config.spreadsheet[month]
data = dict(
    category = json[0]['category']['title'],
    value = json[0]['value'],
    question = json[0]['question'],
    answer = json[0]['answer'],
    link = link
)
html = render_str('email.html', data=data)

message = MIMEText(html, 'html')
msg.attach(message)

def send_mail():
  # Send the email.
  s.sendmail(replyto, sendto, msg.as_string())
  rslt=s.quit()
  print('Sendmail result=' + str(rslt[1]))