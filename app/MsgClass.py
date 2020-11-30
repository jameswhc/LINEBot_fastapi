from pydantic import BaseModel
from typing import List
import requests, logging, json
import base64 ,hashlib, hmac

__all__ = ['tgFrom','tgChat','tgMsg','tgUpdate','Lmessage','Lsource','lnUpdate','lnevent','LINE_MSG']

class tgFrom(BaseModel):
    last_name : str = ''
    id : int
    first_name : str = ''
    username : str = ''

class tgChat(BaseModel):
    last_name : str = ''
    id : int
    first_name : str = ''
    username : str = ''

class tgMsg(BaseModel):
    date : str
    chat : tgChat = None
    message_id : str =''
    from_ : tgFrom = None
    text : str

class tgUpdate(BaseModel):
    update_id : str
    message : set = None
    
class Lmessage(BaseModel):
    id : str
    text : str
    type : str

class Lsource(BaseModel):
    type : str
    userID : str

class lnUpdate(BaseModel):
    message : Lmessage
    replyToken : str
    source : Lsource
    timestamp : int
    type : str

class lnevent (BaseModel):
    events : List [lnUpdate]
    destination : str


class LINE_MSG():
    BS_header =  {   "Content-Type" : "application/json"\
                    ,"Authorization" : "Bearer {}"\
                }
    Reply_URL = 'https://api.line.me/v2/bot/message/reply'
    Logs = None
    def __init__(self,channel_token):
        self._channel_token = channel_token
        self._headers = LINE_MSG.BS_header.copy()
    @property
    def CN_TOKEN(self):
        return self._channel_token
    @CN_TOKEN.setter
    def CN_TOKEN(self,token):
        self._channel_token = token
        self._headers.update({"Authorization":LINE_MSG.BS_header['Authorization'].format(self._channel_token)})

    @property
    def headers (self):
        self._headers.update({"Authorization":LINE_MSG.BS_header['Authorization'].format(self._channel_token)})
        return self._headers

    @classmethod
    def CHK_Cert(cls,channel_secret,body):
        hash = hmac.new(channel_secret.encode('utf-8'),body.encode('utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(hash)
        return signature

    def MsgReact(self,body:lnevent):
        try:
            Update = body['events'][0]
            reply_Token = Update['replyToken']
            msg = Update['message']
            msgtype = msg['type']
            rMsg = {"type":"text","text":"<您的訊息>"}
            rData = {"replyToken":reply_Token}
            if msgtype == 'text' : #回應文字訊息
                txt = msg['text']
                if ('Hi' in txt) or ('hi' in txt):
                    rMsg.update({"text":u"主人，您在呼叫我嗎?"})
                else:
                    rMsg.update({"text":u"抱歉，沒定義這個指令唷"})
            else:
                rMsg.update({"text":u"抱歉，只能處理文字指令唷"})
            rData.update({"messages":[rMsg,]})
            res = requests.post (LINE_MSG.Reply_URL,headers = self.headers ,json = rData)
            if res.status_code != 200 :
                logging.debug("Line 回應錯誤: {}".format (res.text))
        except:
            logging.debug(u"程式有問題唷\n {}".format(body))
            pass
