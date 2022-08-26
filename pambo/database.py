from pambo import posData,logins
from datetime import datetime
from flask_login import current_user,UserMixin,login_user,logout_user,UserMixin,login_required,LoginManager
class posUsers(posData.Model,UserMixin): #users auth table
    id=posData.Column(posData.Integer,primary_key=True)
    user=posData.Column(posData.String(100),nullable=False)
    password=posData.Column(posData.String(100),nullable=False)
    image=posData.Column(posData.String(100),nullable=True)
    def __repr__(self):
        return str(self.id)
class category(posData.Model): # products category table
    catId=posData.Column(posData.Integer,primary_key=True)
    catName=posData.Column(posData.String(100),nullable=False)
    catDesc=posData.Column(posData.String(100),nullable=False)
    catQuant=posData.Column(posData.Float,nullable=False)
    catStatus=posData.Column(posData.String(100),nullable=False)
    catCreator=posData.Column(posData.String(100),nullable=False)
class products(posData.Model): # actual products info
    pid=posData.Column(posData.Integer,primary_key=True)
    serial=posData.Column(posData.String(),nullable=False,default="0")
    pname=posData.Column(posData.String(100),nullable=False)
    pDesc=posData.Column(posData.String(100),nullable=True)
    pCat=posData.Column(posData.String(100),nullable=False)
    pImage=posData.Column(posData.String(100),nullable=True)
    pQuant=posData.Column(posData.Float,nullable=False)
    pCost=posData.Column(posData.Float,nullable=False)
    pPrice=posData.Column(posData.Float,nullable=False)
    pStatus=posData.Column(posData.String(100),nullable=False)
    pDate=posData.Column(posData.DateTime,nullable=False,default=datetime.utcnow)
    pShop=posData.Column(posData.String(100),nullable=False)
    pCreator=posData.Column(posData.String(100),nullable=False)
class sales(posData.Model): # sales info
    sid=posData.Column(posData.Integer,primary_key=True)
    serial=posData.Column(posData.String(100),nullable=False)
    scode=posData.Column(posData.String(100),nullable=False)
    sname=posData.Column(posData.String(100),nullable=False)
    sImage=posData.Column(posData.String(100),nullable=True)
    sDate=posData.Column(posData.DateTime,nullable=False,default=datetime.utcnow)
    sCost=posData.Column(posData.Float,nullable=False)
    sPrice=posData.Column(posData.Float,nullable=False)
    sDisc=posData.Column(posData.Float,nullable=True)
    sQuant=posData.Column(posData.Float,nullable=True)
    sProfit=posData.Column(posData.Float,nullable=False)
    sCreator=posData.Column(posData.String(100),nullable=False)
class customer(posData.Model): # customer info 
    cUid=posData.Column(posData.Integer,primary_key=True)
    cUname=posData.Column(posData.String(100),nullable=False)
    cUphone=posData.Column(posData.String(100),nullable=False)
    cUloc=posData.Column(posData.String(100),nullable=False)
    cUtic=posData.Column(posData.String(100),nullable=True)
class dictionary(posData.Model):
    did=posData.Column(posData.Integer,primary_key=True)
    dname=posData.Column(posData.String(100),nullable=False)
class expenses(posData.Model):
    eid=posData.Column(posData.Integer,primary_key=True)
    amnt=posData.Column(posData.Float,nullable=True)
    edesc=posData.Column(posData.String(100),nullable=True)
    edate=posData.Column(posData.DateTime,nullable=True)
#----load users
