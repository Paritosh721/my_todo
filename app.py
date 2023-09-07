from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
#sqlalchemy- it facilitates us to make changes in the database using python 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_DATABASE_MODIFICATIONS'] = False
with app.app_context():
    db= SQLAlchemy(app)

class Todo(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.SNo} - {self.title}"
    
@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index1.html', allTodo=allTodo)

    # we don't know CSS 
    # so Bootstrap is a website where someone has done the front end coding for you
    # return 'Hello, World!'

@app.route('/products')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route('/update/<int:SNo>', methods=['GET', 'POST'])
def update(SNo):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(SNo=SNo).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    todo = Todo.query.filter_by(SNo=SNo).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:SNo>')
def delete(SNo):
    todo = Todo.query.filter_by(SNo=SNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


#if we don't write the following two lines then the app will not run
# if we put debug = False then we won't be able to see the error.
if __name__ == "__main__": 
    app.run(debug=True, port = 5000)