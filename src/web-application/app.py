import os
import os.path
from flask import Flask, request, redirect, url_for, render_template, session, send_from_directory, send_file
from werkzeug.utils import secure_filename
import pickle
import random

UPLOAD_FOLDER = './media/text-files/'
UPLOAD_KEY = './media/public-keys/'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
-----------------------------------------------------------
					PAGE REDIRECTS
-----------------------------------------------------------
'''
def post_upload_redirect():
	return render_template('post-upload.html')

@app.route('/register')
def call_page_register_user():
	return render_template('register.html')

@app.route('/home')
def back_home():
	return render_template('index.html')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload-file')
def call_page_upload():
	return render_template('upload.html')
'''
-----------------------------------------------------------
				DOWNLOAD KEY-FILE
-----------------------------------------------------------
'''

@app.route('/file-directory/retrieve/file/<filename>')
def download_file(filename):
	filepath = UPLOAD_FOLDER+filename
	if(os.path.isfile(filepath)):
		return send_file(filepath, attachment_filename='fileMessage-thrainSecurity.txt',as_attachment=True)
	else:
		return render_template('file-list.html',msg='An issue encountered, our team is working on that')

'''
-----------------------------------------------------------
		BUILD - DISPLAY FILE - KEY DIRECTORY
-----------------------------------------------------------
'''

# Build public key directory
@app.route('/public-key-directory/')
def downloads_pk():
	username = []
	if(os.path.isfile("./media/database/database_1.pickle")):
		pickleObj = open("./media/database/database_1.pickle","rb")
		username = pickle.load(pickleObj)
		pickleObj.close()
	if len(username) == 0:
		return render_template('public-key-list.html',msg='Aww snap! No public key found in the database')
	else:
		return render_template('public-key-list.html',msg='',itr = 0, length = len(username),directory=username)

# Build file directory
@app.route('/file-directory/')
def download_f():
	for root,dirs,files in os.walk(UPLOAD_FOLDER):
		if(len(files) == 0):
			return render_template('file-list.html',msg='Aww snap! No file found in directory')
		else:
			return render_template('file-list.html',msg='',itr=0,length=len(files),list=files)


if __name__ == '__main__':
	#app.run(host="0.0.0.0", port=80)
	app.run()