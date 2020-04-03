#!/usr/bin/env python3
import smtplib, numbers, string
from smtplib import SMTPException
from render import render_str
from trivia import get_random_question

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from dateutil.parser import parse

# Send the email.
def send_mail(username, password, recipients, form_link, sheet_link, game_title):
  replyto = str(username)
  emails = [player['Email Address'] for player in recipients]
  # Get the trivia question to put into email template.
  json = get_random_question()
  # Create message container - the correct MIME type is multipart/alternative.
  msg = MIMEMultipart('alternative')
  msg['Subject'] = 'Daily Jeopardy for ' + datetime.now().strftime('%B %d')
  msg['From'] = replyto
  msg['To'] = ', '.join(emails)

  # Make sure value is Number. If null, set a default value of 200.
  dollar_amount = 200
  if isinstance(json[0]['value'], numbers.Number):
    dollar_amount = json[0]['value']

  # Generate prefilled Google Form link.
  common_params = str(form_link) + '?usp=pp_url&entry.1341812145=' + json[0]['category']['title'] + '&entry.170899811=' + json[0]['question'] + '&entry.793323660=' + json[0]['answer'] + '&entry.823702681=' + str(dollar_amount) + '&entry.439576061=' + game_title
  yes_link = common_params + '&entry.756768512=Yes'
  no_link  = common_params + '&entry.756768512=No'

  # Format air date.
  datetime_obj = parse(json[0]['airdate'])
  air_date = datetime_obj.strftime('%b %d, %Y')
  data = dict(
      clue_id = json[0]['id'],
      category = string.capwords(json[0]['category']['title'], ' '),
      value = dollar_amount,
      question = json[0]['question'],
      air_date = air_date,
      answer = json[0]['answer'],
      yes_response_link = yes_link,
      no_response_link = no_link,
      scoreboard_link = str(sheet_link)
  )

  html = render_str('email.html', data=data)
  msg.attach(MIMEText(html, 'html'))

  try:
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    # Login as my Gmail user.
    s.login(username, password)

    s.sendmail(replyto, emails, msg.as_string())
  except SMTPException as e:
    print(e)

  result = s.quit()
  print('Sendmail result: ' + str(result[1]))


