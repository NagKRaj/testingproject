#!/usr/bin/env python2.7
# -*- coding: utf-8 -*- 
from app import Flask, request, url_for, redirect, render_template, abort , Response,session,jsonify,flash
from form import UserRegistration,BillingForm,ShopOrderForm,ShopOrderviewForm,ShopsetupForm,ShopUserForm,BankForm,EditForm,ServiceForm
from models import Sup_Upload,ProdInvShipping,ShipData,ProdInvShop,SmtidShop,Prices,Reg_Dealer,UserSignup,Warehouse,\
Category,Sub_Category,Product,Company_Setup,Billing_Setup,Header_Setup,PriceList,InvoiceList,ProdinvWH,ShopOrderInvoice,\
ShopInvoice,ShopCharges,ShopOrders,Orders,Shopsetup,ShopUser,Bank_Setup,CustomerOrders,OrderItem,ConfirmInvoice,\
ConfirmInvoiceOrderItems,ProdInvCMR,CmrInfo,ProdInfo,CustomerDetails,userLoginCheck,Reg_Service,BillingShippingAddress,Header
from flask_login  import login_user ,logout_user ,current_user ,login_required
from flask_login  import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import json,time, os,ast
from os import path
from controler import SignUpControler
import requests
from purchasenumber import PurchaseNumber,ShopPurchaseNumber
import sys
sys.setrecursionlimit(10000)
import PIL.Image
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
import datetime
import urllib
#from shopid import ShopNumber
from randomnumber import Number,DealerNumber,ShopNumber
import traceback
from num2words import num2words
from multiprocessing import Pool
from datetime import date,timedelta
sys.modules['Image'] = PIL.Image
dealerapp = Flask(__name__)
dealerapp.secret_key = 'secret'

login_manager = LoginManager()
login_manager.init_app(dealerapp)
login_manager.session_protection = "strong"
dealerapp.config['UPLOAD_LOGO'] = './static/logo/'
dealerapp.config['Mainurl']='http://127.0.0.1:8000/'
dealerapp.config['Dealer_Dashboard']='http://127.0.0.1:5004/'

dealerapp.config['NOTIFICATIONS']='True'
dealerapp.config['SMS']='True'

def synchronized(wrapped):
    lock = threading.Lock()
    @functools.wraps(wrapped)
    def _wrap(*args, **kwargs):
        with lock:
            return wrapped(*args, **kwargs)
    return _wrap


def sendMail(email,subject,htmlbody):
    if dealerapp.config['NOTIFICATIONS']=='True':
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
        
    if(dealerapp.config['SMS'])=='True':
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

@dealerapp.after_request
def after_request(response):
    # this if avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler
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

@dealerapp.errorhandler(Exception)
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
   logger.info('Entered into unauthorized callback')
   return render_template('error.html',reportsof = 'Unauthorized out ....')


#---------------------------- Dealer Dashbord-------------------

@dealerapp.route('/dealer_dashboard/<userid>', methods = ['GET', 'POST'])
def dealer_dashboard(userid):
       uservalue = UserSignup.objects.get(id=userid)
       login_user(uservalue, remember=True)
       shop_order=ShopOrders.objects(user_id=str(current_user.id)).count()
       shop_invoice=ShopOrderInvoice.objects(dealer_id=str(current_user.userid)).count()
       prod_shop=ProdInvShop.objects(user_id=str(current_user.id)).count()
       shopname=Shopsetup.objects(user_id=str(current_user.id))
       if shopname.count()>0:
           
           customer_order=CustomerOrders.objects(shop=shopname[0].shop_name)
           if customer_order==[]:
               customer_order=0
           else:
              customer_order=customer_order.count()
       else:
           customer_order=0
       if shopname.count()>0:
           customer_invoice=ConfirmInvoice.objects(shop=shopname[0].shop_name)
           if customer_invoice==[]:
               customer_invoice=0
           else:
               customer_invoice=customer_invoice.count()
       else:
           customer_invoice=0
       logger.info('Entered into Delaer dashborad')
       return render_template('dealer-dashboard.html',shop_order=shop_order,shop_invoice=shop_invoice,customer_order=customer_order,customer_invoice=customer_invoice,prod_shop=prod_shop)


@dealerapp.route('/service_center', methods = ['GET', 'POST'])
@login_required
def service_center():  
        with dealerapp.app_context():
            form = ServiceForm()
        if request.method == 'POST' and form.validate():
            service_center = request.form['service_center']
            service_area = request.form['service_center_area']
            serviceUser = Reg_Service(user_id=str(current_user.id),service_center=service_center,service_center_area=service_area)# Insert form data in 
            serviceUser.save()
            return redirect(url_for('service_center'))
        else:
            service=Reg_Service.objects(user_id=str(current_user.id))
            return render_template('service_center.html',form=form,service=service)


@dealerapp.route('/service_delete/', methods=['GET', 'POST'])
@login_required
def service_delete():
        logger.info('Entered into user_delete')
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="i"):
            service = Reg_Service.objects.get(id=docid)
            service.delete()
        logger.info('Sucessfully Deleted  %s  in service',type)
        return redirect(url_for('service_center'))

  
#------------------------------------------shop user -----------------------------------------------------------------------------
@dealerapp.route('/shopuser', methods = ['GET', 'POST','PUT'])
@login_required
def shopuser():
        with dealerapp.app_context():
            form = ShopUserForm()
        if request.method == 'POST':
            userid=request.form['userid']
            username = request.form.get('username')
            email=request.form['email']
            mobile=request.form['mobile']
            shop=request.form.get('shop')
            password = request.form['password']
            createdby = request.form['createdby']
            date=request.form.get('date')
            isuseridExist=ShopUser.objects(userid=userid,user_id=str(current_user.id))
            status=request.form.get('shophide')
            if status=='yes':
                shop_edit = ShopUser.objects.get(user_id=str(current_user.id),userid=userid)
                shop_edit.username=username
                shop_edit.shop=shop
                shop_edit.mobile=mobile
                #shop_edit.password=password
                shop_edit.save()
                logger.info('shopuser edited Successfully')
            else:
                if isuseridExist.count()>0:
                    return render_template('shopuseridexists.html')
                shop = ShopUser(user_id=str(current_user.id),userid=userid,username=username, email=email, mobile=mobile,shop=shop, password =generate_password_hash(password),createdby=createdby,created_date=date)# Insert form data in collection
                shop.save()
            logger.info('New shopuser saved Successfully')
            return redirect(url_for('shopuser'))
        else:
            if current_user.usertype=='Admin':
               user=ShopUser.objects()
          
            user=ShopUser.objects(user_id=str(current_user.id))
            shopid=Shopsetup.objects(user_id=str(current_user.id))
            empDetails = UserSignup.objects.get(email = current_user.email)
            form.createdby.data = empDetails.username
            logger.info('Entered into Shopuser')
            return render_template('shopuser.html', form=form,user=user,shopid=shopid)


@dealerapp.route('/shopuserdelete/', methods=['GET'])
@login_required
def shopuserdelete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="shopuser"):
            quickview = ShopUser.objects.get(id=docid)
            quickview.delete()
        logger.info('shopuser Deleted')
        return redirect(url_for('shopuser'))
  
#----------------------------------------------------------------------shop setup-----------------------------------------------
@dealerapp.route('/shopsetup', methods = ['GET', 'POST'])
@login_required
def shopsetup():
        pool = Pool()
        pool_new(pool)
        with dealerapp.app_context():
            form = ShopsetupForm()
        if request.method == 'POST':
            shop_id= request.form.get('shop_id')
            shop_name=request.form['shop_name']
            reg_shop_name=request.form['reg_shop_name']
            shop_address=request.form['shop_address']
            pincode = request.form['pincode']
            latitude = float(request.form['latitude'])
            #print pincode
            longitude = float(request.form['longitude'])
            email = request.form['email']
            phone=request.form['phone']
            dealer=request.form.get('dealer')
            password = request.form['password']
            isshopidExist=Shopsetup.objects(shop_id=shop_id,user_id=str(current_user.id))
            isshopExist=Shopsetup.objects(shop_name=shop_name)
            isdataExist=Shopsetup.objects(user_id=str(current_user.id))
            status=request.form.get('shophide')
            if status=='yes':
                shop_edit = Shopsetup.objects.get(user_id=str(current_user.id),shop_name=shop_name)
                shop_edit.shop_address=shop_address
                shop_edit.pincode=pincode
                shop_edit.lat_long=[longitude,latitude]
                shop_edit.dealer=dealer
                shop_edit.save()
                logger.info('Shop Edited Successfully')
            else:
                if isshopidExist.count()>0:
                    return render_template('shopidexists.html')
                elif isshopExist.count()>0:
                    return render_template('shopexists.html')
                elif isdataExist.count()>0:
                    return render_template('uniqueshop.html')
                ShopNumber().put(shop_id)
                 
                if latitude=='' and longitude=='':
                    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+pincode)
                    resp_json_payload = response.json()
                    lat_lon=(resp_json_payload['results'][0]['geometry']['location'])
                    lat= lat_lon['lat']
                    lng= lat_lon['lng']
                    setup =Shopsetup(user_id=str(current_user.id),shop_id=shop_id, shop_name=shop_name ,reg_shop_name=reg_shop_name, shop_address=shop_address , pincode=pincode, lat_long=[float(lng),float(lat)],email=email , phone=phone, dealer=dealer ,password=password) 
                    setup.save()
                elif latitude:
                   setup =Shopsetup(user_id=str(current_user.id),shop_id=shop_id, shop_name=shop_name ,reg_shop_name=reg_shop_name, shop_address=shop_address , pincode=pincode, lat_long=[float(longitude),float(latitude)],email=email , phone=phone, dealer=dealer ,password=password) 
                   setup.save() 
                registeredUser = UserSignup.objects(usertype='Market Manager')
                User = Reg_Dealer.objects(user_id=str(current_user.id))
                if registeredUser.count() > 0:
                    fo = open("./static/mailtemp/dealermailtemp.html", "r+")
                    htmlbody = fo.read()
                    fo.close()
                    urldata="A new shop "+shop_name+" of dealer "+User[0].dealer_name+" is added to the location"+ pincode+"."
                    htmlbody = htmlbody.replace("$$urldata$$",urldata)
                    #sendMail(registeredUser[0].email,"A shop "+shop_name+ " is avilable in pin "+pincode+" of Dealer "+User[0].dealer_name,htmlbody)
                    pool.apply_async(sendMail,[registeredUser[0].email,"A shop "+shop_name+ " is avilable at "+pincode,htmlbody])
                    msg="A new shop "+shop_name+" of dealer "+User[0].dealer_name+" is added to the location"+ pincode+"."
                    #mobile='91'+registeredUser[0].mobile
                    mobileList=[]
                    mobileList.append('91'+registeredUser[0].mobile)
                    #SMS(msg,mobile)
                    pool.apply_async(SMS,[msg,mobileList])
            logger.info('New Shop Saved Successfully')
            
            return redirect(url_for('shopsetup'))
        else:
            if current_user.usertype=='Admin':
               shop = Shopsetup.objects()
            else:
                shop = Shopsetup.objects(user_id=str(current_user.id))
            numbers =  ShopNumber().get()
            empDetails = UserSignup.objects.get(email = current_user.email)
            #print empDetails.email
            #print current_user.email
            User = Reg_Dealer.objects(user_id=str(current_user.id))
            #print User[0].dealer_mail
            #print current_user.email,"email"
            form.shop_name.data = User[0].dealer_shopname
            form.reg_shop_name.data = User[0].reg_shopname
            form.email.data = empDetails.email
            form.phone.data = empDetails.mobile
            logger.info('Entered into shopsetup')
            return render_template('shop-setup.html', form=form, shop=shop,numbers=numbers)
    
@dealerapp.route('/shopsetup_delete/', methods=['GET'])
@login_required
def shopsetup_delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="setup"):
            quickview = Shopsetup.objects.get(id=docid)
            quickview.delete()
        logger.info('Shop Deleted')
        return redirect(url_for('shopsetup'))

#-------------------------------------------------------------------shop order/purchase order-----------------------------------------------------------
@dealerapp.route('/shop_order', methods=['GET', 'POST'])
@login_required
def shop_order():
        with dealerapp.app_context():
            form = ShopOrderForm()
        if request.method == 'POST':
            warehouse_docid = request.form.get('warehouse_docid')
            shop_docid=request.form.get('shop_docid')
            return redirect(url_for('shoporder_viewmore'))
        else:
            warehouselist = Warehouse.objects()
            shopslist = Shopsetup.objects(user_id=str(current_user.id))
            if len(shopslist)==0:
                return render_template('errormsg.html')
            logger.info('Entered into shop_order')
            return render_template('shop-order-login.html', form=form,shopslist=shopslist,warehouselist=warehouselist)



@dealerapp.route('/shoporder_viewmore', methods=['GET', 'POST'])
@login_required
def shoporder_viewmore():
        with dealerapp.app_context():
            form = ShopOrderviewForm()
        if request.method == 'POST':
            shop_docid=request.form.get('shop_docid')
            warehouse_docid = request.form.get('warehouse_docid')
            '''if shop_docid=='0' or warehouse_docid =='0':
                  return redirect(url_for('shop_order'))
            warehouselist = Warehouse.objects.get(id=warehouse_docid)
            '''
            shops = Shopsetup.objects(id=shop_docid)
            if len(shops)==0:
                  logger.info('Fialed to shoporder')
                  return render_template('error.html',reportsof = 'Exception',msg='No Shops Available')
            shopslist=shops[0]
            user=current_user
            shoppurchaseNumber = ShopPurchaseNumber().get()
            #ShopPurchaseNumber().put(shoppurchaseNumber)
            categorylist = Category.objects()
            subcategory = Sub_Category.objects()
            dealerlist=UserSignup.objects(email=current_user.email)
            br=[]
            for prod in ProdinvWH.objects():
                data={}
                data['brand']=prod.brand
                inlistFlag = True
                for inlist in br:
                    if(inlist['brand']==prod.brand):
                           inlistFlag=False
                           
                if inlistFlag:
                    br.append(data)
            logger.info('Entered into shoporderviewmore')
            return render_template('shop-orders.html',form=form,dealerlist=dealerlist[0],shopslist=shopslist,subcategory=subcategory,prod=br
                              ,warehouse_docid=warehouse_docid,shop_docid=shop_docid,user=user,categorylist=categorylist,shoppurchaseNumber=shoppurchaseNumber)

        
@dealerapp.route('/newbrand_post/', methods=['GET', 'POST'])
@login_required
def newbrand_post():
       brand=request.args.get('brand')
       #warehouse=request.args.get('warehouse')
       #info=ProdinvWH.objects(brand=brand).only('modelno')
       #modelnos = json.loads(info.to_json())
       br=[]
       for i in ProdinvWH.objects(brand=brand,prices__offer_price_gst__gt=0.0):
                 br.append(i.modelno)
       modelnos=sorted(set(br))
       logger.info('Entered into new brand post')
       return jsonify(modelnos)



@dealerapp.route('/shoporder', methods=['GET', 'POST'])
@login_required
def shoporder():
      if request.method == 'POST':
          logger.info('Entered into shoporder')
          json_data = request.get_json(force=True)
          brand = json_data['brand']
          modelno = json_data['modelno']
          #warehouse=json_data['warehouse']
          wh=[]
          if brand == '0' and modelno == '0':
              wh= ProdinvWH.objects()
          elif brand == '0':
              wh=ProdinvWH.objects(modelno=modelno)
          elif modelno == '0':
             wh= ProdinvWH.objects(brand=brand)
          else:
             wh= ProdinvWH.objects(modelno=modelno,brand=brand)
           
          product=[]
          for products in wh:
            for i in products.prices:
             if i.enduser_price>'0' and i.offer_price>'0':
              qty=ProdInvShop.objects(user_id=str(current_user.id),model=products.modelno,brand=products.brand)
              avlqty = '0'
              if qty.count() >0: 
                    if qty[0].inqty != '0':
                        avlqty = qty[0].inqty
              sup=Sup_Upload.objects(upload_name=products.prod_desc,upload_modelno=products.modelno,upload_brand=products.brand)
              data={}
              data['supplier']=products.brand
              data['modelno']=products.modelno
              data['hsn']=products.hsn
              data['image']=sup[0].upload_photo
              data['prod_desc']=products.prod_desc
              data['quantity']=avlqty
              data['dealer_price']=i.dealer_price
              data['enduser_price']=i.enduser_price
              data['offer_price']=i.offer_price
              op=float(i.offer_price)
              dp=float(i.dealer_price)
              su=op-dp
              sums=format(su, '.2f')
              data['profit']=sums
              product.append(data)
          return jsonify(product)
         
      else:
          return 'You  have to select atleast one product'

@dealerapp.route('/shoporder_post', methods=['GET', 'POST'])
@login_required
def shoporder_post():
    pool = Pool()
    pool_new(pool)
    try:
      if request.method == 'POST':
       json_data = request.get_json(force=True)
       warehouse_name = json_data['ware_house']
       shop_name = json_data['shop_name']
       shop_id=json_data['shop_id']
       shop_address = json_data['shop_address']
       dealer_id = json_data['dealer_id']
       #shop_po = json_data['shop_po']
       po_date = json_data['po_date']
       totalitems = json_data['total_items']
       totalqty = json_data['total_quantity']
       if totalitems=='0' or totalqty =='0':
           return redirect(url_for('shoporder'))
       elif totalitems=='NaN' or totalqty =='NaN':
           return 'Fail'
       totalvalue = json_data['total_value']
       shoppurchaseNumbers = ShopPurchaseNumber().get()    
       
       #print shoppurchaseNumbers
       shoppurchaseinfo = ShopOrders(user_id=str(current_user.id),warehouse_name=warehouse_name, shop_name=shop_name,shop_id=shop_id,
                                        shop_address=shop_address, dealer_id=dealer_id,shop_purchaseorderno=shoppurchaseNumbers,
                                        po_date =po_date,totalitems=totalitems,totalqty=totalqty,totalvalue=totalvalue,order_edit_by="0",order_edited_date="0")
       shoppurchaseinfo.save()
       item=0
       for i in json_data['items']:
            item += 1
            var=str(item)
            #item = i['item']
            supplier=i['supplier']
            hsn = i['item_hsn']
            model_no = i['item_model']
            quantity = i['item_quntity']
            netprice = i['item_price']
            value = i['item_value']
            order = Orders(var,supplier,model_no,hsn,quantity ,netprice,value)
            #print order
            shoppurchaseinfo.orderslist.append(order)
            shoppurchaseinfo.save()
       
       logger.info('Shop Order saved successfully')
   
       User = Reg_Dealer.objects(user_id=str(current_user.id))
       registeredUser = UserSignup.objects(usertype='Market Manager')
       if registeredUser.count() > 0:
           fo = open("./static/mailtemp/dealermailtemp.html", "r+")
           htmlbody = fo.read()
           fo.close()
           urldata=User[0].dealer_name+" has placed an order. Update required on the order status."
           htmlbody = htmlbody.replace("$$urldata$$",urldata)
           #sendMail(registeredUser[0].email,'Dealer Places an order SPO '+shop_po,htmlbody)
           pool.apply_async(sendMail,[registeredUser[0].email,'Order placed with SPO No.: '+shoppurchaseNumbers,htmlbody])
           msg=User[0].dealer_name+" has placed an order. Update required on the order status."
           mobile='91'+registeredUser[0].mobile
           mobileList=[]
           mobileList.append('91'+registeredUser[0].mobile)
           #SMS(msg,mobile)
           pool.apply_async(SMS,[msg,mobileList])
    
       ShopPurchaseNumber().put(shoppurchaseNumbers)
       return 'Success'
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')

@dealerapp.route('/shoporder_delete', methods=['GET'])
@login_required
def shoporder_delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="em"):
            quickview = ShopOrders.objects.get(id=docid)
            quickview.delete()
        logger.info('ShopOrder Deleted')
        return redirect(url_for('shoporderlist'))    

#--------------------------------------------------------------------billing setup--------------------------------------------------
@dealerapp.route('/billing_setup', methods = ['GET', 'POST'])
@login_required
def billing_setup():
        with dealerapp.app_context():
         form = BillingForm()
        if request.method == 'POST':
            dealerid=request.form.get('dealerid')
            companyname = request.form['companyname']
            address=request.form['address']
            pan = request.form['pan']
            gstin=request.form['gstin']
            cin=request.form['cin']
            state=request.form['state']
            b= str(state.split("-")[0])
            statecode=request.form['statecode']
            companylogo= request.files['companylogo']
            contactno=request.form['contactno']
            companylogo.save(os.path.join(dealerapp.config['UPLOAD_LOGO'], companylogo.filename))
            billinginfo =Billing_Setup(user_id=str(current_user.id),dealerid=dealerid,companyname=companyname, address=address , pan=pan , gstin=gstin,cin=cin,state=b,statecode=statecode,
                                       companylogo=companylogo.filename,contactno=contactno) 
            billinginfo.save()
            logger.info('Created Billing in Billing Setup')
            return redirect(url_for('billing_setup'))
        else:
            dealerid=UserSignup.objects(email=current_user.email)
            Billinglist = Billing_Setup.objects(user_id=str(current_user.id))
            regdealer=Reg_Dealer.objects(user_id=str(current_user.id))
            #form.companyname.data=regdealer[0].dealer_shopname
            form.companyname.data=regdealer[0].reg_shopname
            form.address.data=regdealer[0].dealer_address
            form.pan.data=regdealer[0].dealer_pan
            form.gstin.data=regdealer[0].dealer_gstin
            form.cin.data=regdealer[0].dealer_cin
            form.contactno.data=regdealer[0].dealer_mobile
            form.state.data=regdealer[0].dealer_state
            a=regdealer[0].dealer_gstin
            b=a[0:2]
            form.statecode.data=b
            
            logger.info('Entered into billing setup')
            return render_template('billing-setup.html',form=form,Billinglist=Billinglist,dealerid=dealerid[0],regdealer=regdealer)
            

@dealerapp.route('/billingsetup_delete/', methods=['GET', 'POST'])
@login_required
def billingsetup_delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="billing"):
            billing_info = Billing_Setup.objects.get(id=docid)
            billing_info.delete()
        logger.info('Deleted Billing in Billing Setup')
        return redirect(url_for('billing_setup'))
        
#---------------------------------------------- bank setup-----------------------------------------------------------------------------
@dealerapp.route('/bank_configuration', methods = ['GET', 'POST'])
@login_required
def bank_configuration():
        with dealerapp.app_context():
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
               company=Reg_Dealer.objects(user_id=str(current_user.id))
               form.ac_holdername.data = company[0].dealer_shopname
            logger.info('Entered into bank configuration')
            return render_template('bank-configuration.html',form=form,bankdetailes=bankdetailes)


@dealerapp.route('/bankdelete/', methods=['GET', 'POST'])
@login_required
def bankdelete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="bank"):
            bankinfo=Bank_Setup.objects.get(id=docid)
            bankinfo.delete()
        logger.info('Deleted Bank Deatils')
        return redirect(url_for('bank_configuration'))
#----------------------------------------------------------------edit profile--------------------------------------------------------------------------------------
@dealerapp.route('/editprofile', methods = ['GET', 'POST'])
@login_required
def editprofile():
      with dealerapp.app_context():
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
               return redirect(dealerapp.config['Dealer_Dashboard']+'dealer_dashboard/'+str(current_user.id))
               
      else:
            User = UserSignup.objects.get(id=current_user.id)
            userEditForm.username.data = User.username
            userEditForm.email.data = User.email
            userEditForm.mobile.data = User.mobile
            logger.info('Entered into editprofile')
            return render_template('edit_profile.html',userEditForm=userEditForm)

@dealerapp.route('/signupedit', methods = ['GET', 'POST'])
@login_required
def signupedit():
      with dealerapp.app_context():
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
               return redirect(dealerapp.config['Dealer_Dashboard']+'dealer_dashboard/'+str(current_user.id))
      else:
            User = UserSignup.objects.get(id=current_user.id)
            userEditForm.username.data = User.username
            userEditForm.email.data = User.email
            userEditForm.mobile.data = User.mobile
            
            logger.info('Entered into useredit')
            return render_template('signupedit.html',userEditForm=userEditForm,user=User)	

#---------------------------------------------------------------------shop inhouse--------------------------------------------
@dealerapp.route('/shopinhouse', methods=['GET', 'POST'])
@login_required
def shopinhouse():
    try:
        logger.info('Entered into editprofile')
        return render_template('shopinhouse.html')

    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')   


@dealerapp.route('/shopinhouse_ajax', methods=['GET', 'POST'])
@login_required
def shopinhouse_ajax():
    try:
      if request.method == 'POST':
        logger.info('Entered into shopinhouse ajax')
        json_data = request.get_json(force=True)
        invoiceid = json_data['invoice']
        
        detail=[]
        shopinvno=ShopOrderInvoice.objects(shopinvoice_number=invoiceid)
        if shopinvno.count()==0:
                 data={}
                 data['status']='false'
                 detail.append(data)
                 return jsonify(detail)
        shopinv=ShopOrderInvoice.objects.get(shopinvoice_number=invoiceid)
        if shopinv.dealer_id==str(current_user.userid):
            prodinv=ProdInvShipping.objects(invoice=invoiceid,status="Shipping")
            
            for i in prodinv:
                data={}
                data['whName']=i.warehouse
                #print i.warehouse
                data['shopId']=i.shop
                for j in i.orderslist:
                    data['barnd']=j.brand
                    data['modelNo']=j.model
                    
                    data['smtids']= j['smtid']
                    sup = Sup_Upload.objects(upload_modelno=j.model,upload_brand=j.brand)
                    data['category']=sup[0].upload_category
                    data['subCategory']=sup[0].upload_subcategory
                    prodwh = ProdinvWH.objects(modelno=sup[0].upload_modelno,brand=sup[0].upload_brand)
                    data['barcode']= prodwh[0].barcode
                    data['inQty']=j.qty
                    '''
                    avlqty = '0'
                    qtys = CustomerOrders.objects(shop=prodinv[0].shop)
                    if qtys.count() >0:
                     for out in qtys:   
                      for j in out.orderitems:
                         if j.productdescription==prodwh[0].prod_desc:                                                 
                          if j.qty != '0':
                            avlqty = j.qty
                    '''
                    data['outQty']='0'
                    
                    for price in prodwh[0].prices:
                        data['delaerPrice']=price.dealer_price
                        data['enduserPrice']=price.enduser_price
                        supname=UserSignup.objects(id=prodwh[0].supplier)                        
                        data['supCode']=supname[0].username   
                        test=ast.literal_eval(json.dumps(data))
                        detail.append(test)
            return jsonify(detail)  
        else:
            return 'error'
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')

@dealerapp.route('/shopinhousepost',methods = ['GET', 'POST'])
@login_required
def shopinhousepost():
    pool = Pool()
    pool_new(pool)
    try:
     if request.method == 'POST':
       json_data = request.get_json(force=True)
       invoice = json_data['invoice']
       #return invoice
       insert_list=[]
       update_list=[]
       for i in json_data['items']:
           supid = i['item_supcode']
           warehouse = i['item_whname']                  
           shop= i['item_shopId']
           cat = i['item_category']
           subcat= i['item_subcategory']
           brand= i['item_barnd']
           model= i['item_modelNo']
           barcode= i['item_barcode']
           inqty= i['item_inqty']
           outqty= i['item_outqty']
           dealerprice= i['item_dealerprice']
           endprice= i['item_enduserprice']
           smt= i['item_smtid']
           checked=i['item_check']
           a=smt.replace("'",'')
           s=a.split(',')
           shopsmt=[]
           for sid in s:
               shopsmt.append(sid)
           if checked=="false":
                user=UserSignup.objects(usertype='WH-Manager')
                emailList=[]
                emailList.append(user[0].email)
                fo = open("./static/mailtemp/dealermailtemp.html", "r+")
                htmlbody = fo.read()
                fo.close()                                
                urldata= "Your order for the product from "+ str(warehouse) +"Shop Name :"+ str(shop) +"Invoice ID :"+ str(invoice) +" Model No :"+ str(model) +" SMT ID :"+ str(a) +" is delayed.Sorry for the inconvinience.For any further assistance, contact us at 040-46161234 or write to us at smthub.2017@gmail.com on all days between 9am to 10pm."
                
                htmlbody = htmlbody.replace("$$urldata$$",urldata)
                #sendMail(emailList,'Products are Missed',htmlbody)
                pool.apply_async(sendMail,[emailList,'We regret for the inconvinience',htmlbody])
               
           elif checked == "true":
               sup=Sup_Upload.objects(upload_modelno=model,upload_brand=brand)
               print sup
               prodinvobj1=ProdInvShop.objects(supplier=supid,shop=shop,proddescription=sup[0].upload_name)
               if prodinvobj1.count()==0:
                   insert_list.append(sup[0].upload_name)
                   shops = ProdInvShop(user_id=str(current_user.id),supplier=supid,warehouse=warehouse,shop=shop,model=model,brand=brand,category=cat,subcategory=subcat,inqty=inqty,outqty=outqty,
                                       avlsmtid=shopsmt,barcode=barcode,proddescription=sup[0].upload_name,tax=sup[0].upload_tax)
                   shops.save()
                   shopprice = SmtidShop(smtid=shopsmt,invoiceid=invoice)
                   shops.smtidshop.append(shopprice)
                   #return 'Hii'
                   shops.save()
                  
                   for prodwh in ProdinvWH.objects(modelno=model,brand=brand):
                      for price in prodwh.prices:
                         shopprices = Prices(dealer_price=dealerprice,enduser_price=endprice,offer_price=price.offer_price,comboffer=price.bulk_qty,landing_price_gst=price.landing_price_gst,dealer_price_gst=price.dealer_price_gst,offer_price_gst=price.offer_price_gst,enduser_price_gst=price.enduser_price_gst)
                         shops.price.append(shopprices)
                         shops.save()
                   shipping=ProdInvShipping.objects.get(invoice=invoice)
                   shipping.status='Delivered'
                   shipping.save()
                   shopinvoice=ShopOrderInvoice.objects.get(shopinvoice_number=invoice)
                   shopinvoice.status = 'Delivered'
                   shopinvoice.save()
                   
                   shoporder=ShopOrders.objects.get(shop_purchaseorderno=shopinvoice.shop_purchaseorderno)
                   shoporder.status='Delivered'
                   shoporder.save()
                   
                   
               else: 
                  update_list.append(sup[0].upload_name)
                  #prodinvobjects=ProdInvShop.objects(shop=shop,proddescription=sup[0].upload_name)
                  prodinvobj=prodinvobj1[0]
                  smt=[]
                  for i in prodinvobj.avlsmtid:
                      smt.append(i)
                  smtid=smt+shopsmt
                  qty= int(str(prodinvobj.inqty))
                  totalqty = int(inqty)
                  totalinqty=str(qty+totalqty)
                  #print totalinqty
                  inv=SmtidShop(smtid=shopsmt,invoiceid=invoice)
                  prodinvobj.smtidshop.append(inv)                   
                  prodinvobj.avlsmtid=smtid                 
                  prodinvobj.inqty=totalinqty
                  prodinvobj.save()
                  shipping=ProdInvShipping.objects.get(invoice=invoice)
                  shipping.status='Delivered'
                  shipping.save()
                  shopinvoice=ShopOrderInvoice.objects.get(shopinvoice_number=invoice)
                  shopinvoice.status = 'Delivered'
                  shopinvoice.save()
                  shoporder=invoice.replace('SPOIN','SPO')
                  #print shoporder
                  shoporder=ShopOrders.objects.get(shop_purchaseorderno=shoporder)
                  shoporder.status='Delivered'
                  shoporder.save()


                   #print update_list
           
       #print insert_list
       #print update_list
       shop=Shopsetup.objects(shop_name=shop)
       dealeruser=UserSignup.objects(id=shop[0].user_id)
       user=UserSignup.objects(usertype='Accountant')
       user1=UserSignup.objects(usertype='Market Manager')
       user2=UserSignup.objects(usertype='WH-Manager')
       emailList=[]
       emailList.append(user[0].email)
       emailList.append(user1[0].email)
       emailList.append(user2[0].email)
       fo = open("./static/mailtemp/dealermailtemp.html", "r+")
       htmlbody = fo.read()
       fo.close()
       urldata='Order '+ invoice+ " is delivered and acknowledged by the dealer " + dealeruser[0].username+"."
       htmlbody = htmlbody.replace("$$urldata$$",urldata)
       #sendMail(emailList,'Dealer Unpacking and shop in house of products',htmlbody)
       pool.apply_async(sendMail,[emailList,'Order delivered with Invoice No.: '+ str(invoice),htmlbody])
       msg="Order "+ invoice +" is delivered and acknowledged by the dealer " + dealeruser[0].username+"."
       
       mobileList=[]
       mobileList.append('91'+user[0].mobile)
       mobileList.append('91'+user1[0].mobile)
       mobileList.append('91'+user2[0].mobile)
       #SMS(msg,mobileList)
       pool.apply_async(SMS,[msg,mobileList])
                      
       logger.info('ShopInHouse detailes saved successfully')  
       return 'Success'                     
    except Exception as e:
        return render_template('error.html',reportsof = 'Exception',msg=str(e))

@dealerapp.route('/shoporderlist',methods=['GET'])
@login_required
def shoporderlist():
        if current_user.usertype=='Admin' or current_user.usertype=='Accountant'  or current_user.usertype=='WH-Manager'  or current_user.usertype=='Market Manager':
            shop=ShopOrders.objects().order_by(-id)
            logger.info('Entered into shoporderlist')
            return render_template('shop-orderlist.html',shop=shop)
      
        else:
            if current_user.usertype=='Distributor/Dealer':
               
                shop = ShopOrders.objects(user_id=str(current_user.id)).order_by('-id')
                logger.info('Entered into shoporderlist')
                return render_template('shop-orderlist.html',shop=shop)


@dealerapp.route('/shoporderviewmore/<id>',methods = ['GET', 'POST'])
@login_required
def shoporderviewmore(id):
        pool = Pool()
        pool_new(pool)
        if current_user.usertype=='Admin' or current_user.usertype=='Distributor/Dealer' or current_user.usertype=='WH-Manager' or current_user.usertype=='Accountant':
            detailes = ShopOrders.objects.filter(id=id).first()
            billing=Billing_Setup.objects(dealerid=detailes.dealer_id)
            if billing.count()==0:
                    return render_template('billingerror.html')
            company=Company_Setup.objects()
            warehouse=Warehouse.objects()
            number= num2words(float((detailes.totalvalue)))
            regdealer=Reg_Dealer.objects()
            wh=[]
            for qty in ProdinvWH.objects(warehouse=detailes.warehouse_name):
                data={}
                data['quantity']=qty.quantity
                data['modelno']=qty.modelno
                wh.append(data)
            header=Header.objects()
            logo=header[0].headerlogo
            if request.method == 'POST':
                if request.form.get('submit') == 'Accept':
                    detailes.status = 'Pending'
                    detailes.save()
                    return redirect(url_for('shoporderlist'))
                else:
                   detailes.status = 'Cancel'
                   detailes.save()
                   return redirect(url_for('shoporderlist'))
            return render_template('shoporder-viewmore.html',detailes=detailes,billing=billing[0],company=company[0],logo=logo,warehouse=warehouse[0],qty=wh,regdealer=regdealer[0],number=number)
        else :
           if current_user.usertype=='Market Manager':
            detailesarray = ShopOrders.objects(id=id)
            detailes=detailesarray[0]
            #return detailes.user_id
            billing=Billing_Setup.objects(dealerid=detailes.dealer_id)
            if billing.count()==0:
                    return render_template('billingerror.html')
            #return billing[0].dealerid
            company=Company_Setup.objects()
            warehouse=Warehouse.objects()
            regdealer=Reg_Dealer.objects()
            number= num2words(float((detailes.totalvalue)))
            whdata=[]
            if detailes.warehouse_name!='Any WH':
             for value in ProdinvWH.objects(warehouse=detailes.warehouse_name):
                data={}                
                data['quantity']=value.quantity
                data['modelno']=value.modelno
                whdata.append(data)
            #return jsonify(whdata)
            wh=[]
            for qty in ProdinvWH.objects():
                data={}
                data['warehouse']=qty.warehouse
                data['quantity']=qty.quantity
                data['modelno']=qty.modelno
                inlistFlag = True
                for inlist in wh:
                    if(inlist['warehouse']==qty.warehouse):
                           inlistFlag=False      
                if inlistFlag:
                    wh.append(data)
            finalWh=[]
            for whlist in wh:
                if whlist['warehouse']!=detailes.warehouse_name:
                    finalWh.append(whlist)
            if request.method == 'POST':
                        comment=request.form.get('optradio')
                        detailes.remarks=comment
                        if request.form.get('submit') == 'Accept':
                            if request.form.get('optradio') == 'Proceedtosame':
                               detailes.status = 'Accept'
                               detailes.save()
                               user=UserSignup.objects(usertype='WH-Manager')
                               user1=UserSignup.objects(usertype='Accountant')
                               usermail=UserSignup.objects(id=detailes.user_id)
                               emailList=[]
                               emailList.append(usermail[0].email)
                               emailList.append(user[0].email)
                               emailList.append(user1[0].email)
                               fo = open("./static/mailtemp/marketingmailtemp.html", "r+")
                               htmlbody = fo.read()
                               fo.close()
                               urldata=detailes.dealer_id+ " with order SPO " + detailes.shop_purchaseorderno +' is accepted successfully.'
                               htmlbody = htmlbody.replace("$$urldata$$",urldata)
                               #sendMail(emailList,'Approve the dealer order',htmlbody)
                               pool.apply_async(sendMail,[emailList,'Approval for order in progress',htmlbody])
                               msg=detailes.dealer_id+ " with order SPO " + detailes.shop_purchaseorderno +' is accepted successfully.'
                               mobileList=[]
                               mobileList.append('91'+usermail[0].mobile)
                               mobileList.append('91'+user[0].mobile)
                               mobileList.append('91'+user1[0].mobile)
                               #SMS(msg,mobileList)
                               pool.apply_async(SMS,[msg,mobileList])
                               return redirect(url_for('shoporderlist'))
                            elif request.form.get('optradio') == 'ChangeWarehouse':
                               detailes.save() 
                               return render_template('change-warehouse.html',detailes=detailes,warehouseqty=qty,wh=finalWh)
                        else:
                            detailes.status = 'Reject'
                            detailes.save()
                            usermail=UserSignup.objects(id=detailes.user_id)
                            fo = open("./static/mailtemp/marketingmailtemp.html", "r+")
                            htmlbody = fo.read()
                            fo.close()
                            urldata=detailes.dealer_id+ ", your order " + detailes.shop_purchaseorderno +' is not approved. Kindly contact marketing team of ShopMyTools on <9100115019> for further details.'
                            htmlbody = htmlbody.replace("$$urldata$$",urldata)
                            #sendMail(usermail[0].email,'Reject the dealer order',htmlbody)
                            pool.apply_async(sendMail,[usermail[0].email,'Sorry your order is rejected.',htmlbody])
                            msg="Dealer id  "+ detailes.dealer_id +" "+"Order" +" "+ detailes.shop_purchaseorderno +",was rejected Kindly contact Marketing <9100115019> for further details."
                            #mobile='91'+usermail[0].mobile
                            mobileList=[]
                            mobileList.append('91'+usermail[0].mobile)
                            #SMS(msg,mobile)
                            pool.apply_async(SMS,[msg,mobileList])
                            return redirect(url_for('shoporderlist'))
            header=Header.objects()
            logo=header[0].headerlogo
            return render_template('shoporder-viewmore.html',detailes=detailes,billing=billing[0],company=company[0],logo=logo,warehouse=warehouse[0],qty=whdata,regdealer=regdealer[0],number=number)

#---------------------------------------------------------------------purchase order reports-------------------------------

@dealerapp.route('/purchase_orderreport', methods = ['GET', 'POST'])
def purchase_orderreport():
        logger.info('Entered into Customer Report')
        return render_template('purchase-order-reports.html')

@dealerapp.route('/purchase_orderget', methods = ['GET', 'POST'])
def purchase_orderget():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        fromdate=json_data['fromdate']
        todate=json_data['todate']
        fromdates = datetime.datetime.strptime(fromdate, "%Y-%m-%d")
        to = datetime.datetime.strptime(todate, "%Y-%m-%d")
        todates=to+ timedelta(1)
        shop=[]
        orderdata=ShopOrders.objects(user_id=str(current_user.id),created_date__lte=todates,created_date__gte=fromdates)
        if orderdata.count()==0:
            data={}
            data['status']="fail"
            shop.append(data)
            return jsonify(shop)
        for i in orderdata :
            data={}
            data['shoppono']=i.shop_purchaseorderno
            data['warehousename']=i.warehouse_name
            data['podate']=i.po_date
            data['status']=i.status            
            shop.append(data)
        return jsonify(shop)


@dealerapp.route('/purchase_orderviewmore/<pono>',methods = ['GET', 'POST'])
@login_required
def purchase_orderviewmore(pono):
        detailes = ShopOrders.objects.filter(shop_purchaseorderno=pono).first()
        billing=Billing_Setup.objects(dealerid=detailes.dealer_id)
        company=Company_Setup.objects()
        header=Header.objects()
        logo=header[0].headerlogo
        warehouse=Warehouse.objects()
        number= num2words(float((detailes.totalvalue)))
        regdealer=Reg_Dealer.objects()
        logger.info('Entered into shoporderviewmore') 
        return render_template('purchaseorder-reportrviewmore.html',detailes=detailes,billing=billing[0],company=company[0],warehouse=warehouse[0],regdealer=regdealer[0],logo=logo,number=number)


@dealerapp.route('/purchase_invoicereport', methods = ['GET', 'POST'])
def purchase_invoicereport():
        logger.info('Entered into Customer Report')
        return render_template('purchaseorder-invoicereport.html')

@dealerapp.route('/purchase_invoiceget', methods = ['GET', 'POST'])
def purchase_invoiceget():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        prevdate=json_data['prevdate']
        currentdate=json_data['currentdate']
        fromdates = datetime.datetime.strptime(prevdate, "%Y-%m-%d")
        to = datetime.datetime.strptime(currentdate, "%Y-%m-%d")
        todates=to+ timedelta(1)
        shop=[]
        invoicedata=ShopOrderInvoice.objects(dealer_id=str(current_user.userid),created_date__lte=todates,created_date__gte=fromdates)
        if invoicedata.count()==0:
            data={}
            data['status']="fail"
            shop.append(data)
            return jsonify(shop)
        for i in invoicedata:
            data={}
            data['warehousename']=i.ware_house
            data['shoppono']=i.shop_purchaseorderno
            data['invoiceno']=i.shopinvoice_number
            data['indate']=i.invoice_date
            data['status']=i.status
            shop.append(data)
        return jsonify(shop)



@dealerapp.route('/purchase_invoiceviewmore/<invoiceno>',methods = ['GET', 'POST'])
@login_required
def purchase_invoiceviewmore(invoiceno):
    
        detailess = ShopOrderInvoice.objects.filter(shopinvoice_number=invoiceno).first()
        company=Company_Setup.objects()
        billing=Billing_Setup.objects(dealerid=detailess.dealer_id)
        warehouse=Warehouse.objects()
        regdealer=Reg_Dealer.objects()
        header=Header.objects()
        number= num2words(float((detailess.total_value)))
        logo=header[0].headerlogo
        logger.info('Entered into invoice viewmore')
       
        return render_template('purchaseorder-invoiceviewreport.html',detailess=detailess,company=company[0],logo=logo,billing=billing[0],warehouse=warehouse[0],regdealer=regdealer[0],number=number)


#----------------------------------------------------------------------sales reports-----------------------------

@dealerapp.route('/customer_report', methods = ['GET', 'POST'])
def customer_report():
        logger.info('Entered into Customer Report')
        return render_template('customerorder-reports.html')

@dealerapp.route('/customerdata', methods=['GET', 'POST'])
def customerdata():
    try:
        if request.method == 'POST':
             logger.info('Entered into Customer data')
             json_data = request.get_json(force=True)
             fromdate=json_data['fromdate']
             todate=json_data['todate']
             fromdates = datetime.datetime.strptime(fromdate, "%Y-%m-%d")
             to = datetime.datetime.strptime(todate, "%Y-%m-%d")
             todates=to+ timedelta(1)
             detail=[]
             shops = ProdInvShop.objects(user_id=str(current_user.id))
             customerdata=CustomerOrders.objects(shop=shops[0].shop,created_date__lte=todates,created_date__gte=fromdates)
             if customerdata.count()==0:
                    data={}
                    data['status']="fail"
                    detail.append(data)
                    return jsonify(detail)
             for customer in customerdata:
                    data={}
                    data['orderno']=customer.orderid
                    data['customermobile']=customer.customermobile
                    data['nooforders']=customer.total_items
                    data['status']=customer.status                      
                    detail.append(data)                    
             return jsonify(detail)     
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')

		
@dealerapp.route('/customer_orderviewmore/<orderno>',methods = ['GET', 'POST'])
@login_required
def customer_orderviewmore(orderno):
    
        detailess = CustomerOrders.objects.filter(orderid=orderno).first()
        address=[]
        for i in CustomerOrders.objects(orderid=orderno):
            for j in i.shippingaddress:
                data={}
                data['firstname']=j.firstname
                data['lastname']=j.lastname
                data['house_no']=j.house_no
                data['street_address']=j.street_address
                data['city']=j.city
                data['state']=j.state
                data['postal_code']=j.postal_code
                data['country']=j.country
                data['mobile']=j.mobile
                data['alt_mobile']=j.alt_mobile
                #data['address_id']=j.address_id
                #print data
                #test=', '.join(data)
                address.append(data)
        return render_template('customer-orderreport-viewmore.html',detailes=detailess,address=address)

@dealerapp.route('/order_invoice', methods = ['GET', 'POST'])
def order_invoice():
        logger.info('Entered into Customer Report')
        return render_template('customer-invoice-reports.html')

@dealerapp.route('/order_invoicedata', methods=['GET', 'POST'])
def order_invoicedata():
    try:
        if request.method == 'POST':
             logger.info('Entered into Customer data')
             json_data = request.get_json(force=True)
             fromdate=json_data['fromdate']
             todate=json_data['todate']
             fromdates = datetime.datetime.strptime(fromdate, "%Y-%m-%d")
             to = datetime.datetime.strptime(todate, "%Y-%m-%d")
             todates=to+ timedelta(1)
             detail=[]
             shops = ProdInvShop.objects(user_id=str(current_user.id))
             invoicedata=ConfirmInvoice.objects(shop=shops[0].shop,created_date__lte=todates,created_date__gte=fromdates)
             if invoicedata.count()==0:
                    data={}
                    data['status']="fail"
                    detail.append(data)
                    return jsonify(detail)
             for customer in invoicedata:                 
                    data={}
                    data['orderid']=customer.orderid
                    data['shop']=customer.shop
                    data['invoiceid']=customer.invoiceid
                    data['createddate']= customer.created_date.strftime('%d-%m-%Y')
                    detail.append(data)
                    
             return jsonify(detail)     
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')



@dealerapp.route('/customer_invoiceorderviewmore/<orderno>',methods = ['GET', 'POST'])
@login_required
def customer_invoiceorderviewmore(orderno):
        detailess=[]
        for customer in ConfirmInvoice.objects(orderid=orderno):
          for detailes in customer.orderitem:             
            data={}
            data['totalamount']=customer.totalamount
            data['orderid']=customer.orderid
            data['shop']=customer.shop
            data['invoiceid']=customer.invoiceid
            data['createddate']=customer.createddate
            data['paymenttype']=customer.paymenttype
            data['smtids']=', '.join(detailes.smtids)
            data['productdesp']=detailes.productdesp            
            test=ast.literal_eval(json.dumps(data))
            detailess.append(test)
        logger.info('Entered into shophistory')   
        return render_template('customerinvoice-viewmore.html',detailes=detailess)

#----------------------------------------------------------------------stock reports----------------------------------------

@dealerapp.route('/stock_reports', methods = ['GET', 'POST'])
def stock_reports():
        shop=[]
        for i in ProdInvShop.objects(user_id=str(current_user.id)):
            data={}
            data['brand']=i.brand
            inlistFlag = True
            for inlist in shop:
                if(inlist['brand']==i.brand):
                        inlistFlag=False
                           
            if inlistFlag:
                shop.append(data)
        logger.info('Entered into Customer Report')
        return render_template('stock-reports.html',shop=shop)


@dealerapp.route('/brand_post/', methods=['GET', 'POST'])
@login_required
def brand_post():
       brand=request.args.get('brand')
       br=[]
       for i in ProdInvShop.objects(brand=brand,user_id=str(current_user.id)):
                 br.append(i.model)
       modelnos=sorted(set(br))
       logger.info('Entered into new brand post')
       return jsonify(modelnos)
 


@dealerapp.route('/stockreportsdata', methods=['GET', 'POST'])
@login_required
def stockreportsdata():
      if request.method == 'POST':
          logger.info('Entered into shoporder')
          json_data = request.get_json(force=True)
          brand = json_data['brand']
          modelno = json_data['modelno']
          wh=[]
          if brand == '0' and modelno == '0':
              wh= ProdInvShop.objects(user_id=str(current_user.id))
          elif brand == '0':
              wh=ProdInvShop.objects(user_id=str(current_user.id),model=modelno)
          elif modelno == '0':
             wh= ProdInvShop.objects(user_id=str(current_user.id),brand=brand)
          else:
             wh= ProdInvShop.objects(user_id=str(current_user.id),model=modelno,brand=brand)
           
          product=[]
          for products in wh:
              data={}
              data['prod_desc']=products.proddescription
              data['inqty']=products.inqty
              data['outqty']=products.outqty
              bal=int(products.inqty)+int(products.outqty)
              data['balqty']=bal
              product.append(data)
          return jsonify(product)
      else:
          return 'fail'

#---------------------------------------------------------------------advance reports----------------------------------------------

@dealerapp.route('/advance_report',methods = ['GET', 'POST'])
@login_required
def advance_report():    
        return render_template('advancereports.html')


@dealerapp.route('/advancecustomer_report',methods = ['GET', 'POST'])
@login_required
def advancecustomer_report():
         if request.method == 'POST':
             logger.info('Entered into Customer data')
             json_data = request.get_json(force=True)
             fromdate=json_data['fromdate']
             todate=json_data['todate']
             fromdates = datetime.datetime.strptime(fromdate, "%Y-%m-%d")
             to = datetime.datetime.strptime(todate, "%Y-%m-%d")
             todates=to+ timedelta(1)
             detail=[]
             shops = ProdInvShop.objects(user_id=str(current_user.id))
             cm=ProdInvCMR.objects(shop=shops[0].shop,created_date__lte=todates,created_date__gte=fromdates)
             if cm.count()==0:
                    data={}
                    data['user']="fail"
                    detail.append(data)
                    return jsonify(detail)
                
             for customer in cm:
                 for i in customer.cmrinfo:
                   data={}
                   data['user']=i.user
                   inlistFlag = True
                   for inlist in detail:
                      if(inlist['user']==i.user):
                           inlistFlag=False
                           
                   if inlistFlag:
                       detail.append(data)
                  
             return jsonify(detail)     
        
@dealerapp.route('/customerpost', methods=['GET', 'POST'])
@login_required
def customerpost():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        user=json_data['user']
        br=[]
        for customer in ProdInvCMR.objects():
          for i in customer.cmrinfo:
               if i.user==user:
                for  j in i.prodinfo:
                 data={}  
                 data['invoiceid']=j.invoiceid
                 data['smtids']=j.smtids
                 test=ast.literal_eval(json.dumps(data))
                 br.append(test)
        return jsonify(br)

@dealerapp.route('/customerviewmorepost/<mobile>', methods=['GET', 'POST'])
@login_required
def customerviewmorepost(mobile):
        cname=CustomerDetails.objects(mobile=mobile)
        br=[]
        for customer in ProdInvCMR.objects():
          for i in customer.cmrinfo:
               if i.user==mobile:
                for  j in i.prodinfo:
                 data={}
                 data['user']=cname[0].firstname
                 data['invoiceid']=j.invoiceid
                 data['smtids']=', '.join(j.smtids)
                 test=ast.literal_eval(json.dumps(data))
                 br.append(test)
        #return mobile
        return render_template('advancecustomer-viewmore.html',detail=br)     

@dealerapp.route('/advanceproduct_report',methods = ['GET', 'POST'])
@login_required
def advanceproduct_report():
         if request.method == 'POST':
             logger.info('Entered into Customer data')
             json_data = request.get_json(force=True)
             fromdate=json_data['fromdate']
             todate=json_data['todate']
             fromdates = datetime.datetime.strptime(fromdate, "%Y-%m-%d")
             to = datetime.datetime.strptime(todate, "%Y-%m-%d")
             todates=to+ timedelta(1)
             detail=[]
             shops = ProdInvShop.objects(user_id=str(current_user.id))
             cm=ProdInvCMR.objects(shop=shops[0].shop,created_date__lte=todates,created_date__gte=fromdates)
             if cm.count()==0:
                    data={}
                    data['model']="fail"
                    detail.append(data)
                    return jsonify(detail)
             for customer in cm :
              for i in customer.cmrinfo:
                data={}
                data['model']=customer.model
                for  j in i.prodinfo:
                    data['productdesp']=j.productdesp
                detail.append(data)
                        
             return jsonify(detail)     

@dealerapp.route('/productpost', methods=['GET', 'POST'])
@login_required
def productpost():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        model=json_data['model']
        productdesp=json_data['productdesp']
        br=[]
        for customer in ProdInvCMR.objects():
         for i in customer.cmrinfo:
           for  j in i.prodinfo:
            if customer.model==model and j.productdesp==productdesp: 
                
                 data={}  
                 data['usermobile']=i.user
                 br.append(data)
        #modelnos=sorted(set(br))
        return jsonify(br)

@dealerapp.route('/productviewmorepost/<productdesp>', methods=['GET', 'POST'])
@login_required
def productviewmorepost(productdesp):    
        br=[]
        productname=productdesp.replace('_',' ').replace('*','"').replace('@','/')
        for customer in ProdInvCMR.objects():
            for i in customer.cmrinfo:
              for j in i.prodinfo:
               if j.productdesp==productname: 
                 data={}
                 data['productdesp']=j.productdesp 
                 data['user']=i.user
                 br.append(data)
               
                   
        #return mobile
        return render_template('advanceproduct-viewmore.html',detail=br)  
        
#--------------------------------------------------------------------------display product info-----------------------------------------------------
@dealerapp.route('/productinfo/<name>', methods=['GET', 'POST'])
@login_required
def productinfo(name):
        #return name
        #upload_name=request.args.get('prod_desc')
        productname=name.replace('_',' ').replace('*','/')
        #print productname
        detailes=[]
        for pinfo in Sup_Upload.objects():
         if pinfo.upload_name==productname:
          for i in pinfo.attributes:
            data={}
            data['upload_id']=pinfo.upload_id
            data['upload_category']=pinfo.upload_category
            data['upload_subcategory']=pinfo.upload_subcategory
            data['upload_name']=pinfo.upload_name
            data['upload_modelno']=pinfo.upload_modelno
            data['upload_brand']=pinfo.upload_brand
            data['upload_warranty']=pinfo.upload_warranty
            data['upload_pieceperCarton']=pinfo.upload_pieceperCarton
            data['upload_minimumOrder']=pinfo.upload_minimumOrder
            data['upload_netWeight']=pinfo.upload_netWeight
            data['upload_mrp']=pinfo.upload_mrp.replace(pinfo.upload_mrp,'xxx')
            data['upload_price']=pinfo.upload_price.replace(pinfo.upload_price,'xxx')
            data['discount']=pinfo.discount.replace(pinfo.discount,'xxx')
            data['upload_discount']=pinfo.upload_discount.replace(pinfo.upload_discount,'xxx')
            data['tax']=pinfo.tax.replace(pinfo.tax,'xxx')
            data['upload_tax']=pinfo.upload_tax.replace(pinfo.upload_tax,'xxx')
            data['upload_netPrice']=pinfo.upload_netPrice.replace(pinfo.upload_netPrice,'xxx')
            data['upload_hsncode']=pinfo.upload_hsncode
            data['upload_locations']=pinfo.upload_locations
            data['upload_photo']=pinfo.upload_photo
            data['frequency']=pinfo.frequency
            
            data['atrname']=i.atrname
            data['atrvalue']=i.atrvalue
            data['status']=pinfo.status
            data['remarks']=pinfo.remarks
            detailes.append(data)
        #return jsonify(detailes)
        return render_template('productinfo.html',detailes=detailes)

#-----------------------------------------------------logout------------------------------------------

@dealerapp.route('/logout')
def logout():
    logout_user()
    return redirect(dealerapp.config['Mainurl'])


if __name__ == '__main__':
    now = datetime.date.today().strftime("%Y_%m_%d")
    handler = RotatingFileHandler("loggers/dealerapplogs/"+"dealerapp_" + str(now) + ".log", maxBytes=100000, backupCount=3)
    logger = logging.getLogger('__name__')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    dealerapp.run(host='127.0.0.1',port=5004,threaded=True)
