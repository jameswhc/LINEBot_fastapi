from time import sleep
from app.MyCrab import MYSITE,crab

__all__ = ['BOOK']
class BOOK(crab):
    '''
    本模組用來檢查小說網站是否有更新資料
    '''
    def check(self):
        aheaders = {'Host':'m.twfanti.com'}
        #aparams = { 'sort':'desc'}
        CW = self.Sec['check word']
        url = 'https://{}/'.format(aheaders['Host'])
        if not crab.Config.has_section(self.secName) :
            self.logging ('\t未定義 {} Config\r\n'.format (self.secName))
            return 2
        #if len(self.Sec['keyword']) > 20:
        ref = self.Sec['Href']
        url = ref
        #--end if
        try :
            res = MYSITE (url , headers = aheaders)
            tempD = res.soup.select('span')[1]
            chkD = str(tempD.text.strip())
            if chkD == CW :
                self.logging('\t{0} {1} 未有更新\n'.format(self.Sec['Name'],chkD))
                return 0
            else :
                msg = '{0} 發佈更新 {1}\n'.format(self.Sec['Name'],chkD)
                self.Sec['check word'] = chkD
                self.notify(msg + ref +'\n#小說更新')
                self.logging('\t{}'.format(msg))
        except Exception as e:
            print (e)
            self.logging ('\t{}網站連結失敗\r\n'.format(self.secName))
        finally :
            pass

