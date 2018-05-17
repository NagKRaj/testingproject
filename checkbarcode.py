from models import Barcode_Info, BarCode_Carton

productslist = []
class BarcodeUnpacking:
  
  def checkBarcodeType(self, barcodescan):
    global productslist
    try:
      barcodeObj  = Barcode_Info.objects(barcode_id=barcodescan)
      if barcodeObj:
        barcode = barcodeObj[0]
        if barcode.barcode_type=='Product':
          productslist.append(str(barcode.barcode_id))
        else:
          cartons = BarCode_Carton.objects(mainbarcode=barcodescan)
          
          if cartons:
            barcodesinfo  = cartons[0].barcodelist
            subbarcodelist=[]
            for subbarcode in barcodesinfo:
              subbarcodelist.append(str(subbarcode.barcode))
            return subbarcodelist
          else:
            return []
      return []
    except Exception as e:
        return str(e)  
    

  def getProductsBarcode(self, barcodes):
    try:
      for barcode in barcodes:
        if barcode:
          barcodelist  = self.checkBarcodeType(barcode)
          if len(barcodelist)>0:
            self.getProductsBarcode(barcodelist)
      
      return productslist  
    except Exception as e:
        return str(e)   


  def unpack(self, barcodes):
    returnlist = self.getProductsBarcode(barcodes)
    dataset = {}
    for barcode in returnlist:
      if barcode in dataset.keys():
        count = dataset[barcode]
        count += 1
        dataset[barcode] = count
      else:
        dataset[barcode] = 1
    return dataset

