#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from app import Flask,request, url_for, redirect, render_template, abort,Response,session,jsonify,flash,send_file
from form import UserRegistration,MasterBrandEditForm,SuppliertaxForm,SupplierdiscountForm,UploadForm,ShippingForm,BankForm,MasterBrandEditForm,EditForm,UploadfileForm,ImageForm
from models import UserSignup,Reg_Supplier,Goods,Category,Sub_Category,Product,Sup_Upload,atr,Shipping_Setup,Supplier_Tax,Supplier_Discount,Bank_Setup,PurchaseOrders,\
Company_Setup,Billing_Setup,Header_Setup,Warehouse,userLoginCheck,PurchaseInvoice,Charges,Invoice,BankDetail,PriceLists,ProdinvWH,Images,Header,InvoiceList,PriceList,Search_Keywords
from flask_login  import login_user , logout_user , current_user , login_required
from flask_login  import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import json,time, os,ast
from os import path
import requests,io
from purchasenumber import PurchaseNumber,ShopPurchaseNumber
import sys,csv
sys.setrecursionlimit(10000)
import sys
import PIL.Image
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
import datetime
import traceback
import urllib
from multiprocessing import Pool
from num2words import num2words
from werkzeug import secure_filename
from boto3.s3.transfer import S3Transfer
import boto3
import urllib2
import re
import cookielib
import itertools
 
sys.modules['Image'] = PIL.Image
supplierapp = Flask(__name__)
supplierapp.secret_key = 'secret'

login_manager = LoginManager()
login_manager.init_app(supplierapp)
login_manager.session_protection = "strong"

supplierapp.config['UPLOAD_FOLDER'] = './static/uploads/'
supplierapp.config['Supplier_Dashboard']='http://127.0.0.1:5003/'
supplierapp.config['Mainurl']='http://127.0.0.1:8000/'

supplierapp.config['NOTIFICATIONS']='True'
supplierapp.config['SMS']='True'
supplierapp.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
supplierapp.config['UPLOAD_IMAGE'] = './static/image'

ACCESS_ID="AKIAJBNG7KVY2J6NSF4Q"
ACCESS_KEY="VHMWLW5WQcHHqsoVmh8pzkZoLNjK0hX/iYfOA73Q"


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in supplierapp.config['ALLOWED_EXTENSIONS']



def synchronized(wrapped):
    lock = threading.Lock()
    @functools.wraps(wrapped)
    def _wrap(*args, **kwargs):
        with lock:
            return wrapped(*args, **kwargs)
    return _wrap

def sendMail(email,subject,htmlbody):
    if supplierapp.config['NOTIFICATIONS']=='True':
            value = requests.post(
              "https://api.mailgun.net/v3/mg.toolsduniya.com/messages",
            auth=("api", "key-8bee70be27164355bdf6ad96ba54ca6d"),
            data={"from": "ShopMyTools <info@mg.toolsduniya.com>",
                "to": email,
                "subject": subject,
                "html": htmlbody})

def SMS(message,mobile):
    mobilestr=""
    for mob in mobile:
        mobilestr=mobilestr+','+mob
    mobilestr.replace(' ,', '', 1)   
    if(supplierapp.config['SMS'])=='True':
     url = "http://www.smscountry.com/smscwebservice_bulk.aspx"
     values = {'user' : 'powertex',
            'passwd' : 'Powertexgst1',
            'message':message,
            'mobilenumber':mobilestr,
            'mtype':'N',
             'DR':'Y'
             }
     data=urllib.urlencode(values)
     data = data.encode('utf-8')
     f = urllib.urlopen(url, data)
     print f.read().decode('utf-8')

def pool_new(pool):
    #print pool
    if pool=='null':
        pool=Pool()
        return {"pool":pool}
    else:
        return {"pool":pool}

#------------------------------Loggers------------------------------------------------>

@supplierapp.after_request
def after_request(response):
    if response.status_code != 500:
        if current_user.is_authenticated:
            ts = strftime('[%Y-%b-%d %H:%M]')
            user_id=str(current_user.username)
            logger.error('%s %s %s %s %s %s %s',
                  ts,
                  user_id,
                  request.remote_addr,
                  request.method,
                  request.scheme,
                  request.full_path,
                  response.status)
    return response

@supplierapp.errorhandler(Exception)
def exceptions(e):
    if current_user.is_authenticated:
        ts = strftime('[%Y-%b-%d %H:%M]')
        tb = traceback.format_exc()
        user_id=str(current_user.username)
        logger.error('%s %s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                      ts,
                      user_id,
                      request.remote_addr, 
                      request.method,
                      request.scheme, 
                      request.full_path, 
                      tb)
    return render_template('error.html',reportsof = 'Exception',msg=str(e))

#------------------------------login Manager----------------------

@login_manager.user_loader
def load_user(id):
        u = UserSignup.objects.get(id=id)
        return u

@login_manager.unauthorized_handler
def unauthorized_callback():
   return render_template('error.html',reportsof = 'Unauthorized out ....')

#-------------------------Supplier Dashbord--------------------------------------------------------
@supplierapp.route('/supplier_dashboard/<userid>')
def supplier_dashboard(userid):
        logger.info('Supplier Entered into Supplier Dashboard')
        uservalue = UserSignup.objects.get(id=userid)
        login_user(uservalue, remember=True)
        total=Sup_Upload.objects(user_id=str(current_user.id)).count()
        process=Sup_Upload.objects(status='Inprocess',user_id=str(current_user.id)).count() 
        approve=Sup_Upload.objects(status='Accept',user_id=str(current_user.id)).count()
        p_order=PurchaseOrders.objects(status='Accept',supplier_id=str(current_user.id)).count()
        p_invoice=PurchaseInvoice.objects(supplier_id=str(current_user.id)).count()
        return render_template('supplierdashboard.html',total=total,process=process,approve=approve,p_order=p_order,p_invoice=p_invoice)


@supplierapp.route('/process_product_list',methods = ['GET', 'POST'])
@login_required
def process_product_list():
        logger.info('Supplier Entered into Product List')
        product= Sup_Upload.objects(user_id=str(current_user.id),status='Inprocess')    
        return render_template('product-list.html',product=product)

@supplierapp.route('/approved_product_list',methods = ['GET', 'POST'])
@login_required
def approved_product_list():
        logger.info('Supplier Entered into Product List')
        product= Sup_Upload.objects(user_id=str(current_user.id),status='Accept')    
        return render_template('product-list.html',product=product)

@supplierapp.route('/purchase_orders')
@login_required
def purchase_orders():
    sup=Sup_Upload.objects(user_id=str(current_user.id))
    purchase=PurchaseOrders.objects(supplier_id=sup[0].user_id,status='Accept')
    logger.info('Supplier  Entered into Purchase List')
    return render_template('admin_purchaselist.html',purchase=purchase)    
          
'''    
@supplierapp.route('/purchase_invoice_list')
@login_required
def purchase_invoice_list():
        logger.info('Supplier Entered into admin_purchaseinvoice')
        detailes=PurchaseInvoice.objects(supplier_id=str(current_user.id),status='Accept')
        return render_template('admin_purchaseinvoice.html',purchaseinvoice=detailes)
'''
#--------------supplier upload----------------------------------
@supplierapp.route('/supplier_upload', methods = ['GET', 'POST'])
@login_required
def supplier_upload():
    try:
        pool = Pool()
        pool_new(pool)
        with supplierapp.app_context():
            form = UploadForm()
        if request.method == 'POST':
            supplier_id=str(current_user.id)
            #print supplier_id
            #return 'Hi'
            upload_id= request.form['upload_id']
            upload_category=request.form.get('categoryname')
            upload_subcategory=request.form.get('subcategory')
            upload_name = request.form['upload_name']
            upload_modelno = request.form['upload_modelno']
            upload_brand = request.form.get('brand')
            upload_warranty = request.form['upload_warranty']
            upload_pieceperCarton = request.form['upload_pieceperCarton']
            upload_minimumOrder = request.form['upload_minimumOrder']
            upload_netWeight = request.form['upload_netWeight']
            upload_mrp = request.form['upload_mrp']
            upload_discount=request.form['upload_discount']
            discount=request.form.get('discount')
            if upload_discount=='0' or discount =='0':
                  return redirect(url_for('supplier_upload'))
            a= str(discount.split("_")[1])
            upload_price = request.form['upload_price']
            upload_tax=request.form['upload_tax']
            tax=request.form.get('tax')
            if upload_tax=='0' or  tax=='0':
                  return redirect(url_for('supplier_upload'))
            b= str(tax.split("_")[1])
            upload_netPrice=request.form['upload_netPrice']
            upload_hsncode = request.form['upload_hsncode']
            #upload_locations = request.form['upload_locations']
            #frequency=request.form['frequency']
            filename1=request.form.get('photo')
            description = request.form['description']
            manual_video=request.form.get('video')
            manual_pdf=request.form.get('pdf')
            data=request.form['tags']
            metatags=request.form['metadescription']
            keywords=request.form['keywords']
            
            tagsinfo=[]
            for j in data.split(','):
                tagsinfo.append(j)
            
            metatagsinfo=[]
            for info in metatags.split(','):
                metatagsinfo.append(info)
            
            keywordsinfo=[]
            for keys in keywords.split(','):
                keywordsinfo.append(keys)
            #-----------------------------------search keywords------------    
            searchkeywords_list=[]
            product_name_list=upload_name.split(' ')
            searchkeywords_list.append(upload_name)
            searchkeywords_list.append(upload_brand.replace(' ','')+upload_subcategory.replace(' ',''))
            searchkeywords_list.append(upload_brand+' '+upload_subcategory)
            searchkeywords_list.append(upload_brand.replace(' ','')+upload_category.replace(' ',''))
            searchkeywords_list.append(upload_brand+' '+upload_category)
            searchkeywords_list.append(''.join(product_name_list))
            searchkeywords_list.append(' '.join(reversed(product_name_list)))
            searchkeywords_list.append(''.join(reversed(product_name_list)))
            searchkeywords_list.append(''.join(e for e in upload_name if e.isalnum()))
            searchkeywords_list.append(' '.join(re.sub('[^a-zA-Z0-9]+', '', _) for _ in product_name_list))
            #-----------------------------------------------------------end search keywords--------------------------------------
            atrname = request.form.getlist('atrname')
            #return atrname
            atrvalue=request.form.getlist('atrvalue')
            attributes_list=[{'atrname': k, 'atrvalue': v} for k, v in zip(atrname, atrvalue)]
            #filename1.save(os.path.join(supplierapp.config['UPLOAD_FOLDER'], filename1.filename))
            jar = cookielib.FileCookieJar("cookie")
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
            url = 'http://192.168.20.9:80/product_data'
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            data = {"supplier_id":current_user.username,"upload_photo":filename1,"attributes":attributes_list,"upload_brand":upload_brand}
            data1=json.dumps(data)
            login_request = urllib2.Request(url,data1)
            login_reply = opener.open(login_request)
            login_reply_data = login_reply.read()
            rec_data=ast.literal_eval(login_reply_data)
            gifurl= rec_data['upload_photo']
            #print gifurl
            isUseridExist=Sup_Upload.objects(upload_id=upload_id)
            if isUseridExist.count()>0:
                return render_template('existuserid.html')

            uploadUser = Sup_Upload(user_id=str(current_user.id),upload_id=upload_id, upload_category=upload_category,
                                    upload_subcategory=upload_subcategory,upload_name=upload_name.strip(), upload_modelno=upload_modelno,
                                    upload_brand =upload_brand,upload_warranty=upload_warranty,upload_pieceperCarton=upload_pieceperCarton,
                                    upload_minimumOrder=upload_minimumOrder,
                                    upload_netWeight=upload_netWeight,upload_mrp=upload_mrp,discount=a,upload_discount=upload_discount,
                                    upload_price=upload_price,tax=b,upload_tax=upload_tax,upload_netPrice=upload_netPrice,
                                    upload_hsncode=upload_hsncode,upload_locations='0',frequency='0',upload_photo=gifurl,search_keywords=searchkeywords_list,
                                    extraimages=[filename1],description=description,manual_video=manual_video,manual_pdf=manual_pdf,salesqty='0',avgrating='0',tags=tagsinfo,metadescription=metatagsinfo,keywords=keywordsinfo)# Insert form data in 
            uploadUser.save()
            
            for uploadUser in Sup_Upload.objects(upload_name=upload_name,upload_brand=upload_brand):
                price = PriceLists(landing_price='0', dealer_price='0',offer_price='0',enduser_price='0',bulk_unit_price='0',bulk_qty='0',percentage=0,doubleoffer_price=0,landing_price_gst=0, dealer_price_gst=0,offer_price_gst=0,enduser_price_gst=0)  
                uploadUser.prices.append(price)
                uploadUser.save()
            for x in range(len(atrname)):
                atrs = atr(atrname[x], atrvalue[x])
                uploadUser.attributes.append(atrs)
                uploadUser.save()
            logger.info('Supplier Upload Product Sucessfully')

            #search=Search_Keywords(upload_name=upload_name,search_keywords=final_search_list).save()

            prodinvobj=ProdinvWH(supplier=str(current_user.id),warehouse='Default',hsn=upload_hsncode,modelno=upload_modelno,brand=upload_brand,prod_desc=upload_name,smtids=[],
                                        quantity='0',outqty='0',barcode=upload_id)
            prodinvobj.save()
            for prodinvobj in ProdinvWH.objects(prod_desc=upload_name,brand=upload_brand):
                inv=InvoiceList()
                prodinvobj.invoice_smtlist.append(inv)
                prodinvobj.save()
            for prodinvobj in ProdinvWH.objects(prod_desc=upload_name,brand=upload_brand):
                price = PriceList(landing_price='0', dealer_price='0',offer_price='0',enduser_price='0',bulk_unit_price='0',bulk_qty='0',landing_price_gst=0, dealer_price_gst=0,offer_price_gst=0,enduser_price_gst=0)  
                prodinvobj.prices.append(price)
                prodinvobj.save()


            registeredUser1 = UserSignup.objects(usertype="Admin")
            supuser = UserSignup.objects(id=str(current_user.id))
            print supuser[0].email
            fo = open("./static/mailtemp/suppliermailtemp.html", "r+")
            htmlbody = fo.read()
            fo.close()
            emailList=[]
            emailList.append(registeredUser1[0].email)
            emailList.append(supuser[0].email)
            #print adminmail
            urldata='User '+registeredUser1[0].username+'has uploaded a product.'
            htmlbody = htmlbody.replace("$$urldata$$",urldata)
            #print urldata
            #sendMail(email,'Supplier Verification & Approval',htmlbody)
            pool.apply_async(sendMail,[emailList,'Supplier product uploaded',htmlbody])
            msg='User '+registeredUser1[0].username+'has uploaded a product.'
            mobileList=[]
            mobileList.append("91"+registeredUser1[0].mobile)
            mobileList.append("91"+supuser[0].mobile)
            #SMS(msg,mobileList)
            pool.apply_async(SMS,[msg,mobileList])
            '''
            data = {"upload_name":upload_name}
            data1=json.dumps(data)
            print data1,"sairam"
            json_data = request.get_json(force=True)
            print json_data['data1']
            '''
            return render_template('productupload_success.html')
        else:
            categorylist = Category.objects()
            categorylist1 = Sub_Category.objects(categoryname=categorylist[0].categoryname)
            br=[]
            for k in Reg_Supplier.objects(user_id=str(current_user.id)):
                 for i in k.supplier_brands:
                     br.append(i)
            atrlist=[]
            for x in Product.objects():
                for i in x.attribute:
                    atrlist.append(i)
            tax = Supplier_Tax.objects()
            Discount=Supplier_Discount.objects(user_id=str(current_user.id))
            return render_template('supplierproduct-upload.html',form=form,categorylist=categorylist,categorylist1=categorylist1,tax=tax,Discount=Discount,atrlist=atrlist,br=br)
    except Exception as e:
             logger.info('Supplier Failed to Upload Product')              
             return render_template('error.html',reportsof = 'Exception',msg=str(e))

        
@supplierapp.route('/catsubatr_post/', methods=['GET', 'POST'])
@login_required
def catsubatr_post():
    try:
        subcat=request.args.get('catname')
        subcategory=[]
        for subcat in Sub_Category.objects(categoryname=subcat):
            subcategory.append(subcat.subcategory)
        sub=sorted(subcategory)
        return jsonify(sub)
        '''
        subca=Sub_Category.objects(categoryname=subcat)
        subcategory=json.loads(subca.to_json())
        #print subcategory.values()
        sub=sorted(subcategory)
        return jsonify(sub)
        '''
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')    

@supplierapp.route('/attribute_post/', methods=['GET', 'POST'])
@login_required
def attribute_post():
    try:
       cat=request.args.get('catname')
       subcat=request.args.get('subcatname')
       atrarray=[]
       for i in Product.objects(categoryname=cat,subcategory=subcat):
           for atr in i.attribute:
                 atrarray.append(atr.atrname)
       atr=sorted(atrarray)
       return jsonify(atr)
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')   
            
#-------------------------------------------------------product info------------------------------------------------------------

@supplierapp.route('/productlist',methods = ['GET', 'POST'])
@login_required
def productlist():
        logger.info('Supplier Entered into Product List')
        product= Sup_Upload.objects(user_id=str(current_user.id))    
        return render_template('product-list.html',product=product)
            
@supplierapp.route('/productviewmore/<id>',methods = ['GET', 'POST'])
@login_required
def productviewmore(id):
        logger.info('Supplier Entered into Product Viewmore')
        detailes = Sup_Upload.objects.filter(id=id).first()
        sup=Reg_Supplier.objects(user_id=detailes.user_id)
        if request.method == 'POST':
            comment=request.form.get('comment')
            detailes.remarks=comment
            if request.form.get('submit') == 'Accept':
                detailes.status = 'Accept'
                detailes.save()
                return redirect(url_for("productlist"))
            else:
                
                wh=ProdinvWH.objects.get(prod_desc=detailes.upload_name)
                #print detailes.upload_name
                #rint wh
                wh.delete()
                detailes.status='Reject'
                detailes.save()
        return render_template('product-viewmore.html',detailes=detailes,supname=sup[0].supplier_name)



@supplierapp.route('/productdelete/', methods=['GET', 'POST'])
@login_required
def productdelete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="em"):
            quickviews=Sup_Upload.objects.get(id=docid)
            quickviews.delete()
            wh=ProdinvWH.objects()
            for w in wh:
                if w.prod_desc==quickviews.upload_name and w.supplier==quickviews.user_id and w.brand==quickviews.upload_brand:
                   if w.warehouse=='Default':
                        w.delete()
   
        logger.info('Deleted Product sucessfully')        
        return redirect(url_for('productlist'))

        
@supplierapp.route('/productedit/<productid>', methods = ['GET', 'POST'])
@login_required
def productedit(productid):
      pool = Pool()
      pool_new(pool)
      with supplierapp.app_context():
        uploadForm = UploadForm()
      if request.method == 'POST':
            obje = Sup_Upload.objects.get(id=productid)
            obje.upload_hsncode=request.form['upload_hsncode']
            obje.upload_mrp=request.form['upload_mrp']
            obje.upload_price=request.form['upload_price']
            obje.upload_photo=request.form.get('upload_photo')
            #print request.form.get('upload_photo')
            discount=request.form.get('discount')
            obje.discount= str(discount.split("_")[1])
            obje.upload_discount=request.form['upload_discount']
            tax=request.form.get('tax')
            obje.tax= str(tax.split("_")[1])
            obje.upload_tax=request.form['upload_tax']
            obje.upload_netPrice=request.form['upload_netPrice']
            obje.description=request.form['description']
            data=request.form['tags']
            metatags=request.form['metadescription']
            keywords=request.form['keywords']
            
            tagsinfo=[]
            for j in data.split(','):
                tagsinfo.append(j)
            obje.tags=tagsinfo
            
            metatagsinfo=[]
            for info in metatags.split(','):
                metatagsinfo.append(info)
            obje.metadescription=metatagsinfo
            
            keywordsinfo=[]
            for keys in keywords.split(','):
                keywordsinfo.append(keys)
            obje.keywords=keywordsinfo
            
            atrname = request.form.getlist('atrname')
            atrvalue=request.form.getlist('atrvalue')
            sup = Sup_Upload.objects.get(id=obje.id)
            extraimages=request.form.getlist('imageurl')
            listofattrs = sup.attributes
            for i in range(len(sup.attributes)):
                obje.attributes.remove(listofattrs[i])
            for x in range(len(atrname)):
                atrs = atr(atrname[x], atrvalue[x])
                obje.attributes.append(atrs)
  
            if len(obje.extraimages)>0:
                image=obje.extraimages+extraimages
                obje.extraimages=image
            else:
                obje.extraimages=extraimages
            obje.save()
            prodinv=ProdinvWH.objects(supplier=str(current_user.id),prod_desc=obje.upload_name,modelno=obje.upload_modelno,brand=obje.upload_brand)
            prodinvwh=prodinv[0]
            prodinvwh.hsn=obje.upload_hsncode
            prodinvwh.prod_desc=obje.upload_name
            prodinvwh.modelno=obje.upload_modelno
            prodinvwh.brand=obje.upload_brand
            prodinvwh.save()
            #registeredUser = Reg_Supplier.objects(user_id=str(current_user.id))
            #username=registeredUser[0].supplier_name
            registeredUser1 = UserSignup.objects(usertype="Admin")
            mmuser = UserSignup.objects(usertype="Market Manager")
            supuser = UserSignup.objects(id=str(current_user.id))
            #print supuser[0].email
            fo = open("./static/mailtemp/suppliermailtemp.html", "r+")
            htmlbody = fo.read()
            fo.close()
            emailList=[]
            emailList.append(registeredUser1[0].email)
            emailList.append(mmuser[0].email)
            emailList.append(supuser[0].email)
            #print adminmail
            urldata='User '+registeredUser1[0].username+'has updated a product.'
            htmlbody = htmlbody.replace("$$urldata$$",urldata)
            #print urldata
            #sendMail(email,'Supplier Verification & Approval',htmlbody)
            pool.apply_async(sendMail,[emailList,'Supplier product updated',htmlbody])
            msg='User '+registeredUser1[0].username+'has updated a product.'
            mobileList=[]
            mobileList.append("91"+registeredUser1[0].mobile)
            mobileList.append("91"+mmuser[0].mobile)
            mobileList.append("91"+supuser[0].mobile)
            #SMS(msg,mobileList)
            pool.apply_async(SMS,[msg,mobileList])
            logger.info('Product Edited and Saved sucessfully')
            return redirect(url_for('productlist'))
      else:
          obje = Sup_Upload.objects.get(id=productid)
          uploadForm.upload_id.data = obje.upload_id
          uploadForm.categoryname.data = obje.upload_category
          uploadForm.subcategory.data= obje.upload_subcategory
          uploadForm.upload_name.data=obje.upload_name
          uploadForm.upload_modelno.data=obje.upload_modelno
          uploadForm.brand.data=obje.upload_brand
          uploadForm.upload_hsncode.data=obje.upload_hsncode
          uploadForm.upload_warranty.data=obje.upload_warranty
          uploadForm.upload_pieceperCarton.data=obje.upload_pieceperCarton
          uploadForm.upload_minimumOrder.data=obje.upload_minimumOrder
          uploadForm.upload_netWeight.data=obje.upload_netWeight
          uploadForm.upload_mrp.data=obje.upload_mrp
          uploadForm.discount.data=obje.discount
          uploadForm.upload_discount.data=obje.upload_discount
          uploadForm.upload_price.data=obje.upload_price
          uploadForm.tax.data=obje.tax
          #return obje.tax
          uploadForm.upload_tax.data=obje.upload_tax
          uploadForm.upload_netPrice.data=obje.upload_netPrice
          #uploadForm.upload_locations.data=obje.upload_locations
          #uploadForm.frequency.data=obje.frequency
          uploadForm.upload_photo.data=obje.upload_photo
          uploadForm.description.data=obje.description
          uploadForm.manual_video.data=obje.manual_video
          uploadForm.manual_pdf.data=obje.manual_pdf
          uploadForm.tags.data=', '.join(obje.tags)
          uploadForm.metadescription.data=', '.join(obje.metadescription)
          uploadForm.keywords.data=', '.join(obje.keywords)
          a=[] 
          for i in obje.attributes:
               a.append(i)
               uploadForm.atrname.data=i.atrname
               uploadForm.atrvalue.data=i.atrvalue
          atrarray=[]
          for i in Product.objects(categoryname=obje.upload_category,subcategory=obje.upload_subcategory):
              for atrs in i.attribute:
                 atrarray.append(atrs)
          sortatr=sorted(atrarray)
          tax = Supplier_Tax.objects()
          Discount=Supplier_Discount.objects(user_id=str(current_user.id))
          logger.info('Entered into Product Edit')
          
          return render_template('edit.html',uploadForm=uploadForm,obje=obje,a=a,tax=tax,Discount=Discount,sortatr=sortatr)

    
@supplierapp.route('/product_delete/<id>', methods=['GET', 'POST'])
@login_required
def product_delete(id):
        if current_user.email:
            quickview = Sup_Upload.objects.get(id=id)
            quickview.delete()
            logger.info('Supplier Deleted product Sucessfully')
            return redirect(url_for('productlist'))
#---------------sales info-------------------------------------------------------------
@supplierapp.route('/admin_purchaselist')
@login_required
def admin_purchaselist():
    #sup=Sup_Upload.objects(user_id=str(current_user.id))
    purchase=PurchaseOrders.objects(supplier_id=str(current_user.id)).order_by('-id')
    logger.info('Supplier  Entered into Purchase List')
    return render_template('admin_purchaselist.html',purchase=purchase)

          
@supplierapp.route('/adminpurchaseinformation/<id>',methods = ['GET', 'POST'])
@login_required
def adminpurchaseinformation(id):
            pool = Pool()
            pool_new(pool)
            invoicenum=Bank_Setup.objects(user_id=str(current_user.id))
            if invoicenum.count()==0:
                 return render_template('bankerrormsg.html')
            else:
                detailes = PurchaseOrders.objects.filter(id=id).first()
                number= num2words(float((detailes.totalvalue)))
                company=Company_Setup.objects()
                billing=Billing_Setup.objects()
                header=Header.objects()
                logo=header[0].headerlogo
                warehouse=Warehouse.objects(warehouse_name=detailes.warehouse_name)
                headerlist = Header_Setup.objects()
                regsup=Reg_Supplier.objects(user_id=detailes.supplier_id)
                logger.info(' Supplier Entered into Purchase Information')
                if request.method == 'POST':
                    comment=request.form.get('comment')
                    detailes.remarks=comment
                    if request.form.get('submit') == 'Accept':
                        detailes.status = 'Accept'
                        detailes.save()
                        user=UserSignup.objects(usertype='Purchase-Manager')
                        user1=UserSignup.objects(usertype='Market Manager')
                        user2=UserSignup.objects(usertype='WH-Manager')
                        user3=UserSignup.objects(usertype='Accountant')
                        #registeredUser = Reg_Supplier.objects()
                        emailList=[]
                        emailList.append(user[0].email)
                        emailList.append(user1[0].email)
                        emailList.append(user2[0].email)
                        emailList.append(user3[0].email)                    
                        fo = open("./static/mailtemp/suppliermailtemp.html", "r+")
                        htmlbody = fo.read()
                        fo.close()
                        urldata='Suppiler ' +detailes.supplier_name+ ' has accepted the order : ' + detailes.purchaseOrder_no
                        htmlbody = htmlbody.replace("$$urldata$$",urldata)
                        #sendMail(emailList,"Supplier had accepted the Purchase order.",htmlbody)
                        pool.apply_async(sendMail,[emailList,"Purchase order accepted from supplier",htmlbody])
                        msg='Suppiler ' + detailes.supplier_name + ' has accepted the order : ' + detailes.purchaseOrder_no
                        mobileList=[]
                        mobileList.append('91'+user[0].mobile)
                        mobileList.append('91'+user1[0].mobile)
                        mobileList.append('91'+user2[0].mobile)
                        mobileList.append('91'+user3[0].mobile)
                        #SMS(msg,mobileList)
                        pool.apply_async(SMS,[msg,mobileList])
                        return redirect(url_for('purchase_invoice',id=id))
                    else:
                        detailes.status='Reject'
                        detailes.save()
                        user=UserSignup.objects(usertype='Purchase-Manager')
                        user1=UserSignup.objects(usertype='Market Manager')
                        #registeredUser = Reg_Supplier.objects()
                        emailList=[]
                        emailList.append(user[0].email)
                        emailList.append(user1[0].email)
                        #if registeredUser.count() > 0:
                        fo = open("./static/mailtemp/suppliermailtemp.html", "r+")
                        htmlbody = fo.read()
                        fo.close()
                        urldata='Dear '+detailes.supplier_name+' has rejected the purchase order. Kindly contact Supplier for further details.'
                        htmlbody = htmlbody.replace("$$urldata$$",urldata)
                        #sendMail(emailList,"Supplier had rejected the Purchase Order",htmlbody)
                        pool.apply_async(sendMail,[emailList,"Purchase order rejected",htmlbody])
                        msg="Purchase order rejected from supplier"
                        mobileList=[]
                        mobileList.append('91'+user[0].mobile)
                        mobileList.append('91'+user1[0].mobile)                      
                        #SMS(msg,mobileList)
                        pool.apply_async(SMS,[msg,mobileList])
            return render_template('admin-orderviewmore.html',detailes=detailes,company=company[0],billing=billing[0],logo=logo,warehouse=warehouse[0],regsup=regsup[0],headerlist=headerlist[0],number=number)
    
@supplierapp.route('/purchase_invoice/<id>', methods = ['GET', 'POST'])
@login_required
def purchase_invoice(id):
          detailes = PurchaseOrders.objects.filter(id=id).first()
          poinvoice=detailes.purchaseOrder_no.replace('PO','POIN')
          shipping=Shipping_Setup.objects()
          logger.info('Entered into Purchase Invoice')
          bankinfo=[]
          for shippings in Bank_Setup.objects(user_id=str(current_user.id)):
              data={}
              data['bankac_number']=shippings.bankac_number              
              bankinfo.append(data)
          regsup=Reg_Supplier.objects(user_id=detailes.supplier_id) 
          return render_template('purchaseorder-invoice.html',shipping=shipping,detailes=detailes,poinvoice=poinvoice, regsup=regsup[0].supplier_gstin,bankinfo=bankinfo) 


@supplierapp.route('/purchaseinvoice_post', methods = ['GET', 'POST'])
@login_required
def purchaseinvoice_post():
    try:
        if request.method == 'POST':
            logger.info('Entered into Purchase Invoice Post')
            json_data = request.get_json(force=True)
            ware_house= json_data['ware_house']
            supplier_id = json_data['supplier_id']
            purchase_manager_id=json_data['purchase_manager_id']
            purchaseOrder_no = json_data['purchaseOrder_no']
            supplier_gstno = json_data['supplier_gstno']
            invoice_no = json_data['invoice_number']
            invoice_date = json_data['invoice_date']
            expected_date=json_data['expected_date']
            #shipping_charges = json_data['shipping_charges'] 
            total_items= json_data['total_items']
            total_quantity = json_data['total_quantity']
            total_value = json_data['total_value']
            #return total_value
            purchaseinfo = PurchaseInvoice(user_id=str(current_user.id),ware_house=ware_house, supplier_id=supplier_id,purchase_manager_id=purchase_manager_id,
                                                purchaseOrder_no=purchaseOrder_no, supplier_gstno=supplier_gstno,invoice_no=invoice_no,
                                                invoice_date =invoice_date,expected_date=expected_date,total_items=total_items,
                                                  total_quantity=total_quantity,total_value=total_value)
            purchaseinfo.save()
            for i in json_data['items']:
                item = i['item']
                item_id = i['item_id']
                item_model = i['item_model']
                item_quntity = i['item_quntity']
                order_id = i['item_id']
                model_no = i['item_model']
                quantity = i['item_quntity']
                netprice = i['item_price']
                value = i['item_value']
                invoice = Invoice(item,item_id,item_model,item_quntity,netprice,value)
                purchaseinfo.invoice.append(invoice)
                purchaseinfo.save()
            for j in json_data['othercharges']:
                charge_name = j['charge_name']
                charge_value = j['charge_value']
                charges = Charges(charge_name,charge_value)
                purchaseinfo.othercharges.append(charges)
                purchaseinfo.save()
            for k in json_data['bankdetails']:
                acname = k['acname']
                accountnumber = k['accountnumber']
                accounttype = k['accounttype']
                ifsccode = k['ifsccode']
                microcode = k['microcode']
                bank = BankDetail(acname,accountnumber,accounttype,ifsccode,microcode)
                purchaseinfo.bankdetails.append(bank)
                purchaseinfo.save()
            return 'Success'                 
    except Exception as e:
       return jsonify('{"mesg":' + str(e) +'}')    
    

@supplierapp.route('/admin_purchaseinvoice')
@login_required
def admin_purchaseinvoice():
        logger.info('Supplier Entered into admin_purchaseinvoice')
        detailes=PurchaseInvoice.objects(supplier_id=str(current_user.id))
        return render_template('admin_purchaseinvoice.html',purchaseinvoice=detailes)

@supplierapp.route('/adminpurchaseinvoiceinfo/<id>',methods = ['GET', 'POST'])
@login_required
def adminpurchaseinvoiceinfo(id):
           logger.info('Purchase-Manager Entered into adminpurchaseinvoiceinfo')
           detailess = PurchaseInvoice.objects.filter(id=id).first()
           purchase_data=PurchaseOrders.objects(purchaseOrder_no=detailess.purchaseOrder_no)
           company=Company_Setup.objects()
           billing=Billing_Setup.objects()
           warehouse=Warehouse.objects()
           headerlist = Header_Setup.objects()
           header=Header.objects()
           logo=header[0].headerlogo
           regsup=Reg_Supplier.objects(user_id=detailess.supplier_id)
           number= num2words(float((detailess.total_value)))
           return render_template('purchaseinvoice-viewmore.html',purchase_data=purchase_data,detailess=detailess,company=company[0],billing=billing[0],logo=logo,warehouse=warehouse[0],headerlist=headerlist[0],regsup=regsup[0],number=number)
      
@supplierapp.route('/purchase_delete/', methods=['GET', 'POST'])
@login_required
def purchase_delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="em"):
            quickview = PurchaseOrders.objects.get(id=docid)
            quickview.delete()
        logger.info('Deleted Purchase list')
        return redirect(url_for('admin_purchaselist'))

  
#---------------------------more info-----------------------------------------------------          
@supplierapp.route('/bankinfo', methods=['GET', 'POST'])
@login_required
def bankinfo():
     if request.method == 'POST':           
        json_data = request.get_json(force=True)
        bankDetails= json_data['bankDetails']  
        br=[]
        for i in Bank_Setup.objects(bankac_number=bankDetails):
              data={}                
              data['ac_holdername']=i.ac_holdername
              data['bankac_number']=i.bankac_number
              data['ac_type']=i.ac_type
              data['ifsc_code']=i.ifsc_code
              data['micr_code']=i.micr_code
              br.append(data)
        return jsonify(br)


@supplierapp.route('/tax_discount', methods = ['GET', 'POST'])
@login_required
def tax_discount():
        with supplierapp.app_context():
         form1 = SuppliertaxForm()
         form2 = SupplierdiscountForm()
        if request.method == 'POST':
            if form1.validate():
                taxId = request.form['taxId']
                taxName=request.form['taxName']
                taxRate=request.form['taxRate']
                istaxId=Supplier_Tax.objects(taxId=taxId)
                status=request.form.get('taxhide')
                if status=='yes':
                    tax_list = Supplier_Tax.objects.get(taxId=taxId)
                    tax_list.taxName=taxName
                    tax_list.save()
                elif status !='yes' :
                    if istaxId.count()>0:
                     return render_template('taxdiscountt.html')
                    tax = Supplier_Tax(user_id=str(current_user.id),taxId=taxId,taxName=taxName, taxRate=taxRate) 
                    tax.save()
                logger.info('Entered new Tax')
                return redirect(url_for('tax_discount'))
            
            elif form2.validate():
                discountId=request.form['discountId']
                discountName = request.form['discountName']
                discountRate = request.form['discountRate']
                isdiscountId=Supplier_Discount.objects(discountId=discountId)
                status=request.form.get('discounthide')
                if status=='yes':
                    dislist = Supplier_Discount.objects.get(discountId=discountId)
                    dislist.discountName=discountName
                    dislist.save()
                elif status !='yes' :
                    if isdiscountId.count()>0:
                     return render_template('taxdiscountt.html')
                    discount = Supplier_Discount(user_id=str(current_user.id),discountId=discountId,discountName=discountName,discountRate=discountRate) 
                    discount.save()
                logger.info('Entered Discount')
                return redirect(url_for('tax_discount'))
                
        taxlist = Supplier_Tax.objects(user_id=str(current_user.id))
        discountlist = Supplier_Discount.objects(user_id=str(current_user.id))
                       
        return render_template('tax-discount-configuration.html',form1=form1,form2=form2,taxlist=taxlist,discountlist=discountlist)
  

@supplierapp.route('/tax_discountt_delete/', methods=['GET', 'POST'])
@login_required
def tax_discountdelete():
            type = request.args.get('type')
            docid = request.args.get('docid')
            if(type=="tax"):
                user=Supplier_Tax.objects.get(id=docid)
                user.delete()
                logger.info('Deleted Tax')
                return redirect(url_for('tax_discount'))
        
            else:
                user=Supplier_Discount.objects.get(id=docid)
                user.delete()
                logger.info('Deleted Discount')
                return redirect(url_for('tax_discount'))     
'''
@supplierapp.route('/bank_configuration', methods = ['GET', 'POST'])
@login_required
def bank_configuration():
        with supplierapp.app_context():
         form = BankForm()
        if request.method == 'POST' and form.validate():
            bankac_number = request.form['bankac_number']
            ac_holdername = request.form['ac_holdername']
            ac_type = request.form.get('accountType')
            bank_name=request.form['bank_name']
            ifsc_code = request.form['ifsc_code']
            micr_code=request.form['micr_code']
            branch_name=request.form['branch_name']
            branch_address=request.form['branch_address']
            ifacnum=Bank_Setup.objects(bankac_number=bankac_number)
            status=request.form.get('bankhide')
            if status=='yes':
                    bankinfo = Bank_Setup.objects.get(bankac_number=bankac_number)
                    bankinfo.bank_name=bank_name
                    bankinfo.ac_holdername=ac_holdername
                    bankinfo.ac_type=ac_type
                    bankinfo.ifsc_code=ifsc_code
                    bankinfo.micr_code=micr_code
                    bankinfo.branch_name=branch_name
                    bankinfo.branch_address=branch_address 
                    bankinfo.save()
            elif status !='yes':
                if ifacnum.count()>0:
                    return render_template('bankac.html')
                bank =Bank_Setup(user_id=str(current_user.id),bankac_number=bankac_number,ac_holdername=ac_holdername,ac_type=ac_type, bank_name=bank_name , ifsc_code=ifsc_code , micr_code=micr_code,branch_name=branch_name,branch_address=branch_address) 
                bank.save()
            logger.info('Entered Bank Details Sucessfully')
            return redirect(url_for('bank_configuration'))
        else:
            
            if current_user.usertype=='Admin':
               bankdetailes = Bank_Setup.objects()
            else:
               bankdetailes = Bank_Setup.objects(user_id=str(current_user.id))
               cname=Reg_Supplier.objects(user_id=str(current_user.id))
               form.ac_holdername.data=cname[0].supplier_companyname
            return render_template('bank-configuration.html',form=form,bankdetailes=bankdetailes,cname=cname)

'''
@supplierapp.route('/bank_configuration', methods = ['GET', 'POST'])
@login_required
def bank_configuration():
        with supplierapp.app_context():
         form = BankForm()
        if request.method == 'POST':
            bankac_number = request.form['bankac_number']
            ac_holdername = request.form['ac_holdername']
            ac_type = request.form.get('accountType')
            bank_name=request.form['bank_name']
            ifsc_code = request.form['ifsc_code']
            micr_code=request.form['micr_code']
            vpa=request.form['vpa']
            branch_name=request.form['branch_name']
            branch_address=request.form['branch_address']
            ifacnum=Bank_Setup.objects(bankac_number=bankac_number)
            status=request.form.get('bankhide')
            if status=='yes':
                    bankinfo = Bank_Setup.objects.get(bankac_number=bankac_number)
                    bankinfo.bank_name=bank_name
                    bankinfo.ac_holdername=ac_holdername
                    bankinfo.ac_type=ac_type
                    bankinfo.ifsc_code=ifsc_code
                    bankinfo.micr_code=micr_code
                    bankinfo.branch_name=branch_name
                    bankinfo.branch_address=branch_address 
                    bankinfo.save()
            elif status !='yes':
                if ifacnum.count()>0:
                    return render_template('bankac.html')
                bank =Bank_Setup(user_id=str(current_user.id),bankac_number=bankac_number,ac_holdername=ac_holdername,ac_type=ac_type, bank_name=bank_name , ifsc_code=ifsc_code , micr_code=micr_code,vpa=vpa,branch_name=branch_name,branch_address=branch_address) 
                bank.save()
            logger.info('Entered Bank Details Sucessfully')
            return redirect(url_for('bank_configuration'))
        else:
            
            if current_user.usertype=='Admin':
               bankdetailes = Bank_Setup.objects()
            else:
               bankdetailes = Bank_Setup.objects(user_id=str(current_user.id))
               company=Reg_Supplier.objects(user_id=str(current_user.id))
               #company=Reg_Supplier.objects(user_id=str(current_user.id))
               form.ac_holdername.data=company[0].supplier_companyname
            logger.info('Entered into bank configuration')
            return render_template('bank-configuration.html',form=form,bankdetailes=bankdetailes)

        
			
@supplierapp.route('/masterbrand_edit', methods = ['GET', 'POST'])
@login_required
def masterbrand_edit():
        if current_user.usertype=='Admin':
            with supplierapp.app_context():
             form = MasterBrandEditForm()
            if request.method == 'POST':
                supplier_id = request.form['supplier_id']
                supplier_brand = request.form.getlist('brand')
                supplier_tm = request.form.getlist('supplier_tm')
                supplierUser = Reg_Supplier(user_id=str(current_user.id),supplier_id=supplier_id)
                supplierUser.save()
                for x in range(len(supplier_brand)):
                    goods = Goods(supplier_brand[x], supplier_tm[x])
                    supplierUser.supplier_brands.append(goods)
                    supplierUser.save()
                    logger.info('Entered brands in Master Brand Setup')
                    return redirect(url_for('masterbrand_edit'))
            brandlist = Reg_Supplier.objects()
                
        
            return render_template('brand_configuration.html',form=form,brandlist=brandlist)
        elif current_user.usertype=='Supplier':
                with supplierapp.app_context():
                  form = MasterBrandEditForm()
                if request.method == 'POST' and form.validate():
                    #return 'hi'
                    supplier_id = request.form.get('supplier_id')
                    supplier_brand = request.form['brand']
                    supplier_tm = request.form['supplier_tm']
                    
                   
                    sup=Reg_Supplier.objects(user_id=str(current_user.id),supplier_brands__supplier_tm=supplier_tm)
                    if sup.count()>0:
                            return render_template('unique.html')
                    supplierUser = Reg_Supplier(user_id=str(current_user.id))
                    #supplierUser.supplier_id=supplier_id                          
                    supplierUser.save()
                    #for x in range(len(supplier_brand)):
                    goods = Goods(supplier_brand, supplier_tm)
                    supplierUser.supplier_brands.append(goods)
                    supplierUser.save()
                logger.info(' Supplier Entered brands in Master Brand Setup')        
                brandlist = Reg_Supplier.objects(user_id=str(current_user.id))
                return render_template('brand_configuration.html',form=form,brandlist=brandlist)
            

@supplierapp.route('/masterbrand_delete/', methods=['GET', 'POST'])
@login_required
def masterbrand_delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="edit"):
            brand_info = Reg_Supplier.objects.get(id=docid)
            brand_info.delete()
        logger.info('Deleted brand in Master Brand Setup')
        return redirect(url_for('masterbrand_edit'))
   
                 

@supplierapp.route('/bankdelete/', methods=['GET', 'POST'])
@login_required
def bankdelete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="bank"):
            bankinfo=Bank_Setup.objects.get(id=docid)
            bankinfo.delete()
        logger.info('Deleted Bank Deatils')
        return redirect(url_for('bank_configuration'))
#----------------------edit profile---------------------------------   
@supplierapp.route('/editprofile', methods = ['GET', 'POST'])
@login_required
def editprofile():
      with supplierapp.app_context():
        userEditForm = EditForm()
      if request.method == 'POST' and userEditForm.validate():
           email = request.form['email']
           oldpassword=request.form['oldpassword']
           value = userLoginCheck(userEditForm.email.data,userEditForm.oldpassword.data)
           if value=='Fail':
               logger.info('Failed to edit profile')
               return render_template('profileerror.html')
           else:
               newpassword = request.form['password']
               User = UserSignup.objects.get(id=current_user.id)
               User.password=generate_password_hash(newpassword)
               User.save()
               logger.info('Profile Edited Sucessfully')
               return redirect(supplierapp.config['Supplier_Dashboard']+'supplier_dashboard/'+str(current_user.id))
             
               
      else:
            User = UserSignup.objects.get(id=current_user.id)
            userEditForm.username.data = User.username
            userEditForm.email.data = User.email
            userEditForm.mobile.data = User.mobile
            logger.info('Entered into editprofile')
            return render_template('edit_profile.html',userEditForm=userEditForm)


@supplierapp.route('/signupedit', methods = ['GET', 'POST'])
@login_required
def signupedit():
      with supplierapp.app_context():
        userEditForm = UserRegistration()
      if request.method == 'POST':
           mobile = request.form['mobile']
           userpn=UserSignup.objects(mobile=mobile)           
           if userpn.count()>0:
               return "Mobile already existed!"
           else:
               userpn=UserSignup.objects(id=current_user.id)
               user= userpn[0]
               user.mobile=mobile
               user.save()
               return redirect(supplierapp.config['Supplier_Dashboard']+'supplier_dashboard/'+str(current_user.id))
               
      else:
            User = UserSignup.objects.get(id=current_user.id)
            userEditForm.username.data = User.username
            userEditForm.email.data = User.email
            userEditForm.mobile.data = User.mobile
            
            logger.info('Entered into useredit')
            return render_template('signupedit.html',userEditForm=userEditForm,user=User)        
#-------------------------------------bulk upload---------------------------------
@supplierapp.route('/bulkupload', methods = ['GET', 'POST'])
def bulkupload():
    try:
        with supplierapp.app_context():
            form = UploadfileForm()
        if request.method == 'POST':
            f = request.files['upload_file']
            stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
            reader = csv.DictReader(stream)
            header= [ '*Product_Id','*Product_Category', '*Product_Subcategory', '*Product_Name', '*Product_Modelno','*Brand','*HSNcode','Warranty',
                          '*PieceperCarton','*MinimumOrder','*MRP','*Discount_Name','*Discount','*Unit_Price','*Tax_Name','*Tax','*NetPrice','NetWeight',
                      '*Product_Photo','*Attributes','Description','Manual_Video','Manual_PDF','*Extraimages1','Extraimages2','Extraimages3',
                          'Extraimages4','Extraimages5','Tags','Metadescription','Keywords']
            for each  in reader:
                user_id=str(current_user.id)
                upload_id=each['*Product_Id']
                upload_category=each['*Product_Category']
                upload_subcategory=each['*Product_Subcategory']
                upload_name=each['*Product_Name']
                upload_modelno=each['*Product_Modelno']
                upload_brand=each['*Brand']
                upload_warranty=each['Warranty']
                upload_pieceperCarton=each['*PieceperCarton']
                upload_minimumOrder=each['*MinimumOrder']
                upload_netWeight=each['NetWeight']
                upload_mrp=each['*MRP']
                upload_price=each['*Unit_Price']
                discount=each['*Discount_Name']
                upload_discount=each['*Discount']
                tax=each['*Tax_Name']
                upload_tax=each['*Tax']
                upload_netPrice=each['*NetPrice']
                upload_hsncode=each['*HSNcode']
                upload_photo=each['*Product_Photo']
                attributes=each['*Attributes']
                description=each['Description']
                manual_video=each['Manual_Video']
                manual_pdf=each['Manual_PDF']            
                extraimages1=each['*Extraimages1']
                extraimages2=each['Extraimages2']
                extraimages3=each['Extraimages3']
                extraimages4=each['Extraimages4']
                extraimages5=each['Extraimages5']
                data=each['Tags']
                metatags=each['Metadescription']
                keywords=each['Keywords']
                
                tagsinfo=[]
                for j in data.split(','):
                    tagsinfo.append(j)
                
                metatagsinfo=[]
                for info in metatags.split(','):
                    metatagsinfo.append(info)
                
                keywordsinfo=[]
                for keys in keywords.split(','):
                    keywordsinfo.append(keys)
                searchkeywords_list=[]
                product_name_list=upload_name.split(' ')
                searchkeywords_list.append(upload_name)
                searchkeywords_list.append(upload_brand.replace(' ','')+upload_subcategory.replace(' ',''))
                searchkeywords_list.append(upload_brand+' '+upload_subcategory)
                searchkeywords_list.append(upload_brand.replace(' ','')+upload_category.replace(' ',''))
                searchkeywords_list.append(upload_brand+' '+upload_category)
                searchkeywords_list.append(''.join(product_name_list))
                searchkeywords_list.append(' '.join(reversed(product_name_list)))
                searchkeywords_list.append(''.join(reversed(product_name_list)))
                searchkeywords_list.append(''.join(e for e in upload_name if e.isalnum()))
                searchkeywords_list.append(' '.join(re.sub('[^a-zA-Z0-9]+', '', _) for _ in product_name_list))
                #print searchkeywords_list
                
                attr = ast.literal_eval(attributes)
                update=Sup_Upload.objects(upload_id=upload_id,user_id=str(current_user.id))
                if update.count()>0:
                   warehouse=ProdinvWH.objects(prod_desc=upload_name,modelno=upload_modelno)
                   if warehouse:
                      sup= Sup_Upload.objects(upload_name=warehouse[0].prod_desc)
                      if upload_id!='' and upload_category!= '' and upload_subcategory!='' and upload_name!='' and upload_modelno!='' and upload_brand!='' and upload_pieceperCarton!='' and upload_minimumOrder!='' and upload_mrp!='' and upload_price!='' and discount!='' and upload_discount!='' and tax!='' and upload_tax!='' and upload_netPrice!='' and upload_hsncode!='' and upload_photo!='' and attributes!='' and extraimages1!='':
                          if Category.objects(categoryname=upload_category).count()>0 and Sub_Category.objects(subcategory=upload_subcategory).count()>0 and Reg_Supplier.objects().filter(supplier_brands__match={"supplier_brand":upload_brand}):
                            update=Sup_Upload.objects.get(upload_id=upload_id, user_id=str(current_user.id))
                            update.upload_id=upload_id
                            update.upload_category=upload_category
                            update.upload_subcategory=upload_subcategory
                            update.upload_name=upload_name.strip()
                            update.upload_modelno=upload_modelno
                            update.upload_brand=upload_brand
                            update.upload_warranty=upload_warranty
                            update.upload_pieceperCarton=upload_pieceperCarton
                            update.upload_minimumOrder=upload_minimumOrder
                            update.upload_netWeight=upload_netWeight
                            update.upload_mrp=upload_mrp
                            update.upload_price=upload_price
                            update.discount=discount
                            update.upload_discount=upload_discount
                            update.tax=tax
                            update.upload_tax=upload_tax
                            update.upload_netPrice=upload_netPrice
                            update.upload_hsncode=upload_hsncode
                            jar = cookielib.FileCookieJar("cookie")
                            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
                            url = 'http://192.168.20.9:80/product_data'
                            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
                            data = {"supplier_id":current_user.username,"upload_photo":upload_photo,"attributes":attr,"upload_brand":upload_brand}
                            data1=json.dumps(data)
                            #print data1
                            login_request = urllib2.Request(url,data1)
                            login_reply = opener.open(login_request)
                            login_reply_data = login_reply.read()
                            rec_data=ast.literal_eval(login_reply_data)
                            gifurl= rec_data['upload_photo']
                            #print gifurl
                            update.upload_photo=gifurl
                            #update.upload_locations=upload_locations
                            #update.frequency=frequency
                            update.description=description
                            update.extraimages=[upload_photo,extraimages1,extraimages2,extraimages3,extraimages4,extraimages5]
                            update.manual_video=manual_video
                            update.manual_pdf=manual_pdf
                            update.tags=tagsinfo                                                
                            update.metadescription=metatagsinfo                                                    
                            update.keywords=keywordsinfo
                            update.search_keywords=searchkeywords_list
            
                            attr = ast.literal_eval(each['*Attributes'])
                            listofattrs = update.attributes
                            update.attributes=[]
                            update.save()
                            for i in attr:
                                atrname=i['atrname']
                                atrvalue=i['atrvalue']
                                items=atr(atrname=atrname,atrvalue=atrvalue)
                                update.attributes.append(items)
                            update.save()
                            prodinv=ProdinvWH.objects(supplier=str(current_user.id),prod_desc=upload_name,modelno=upload_modelno,brand=upload_brand)
                            prodinvwh=prodinv[0]
                            prodinvwh.hsn=upload_hsncode
                            prodinvwh.prod_desc=upload_name
                            prodinvwh.modelno=upload_modelno
                            prodinvwh.brand=upload_brand
                            prodinvwh.save()
                          else:
                            return render_template('bulk-productupload-failed.html')
                      else:
                          return render_template('bulk-product-mandatory.html')
                            
                   else:
                       return render_template("nodatasup.html")
                else:
                   print "Insert Part"
                   #warehouse=ProdinvWH.objects(modelno__ne=upload_modelno)
                   sup= Sup_Upload.objects(upload_modelno=upload_modelno,upload_name=upload_name)
                   if sup:
                      return render_template("nodatasup.html")
                   else:
                        jar = cookielib.FileCookieJar("cookie")
                        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
                        url = 'http://192.168.20.9:80/product_data'
                        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
                        data = {"supplier_id":current_user.username,"upload_photo":upload_photo,"attributes":attr,"upload_brand":upload_brand}
                        data1=json.dumps(data)
                        #print data1
                        login_request = urllib2.Request(url,data1)
                        login_reply = opener.open(login_request)
                        login_reply_data = login_reply.read()
                        rec_data=ast.literal_eval(login_reply_data)
                        gifurl= rec_data['upload_photo']
                        #print gifurl
                        if upload_id!='' and upload_category!= '' and upload_subcategory!='' and upload_name!='' and upload_modelno!='' and upload_brand!='' and upload_pieceperCarton!='' and upload_minimumOrder!='' and upload_mrp!='' and upload_price!='' and discount!='' and upload_discount!='' and tax!='' and upload_tax!='' and upload_netPrice!='' and upload_hsncode!='' and upload_photo!='' and attributes!='' and extraimages1!='':
                          if '&' not in upload_name:  
                           if Category.objects(categoryname=upload_category).count()>0 and Sub_Category.objects(categoryname=upload_category,subcategory=upload_subcategory).count()>0 and Reg_Supplier.objects().filter(supplier_brands__match={"supplier_brand":upload_brand}):
                               value=Sup_Upload(user_id=user_id,upload_id=upload_id,upload_category=upload_category,upload_subcategory=upload_subcategory,upload_name=upload_name.strip(),upload_modelno=upload_modelno,
                                            upload_brand=upload_brand,upload_warranty=upload_warranty,upload_pieceperCarton=upload_pieceperCarton,upload_minimumOrder=upload_minimumOrder,upload_netWeight=upload_netWeight,upload_mrp=upload_mrp,
                                            upload_price=upload_price,discount=discount,upload_discount=upload_discount,tax=tax,upload_tax=upload_tax,upload_netPrice=upload_netPrice,upload_hsncode=upload_hsncode,
                                            upload_photo=gifurl,upload_locations='0',frequency='0',description=description,manual_video=manual_video,manual_pdf=manual_pdf,
                                                tags=tagsinfo,metadescription=metatagsinfo,keywords=keywordsinfo,search_keywords=searchkeywords_list,
                                             extraimages=[upload_photo,extraimages1,extraimages2,extraimages3,extraimages4,extraimages5],salesqty='0',avgrating='0')
                               value.save()
                               for value in Sup_Upload.objects(upload_name=upload_name,upload_modelno=upload_modelno,upload_brand=upload_brand):
                                   price = PriceLists(landing_price='0', dealer_price='0',offer_price='0',enduser_price='0',bulk_unit_price='0',bulk_qty='0',percentage=0,doubleoffer_price=0,landing_price_gst=0, dealer_price_gst=0,offer_price_gst=0,enduser_price_gst=0)  
                                   value.prices.append(price)
                                   value.save()
                               for i in attr:
                                   atrname=i['atrname']
                                   atrvalue=i['atrvalue']
                                   items=atr(atrname=atrname,atrvalue=atrvalue)
                                   value.attributes.append(items)
                                   value.save()
                               prodinvobj=ProdinvWH(supplier=str(current_user.id),warehouse='Default',hsn=upload_hsncode,modelno=upload_modelno,brand=upload_brand,prod_desc=upload_name,smtids=[],
                                       quantity='0',outqty='0',barcode=upload_id)
                               prodinvobj.save()
                               
                               for prodinvobj in ProdinvWH.objects(prod_desc=upload_name,modelno=upload_modelno,brand=upload_brand):
                                    inv=InvoiceList()
                                    prodinvobj.invoice_smtlist.append(inv)
                                    prodinvobj.save()
                               for prodinvobj in ProdinvWH.objects(prod_desc=upload_name,modelno=upload_modelno,brand=upload_brand):
                                    price = PriceList(landing_price='0', dealer_price='0',offer_price='0',enduser_price='0',bulk_unit_price='0',bulk_qty='0',landing_price_gst=0, dealer_price_gst=0,offer_price_gst=0,enduser_price_gst=0)  
                                    prodinvobj.prices.append(price)
                                    prodinvobj.save()
                                  
                           else:
                               return render_template('bulk-productupload-failed.html')
                          else:
                             return render_template('product_name_fail.html')
                        else:
                           return render_template('bulk-product-mandatory.html')
            return render_template('productupload_success.html')
        logger.info('Entered into Bulk Products upload')
        return render_template('bulkproduct-upload.html',form=form)
    except Exception as e:
       return jsonify('{"mesg":' + str(e) +'}')


@supplierapp.route('/image_setup', methods = ['GET', 'POST'])
def image_setup():
        with supplierapp.app_context():
         form = ImageForm()
        if request.method == 'POST':
            supplier_id= request.form['supplier_id']
            supname=current_user.username
            print supname
            productname = request.form['productname']
            uploaded_files = request.files.getlist("file1[]")
            print uploaded_files
            filenames = []
            s3 = boto3.resource('s3',
            aws_access_key_id=ACCESS_ID,
            aws_secret_access_key=ACCESS_KEY)
            client = boto3.client('s3', aws_access_key_id=ACCESS_ID,aws_secret_access_key=ACCESS_KEY)
            item=0
            img=[]
            images=[]
            for file in uploaded_files:
               if file and allowed_file(file.filename):
                   filename = secure_filename(file.filename)
                   item += 1
                   var=str(item)
                   file.save(os.path.join(supplierapp.config['UPLOAD_IMAGE'],var+productname+'_'+filename))
                   full_key_name = os.path.join(supplierapp.config['UPLOAD_IMAGE'],var+productname+'_'+filename)
                   transfer = S3Transfer(client)
                   transfer.upload_file(full_key_name, 'gstbucket1', 'static/images/'+supname+'/'+var+productname+'_'+filename)
                   #s3 = boto3.resource('s3')
                   object_acl = s3.ObjectAcl('gstbucket1','static/images/'+supname+'/'+var+productname+'_'+filename)
                   response = object_acl.put(ACL='public-read')
                   filenames.append(file.filename)
                   img.append("https://s3.ap-south-1.amazonaws.com/gstbucket1/static/images/"+supname+'/'+var+productname+'_'+filename)
            imageinfo =Images(user_id=str(current_user.id),supplier_id=supplier_id,productname=productname,image=img) 
            imageinfo.save()
            return redirect(url_for('image_setup'))
        else:
            Imageslist = Images.objects(user_id=str(current_user.id))
            logger.info('Sucessfully setup header')
            return render_template('image_setup.html',form=form,Imageslist=Imageslist)

@supplierapp.route('/image_setup_delete/', methods=['GET', 'POST'])
@login_required
def headersetup_delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="head"):
            img_info = Images.objects.get(id=docid)
            img_info.delete()
        logger.info('Deleted header in header setup')
        return redirect(url_for('image_setup'))                                                   
#-------------------------   logout----------------------------
@supplierapp.route('/logout')
def logout():
    logout_user()
    logger.info('Supplier Loggedout Sucessfully')
    return redirect(supplierapp.config['Mainurl'])


if __name__ == '__main__':
    now = datetime.date.today().strftime("%Y_%m_%d")
    handler = RotatingFileHandler("loggers/supplierapplogs/"+"supplierapp_" + str(now) + ".log", maxBytes=100000, backupCount=3)
    logger = logging.getLogger('__name__')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    supplierapp.run(host='127.0.0.1',port=5003,threaded=True)
