import os

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy


import forms


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = '4654f5dfadsrfasdr54e6rae'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bill.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "information"


association_table = db.Table('association', db.metadata,
        db.Column('customer.id', db.Integer, db.ForeignKey('customer.id')),
        db.Column('group_id', db.Integer, db.ForeignKey("group.id"))
)

class Group(db.Model):
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key=True)
    groupsid = db.Column(db.String(50), unique=True, nullable=False)
    tripto = db.Column(db.String(50), unique=True, nullable=False)
    customers = db.relationship("Customer", secondary=association_table, back_populates="groups")
    
class Bill(db.Model):
    tablename__ = "bill"
    id = db.Column(db.Integer, primary_key=True)
    ammount = db.Column(db.Integer,  nullable=False)
    descriptionn = db.Column(db.String(100), nullable=False)
        
    
class Customer(db.Model, UserMixin):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(160), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(40), unique=True, nullable=False)
    groups = db.relationship("Group", secondary=association_table, back_populates="customers")

@login_manager.user_loader
def load_user(customer_id):
    return Customer.query.get(int(customer_id))

@app.route("/register", methods=['GET', 'POST'])
def register():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('new_group'))
    form = forms.registerform()
    if form.validate_on_submit():
        code_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        customer = Customer(fullname=form.fullname.data, email=form.email.data, password=code_password)
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('new_group'))
    return render_template('register.html', form=form)


@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('new_group'))
    form = forms.loginform()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer and bcrypt.check_password_hash(customer.password, form.password.data):
            login_user(customer)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('new_group'))
        else:
            flash('You cant login, check email or password')
    return render_template("/login.html", form=form)

@app.route('/groups', methods=["GET","POST"])
def new_group():
    form = forms.Groups()
    if form.validate_on_submit():
        group1 = Group(groupsid=form.groupsid.data, tripto=form.tripto.data)
        db.session.add(group1)
        db.session.commit()
        return redirect(url_for('new_group'))
    group_list = Group.query.all()
    return render_template('groups.html', form=form, group_list=group_list)

@app.route('/bills', methods=["GET","POST"])
def new_bills():
    form = forms.bills()
    if form.validate_on_submit():
        bills = Bill(ammount=form.ammount.data, descriptionn=form.descriptionn.data)
        db.session.add(bills)
        db.session.commit()
        return redirect(url_for('new_bills'))
    new_bills = Bill.query.all()
    return render_template('bills.html', form=form, new_bills=new_bills)



if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.run(host='localhost', port=8000, debug=True)