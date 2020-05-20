CURRENTENV = 2

STATE_OAUTH = ''
TOKEN_OAUTH_FB = ''

def appEntry():
    global CURRENTENV
    return CURRENTENV

def enableDevManage():
    global CURRENTENV
    CURRENTENV = 0
    #return CURRENTENV

def enableProdManage():
    global CURRENTENV
    CURRENTENV = 1
    #return CURRENTENV

def enableProdWsgi():
    global CURRENTENV
    CURRENTENV = 2
    #return CURRENTENV

def getOauthState():
    global STATE_OAUTH
    return STATE_OAUTH

def setOauthState(newstate=''):
    global STATE_OAUTH
    STATE_OAUTH = newstate

def getFacebookToken():
    global TOKEN_OAUTH_FB
    return TOKEN_OAUTH_FB

def setFacebookToken(newtoken=''):
    global TOKEN_OAUTH_FB
    TOKEN_OAUTH_FB = newtoken