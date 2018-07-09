import requests

class CookiesUpdater():

    def __init__(self):
        self.s = requests.session()
        self.cookie = {}
        self.header = {}
        self.s.headers = self.header

    def login(self):



if __name__ == '__main__':
    C = CookiesUpdater()
    C.login()

#wap weibo登陆:https://passport.weibo.cn/signin/login


#get(https://login.sina.com.cn/sso/prelogin.php?
# checkpin=1&
# entry=mweibo&
# su=bnlhc29jaGFuJTQwZ21haWwuY29t& ##这个是哪来的
# callback=jsonpcallback1531033008617 ##这个是哪来的)
#su: bnlhc29jaGFuJTQwZ21haWwuY29t  -->su是不变的
#callback: jsonpcallback1531035032236  -->随机的???
#su: bnlhc29jaGFuJTQwZ21haWwuY29t
#callback: jsonpcallback1531035304028
#POST(https://passport.weibo.cn/sso/login)
# data-->cookie
#get(https://m.weibo.cn/)
# cookie-->cookie

# 我滴妈我放弃了