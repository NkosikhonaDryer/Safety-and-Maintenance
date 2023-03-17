from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
from wtforms.validators  import InputRequired, Length, ValidationError
import getpass


db = SQLAlchemy() 
main = Flask(__name__)
main.secret_key = "secretkey"
main.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
db.init_app(main)



login_manager = LoginManager()
login_manager.init_app(main)
login_manager.login_view ="login" 

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))


class Account(db.Model,UserMixin):
    __tablename__='Account'
    id= db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    role = db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return '<Account %r' %self.id
    


    
 

class Block(db.Model):
    __tablename__='blocks'
    id= db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable=False,unique=True)
    campus_name = db.Column(db.String(200),nullable=False,unique=True)
    team_email = db.Column(db.String(200),nullable=False,unique=True)

    def __repr__(self):
        return '<Block %r' %self.id
    



class Report(db.Model):
    __tablename__='reports'
    id= db.Column(db.Integer,primary_key=True)
    campus_name = db.Column(db.String(200),nullable=False)
    block_name = db.Column(db.String(200),nullable=False)
    room_name = db.Column(db.String(200),nullable=False)
    team_email = db.Column(db.String(200),nullable=False)
    status = db.Column(db.String(200),nullable=False)
    status_num = db.Column(db.Integer,nullable=False)
    report_description =db.Column(db.String(500),nullable=False)



    def __repr__(self):
        return '<Report %r' %self.id
    


    
   

@main.route('/maintdash',methods= ['POST', 'GET'])
def maintdash():

    if request.method =='POST':
        name = request.form['block_name'].lower()
        campus_name = request.form['campus_name'].lower()
        team = request.form['team']

        bloc = Block(name = name,team_email =team, campus_name = campus_name)
        try:
            db.session.add(bloc)
            db.session.commit()

            bl = Block.query.all()
            return redirect('maint/maintdash.html')
    
        except:
            return redirect('maint/maintdash.html')

            
        
    else:
        rep = Report.query.all()

        return render_template('maint/maintdash.html',rep=rep)
    




@main.route('/blocks',methods= ['POST', 'GET'])
def blocks():

    if request.method =='POST':
        name = request.form['block_name'].lower()
        campus_name = request.form['campus_name'].lower()
        team = request.form['team']

        bloc = Block(name = name,team_email =team, campus_name = campus_name)
        try:
            db.session.add(bloc)
            db.session.commit()

            bl = Block.query.all()
            return redirect('/blocks')
    
        except:
            return redirect('/blocks')

            
        
    else:
        bloc = Block.query.all() 
        staff = Account.query.filter_by(role ='maintenance').all()

        return render_template('admin/blocks.html',bloc = bloc,staff = staff)
    


@main.route('/report',methods= ['POST', 'GET'])
def report():



    if request.method =='POST':
        blkid = request.form['blkid'].lower()
        room_name = request.form['room_name']
        des = request.form['des']

        blk = Block.query.filter_by(id =blkid).first()

        staff = Report(campus_name = blk.campus_name, block_name = blk.name, room_name = room_name,team_email = blk.team_email,status="reported",status_num =1,report_description=des)
        db.session.add(staff)
        db.session.commit()
        try:
            db.session.add(staff)
            db.session.commit()
            return redirect('/report')
    
        except:
            return redirect('/report')

            
        
    else:
        blks = Block.query.all()

        return render_template('report.html',blks = blks)
    





@main.route('/staff',methods= ['POST', 'GET'])
def staff():


    if request.method =='POST':
        email = request.form['email'].lower()
        password = request.form['password']
        role = request.form['role']

        staff = Account(email = email, password = password, role =role)
        try:
            db.session.add(staff)
            db.session.commit()
            return redirect('/staff')
    
        except:
            return redirect('/staff')

            
        
    else:
        staff = Account.query.all() 
        return render_template('admin/staff.html',staff = staff)
    


@main.route('/',methods=['POST','GET'])
def index():


    user = Account.query.filter_by(email = 'admin@gmail.com').first()
    if user:

        reps = Report.query.all()
            
        return render_template('main.html',reps = reps)


    else:
        new_user = Account(email ='admin@gmail.com',password='Admin@123',role ='admin')
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        
        except:

            reps = Report.query.all()

            return render_template('main.html',reps = reps)



@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')


@main.route('/login',methods= ['POST', 'GET'])
def login():


    if request.method =='POST':
        user_email = request.form['email'].lower()
        user_password = request.form['password']
        user = Account.query.filter_by(email = user_email).first()

        
        if user:
            if user.password == user_password:
                login_user(user)
                if user.role == 'admin':
                    return redirect(url_for('admin'))
                
                if user.role == 'maintenance':
                    return redirect(url_for('maintdash'))
                
                if user.role == 'lecture':
                    return redirect(url_for('lecturedash'))

                else:
                     return redirect(url_for('index'))
                
            else:
                return render_template('/login.html')
        
    else:
        uss = Account.query.all()
        return render_template('/login.html',uss = uss)
    


@main.route('/createaccount',methods=['POST','GET'])
def createaccount():

    if request.method =='POST':
        user_email = request.form['email'].lower()
        user_password = request.form['password']
        
        new_user = Account(email = user_email,password= user_password,role ='student')
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
    
        except:
            return 'The was an issue when creating your account'

    else:
        return render_template('createaccount.html')






@main.route('/admin')
@login_required
def admin():
    return render_template('admin/admin.html')





if __name__ == "__main__":
    main.run(debug = True) 