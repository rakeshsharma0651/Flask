from flask import Flask,render_template,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone

#Create a Flask Instance
app = Flask(__name__)
# Secret key
app.config['SECRET_KEY']='1234567890ASDFGHJKLasdfghjkl'
# Add a database sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# add a mysql database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:India@localhost/flask'
# Initialize the database
db = SQLAlchemy(app)
# Create a Model
class Users(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255),nullable=False)
    email=db.Column(db.String(255),nullable=False,unique=True)
    date_added=db.Column(db.DateTime,default=datetime.now(timezone.utc))


class UserForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired()]) 
    submit = SubmitField("Submit")


@app.route('/user',methods=['GET','POST'])
def user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data,email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data=''
        form.email.data=''
        flash("User added sucessfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("user.html",form=form,name=name,our_users=our_users)


# Create A string 
def __repr__(self):
    return '<Name %r>' % self.name


@app.route('/')
def index():
    return "Hello world"



if __name__ == '__main__':
    app.run(debug=True)

