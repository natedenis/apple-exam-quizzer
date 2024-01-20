from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)


class QuestionForm(FlaskForm):
    text = StringField('Question', validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(50), nullable=False)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(text=form.text.data, answer=form.answer.data)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('questions'))
    return render_template('add.html', form=form)


@app.route('/questions')
def questions():
    questions = Question.query.all()
    return render_template('questions.html', questions=questions)


if __name__ == '__main__':
    app.run(debug=True)
