import smtplib
import socket
import imghdr
import os
from email.message import EmailMessage
USER_MAIL=open('.user','r').read().replace('\n','')
USER_PASS=open('.pass','r').read().replace('\n','')
def send_mail(subject,to_address,content,img_send,img_name,doc_send,doc_name):
	msg=EmailMessage()
	msg['Subject']=subject
	msg['From']=USER_MAIL
	msg['To']=to_address
	msg.set_content(content)

	try:
		with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:	
			smtp.login(USER_MAIL,USER_PASS)	

			if img_send:
				with open(f'./files/{img_name}','rb') as f:
					file_data = f.read()
					file_type = imghdr.what(f.name)
					file_name = f.name.split('/')
					file_name = file_name[len(file_name)-1]
					#print(file_name)
				msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

			if doc_send:
				with open(f'./files/{doc_name}','rb') as f:
					file_data = f.read()
					file_name = f.name.split('/')
					file_name = file_name[len(file_name)-1]
					#print(file_name)
				msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

			smtp.send_message(msg)
			error=False
			return error
	except smtplib.SMTPRecipientsRefused as RR:
		error='Error! No Proper Recipient Address'
		return error
	except socket.gaierror as nonet:
		error='Error! Check the internet connection'
		return error
	except Exception:
		error="Opps! something went wrong please check mail address."
		return error