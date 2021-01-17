from flask import*
import os
from werkzeug.utils import secure_filename
from send import send_mail
app=Flask(__name__)
app.config['UPLOAD_FOLDER']="./files"
@app.route('/')
def home():
	return render_template('index.html')

@app.route('/',methods=['POST'])
def sent():
	to=request.form['address'].split(',')
	subject=request.form['subject']
	body=request.form['body']

	img = request.files['file1']
	doc = request.files['file2']
	if img.filename != '':
		img.save((os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(img.filename))))
		img_send=True
	else:
		img_send = False
	if doc.filename != '':
		doc.save((os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(doc.filename))))
		doc_send = True
	else:
		doc_send = False
	flag=0
	for mail in to:
		msg_sent_no_error=send_mail(subject=subject,to_address=mail,content=body,img_send=img_send,img_name=img.filename,doc_send=doc_send,doc_name=doc.filename)
		if msg_sent_no_error==False:
			flag=1
		else:
			return render_template( "error.html",msg_sent_no_error=msg_sent_no_error,title="Error")
	msg="Mail Sent Successfully to:"
	addresses=to
	return render_template("success.html",msg=msg,addresses=addresses,title="success")
if __name__=="__main__":
	app.run(debug=True)
