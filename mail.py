#!/usr/bin/env python3
import smtplib, config, numbers, string
from render import render_str
from trivia import get_random_question

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from dateutil.parser import parse

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.ehlo()
# Login as my Gmail user.
username=config.email['username']
password=config.email['password']
s.login(username,password)

replyto=config.email['reply']
sendto=[contact['email'] for contact in config.email['recipients']] # The list to send to.

# Get the trivia question to put into email template.
json = get_random_question()

def send_mail():
  # Send the email.
  for contact in config.email['recipients']:
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Daily Jeopardy for " + datetime.now().strftime('%b %d')
    msg['From'] = replyto
    msg['To'] = contact['email']

    # Make sure value is Number. If null, set a default value of 200.
    dollar_amount = 200
    if isinstance(json[0]['value'], numbers.Number):
      dollar_amount = json[0]['value']

    # Generate prefilled Google Form link.
    common_params = config.form['base_link'] + '?usp=pp_url&entry.1855541136=' + json[0]['category']['title'] + '&entry.1547920482=' + json[0]['question'] + '&entry.267256741=' + json[0]['answer'] + '&entry.385374182=' + str(dollar_amount) + '&entry.701029748=' + contact['name']
    yes_link = common_params + '&entry.1912653224=Yes'
    no_link  = common_params + '&entry.1912653224=No'
    
    # Format air date.
    datetime_obj = parse(json[0]['airdate'])
    air_date = datetime_obj.strftime('%b %d, %Y')
    data = dict(
        clue_id = json[0]['id'],
        name = contact['name'],
        category = string.capwords(json[0]['category']['title'], ' ')(),
        value = dollar_amount,
        question = json[0]['question'],
        air_date = air_date,
        answer = json[0]['answer'],
        yes_response_link = yes_link,
        no_response_link = no_link,
        scoreboard_link = config.sheet['link']
    )

    image_path = config.image_link
    html = render_str('email.html', data=data, image_path=image_path)

    message = MIMEText(html, 'html')
    msg.attach(message)
    s.sendmail(replyto, contact['email'], msg.as_string())

  rslt=s.quit()
  print('Sendmail result=' + str(rslt[1]))