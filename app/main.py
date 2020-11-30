from fastapi import FastAPI,Request,HTTPException
import requests,json,logging
from app.MyCrab import Telegram
from configparser import ConfigParser as CF
from app.MsgClass import tgUpdate, lnUpdate , LINE_MSG
from typing import List

#from linebot import LineBotApi ,WebhookHandler
#from linebot.exceptions import InvalidSignatureError
#from linebot.models import TextMessage,TextSendMessage,MessageEvent
#from CK_Book import BOOK
Config = CF(allow_no_value=True)
Config.optionxform = str
Config.read('set.ini')
TGconf = Config['Telegram']
LNconf = Config['LINE']
myT = Telegram(TGconf['token'],TGconf['cid'])
myL = LINE_MSG(LNconf['Channel_Token'])
baseurl='https://api.telegram.org/bot{}/{}'
Tmethod_setHook = 'setWebhook?url={}'

app = FastAPI()
#line_bot_api = LineBotApi(LNconf['Channel_Token'])
#LNhandler = WebhookHandler(LNconf['Channel_Secret'])
logger = logging.getLogger("app")
logging.basicConfig(level = logging.DEBUG,
                    format = '%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt ='%Y-%m-%d %H:%M',
                    handlers = [logging.FileHandler('james.log','a','utf-8')]
                    )

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/hoook")
async def Thoook (updates : tgUpdate = None):
    return updates

@app.get("/Setini")
def set_ini():
    #myINI = TGconf
    return {'OK':'200'}

@app.post("/SetTGHook")
def set_TG_hook (keyname : str):
    set_url= 'https://chienfs.synology.me:8443/hoook'
    url = baseurl.format(TGconf['token'],Tmethod_setHook.format(set_url))
    
    with open('/app/httpskey/'+keyname,'rb') as f:
        A = requests.post(url,files=(('certificate',f),))
    return A.json()

@app.get("/delTGHook")
def del_TG_hook():
    url = baseurl.format(TGconf['token'],Tmethod_setHook.format(''))
    A = requests.get (url)
    return A.json()

@app.get("/TGHookstaus")
def status_TG_hook():
    Tmethod = 'getWebhookInfo'
    url = baseurl.format(TGconf['token'],Tmethod)
    A = requests.get(url)
    return A.json()

@app.post("/LineHoook")
async def Lhoook(req : Request):
    sig = req.headers['X-Line-Signature']
    bdb = b''
    async for t in req.stream():
        bdb += t
    body = bdb.decode()
    #logging.debug(body)
    try :
        ### json.loads(a) 將json格式的 a:str 轉為 dict， 
        ### json.dumps(a) 將 a:dict 轉為 json格式的字串
        #logging.debug(json.loads(body))
        B = LINE_MSG.CHK_Cert(LNconf['Channel_Secret'],body)
        logging.debug({'sig:{},\n=====:{}'.format(sig.encode(),B)})
        myL.MsgReact(json.loads(body))
        #if B != sig:
        #    raise HTTPException( status_code=404,\
        #                         detail="Signature error")
    except Exception as e:
        logging.error(e)
    return {'200':'OK'}

'''
@LNhandler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    logging.debug("OK , We got into the Message handler")
    txt = event.message.text
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=txt))
'''