from flask import Flask, request, render_template, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '02Panoslek02!',
    'database': 'simple_app'
}


# Route for signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    connection = None
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            connection.commit()
            message = 'Signed up successfully!'
        except Error as e:
            message = f'Error: {e}'
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    return render_template('signup.html', message=message)

# Route for signin
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    connection = None
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            query = "SELECT id FROM users WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            if user:
                session['userid'] = user[0]  # Store user ID in session
                return redirect(url_for('posts'))
            else:
                message = 'Invalid username or password.'
        except Error as e:
            message = f'Error: {e}'
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    return render_template('signin.html', message=message)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))

# # Route to display user's posts
# @app.route('/posts', methods=['GET', 'POST'])
# def posts():
#     if 'userid' not in session:
#         return redirect(url_for('signin'))
    
#     connection = None
#     posts = []
#     try:
#         connection = mysql.connector.connect(**db_config)
#         cursor = connection.cursor(dictionary=True)
#         query = "SELECT * FROM posts WHERE userid=%s ORDER BY createdat DESC"
#         cursor.execute(query, (session['userid'],))
#         posts = cursor.fetchall()
#     except Error as e:
#         flash(f'Error: {e}', 'danger')
#     finally:
#         if connection and connection.is_connected():
#             cursor.close()
#             connection.close()
    
#     return render_template('posts.html', posts=posts)

# Route to add a new post
@app.route('/add_post', methods=['POST'])
def add_post():
    if 'userid' not in session:
        return redirect(url_for('signin'))
    
    connection = None
    text = request.form['text']
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "INSERT INTO posts (userid, text) VALUES (%s, %s)"
        cursor.execute(query, (session['userid'], text))
        connection.commit()
        flash('post added successfully!', 'success')
    except Error as e:
        flash(f'Error: {e}', 'danger')
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
    
    return redirect(url_for('posts'))



@app.route('/posts', methods=['GET'])
def posts():
    if 'userid' not in session:
        return redirect(url_for('signin'))
    
    connection = None
    posts = []  # List to hold all posts
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        # Fetch all posts with usernames
        query = """
            SELECT posts.id, posts.text, posts.createdat, users.username
            FROM posts
            JOIN users ON posts.userid = users.id
            ORDER BY posts.createdat DESC
        """
        cursor.execute(query)
        posts = cursor.fetchall()
    except Error as e:
        flash(f'Error: {e}', 'danger')
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
    
    return render_template('posts.html', posts=posts)


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)

