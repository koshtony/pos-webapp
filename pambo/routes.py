from pambo import app,posData,logins
from pambo.database import posUsers,products,sales,customer,expenses,category,dictionary,credit
from flask_login import current_user,UserMixin,login_user,logout_user,UserMixin,login_required,LoginManager
from flask import render_template,request,redirect,url_for,send_from_directory,jsonify,flash,send_file;
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime,date
from pambo.grpProd import getCat,getProdCat,scanOut,getProds,prodOut,prodChange,salesFilter,prodFilter,retProd,graphSales,catList
from pambo.calc import profSum,expSum,numProd,sumDebt,lettNum
from pambo.mtrans import stk_push
import random
import os

@logins.user_loader
def load_user(id):
    return posUsers.query.get(int(id))
@app.route('/admin',methods=["GET",'POST'])
@login_required
def admin():
    users_=posUsers.query.all()
    if current_user.user!="500":
        return render_template('403.html')
    else:
        if request.method=="POST":
            userid=request.form["userid"]
            password=request.form["password"]
            confirm=request.form["confirm"]
            if password==confirm:
                
                if posUsers.query.filter_by(user=userid).first() ==None:
                    password=generate_password_hash(password)
                    userInfo=posUsers(user=userid,password=password)
                    posData.session.add(userInfo)
                    posData.session.commit()
                    return redirect(url_for('home'))
                else:
                    flash("user already exists")

                
            else:
                flash("password does not match")
        return render_template('add_user.html',users=users_)
@app.route('/admin/del/<int:id>')
@login_required
def delUser(id):
    delUser=posUsers.query.get_or_404(id)
    posData.session.delete(delUser)
    posData.session.commit()
    return redirect(url_for('admin'))

#----- login route
@app.route('/',methods=["GET","POST"])
def login():
    # 400 @Jemoo400
    if request.method=="POST":
        userid=request.form["userid"]
        password=request.form["password"]
        users=posUsers.query.filter_by(user=userid).first()
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
    cats=category.query.all()
    return render_template('category.html',cat=cat,cats=cats)
@app.route('/add_category',methods=['GET','POST'])
@login_required
def addCat():
    if request.method=='POST':
        catName=catList(request.form["name"])
        catDesc=request.form["description"]
        catStatus=request.form["status"]
        for cat in catName:
            catInfo=category(catName=cat,catDesc=catDesc,catQuant=1,catStatus=catStatus,catCreator="")
            posData.session.add(catInfo)
            posData.session.commit()
        return redirect(url_for('catInfo'))
    return render_template('add_category.html')
# ------product route
@app.route('/category/del/<int:id>')
@login_required
def delCat(id):
    catInfo=category.query.get_or_404(id)
    posData.session.delete(catInfo)
    posData.session.commit()
    return redirect(url_for('catInfo'))
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
            print(imFile)
            if imFile.filename!="":
                imFile.save(os.path.join("./pambo/images/",secure_filename(imFile.filename)))
            posData.session.add(prodInfo)
            posData.session.commit()
            return redirect(url_for('prodInfo'))
        except:
            dict_=catList(request.form["dict"])
            for d in dict_:
                dictInfo=dictionary(
                    dname=d
                )
                posData.session.add(dictInfo)
                posData.session.commit()
            return redirect(url_for('addProd'))
    return render_template('add_product.html',cat=cat,prodDicts=prodDicts)

@app.route('/imdownload/<path:filename>')
@login_required
def prodImg(filename):
    return send_from_directory("images/",filename,as_attachment=True)
@app.route('/pos',methods=['GET','POST'])
@login_required
def posPage():
    if request.method=="POST":
        serial=request.form.get("serial")
        qty=request.form.get("qty")
        disc=request.form.get("disc")
        cname=request.form.get("cname")
        cphone=request.form.get("cphone")
        debt=request.form.get("debt")
        scans=scanOut(serial)
        print(scans)
        if len(scans)>0:
            try:
                code=int(str(random.randrange(1,100))+str(lettNum(cname)))
                print(code)
                scanned=sales(
                sid=code,
                serial=scans[0][0],scode=code,sname=scans[0][1],sImage=scans[0][2],
                sDate=date.today(),sCost=scans[0][5],sPrice=int(scans[0][4])*int(qty)-int(disc),sPriceind=int(scans[0][4]),
                sProfit=int(scans[0][4])*int(qty)-int(disc)-int(scans[0][5])*int(qty)-float(debt),sDisc=float(disc),sQuant=qty,
                sDebtin=float(debt),sDebt=float(debt),sDebtor=cname,sPhone=cphone,sCreator=current_user.user
                )
                posData.session.add(scanned)
                posData.session.commit()
                prodChange(qty,serial)
            except:
                flash("input error")
                
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
            dates=request.form["dd"]
            sumInfo=expenses(
                amnt=amount,edesc=exp,edate=datetime.strptime(dates,"%Y-%m-%d")
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
        Imfile=request.files["pi"]
        prodByid.pImage=Imfile.filename
        prodByid.pDate=date.today()
        posData.session.commit()
        if Imfile.filename!="":
            Imfile.save(os.path.join('./pambo/images/',secure_filename(Imfile.filename)))
        return redirect(url_for('prodInfo'))
    return render_template('proEdit.html',prodbyid=prodByid,prodDicts=prodDicts)
@app.route('/sales/del/<int:id>')
@login_required
def delSales(id):
    salesbyId=sales.query.get_or_404(id)
    posData.session.delete(salesbyId)
    posData.session.commit()
    return redirect(url_for('salesInfo'))
# return already sold items route
@app.route('/sales/return/<int:id>',methods=["GET","POST"])
@login_required
def retSales(id):
    sales_=sales.query.get_or_404(id)
    if request.method=="POST":
        qty=int(request.form["quant"])
        dsc=int(request.form["discount"])
        prevQty=sales_.sQuant
        sales_.sQuant=prevQty-qty
        sales_.sPrice=(prevQty-qty)*(sales_.sPriceind)
        sales_.sProfit=((prevQty-qty)*sales_.sPriceind)-((prevQty-qty)*sales_.sCost)-dsc-sales.sDebt
        sales_.sDisc=dsc
        posData.session.commit()
        retProd(int(request.form["quant"]),sales_.sname)
        return redirect(url_for('salesInfo'))
    return render_template("return.html",sales=sales_)
#----clear debt route
@app.route('/sales/debt/<int:id>',methods=["GET","POST"])
@login_required
def clearDebt(id):
    d_sales=sales.query.get_or_404(id)# debtor sales
    d_credit=credit.query.filter(credit.did==id).all() #debtors credit
    if request.method=="POST":
        paid=float(request.form["pay"])
        paydate=datetime.strptime(request.form["paydate"],"%Y-%m-%d")
        d_sales.sDebt=d_sales.sDebt-paid
        d_sales.sPay=paydate
        d_sales.sProfit=d_sales.sProfit+paid
        credit_=credit(
            did=d_sales.sid,
            dname=d_sales.sDebtor,
            amount=paid,
            ddate=paydate
        )
        posData.session.add(credit_)
        posData.session.commit()
        return redirect(url_for('salesInfo'))
    bal=d_sales.sDebtin-float(sumDebt(d_credit))
    return render_template('debts.html',sales=d_sales,credits=d_credit,bal=bal)
@app.route('/payment')
@login_required
def mpesa_pay():
    resp=stk_push()
    if resp[0]["info"]["ResponseCode"]=="0":
        return "<h1>success</h1>"
# graphical reports url
@app.route('/reports')
def graphs():
    prodx=[]
    products_ = products.query.all()
    sales_=sales.query.all()
    for prods in products_:
        scan={
        "quant":round(prods.pQuant),
        "name":prods.pname,
        "price":prods.pPrice
         }
        prodx.append(scan)
    sale_=graphSales()

    return render_template('charts.html',products=prodx,sales=sale_)
@app.errorhandler(404)
def error404(error):
    return render_template('404.html'),404
@app.errorhandler(500)
def error500(error):
    return render_template('500.html'),500
@app.errorhandler(401)
def error401(error):
    return render_template('403.html'),401
