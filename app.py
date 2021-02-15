from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import  SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
#from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False, index=True, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return '<Task %r>' % self.id

# main route
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method =="POST":
        received_task = request.form['content']
        create_task_in_db = Todo(content = received_task)
        try:
            db.session.add(create_task_in_db)
            db.session.commit()
            return redirect('/')
        except:
            return 'Task was not created successfully'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

# DElete route
@app.route('/delete/<int:id>')
def deleteTask(id):
    task_to_del = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_del)
        db.session.commit()
        return redirect('/')
    except:
        return 'Deletion could not be done. '

#PUT ROUTE
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error in updating the task'
    else:
        return render_template('update.html', task = task)
    

if __name__ == "__main__":
    app.run(debug=True) 