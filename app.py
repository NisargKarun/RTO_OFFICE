from flask import Flask, render_template, json, jsonify, request
from flask_restful import Resource,Api
from flaskext.mysql import MySQL
#from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'nisarg652'
app.config['MYSQL_DATABASE_DB'] = 'RTOwebsite'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


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
                return json.dumps({'message':'User created successfully !'})
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
                return jsonify(data=data)
            else:
                return json.dumps({'error':'No such user'})
            
            cursor.close() 
            conn.close()
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})


if __name__ == "__main__":
	app.run(port=5002)
