#imports
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#my app
app = Flask(__name__)
Scss(app)

#where to find the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#connecting flask to database
db = SQLAlchemy(app)


#defining blueprint structure of the table in the database
class MyTask(db.Model): #mytask represents a database record
    #defining columns using db.column
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(100), nullable = False)
    complete = db.Column(db.Integer, default = 0) 
    created = db.Column(db.DateTime, default = datetime.utcnow) 

    #for debugging readability purposes
    def __repr__(self) -> str:
        return f"Task{self.id}"




#buildin on top of the sql connection to handle http request. what does handling http request mean?
@app.route("/", methods=["POST","GET"]) #route in an endpoint
#user simply visitn page is GET request
#user submitting new task is POST req, store in database
def index():
    #add a task. what is a request here? a req is like submitting a form, load a webpage, 
    if request.method == "POST":
        #form sends the content and flask uses the data to create a new task in the table.
        # This looks for the input field with name="content" and gets the value that the user entered in that field. we are stroing 
        #the content in current task so that we can use this value else where or for modifyin the input before saving it
        current_task = request.form['content']
        #creating an instance of the blueprint MyTask/represents row in db and is filled with content which is data typed in the form.
        new_task = MyTask(content = current_task)
        # We want to create a new row in the tasks table with a value for the content column. why is it in try and exception
        #because working with db means the connection can fail or data inserted is invalidates. we dont want prog to crash if this case
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    else:
        #tasks is a local variable inside route func. holds result of query we want to feed this to index.html
        tasks = MyTask.query.order_by(MyTask.created).all()
        #this tasks is a template variable you are passing to the HTML file
        #cann be accessed using jinja like {{tasks}} to display on web page
        return render_template('index.html', tasks = tasks) #passing keyword arguments: dynamially redner this in the html file
        #name for keyword argument you have to access in the html file. go into html file and to display them use double {} and put it in that




@app.route("/delete/<int:id>") #flask assumes/defaults to get method if not specified
#url processors means u can hav variable in url itself that u can handle in the ducntion
def delete(id:int): #id is paramater. this is called type hinting. when i click the delete button a req is send to this and this func gets trigegred
    
    delete_task = MyTask.query.get_or_404(id) #where does flask get value fo id from
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"

@app.route("/edit/<int:id>", methods = ["GET","POST"])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template('edit.html', task = task)


    return render_template("index.html")


if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

 