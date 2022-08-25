import sqlite3
from datetime import date,datetime
def getCat():
    conn=sqlite3.connect('pos.db')
    rows=[]
    con=conn.execute('select pCat,pDesc,count(*) as number,sum(pCost) as total_cost,sum(pPrice) as total_price from products group by pCat')
    for row in con:
       rows.append(row)
    return rows
def getProdCat():
    conn=sqlite3.connect('pos.db')
    rows=[]
    cur=conn.execute('select pName,pCat,count(*) as No_Products,sum(pCost) as total_cost,sum(pPrice) as total_Price from products group by pName')
    for row in cur:
        rows.append(row)
    return rows
def getProds():
    conn=sqlite3.connect('pos.db')
    products=[]
    rows=conn.execute('select pid,serial,pName,pPrice from products')
    for row in rows:
        products.append(list(row))
    return products
def scanOut(name):
    items=[]
    conn=sqlite3.connect('pos.db')
    con=conn.cursor()
    sales=con.execute('select serial,pname,pImage,pQuant,pPrice,pCost,pPrice-pCost as total_profit from products where pname=?',(name,))
    for sale in sales:
        items.append(sale)
    con.close()
    return items
def prodOut(serial):
    conn=sqlite3.connect('pos.db')
    conn.execute('delete from products where serial=?',(serial,))
    conn.commit()
def prodChange(qty,name):
    conn=sqlite3.connect('pos.db')
    conn.execute('update products set pQuant=pQuant-? where pname=?',(qty,name,))
    conn.commit()
def salesFilter():
    allSales=[]
    conn=sqlite3.connect('pos.db')
    con=conn.cursor()
    sales=con.execute('select sDate from sales')
    for sale in sales:
        allSales.append(datetime.strptime(sale[0].split(" ")[0],"%Y-%m-%d"))
    return len([i for i in allSales if str(i).split(" ")[0]==str(date.today()).split(" ")[0]])
def prodFilter():
    tdyProd=[]
    conn=sqlite3.connect("pos.db")
    con=conn.cursor()
    prods=con.execute('select pDate from products')
    for prod in prods:
        tdyProd.append(datetime.strptime(prod[0].split(" ")[0],"%Y-%m-%d"))
    return len([i for i in tdyProd if str(i).split(" ")[0]==str(date.today()).split(" ")[0]])
def remvSale(name,quant):
    conn=sqlite3.connect("pos.db")
    conn.execute('update sales set sPrice= ',(name,))
    conn.commit()
def retProd(name):
    pass







