from unittest import result
from flask import Flask, flash, redirect, render_template, request,url_for,session
import sqlite3
import functools
import keras
import numpy as np
import cv2
import os

def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if session['username'] == None:
            return redirect(url_for("login"))
        return func()

    return secure_function

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'MRI_image'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = "se_project_2022"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def load_home():
    session['username']  = None
    return render_template('index.html',login_logout = "Login")

# Route for handling the login page logic
@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'GET':
            session['username'] = None
            return render_template("form2.html",login_logout = "Login")
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        conn  = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('select* from users')
        rows = cursor.fetchall()
        for row in rows:
            if(row['username'] == username and row["password"] == password):
                #flash("Successfully Logged in!")
                session['username'] = username
                return redirect(url_for('predict'))
                #return render_template('predict.html',login_logout = "Logout")
        flash('Invalid login details!')
        return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html',login_logout = "Login")


@app.route('/predict', methods = ['GET','POST'])
@login_required
def predict():
    if(request.method == 'GET'):
        return render_template('predict.html', login_logout = "Logout")
    else:
        if 'img' not in request.files:
            flash('No file Uploaded!')
            return redirect(request.url)

        file = request.files['img']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            image = cv2.imread(os.path.join('MRI_image\\',file.filename))
            image = cv2.resize(image, (224,224))
            image = np.array(image)
            image = image/255.0
            image = np.resize(image,(1,224,224,3))
            loaded_model = keras.models.load_model('brain_tumor_predction_model')
            pred_result = loaded_model.predict(image)
            os.remove(os.path.join('MRI_image\\',file.filename))
            if(pred_result[0][0]<pred_result[0][1]):
                print("Brain Tumor detected!")
                r = "Brain Tumor detected!"
            else:
                r = "Brain Tumor not detected!"
                print("Brain Tumor not detected!")
            return render_template('predict.html',result = r,login_logout = "Logout")       
        flash("Invalid File type!")
        return redirect(request.url)

if __name__=='__main__':
    app.run(debug=True)
