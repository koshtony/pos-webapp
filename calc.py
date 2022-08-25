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

