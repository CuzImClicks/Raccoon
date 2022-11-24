import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

msg = MIMEMultipart()

to = "henrik.hoppe@satrent.de"
fr = "test@test.com"

msg["Subject"] = "This is a test"
msg["To"] = to
msg["From"] = fr

with open("./new_image10.jpg", "rb") as fp:
    img = MIMEImage(fp.read())

msg.attach(img)

s = smtplib.SMTP("localhost:1025")
s.sendmail(to, [fr], msg.as_string())
s.quit()