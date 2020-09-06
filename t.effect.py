hp, shell, lastDealZid, nHand [, cvrTok] # plyStat
NPLAYER = 2 # the number of players
env.plyStat # store all player's stat

isBasZen = lambda zid: 0 <= zid < 25 # 0-24
isBasAtk = lambda zid: zid in {0,1,2,3,4,5,10,11,12,13,14,18,21}
isBasXinAtk = lambda zid: zid in {0,1,2,3,4,10,11,12,13,14}
isBasPhyAtk = lambda zid: zid in {5,18}
isBasSpcAtk = lambda zid: zid in {21}
isBasSpl = lambda zid: zid in {6,7,8,9,15,16,17,19,20,22,23,24}
# needVal = lambda zid: zid in {0,1,2,3,4,5,9,10,11,12,13,14,16,17,18,21,22,23}

getXinId = lambda zid: (zid % 5) + 1 if isBasXinAtk(zid) else None
getPreId = lambda n, pid: n - 1 if pid == 0 else pid - 1
getNextId = lambda n, pid: pid + 1 if pid < n else 0

def getObjId(n_player,pid, zid):
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

def getZval(selC, zid, leftaNhand):
    valType = [1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 3, 3, 3, 3, 3,\
            0, 4, 4, 4, 0, 0, 5, 3, 3, 0]
    s = _getSum(selC)
    if valType == 1:
        return s + 4
    elif 1 < valType < 5:
        return s * valType
    elif valType == 5:
        return 15 * leftaNhand
    else:
        return None

def getPlyStat(pid): # TODO
    return env.plyStat[pid]

def getLeftaStat(pid): 
    return getPlyStat(getPreId(NPLAYER,pid))

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

def _chgPlyAttr(pid, attr, val):
    stat = getPlyStat(pid)
    assert type(stat[attr]) is int, "TypeError: attr is not int "
    assert type(val) is int, "TypeError: val is not int"
    stat[attr] = stat[attr] + val if stat[attr] + val > 0 else 0 # fix negative val

def _setPlyAttr(pid, attr, val):
    stat = getPlyStat(pid)
    stat[attr] = val
    
def hurt(pid, zid, val): # 修正數值：五行生剋、物理打盾
    plyStat = getPlyStat(pid)
    undertake = 'hp'
    if plyStat['shell'] > 0:
        undertake = 'shell'
        if isBasPhyAtk(zid):
            val = val * 2
            # TODO: add tok to gamelog
    else:
        if isBasXinAtk(zid) and isBasXinAtk(plyStat['lastDealZid']):
            r = chkShenKer(getXinId(plyStat['lastDealZid']), getXinId(zid))
            if r == 1:
                val = val * (-1)
            elif r == 2:
                val = val * 2 # TODO: add tok to gamelog
            elif r == 3:
                val = math.ceil(val / 2) # TODO: add tok to gamelog
    _chgPlyAttr(pid, undertake, val)
    if undertake is 'shell' and plyStat['shell'] <= 0:
        plyStat['shell'] = None # shell is pass off. TODO: add tok to gamelog
    if undertake is 'hp' plyStat['hp'] <= 0:
        endGame(pid) # pid is lose, end game. TODO: add tok to gamelog

def heal(pid, val):
    _chgPlyAttr(pid, 'hp', val)
    
def shell(pid, val):
    _setPlyAttr(pid, 'shell', val)
    
def effect(pid, selC, zid): # p play(selC, zid)
    if zenFilter[zid](selC):
        print('player#%s deal %s to use zid#%d' % (pid, selC, zid))
    else:
        raise TypeError("invalid zen")

    leftaStat = getLeftaStat(pid)
    # 檢查上家被動陣法
    if 'defense' in leftaStat['cvrTok'] and isBasAtk(zid): # defense become effective
        zid = 24
        # TODO: add tok to gamelog
    elif 'seal' in leftaStat['cvrTok'] and isBasSpl(zid): # seal become effective
        zid = 24
        # TODO: add tok to gamelog
    elif 'reflect' in leftaStat['cvrTok'] and isBasAtk(zid): # reflect become effective
        hurtBoth = True
    
    # 查表、計算點數，準備輸出的資料位置。
    z2v = [hurt, hurt, hurt, hurt, hurt, 
    hurt, seal, defense, refelect, imitat, 
    hurt, hurt, hurt, hurt, hurt, 
    blind, heal, shell, hurt, robber, 
    samsara, conflux, heal, disperse, idle]

    func = z2v[zid]
    if func is imitat and isBasZen(leftaStat['lastDealZid']): # imitat become effective
        func = z2v[leftaStat['lastDealZid']]
    else:
        func = idle

    objId = _getObjId(NPLAYER, pid, zid)    
    zVal = getZval(selC, zid, leftaStat['nHand'])

    if func is hurt:
        if hurtBoth:
            zVal = math.ceil(zVal / 2)
            func(pid, zid, zVal)
            func(objId, zid, zVal)
        else:
            func(objId, zVal)
    elif objId and zVal:
        func(objId, zVal)
    elif objId:
        func(objId)
    else:
        func()
    _setPlyAttr(pid, 'lastDealZid', zid) # add lastDealZid
    # TODO: add log to system
    # TODO: change state of game



function _mimicry(lastDealZid,cVal)
	zid = lastDealZid if isBasZid(lastDealZid) else 24
	zVal = getVal(zid,cVal)
	return zid, zVal
end

function getHurt(s,bag)
    local v=s.val
    if bag.xShell then --shell Damage
        if _isPhyAtk(s.zid) then
            return 2, v*2, "2x"
        else
            return 2, v
        end
    elseif _isEleAtk(s.zid) and _isEleAtk(bag.lastDeal) then --element attack
        local c=_getEleRel(_getEleType(s.zid),_getEleType(bag.lastDeal))
        if c==1 then return 1, math.ceil(v/2), "0.5x"
        elseif c==3 then return 1, v*2, "2x"
        elseif c==2 then return 3, v, "-x"
        else return 1, v
        end
    else
        return 1, v
    end
end

