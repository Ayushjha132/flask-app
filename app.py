from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        new_content = request.form['content']
        new_task = Todo(content=new_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print('There was an issue with adding task')
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>',)
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There is some issues with deleting'

@app.route('/update/<int:id>',methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if(request.method == 'POST'):
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There is some issues with updating'
    else:
        return render_template('update.html', task=task)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == "GET":
        return render_template('form.html')
    else:
        name = float(request.form['math'])
        email = float(request.form['science'])
        password = float(request.form['history'])

        average_score = (name + email + password) / 3

        return render_template('form.html', score=average_score)


if __name__ == '__main__':
    app.run(debug=True)
