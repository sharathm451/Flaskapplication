import smtplib
fromaddr = 'qmessaging@gmail.com'
toaddrs  = 'qmessaging@gmail.com'
msg = "\r\n".join([
  "From: qmessaging@gmail.com",
  "To: qmessaging@gmail.com",
  "Subject: Just a message",
  "",
  "You have reached the front of the Queue! Please approach the front desk."
  ])

try:

  server = smtplib.SMTP('smtp.gmail.com',587)
  server.ehlo()
  server.starttls()
  server.login(username,password)
  server.sendmail(fromaddr, toaddrs, msg)
  server.close()
  print('successfully sent the mail')

except:
  print("failed to send email")
