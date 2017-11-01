from flask import Flask, render_template, json, jsonify, request,session,redirect,url_for,flash
from flask_session import Session
from flask_uploads import UploadSet,configure_uploads,IMAGES, patch_request_class   
from flask_restful import Resource,Api
from flaskext.mysql import MySQL
from flask_wtf import FlaskForm
from werkzeug import secure_filename
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import os
#from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)
sess = Session()

# MySQL configurations
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/static'
photos = UploadSet('photos',IMAGES)

configure_uploads(app,photos)
patch_request_class(app)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'nisarg652'
app.config['MYSQL_DATABASE_DB'] = 'RTOwebsite'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, u'Image Only!'), FileRequired(u'Choose a file!')])
    submit = SubmitField(u'Upload')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/showMenuPage')
def showMenuPage():
    return render_template('menupage.html')

@app.route('/showLearnersLicense')
def showLearnersLicense():
    return render_template('learnerslicense.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
        #    _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_password))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                flash('User created successfully !')
                return jsonify(data=data)
            else:
                return json.dumps({'error':str(data[0])})
            
            cursor.close() 
            conn.close()
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
        
@app.route('/signIn',methods=['GET'])
def signIn():
    try:
        _email = request.args.get('inputEmail')
        _password = request.args.get('inputPassword')
        
        # validate the received values
        if _email and _password:
            
            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
        #    _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_signIn',(_email,_password))
            data = cursor.fetchone()
            
            if data is not None:
                conn.commit() 
                session['email'] = _email
                return jsonify(data=data)
            else:
                return json.dumps({'error':'No such user'})
            
            cursor.close() 
            conn.close()
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    
@app.route('/signOut')
def signOut():
   # remove the username from the session if it is there
    session.pop('email', None)
    return redirect(url_for('main'))

@app.route('/learnersLicense',methods=['POST'])
def learnersLicense():
    try:
        _firstname = request.form['firstName']
        _lastname= request.form['lastName']
        _dob = request.form['dob']
        _sex = request.form['sex']
        _aadharno = request.form['aadharNo']
        _mobileno = request.form['mobileNo']
        _addressno = request.form['addressNo']
        _addresslocality = request.form['addressLocality']
        _addressdistrict = request.form['addressDistrict']
        _addresspincode = request.form['addressPincode']
        _licensetype = request.form['licenseType']
        _rtooffice = request.form['rtoOffice']
        _picture = request.files.get('photo','')
        _addressproof =request.files.get('addressProof','')
        _aadharcard = request.files.get('aadharcard','')
        form = UploadForm()
        if form.validate_on_submit():
            _picture = photos.save(request.files.get('photo',''))
            _addressproof = photos.save(request.files.get('addressProof',''))
            _aadharcard = photos.save(request.files.get('aadharcard',''))
            
        # validate the received values
        
        if _firstname and _lastname and _dob and _sex and _aadharno and _mobileno and _addressno and _addresslocality and _addressdistrict and \
        _addresspincode and _licensetype and _rtooffice:
           
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
                #    _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_learnersLicense', (_firstname,_lastname,_dob,_sex,_aadharno,_mobileno,_addressno,_addresslocality,_addressdistrict,\
            _addresspincode,_licensetype,_rtooffice,_picture,_addressproof,_aadharcard,session['email']))

            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                flash('User created successfully !')
                return json.dumps({'message':'User created successfully !'})
            else:
                flash('User already exists !')
                return json.dumps({'error':str(data[0])})

            cursor.close() 
            conn.close()
            
        else:
            flash('Enter the required fields')
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
        


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.debug = True
    app.run(port=5002)
