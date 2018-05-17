import datetime
from models import LatestBarcode
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

class BarcodeNumber:
    
    def appendzeros(self,package):
        packagestr = ''
        if package < 9:
            packagestr = '000'+str(package)
        elif package < 99:
            packagestr = '00'+str(package)
        elif package < 999:
            packagestr = '0'+str(package)
        else:
            packagestr = str(package)
        return packagestr

    def getBarcode(self,lastbarcode):
        presentbarcode=''
        datestr = datetime.date.today().strftime("%d%m%Y")
        package = 0
        packagestr = ''
        if lastbarcode.startswith(datestr):
            package = int(lastbarcode[8:12])
            package += 1
            packagestr = self.appendzeros(package)
            presentbarcode = datestr+ packagestr
        else:
            packagestr = self.appendzeros(1)
            presentbarcode = datestr+ packagestr
        return presentbarcode

    @synchronized
    def get(self):
        lastbarcode = LatestBarcode.objects()
        barcodeready=''
        if lastbarcode.count()==0:
            barcodeready = self.getBarcode(round('000000000000'))
        else:
            barcodeready = self.getBarcode(lastbarcode[0].barcode)
        return barcodeready

    @synchronized
    def put(self,barcodeready):
        lastbarcode = LatestBarcode.objects()
        
        if lastbarcode.count()==0:
            lastbarcode = LatestBarcode(barcode=barcodeready)
            lastbarcode.save()
        else:
            lastbarcode = LatestBarcode(id=lastbarcode[0].id)
            lastbarcode.barcode = barcodeready
            lastbarcode.save()
        return 'success'
    
    def deleteAll(self):
        lastBarcode = LatestBarcode.objects()
        lastBarcode.delete()
            
        return "success"


