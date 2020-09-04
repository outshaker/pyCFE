from random import randint, choice

zstr = ["金", "水", "木", "火", "土",
        "武器", "封印", "防禦", "反震", "幻化",
        "大金", "大水", "大木", "大火", "大土",
        "光芒", "歸元", "氣壁", "震爆", "混沌",
        "五行輪迴", "五流歸一", "生陣", "剋陣", "空城"]

zTier = [1, 1, 1, 1, 1, 2, 0, 0, 0, 2, 3, 3, 3, 3, 3, 0, 4, 4, 4, 0, 0, 0, 3, 3, 0]
# z21 五流歸一採用自己的判定

zEfct = [1,1,1,1,1,1,5,6,7,0,1,1,1,1,1,8,2,3,1,0,9,1,2,4,0]
zEfctStr = ["無行動", "受傷", "補血", "叫盾", "扣盾", "封印", "防禦", "反震", "中光芒", "輪迴"]

zRltv = [2,2,2,2,2,2,1,1,1,2,2,2,2,2,2,3,1,1,2,3,4,2,1,3,0]
objIDStr = ["玩家1", "玩家2", "雙方", "無對象"]

zAtkTy = [1,2,3,4,5,6,0,0,0,0,1,2,3,4,5,0,0,0,6,0,0,7,0,0,0]
atkTyStr = ["未定義","金行", "水行", "木行", "火行", "土行", "物理", "特殊"]
isWuXingAtk = lambda atkTy: type(atkTy) is int and 1<=atkTy<=5

# 判斷五行生剋
def chkShenKer(x,y): # x is LEFTA, y is self
	diff = y - x
	if diff in {1, -4}: # x shen y
        return 1
    elif diff in {2, -3}: # x ker y
        return 2
    elif diff == 0: # x same as y
        return 3
    else: # no implement this
        return None

#修飾語句
# 傷害兩倍
def fixDbDmg(s):
    if s['efct'] == 1:
        s['val'] = s['val'] * 2

# 傷害減半
def fixHlfDmg(s):
    if s['efct'] == 1:
        s['val'] = math.ceil(s['val'] / 2)

# 傷害轉治療
def fixHeal(s):
    if s['efct'] == 1:
        s['efct'] = 2 # EFCT_HEAL

turn = 0
endturn = 49

def rAction(zid = None): # -> zenID, zenVal
    if zid != None and 0 <= zid <= 24:
        zenID = zid
    else:
        zenID = randint(0,24) # 0-24
        
    zenTier = zTier[zenID]
    zenList = [randint(1,5) for i in range(zenTier)]
    val = sum(zenList)

    if zenID == 9: # 幻化保留自己的組合點數作為陣法數值
        zenVal = val
    elif zenTier == 1:
        zenVal = val + 4
    elif zenTier > 1:
        zenVal = val * zenTier
    else:
        zenVal = None

    return zenID, zenVal

def rAtk():
    atkZenLst = [0,1,2,3,4,5,10,11,12,13,14,18,21]
    zid = choice(atkZenLst)
    return rAction(zid)

# TODO: 計算五流歸一的數值，需要場面資訊:上家手牌數
def effect1(plyID, zenID, zenVal): # -> objID, efctID, zenVal
    if zRltv[zenID] == 0: # no object
        objID = 3
    elif zRltv[zenID] == 1: # self
        objID = plyID
    elif zRltv[zenID] == 2: # pre, up
        objID = (plyID + 1) % 2
    elif zRltv[zenID] == 3: # next, down
        objID = (plyID + 1) % 2
    elif zRltv[zenID] == 4: # both
        objID = 2
    else:
        objID = 3
    efctID = zEfct[zenID]

    return objID, efctID, zenVal

# def execute(objID, efctID, zenVal):

# def showEfct(s):



def testGameLoop():
    while True:
        plyID = turn % 2 # 0, 1
        zenID, zenVal = rAction()
        zen = zstr[zenID]
        #封裝：[玩家代號, 陣法代號, 陣法數值]
        #格式：回合n 玩家 陣法名稱 陣法數值 資料封裝
        
        zcode = [plyID, zenID, zenVal]
        if zenVal:
            print(f'回合{turn+1} 玩家{plyID+1} {zen} {zenVal}\t{zcode}')
        else:
            print(f'回合{turn+1} 玩家{plyID+1} {zen}\t{zcode}')
        
        # TODO: 根據玩家血量判定是否結束模擬
        turn += 1
        if turn > endturn:
            break
            
def testAllZen():
    for i in range(0,25):
        zid, zval = rAction(i)
        objID, efctID, zenVal = effect1(0, zid, zval)
        # plyID, efctID, objID, zenVal
        if efctID == 1:
            print(f'{zstr[zid]}\t{objIDStr[objID]} {atkTyStr[zAtkTy[zid]]}攻擊 {zenVal}')
        else:
            print(f'{zstr[zid]}\t{objIDStr[objID]} {zEfctStr[efctID]} {zenVal}')

def testAllAtkTy():
    for i in range(0,8):
        if isWuXingAtk(i):
            print(f'{atkTyStr[i]}攻擊是五行攻擊')
        else:
            print(f'{atkTyStr[i]}攻擊不是五行攻擊')

def testAllFix():
    zid, zval = rAtk()
    objID, efctID, zenVal = effect1(0, zid, zval)
    efctSt = {'obj':objID, 'efct':efctID, 'val':zenVal}
    
#testGameLoop()
#testAllZen()
testAllAtkTy()
