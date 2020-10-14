# import sendgrid
# import os
# from sendgrid.helpers.mail import *

# #sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
# from_email = Email("attendance-app@mdyschool.org")
# subject = "Hello World from the SendGrid Python Library!"
# to_email = Email("rfriedman113@gmail.com")
# content = Content("text/plain", "Hello, Email!")
# mail = Mail(from_email, subject, to_email, content)
# response = sg.client.mail.send.post(request_body=mail.get())
# print(response.status_code)
# print(response.body)
# print(response.headers)

import sendgrid
import os

sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
data = {
  "personalizations": [
    {
      "to": [
        {
          "email": "rfriedman113@gmail.com"
        }
      ],
      "subject": "Hello World 2 from the SendGrid Python Library!"
    }
  ],
  "from": {
    "email": os.environ.get('MAIL_DEFAULT_SENDER')
  },
  "content": [
    {
      "type": "text/plain",
      "value": "Hello, Email!"
    }
  ]
}
response = sg.client.mail.send.post(request_body=data)
print(response.status_code)
print(response.body)
print(response.headers)