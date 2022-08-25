from datetime import datetime
from flask import Flask,render_template,request,redirect,url_for,send_from_directory,jsonify,flash;
from flask_login import current_user,UserMixin,login_user,logout_user,UserMixin,login_required,LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime,date
from grpProd import getCat,getProdCat,scanOut,getProds,prodOut,prodChange,salesFilter,prodFilter
from calc import profSum,expSum,countRes,numProd
import hashlib
import socket
import json
import os
import random
app=Flask(__name__,template_folder='template');
key="@piontonsale"
app.config["SECRET_KEY"]=key;
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///pos.db'
app.config["UPLOAD_FOLDER"]="./images"
posData=SQLAlchemy(app)
logins=LoginManager(app)
#-----create Database tables 
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
@logins.user_loader
def load_user(id):
    return posUsers.query.get(int(id))

# --- creating routes routes 
# ----create users
@app.route('/admin',methods=["GET",'POST'])
@login_required
def admin():
    if current_user.user!="400":
        return render_template('403.html')
    else:
        if request.method=="POST":
            userid=request.form["userid"]
            password=request.form["password"]
            password=generate_password_hash(password)
            userInfo=posUsers(user=userid,password=password)
            posData.session.add(userInfo)
            posData.session.commit()
            return redirect(url_for('home'))
        return render_template('add_user.html')
#----- login route
@app.route('/',methods=["GET","POST"])
def login():
    # 400 @Jemoo400
    if request.method=="POST":
        userid=request.form["userid"]
        password=request.form["password"]
        users=posUsers.query.filter_by(user=userid).first()
        print(password)
        if users and check_password_hash(users.password,password):
            login_user(users)
            return redirect(url_for('home'))
        else: 
            flash("invlid password or user id")

    return render_template('login.html')
# ----logout user
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
# --------home route ------

@app.route('/home')
@login_required
def home():
    cat=len(category.query.all())
    prod=round(numProd(products.query.all()),0)
    res1,res2=salesFilter(),prodFilter()
    trans=res1+res2
    salesTdy_=res1
    return render_template('home.html',cat=cat,prod=prod,trans=trans,sales=salesTdy_)
# --------category route-----

@app.route('/category')
@login_required
def catInfo():
    cat=getCat()
    return render_template('category.html',cat=cat)
@app.route('/add_category',methods=['GET','POST'])
@login_required
def addCat():
    if request.method=='POST':
        catName=request.form["name"]
        catDesc=request.form["description"]
        catStatus=request.form["status"]
        catInfo=category(catName=catName,catDesc=catDesc,catQuant=1,catStatus=catStatus,catCreator="")
        posData.session.add(catInfo)
        posData.session.commit()
        return redirect(url_for('catInfo'))
    return render_template('add_category.html')
# ------product route
@app.route('/products')
@login_required
def prodInfo():
    prods=products.query.all()
    prodGrp=getProdCat()
    return render_template('products.html',prods=prods,prodGrp=prodGrp)

@app.route('/add_products',methods=['GET','POST'])
@login_required
def addProd():
    cat=category.query.all()
    prodDicts=dictionary.query.all()
    if request.method=="POST":
        try:
            serial=request.form["serial"]
            pname=request.form["pname"]
            pdesc=request.form["pdesc"]
            pcat=request.form["pcat"]
            imFile=request.files['pi']
            pq=request.form["pq"]
            pcost=request.form["pcost"]
            pp=request.form["pp"]
            shop=request.form["shop"]
            status=request.form["status"]
            prodInfo=products(
                serial=serial, pname=pname,pDesc=pdesc,
                pCat=pcat,pImage=imFile.filename,pQuant=pq,pCost=pcost,pPrice=pp,pStatus=status,
                pDate=date.today(),pShop=shop,pCreator=""
            )
            imFile.save(os.path.join(app.config["UPLOAD_FOLDER"],secure_filename(imFile.filename)).replace("\\","/"))
            posData.session.add(prodInfo)
            posData.session.commit()
            return redirect(url_for('prodInfo'))
        except:
            dict_=request.form["dict"]
            dictInfo=dictionary(
                dname=dict_
            )
            posData.session.add(dictInfo)
            posData.session.commit()
            return redirect(url_for('addProd'))
    return render_template('add_product.html',cat=cat,prodDicts=prodDicts)

@app.route('/imdownload/<path:filename>')
@login_required
def prodImg(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"],filename)
@app.route('/pos',methods=['GET','POST'])
@login_required
def posPage():
    if request.method=="POST":
        serial=request.form.get("serial")
        qty=request.form.get("qty")
        disc=request.form.get("disc")
        scans=scanOut(serial)
        if len(scans)>0:
            code=str(scans[0][0])+str(random.randrange(1,100))
            scanned=sales(
            serial=scans[0][0],scode=code,sname=scans[0][1],sImage=scans[0][2],
            sDate=date.today(),sCost=scans[0][3],sPrice=int(scans[0][4])*int(qty)-int(disc),
            sProfit=int(scans[0][4])*int(qty)-int(disc)-int(scans[0][5])*int(qty),sCreator=""
            )
            posData.session.add(scanned)
            posData.session.commit()
            prodChange(qty,serial)
    prods=products.query.all()
    scans=[]
    for prods in prods:
        scan={
           "pid":prods.pid,
           "serial":prods.serial,
        "quant":prods.pQuant,
        "name":prods.pname,
        "price":prods.pPrice
         }
        scans.append(scan)
    return render_template('pos.html',scans=scans)
@app.route('/sales',methods=['GET','POST'])
@login_required
def salesInfo():
    if request.method=="POST":
        try:
            date1=request.form["date1"]
            date2=request.form["date2"]
            date1=datetime.strptime(date1,"%Y-%m-%d")
            date2=datetime.strptime(date2,"%Y-%m-%d")
            saleFilt = sales.query.filter(sales.sDate <= date2).\
            filter(sales.sDate >= date1)
            profit,price=profSum(saleFilt)
            return render_template('sales.html',sales=saleFilt,profit=profit,price=price)
        except:
            saleFilt = sales.query.filter(sales.sDate <= date.today()).\
            filter(sales.sDate >= date.today())
            profit,price=profSum(saleFilt)
            return render_template('sales.html',sales=saleFilt,profit=profit,price=price)

    sales_=sales.query.all()
    profit,price=profSum(sales_)
    return render_template('sales.html',sales=sales_,profit=profit,price=price)
@app.route('/summary',methods=['GET','POST'])
@login_required
def summaryInfo():
    if request.method=="POST":
        try:
            amount=request.form["amount"]
            exp=request.form["exp"]
            sumInfo=expenses(
                amnt=amount,edesc=exp,edate=date.today()
            )
            posData.session.add(sumInfo)
            posData.session.commit()
            return redirect(url_for('summaryInfo'))
        except:
            date1=request.form["date1"]
            date2=request.form["date2"]
            if date1=="" or date2=="":
                date1=str(date.today())
                date2=str(date.today())
            date1=datetime.strptime(date1,"%Y-%m-%d")
            date2=datetime.strptime(date2,"%Y-%m-%d")
            saleFilt = sales.query.filter(sales.sDate <= date2).\
            filter(sales.sDate >= date1)
            expFilt = expenses.query.filter(expenses.edate <= date2).\
            filter(expenses.edate >= date1)
            profits,_=profSum(saleFilt)
            expsum=expSum(expFilt)
            netProf=profits-expsum
            return render_template('summary.html',exps=expFilt,sales=saleFilt,profits=profits,expsum=expsum,netf=netProf)
            
    exps=expenses.query.all()
    sales_=sales.query.all()
    profits,_=profSum(sales_)
    expsum=expSum(exps)
    netProf=profits-expsum
    return render_template('summary.html',exps=exps,sales=sales_,profits=profits,expsum=expsum,netf=netProf)
@app.route('/products/delete/<int:id>')
@login_required
def delProd(id):
    delInfo=products.query.get_or_404(id)
    posData.session.delete(delInfo)
    posData.session.commit()
    return redirect(url_for('prodInfo'))
@app.route('/products/edit/<int:id>',methods=['GET','POST'])
@login_required
def editProd(id):
    prodByid=products.query.get_or_404(id)
    prodDicts=dictionary.query.all()
    if request.method=="POST":
        prodByid.pQuant=request.form["pq"]
        prodByid.pname=request.form["pname"]
        prodByid.pDesc=request.form["pdesc"]
        prodByid.pPrice=request.form["pp"]
        prodByid.pCost=request.form["pcost"]
        prodByid.pShop=request.form["shop"]
        prodByid.pDate=date.today()
        posData.session.commit()
        return redirect(url_for('prodInfo'))
    return render_template('proEdit.html',prodbyid=prodByid,prodDicts=prodDicts)
@app.route('/sales/del/<int:id>')
@login_required
def delSales(id):
    salesbyId=sales.query.get_or_404(id)
    posData.session.delete(salesbyId)
    posData.session.commit()
    return redirect(url_for('salesInfo'))
@app.route('/sales/return',methods=["GET","POST"])
@login_required
def retSales():
    pass


@app.errorhandler(404)
def error404(error):
    return render_template('404.html'),404
@app.errorhandler(500)
def error500(error):
    return render_template('500.html'),500
@app.errorhandler(401)
def error401(error):
    return render_template('403.html'),401
ip=str(socket.gethostbyname(socket.gethostname()))
if __name__=="__main__":
    app.run(host=ip,port=200,debug=True)
