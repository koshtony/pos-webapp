def profSum(object):
    profit=[]
    price=[]
    for obj in object:
        profit.append(obj.sProfit)
        price.append(obj.sPrice)
    return sum(profit),sum(price)
def expSum(object):
    exps=[]
    for obj in object:
        exps.append(obj.amnt)
    return sum(exps)
def countRes(object1,object2):
    res1,res2=[],[]
    for obj1 in object1:
        res1.append(obj1.sid)
    for obj2 in object2:
        res2.append(obj2.pQuant)
    return len(res1),len(res2)
def numProd(object):
    total=[]
    for obj in object:
        total.append(obj.pQuant)
    return sum(total)
def zerofy(x):
    if x<0:
        x=0;
    return x
def sumDebt(credits):
    paid=[]
    for credit in credits:
        paid.append(credit.amount)
    return sum(paid)
def lettNum(letters):
    num=[str(ord(letter)) for letter  in letters]
    return splitNum(num)
def splitNum(strNum):
    if len(strNum)>4:
        strNum_="".join(strNum[0:4])
    else:
        strNum_="".join(strNum)
    return strNum_



