from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY.DATABASE.URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    def __repr__(self):
        return self.id 


db.create_all()


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        new_content = request.form['content']
        new_task = Todo(content=new_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "content cannot be added"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

    
if __name__ == "__main__":
    app.debug = True
    app.run(host='localhost', port=5000)