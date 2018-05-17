import datetime
from models import LatestPurchasecode,LatestInvoicecode,LatestShopPurchasecode
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

class PurchaseNumber:
    
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

    def getPurchase(self,purchaseCode):
        presentPurchaseCode=''
        dateStr = datetime.date.today().strftime("%d%m%Y")
        package = 0
        packageStr = ''
        if purchaseCode.startswith('PO'+dateStr):
            package = int(purchaseCode[10:14])
            package += 1
            packageStr = self.appendzeros(package)
            presentPurchaseCode = 'PO'+dateStr+ packageStr
        else:
            packageStr = self.appendzeros(1)
            presentPurchaseCode = 'PO'+dateStr+ packageStr
        return presentPurchaseCode

    @synchronized
    def get(self):
        lastPurchase = LatestPurchasecode.objects()
        purchaseReady=''
        #return lastPurchase[0].purchasecode
        if lastPurchase.count()==0:
            purchaseReady = self.getPurchase('000000000000')
            
        else:
            purchaseReady = self.getPurchase(lastPurchase[0].purchasecode)
            
        return purchaseReady
    
    @synchronized
    def put(self, purchaseCreated):
        lastPurchase = LatestPurchasecode.objects()
        
        if lastPurchase.count()==0:
            lastPurchase = LatestPurchasecode(purchasecode=purchaseCreated)
            lastPurchase.save()
        else:
            lastPurchase = LatestPurchasecode(id=lastPurchase[0].id)
            lastPurchase.purchasecode = purchaseCreated
            lastPurchase.save()
        return "success"
    
    def deleteAll(self):
        lastPurchase = LatestPurchasecode.objects()
        lastPurchase.delete()
            
        return "success"

class ShopPurchaseNumber:
    
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

    def getPurchase(self,purchaseCode):
        presentPurchaseCode=''
        dateStr = datetime.date.today().strftime("%d%m%Y")
        package = 0
        packageStr = ''
        if purchaseCode.startswith('SPO'+dateStr):
            package = int(purchaseCode[11:15])
            package += 1
            packageStr = self.appendzeros(package)
            presentPurchaseCode = 'SPO'+dateStr+ packageStr
        else:
            packageStr = self.appendzeros(1)
            presentPurchaseCode = 'SPO'+dateStr+ packageStr
        return presentPurchaseCode

    @synchronized
    def get(self):
        lastPurchase = LatestShopPurchasecode.objects()
        purchaseReady=''
        #return lastPurchase[0].purchasecode
        if lastPurchase.count()==0:
            purchaseReady = self.getPurchase('000000000000')
            
        else:
            purchaseReady = self.getPurchase(lastPurchase[0].purchasecode)
            
        return purchaseReady

    @synchronized
    def put(self, purchaseCreated):
        lastPurchase = LatestShopPurchasecode.objects()
        
        if lastPurchase.count()==0:
            lastPurchase = LatestShopPurchasecode(purchasecode=purchaseCreated)
            lastPurchase.save()
        else:
            lastPurchase = LatestShopPurchasecode(id=lastPurchase[0].id)
            lastPurchase.purchasecode = purchaseCreated
            lastPurchase.save()
        return "success"
    
    def deleteAll(self):
        lastPurchase = LatestShopPurchasecode.objects()
        lastPurchase.delete()
            
        return "success"



class InvoiceNumber:
    
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

    def getInvoice(self,invoiceCode):
        presentInvoiceCode=''
        dateStr = datetime.date.today().strftime("%d%m%Y")
        package = 0
        packageStr = ''
        if invoiceCode.startswith('IN'+dateStr):
            package = int(invoiceCode[10:14])
            package += 1
            packageStr = self.appendzeros(package)
            presentInvoiceCode = 'IN'+dateStr+ packageStr
        else:
            packageStr = self.appendzeros(1)
            presentInvoiceCode = 'IN'+dateStr+ packageStr
        return presentInvoiceCode

    @synchronized
    def get(self):
        lastInvoice = LatestInvoicecode.objects()
        invoiceReady=''
        #return lastPurchase[0].invoiceCode
        if lastInvoice.count()==0:
            invoiceReady = self.getInvoice('000000000000')
            
        else:
            invoiceReady = self.getInvoice(lastInvoice[0].invoiceCode)
            
        return invoiceReady
    
    @synchronized
    def put(self, invoiceCreated):
        lastInvoice = LatestInvoicecode.objects()
        
        if lastInvoice.count()==0:
            lastInvoice = LatestInvoicecode(invoiceCode=invoiceCreated)
            lastInvoice.save()
        else:
            lastInvoice = LatestInvoicecode(id=lastInvoice[0].id)
            lastInvoice.invoiceCode = invoiceCreated
            lastInvoice.save()
        return "success"
    
    def deleteAll(self):
        lastInvoice = LatestInvoicecode.objects()
        lastInvoice.delete()
            
        return "success"

