import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect,abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CMSC 447 HW 2'

# This is the connection that gets the access to the database to do things with 
def get_db_connection():
    conn = sqlite3.connect('user_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# This get the users from the database that has the id that is fed into it 
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?',
                        (user_id,)).fetchone()
    conn.close()

    return user


# This is the index and such the front page of the app and gets all the users
# from the database and dsiaply the entire thing, with name,id and points
@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)





@app.route('/insert/', methods=('GET', 'POST'))
def insert():
  # Set up up the search form and let the person fill in the form of the new user of 
  # user name , id, points and when the form is sumbit the post request will be received

  if request.method == 'POST':
        user_name = request.form['user_name']
        id = request.form['id']
        points = request.form['points']

        if not user_name:
            flash('Title is required!')
          
        elif not id:
            flash('Content is required!')

        elif not points:
            flash('Content is required!')
        else:
            # This insert into the databse with the user name , id and points and redirct
            # back to the index and the new user will be displayed in the bottom of the # page
            conn = get_db_connection()
            conn.execute('INSERT INTO users (user_name,id,points) VALUES (?, ?,?)',(user_name,id,points))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
 
  return render_template('insert.html')


# This edit the user by using the id and the index way to edit the user name, id and # points
# and isn't in a new page but at the bottom of each user display set 

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    user = get_user(id)
    # After POST get the user name and points change and update the database with no id
    # Can't change the id as need id to edit
    if request.method == 'POST':
        user_name = request.form['user_name']
        points = request.form['points']

        if not user_name:
            flash('User Name is required!')

        elif not points:
            flash('Points is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE users SET user_name = ?, points = ?'
                         ' WHERE id = ?',
                         (user_name, points, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', user=user)


# Delete the user by using the using the id and is delete in the edit html and is a
# button in below the eidt page
@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    user = get_user(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(user['user_name']))
    return redirect(url_for('index'))


# Allow for searching of user by name and diapsly the name , id and points
@app.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        user_name = request.form['user_name'] # Get the requested name

        conn = get_db_connection()# Find the user by using like and % user_name% to find
        # the user that has the user_name that has the request name in any position
        users = conn.execute('SELECT * FROM users WHERE user_name LIKE ?',
                        ('%' + user_name + '%',)).fetchall()

        return render_template('search.html', users=users) # display the
      # search user
    else:
        return render_template('search.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0') # run the app and should work as the host ip will allow for anyone to assess it .
