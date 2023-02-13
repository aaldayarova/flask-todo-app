# Boilerplate code importing the flask module and render_template module, which will allow us to create and render
# different templates for our pages, not just words
from flask import Flask, render_template, request, redirect, url_for
# Importing a database
from flask_sqlalchemy import SQLAlchemy

# '__name__' argument is passed in the Flask class to create its instance, which is then used to run the application
app = Flask (__name__)
# Setting up the path to our database (the /// mean the path is relative, aka in the same folder)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# Setting another config to avoid Flask throwing us errors
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Actually create the database
db = SQLAlchemy(app)

# Inside of our database, we want to create model for our todo items, so we create a class for them; 
# This Todo class will inherit db.Model and will have thre key properties
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


# Creating an index page for the website and routing it to the default URL via '/'
@app.route('/')
def index():

    # Show all todos
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list = todo_list)

# Creating functionality for the "add" button 
@app.route('/add', methods = ["POST"])
def add():

    # Create a todo
    title = request.form.get("title")
    new_todo = Todo(title = title, complete = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

# Creating functionality for the "update" button 
@app.route('/update/<int:todo_id>')
def update(todo_id):

    # Update a todo
    todo = Todo.query.filter_by(id = todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

# Creating functionality for the "delete" button 
@app.route('/delete/<int:todo_id>')
def delete(todo_id):

    # Delete a todo
    todo = Todo.query.filter_by(id = todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))



# A way for our app to automatically generate a URL for our app in developer mode (this is where the 'debug=True' comes in)
# Once you exit out of VSCode and return to continue working on the app, simply follow the below steps:
#1) Save this file
#2) Run pyhton app.py (and a link should generate)
# If that doesn't work, you might need to set the settings for the URL again using the below steps first:
#1) export FLASK_APP=app.py
#2) export FLASK_DEBUG=true
# If that doesn't work either, then you might not be in your virtual environment and might need to set that up too:
#1) python3 -m venv venv
#2) . venv/bin/activate  
if __name__ == "__main__":
    # A with block to encapsulate the creation of the db.sqlite database in the app context manually;
    # Learned from https://flask.palletsprojects.com/en/2.2.x/appcontext/ 
    with app.app_context():
        db.create_all()

    app.run(debug=True)
