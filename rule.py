# 190312 CFE rule module
# load pattern str to make zen filter
#  1-20: use vector filter, 21-25: use xfilter
from card import Card, Cards
from collections import Counter
from ring import Ring


def _getVect(crds,field):
    assert isinstance(crds,Cards), "TypeError: not Cards"
    assert field in {"xing", "lv"}, "TypeError: invalid field"
    if field == 'xing':
        vLst = [c.getXingId() for c in crds]
    else:
        vLst = [c.getLv() for c in crds]
    cout = Counter(vLst)
    vect = [cout[i] for i in range(5)]
    # print('_getVect(): vLst -> ', vLst)
    # print('_getVect(): cout[] -> ', cout)
    # print('_getVect(): vect[] -> ', vect)
    return vect
def _getPatType(crds,field):
    assert isinstance(crds,Cards), "TypeError: not Cards"
    assert field in {"xing", "lv"}, "TypeError: invalid field"
    if field == 'xing':
        vLst = [c.getXingId() for c in crds]
    else:
        vLst = [c.getLv() for c in crds]
    pat = [1 if i in vLst else 0 for i in range(5)]
    w = [1,2,4,8,16]
    n = sum(pat) # number of elements
    val = sum([w[i] * pat[i] for i in range(5)]) # val by binarry encoding
    patType = []
    if field == 'xing': # this test only for xing
        if len(crds) == n:
            patType.append('flat')
        if n == 3 and (val in {7,14,28,25,19}):
            patType.append('shen')
        if n == 3 and (val in {13,26,21,11,22}):
            patType.append('ker')
        else: pass
    if n == 1:
        patType.append('same')
    # print('_getPatType(): vLst -> ', vLst)
    # print('_getPatType(): pat -> ', pat)
    # print('_getPatType(): n -> ', n)
    return patType
def _getSum(crds): # use at effect
    vect = _getVect(crds,'lv')
    return sum(vect)

def makeVecFilter(s): # "Voo" ex: V2M1G1H, len=7
    def vecFilter(vec,crds):
        cVect = _getVect(crds,'xing')
        return all([vec[i] == cVect[i] for i in range(5)])

    assert s[0]=='V' and len(s)>=3 and len(s)%2==1, 'wrong format'
    # TODO: use re to check ^V(\d[GSMHT])+$
    vec=[0,0,0,0,0]
    t2i={'J':0,'S':1,'M':2,'H':3,'T':4}
    for i in range(1,len(s),2):
        t = s[i+1] # get ty
        x = t2i[t] # get ty id
        vec[x] = int(s[i]) # set val
    # print('makeVecFilter(): vec[] -> ',vec)
    return lambda crds: vecFilter(vec,crds)
def makeNumFilter(s): # "N."
    def numFilter(n,crds):
        return n == len(crds)

    assert s[0]=='N' and len(s)==2, 'wrong format'
    # TODO: use re to check ^N\d$
    n = int(s[1])
    return lambda crds: numFilter(n,crds)
def makeXFilter(s): # "X....."
    flat = lambda crds: 'flat' in _getPatType(crds, 'xing')
    shenZen = lambda crds: 'shen' in _getPatType(crds, 'xing')
    kerZen = lambda crds: 'ker' in  _getPatType(crds, 'xing')
    sameLv = lambda crds: 'same' in _getPatType(crds, 'lv')
    assert s[0]=='X', 'wrong format'
    s = s[1:] # get string after first char
    XFilter={'flat':flat, 'sameLv':sameLv, 'shenZen':shenZen, 'kerZen':kerZen}
    return lambda crds: XFilter.get(s)(crds)
def makeFilter(s): # str may has ','
    def makeOneFilter(s): # -> one filter func()
        assert type(s) is str, "TypeError: need str"
        # print('makeFlt() s -> ', s)
        if s[0]=='V':
            return makeVecFilter(s)
        elif s[0]=='N':
            return makeNumFilter(s)
        elif s[0]=='X':
            return makeXFilter(s)
        else:
            raise ValueError("invalid str")
    def makeCompositeFilter(sLst): # as strLst
        # print('makeCompFlt() sLst -> ', sLst)
        flts = [ makeOneFilter(s) for s in sLst]
        return lambda s: all([f(s) for f in flts])

    assert type(s) is str, "TypeError: need str"
    # print('makeFlt(): s ->', s)
    strLst = s.split(',') # as strLst
    assert len(strLst)>0, "ValueError: empty list"
    if len(strLst)==1: return makeOneFilter(strLst[0])
    else: return makeCompositeFilter(strLst)

zenRules = [
"V1J", "V1S", "V1M", "V1H", "V1T", 
"V2J", "V2S", "V2M", "V2H", "V2T", 
"V3J", "V3S", "V3M", "V3H", "V3T", 
"V2J1H1S", "V2S1T1M", "V2M1J1H", "V2H1S1T", "V2T1M1J", 
"N5,Xflat", "N5,XsameLv", "N3,XshenZen", "N3,XkerZen", "N2,Xflat" ]
zenFilter = [makeFilter(s) for s in zenRules] # str -> filter

def match(selC): # -> actionList#zid[]
    tierMap = [[0,1,2,3,4],[5,6,7,8,9,24],[10,11,12,13,14,22,23],
              [15,16,17,18,19],[20,21]]
    actionList = []
    # print('tierMap[%d] -> %s' % (len(selC) - 1, tierMap[len(selC) - 1]))
    for x in tierMap[len(selC) - 1]:
        if zenFilter[x](selC):
            actionList.append(x) # add zid
    return actionList

_getPid = lambda pid: pid
_getPreId = lambda n, pid: n - 1 if pid == 0 else pid - 1
_getNextId = lambda n, pid: pid + 1 if pid < n else 0

def _getObjId(n_player,pid, zid):
    toPre = {0,1,2,3,4,5,10,11,12,13,14,18,21}
    toNext = {15,19,23}
    toSelf = {6,7,8,16,17,22,24}

    if zid in toPre: # get pre, LEFTA
         return _getPreId(n_player, pid)
    elif zid in toSelf: # get self
        return _getPid(pid)
    elif zid in toNext:
        return _getNextId(n_player, pid)
    else:
        return None

def _getVal(selC, zid):
    valType = [1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 3, 3, 3, 3, 3,\
            0, 4, 4, 4, 0, 0, 5, 3, 3, 0]
    s = _getSum(selC)
    if valType == 1:
        return s + 4
    elif 1 < valType < 5:
        return s * valType
    elif valType == 5:
        # TODO: call func to get len(LEFTA.Hand)
        return 15 * 1
    else:
        return None
isAtt = lambda zid: zid in {0,1,2,3,4,5,10,11,12,13,14,18,21}
isSpell = lambda zid: zid in {6,7,8,9,15,16,17,19,20,22,23,24}
def effect(pid, selC, zid): # p play(selC, zid)
    if zenFilter[zid](selC):
        print('player#%s deal %s to use zid#%d' % (pid, selC, zid))
    
    objId = _getObjId(2, pid, zid)
    val = _getVal(selC, zid)
    # 檢查上家被動陣法
    # 查表、計算點數，準備輸出的資料位置。
    # 修正數值：五行生剋、物理打盾
    # 最終結果
    # TODO: add log to system
    # TODO: change state of game

if __name__ == '__main__':
    # print('test _getVect()')
    # crds = Cards([1,3,5])
    # print('cards xing -> ', _getVect(crds,'xing'))
    # print('cards lv -> ', _getVect(crds,'lv'))
    # print('test _getPatType()')
    # print('_getPatType(crds) -> ', _getPatType(crds,'xing'))

    crds_z15 = Cards([1,1,2,4])
    # v2J1H1S = makeVecFilter('V2J1H1S')
    # print('test vectFilter v2J1H1S(crds) -> ', crds_z15, v2J1H1S(crds_z15))
    print('test match(z15) -> ', crds_z15, match(crds_z15))
    print('getVect(z15) -> ', _getVect(crds_z15, 'xing'))

    crds_z22 = Cards([1,2,3])
    # n3 = makeNumFilter('N3')
    # print('test numFilter n3(crds) -> ', crds_z22, n3(crds_z22))
    # xflat = makeXFilter("Xflat")
    # print('test xFilter xflat(crds) -> ', crds_z22,  xflat(crds_z22))
    print('test match(z22) -> ', crds_z22, match(crds_z22))
    print('getPatType(z22) -> ', _getPatType(crds_z22, 'xing'))

    # for i in zenFilter: print(i)
    