import datetime
from models import RandomCode,DealerRandomCode,ShopRandomCode,Latestsmtcode,CategoryId,SubcategoryId
from multiprocessing import Pool
import threading
import functools

def synchronized(wrapped):
    lock = threading.Lock()
    @functools.wraps(wrapped)
    def _wrap(*args, **kwargs):
        with lock:
            return wrapped(*args, **kwargs)
    return _wrap

class Number:
    
    def appendzeros(self,package):
        packagestr = ''
        if package <= 9:
            packagestr = '00'+str(package)
        elif package <= 99:
            packagestr = '0'+str(package)
        #elif package < 999:
            #packagestr = '0'+str(package)
        else:
            packagestr = str(package)
        return packagestr

    def getBarcode(self,lastbarcode):
        presentbarcode=''
        #datestr = datetime.date.today().strftime("%d%m%Y")
        package = 0
        packagestr = ''
        if lastbarcode:
            package = int(lastbarcode[1:3])
			
            package += 1
            packagestr = self.appendzeros(package)
            presentbarcode = packagestr
		#return package
        else:
            packagestr = self.appendzeros(1)
            presentbarcode =  packagestr
        return presentbarcode

    @synchronized
    def get(self):
        lastbarcode = RandomCode.objects()
        barcodeready=''
        if lastbarcode.count()==0:
            barcodeready = self.getBarcode('00')
        else:
            barcodeready = self.getBarcode(lastbarcode[0].number)
        return barcodeready
    
    @synchronized
    def put(self,barcodeready):
        lastbarcode = RandomCode.objects()
        
        if lastbarcode.count()==0:
            lastbarcode = RandomCode(number=barcodeready)
            lastbarcode.save()
        else:
            lastbarcode = RandomCode(id=lastbarcode[0].id)
            lastbarcode.number = barcodeready
            lastbarcode.save()
        return 'success'
    
    def deleteAll(self):
        lastBarcode = RandomCode.objects()
        lastBarcode.delete()
            
        return "success"

class DealerNumber:
    
    def appendzeros(self,package):
        packagestr = ''
        if package <= 9:
            packagestr = '000'+str(package)
        elif package <= 99:
            packagestr = '00'+str(package)
        elif package <= 999:
            packagestr = '0'+str(package)
        else:
            packagestr = str(package)
        return packagestr

    def getBarcode(self,lastbarcode):
        presentbarcode=''
        #datestr = datetime.date.today().strftime("%d%m%Y")
        package = 0
        packagestr = ''
        if lastbarcode:
            package = int(lastbarcode[1:4])
			
            package += 1
            packagestr = self.appendzeros(package)
            presentbarcode = packagestr
		#return package
        else:
            packagestr = self.appendzeros(1)
            presentbarcode =  packagestr
        return presentbarcode

    @synchronized
    def get(self):
        lastbarcode = DealerRandomCode.objects()
        barcodeready=''
        if lastbarcode.count()==0:
            barcodeready = self.getBarcode('000')
        else:
            barcodeready = self.getBarcode(lastbarcode[0].number)
        return barcodeready

    @synchronized
    def put(self,barcodeready):
        lastbarcode = DealerRandomCode.objects()
        
        if lastbarcode.count()==0:
            lastbarcode = DealerRandomCode(number=barcodeready)
            lastbarcode.save()
        else:
            lastbarcode = DealerRandomCode(id=lastbarcode[0].id)
            lastbarcode.number = barcodeready
            lastbarcode.save()
        return 'success'
    
    def deleteAll(self):
        lastBarcode = DealerRandomCode.objects()
        lastBarcode.delete()
            
        return "success"



class ShopNumber:
    
    def appendzeros(self,package):
        packagestr = ''
        if package <=9:
            packagestr = '100'+str(package)
        elif package <= 99:
            packagestr = '10'+str(package)
        elif package <= 999:
            packagestr = '1'+str(package)
        
        else:
            packagestr = str(package)
        return packagestr

    def getBarcode(self,lastbarcode):
        presentbarcode=''
        #datestr = datetime.date.today().strftime("%d%m%Y")
        package = 0
        packagestr = ''
        if lastbarcode:
            package = int(lastbarcode[1:4])
			
            package += 1
            packagestr = self.appendzeros(package)
            presentbarcode = packagestr
		#return package
        else:
            packagestr = self.appendzeros(1)
            presentbarcode =  packagestr
        return presentbarcode

    @synchronized
    def get(self):
        lastbarcode = ShopRandomCode.objects()
        barcodeready=''
        if lastbarcode.count()==0:
            barcodeready = self.getBarcode('100')
        else:
            barcodeready = self.getBarcode(lastbarcode[0].number)
        return barcodeready

    @synchronized
    def put(self,barcodeready):
        lastbarcode = ShopRandomCode.objects()
        
        if lastbarcode.count()==0:
            lastbarcode = ShopRandomCode(number=barcodeready)
            lastbarcode.save()
        else:
            lastbarcode = ShopRandomCode(id=lastbarcode[0].id)
            lastbarcode.number = barcodeready
            lastbarcode.save()
        return 'success'
    
    def deleteAll(self):
        lastBarcode = ShopRandomCode.objects()
        lastBarcode.delete()
            
        return "success"


class SMTIdNumber:
    
    def appendzeros(self,package):
        packagestr = ''
        if package < 9:
            packagestr = '00000'+str(package)
        elif package < 99:
            packagestr = '0000'+str(package)
        elif package < 999:
            packagestr = '000'+str(package)
        elif package < 9999:
            packagestr = '00'+str(package)
        elif package < 99999:
            packagestr = '0'+str(package)
        else:
            packagestr = str(package)
        return packagestr

    def getSmtid(self,SmtidCode):
        presentSmtidCode=''
        dateStr = datetime.date.today().strftime("%d%m%y")
        package = 0
        packageStr = ''
        if SmtidCode.startswith('SMT'+dateStr):
            package = int(SmtidCode[9:15])
            package += 1
            packageStr = self.appendzeros(package)
            presentSmtidCode = 'SMT'+dateStr+ packageStr
        else:
            packageStr = self.appendzeros(1)
            presentSmtidCode = 'SMT'+dateStr+ packageStr
        return presentSmtidCode

    @synchronized
    def get(self):
        lastSmtid = Latestsmtcode.objects()
        purchaseReady=''
        #return lastPurchase[0].SmtidCode
        if lastSmtid.count()==0:
            purchaseReady = self.getSmtid('000000000000')
            
        else:
            purchaseReady = self.getSmtid(lastSmtid[0].SmtidCode)
            
        return purchaseReady

    @synchronized
    def put(self, smtidCreated):
        lastSmtid = Latestsmtcode.objects()
        
        if lastSmtid.count()==0:
            lastSmtid = Latestsmtcode(SmtidCode=smtidCreated)
            lastSmtid.save()
        else:
            lastSmtid = Latestsmtcode(id=lastSmtid[0].id)
            lastSmtid.SmtidCode = smtidCreated
            lastSmtid.save()
        return "success"
    
    def deleteAll(self):
        lastSmtid = Latestsmtcode.objects()
        lastSmtid.delete()
            
        return "success"

class CatNumber:
    def appendzeros(self,package):
        packagestr = ''
        if package <=9:
            packagestr = '10'+str(package)
        elif package <= 99:
            packagestr = '1'+str(package)
     
        
        else:
            packagestr = str(package)
        return packagestr

    def getBarcode(self,lastbarcode):
        presentbarcode=''
        #datestr = datetime.date.today().strftime("%d%m%Y")
        package = 0
        packagestr = ''
        if lastbarcode:
            package = int(lastbarcode[1:4])
			
            package += 1
            packagestr = self.appendzeros(package)
            presentbarcode = packagestr
		#return package
        else:
            packagestr = self.appendzeros(1)
            presentbarcode =  packagestr
        return presentbarcode

    @synchronized
    def get(self):
        lastbarcode = CategoryId.objects()
        barcodeready=''
        if lastbarcode.count()==0:
            barcodeready = self.getBarcode('10')
        else:
            barcodeready = self.getBarcode(lastbarcode[0].categoryid)
        return barcodeready

    @synchronized
    def put(self,barcodeready):
        lastbarcode = CategoryId.objects()
        
        if lastbarcode.count()==0:
            lastbarcode = CategoryId(categoryid=barcodeready)
            lastbarcode.save()
        else:
            lastbarcode = CategoryId(id=lastbarcode[0].id)
            lastbarcode.categoryid = barcodeready
            lastbarcode.save()
        return 'success'
    
    def deleteAll(self):
        lastBarcode = CategoryId.objects()
        lastBarcode.delete()
            
        return "success"

class SubcatNumber:
    
    def appendzeros(self,package):
        packagestr = ''
        if package <=9:
            packagestr = '10'+str(package)
        elif package <= 99:
            packagestr = '1'+str(package)
        
        
        else:
            packagestr = str(package)
        return packagestr

    def getBarcode(self,lastbarcode):
        presentbarcode=''
        #datestr = datetime.date.today().strftime("%d%m%Y")
        package = 0
        packagestr = ''
        if lastbarcode:
            package = int(lastbarcode[1:4])
			
            package += 1
            packagestr = self.appendzeros(package)
            presentbarcode = packagestr
		#return package
        else:
            packagestr = self.appendzeros(1)
            presentbarcode =  packagestr
        return presentbarcode

    @synchronized
    def get(self):
        lastbarcode = SubcategoryId.objects()
        barcodeready=''
        if lastbarcode.count()==0:
            barcodeready = self.getBarcode('10')
        else:
            barcodeready = self.getBarcode(lastbarcode[0].subcategoryid)
        return barcodeready

    @synchronized
    def put(self,barcodeready):
        lastbarcode = SubcategoryId.objects()
        
        if lastbarcode.count()==0:
            lastbarcode = SubcategoryId(subcategoryid=barcodeready)
            lastbarcode.save()
        else:
            lastbarcode = SubcategoryId(id=lastbarcode[0].id)
            lastbarcode.subcategoryid = barcodeready
            lastbarcode.save()
        return 'success'
    
    def deleteAll(self):
        lastBarcode = SubcategoryId.objects()
        lastBarcode.delete()
            
        return "success"

    
    
