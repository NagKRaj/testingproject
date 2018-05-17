#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from __future__ import division
from flask import Flask, request, url_for, redirect, render_template, abort , Response,session,jsonify,flash,send_file
from form import PricesUploadfileForm,ServicetaxForm, MasterBrandEditForm,BillingForm,CompanyForm,ShopOrderviewForm,ShopsetupForm,ShopUserForm,PurchaseOrderviewForm,ProductsInHouseForm,\
     BarcodeForm,BarCodeCartonForm,PurchaseOrderForm,WHRegistration,UserList,UsertypeForm,UserRegistration,LoginForm,DealerForm,EditForm,SupplierForm,ContractorForm,SuppliertaxForm,\
     ServiceForm,SupplierdiscountForm,ForgotPassword,ResetPassword,MasterproductForm1,MasterproductForm2,MasterproductForm3,UploadForm,ShippingForm,BankForm,\
     HeaderForm,CouponsForm,ExchangeForm,CollectionForm,BrandForm,BannerForm,FooterForm,HeadForm,CountryForm1,CountryForm2,CountryForm3,Promotions
from models import ServiceTax,ProdInvShop,SmtidShop,Prices,ProdInvShipping,ShipData,PriceList,InvoiceList,ProdinvWH,Atname,Company_Setup,Billing_Setup,ShopOrderInvoice,ShopInvoice,ShopCharges,PurchaseInvoice,Invoice,Charges,ShopOrders,Orders,Shopsetup,ShopUser,WHOrders,PurchaseOrders,\
     LatestBarcode,Barcode_Info,BarCode_Carton,Carton,DealerSettlement,Settlement,Configuration,\
     OrderCoupons,Warehouse,Usertype,UserSignup,Reg_Dealer,Reg_Supplier,Goods,Reg_Service,Reg_Contractor,userLoginCheck,Category,Sub_Category,Product,Sup_Upload,atr,Shipping_Setup,Supplier_Tax,\
     Supplier_Discount,userLoginCheck1,Charges,Bank_Setup,Header_Setup,Fair_Contact,Notifications,UserOrderList,UserOrders,CustomerOrders,BillingShippingAddress,Rating_ShopToUser,Rating_UserToShop,\
     OrderItem,Tax,BankDetail,Collections,Brand,Banner,BannerUrlLink,PriceLists,Footer,FooterUrlLink,Header,Country,State,City,ConfirmInvoice,ConfirmInvoiceOrderItems,\
     Reviews_info,Header,InitiateOrders,Orderitems,CustomerDetails,CategoryId,SubcategoryId
from controler import SignUpControler,DashboardLink
from flask_login  import login_user , logout_user , current_user , login_required
from flask_login  import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import json,time, os,ast
from os import path
import requests,io
from barcodegen import BarcodeNumber
from randomnumber import Number,DealerNumber,SMTIdNumber,ShopNumber,SubcatNumber,CatNumber
from eanbarcode import EanBarCode
from smtbarcode import EanBarCodes
from purchasenumber import PurchaseNumber,ShopPurchaseNumber
import urllib
import urllib2
import cookielib
import sys,csv
import PIL.Image
from flask_ckeditor import CKEditorField
sys.modules['Image'] = PIL.Image
sys.setrecursionlimit(1000)
from num2words import num2words
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
import datetime
import traceback
import requests,urllib
import math
from datetime import date,timedelta
from mongoengine.queryset.visitor import Q
from multiprocessing import Pool
import locale
from dateutil.relativedelta import relativedelta
import threading
import functools
from bson import json_util, ObjectId
#import resource
#pool=Pool()

app = Flask(__name__)
app.secret_key = 'secret'
app.config['UPLOAD_LOGO'] = './static/logo/'
app.config['UPLOAD_FOLDER'] = './static/uploads/'

app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['Register'] = 'http://127.0.0.1:5002/'
app.config['Supplier_Dashboard']='http://127.0.0.1:5003/'
app.config['Dealer_Dashboard']='http://127.0.0.1:5004/'
app.config['Mainurl']='http://127.0.0.1:8000/'
#app.config['Faq']='http://127.0.0.1:8000/'
app.config['NOTIFICATIONS']='True'
app.config['SMS']='True'

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

'''
resource.setrlimit(
    resource.RLIMIT_CORE,
    (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
'''

#--------------------------------------------currency represent format----------------------------------


'''
def synchronized(wrapped):
        lock = threading.Lock()
        @functools.wraps(wrapped)
        def _wrap(*args, **kwargs):
            with lock:
                return wrapped(*args, **kwargs)
        return _wrap
'''

def sendMail(email,subject,htmlbody):
    if(app.config['NOTIFICATIONS'])=='True':
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
        
    if(app.config['SMS'])=='True':
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


def UpdateInitiateOrder(product_name,offer_price):
        pool = Pool()
        pool_new(pool)
        init_orders=InitiateOrders.objects()
        for order in init_orders:
            for item in order.orderitem:
                old_price=item.offer_price
                json_data = request.get_json(force=True)
                if item.productdescription == product_name:
                    item.offer_price = offer_price
                    item.save()
                    header=Header.objects()
                    logo=header[0].headerlogo
                    if len(order.user_id) > 20:
                        customer_data=CustomerDetails.objects(id=order.user_id)
                        fo = open("./static/mailtemp/dealer_mail.html", "r+")
                        htmlbody = fo.read()
                        fo.close()
                        urldata ='Dear '+customer_data[0].firstname.encode('ascii','ignore')+', few products in your cart were updated with prices. New prices for  '+(item.productdescription).encode('ascii','ignore')+ ' are '+old_price+' and  '+item.offer_price+ 'respectively.'
                        htmlbody = htmlbody.replace("$$urldata$$",urldata.encode('ascii','ignore'))
                        htmlbody = htmlbody.replace("$$logo$$",logo.encode('ascii','ignore'))
                        email_list=[]
                        email_list.append(customer_data[0].email)
                        pool.apply_async(sendMail,[email_list,'Price changes for products in your cart',htmlbody])
        logger.info('email sent')
        print 'email sent successfully'
#------------------------------Loggers------------------------------------------------>

@app.after_request
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

@app.errorhandler(Exception)
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
                      request.full_path,tb)
    return render_template('error.html',reportsof = 'Exception',msg=str(e))

#------------------------------Login Manager------------------------------------------------>
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(id):
        u = UserSignup.objects.get(id=id)
        return u
    
@login_manager.unauthorized_handler
def unauthorized_callback():
   return render_template('error.html',reportsof = 'Unauthorized out ....')

#---------------------------------------------Login Page--------------------------------------------->
@app.route('/', methods = ['GET', 'POST'])
def login():
      with app.app_context():
        loginForm = LoginForm()
      if request.method == 'POST' and loginForm.validate():
          loginid = request.form['loginid']
          password=request.form['password']
          value = userLoginCheck(loginForm.loginid.data,loginForm.password.data)
          if value=="Fail":
             logger.info('failed to log in')
             loginForm.loginid.errors.append("Please enter valid email")
             userin=UserSignup.objects(email=loginid.lower())
             if userin.count()==0:
                 return render_template('emailwrrong.html')
             user=UserSignup.objects.get(email=loginid.lower())
             user1=int(user.login_attempts)+1
             user.login_attempts=str(user1)
             user.save()
             if int(user.login_attempts) >= 3:
                if '@' in loginid:
                    userstatus = UserSignup.objects.get(email=loginid.lower())
                    if userstatus:
                        userstatus.status = 'Inactive'
                        userstatus.save()
                        return render_template('wrong.html')
                else:
                    userstatus = UserSignup.objects.get(mobile=loginid)
                    if userstatus:
                        userstatus.status = 'Inactive'
                        userstatus.save()
                        return render_template('wrong.html')   
             else:
                logger.info('failed to log in')
                return render_template('user_wrong.html')
          else:
                logger.info('success to log in')
                login_user(value, remember=True)
                return redirect(url_for('home'))
      logger.info('Entered into login')
      return render_template('home-login.html', loginForm=loginForm)
   
#------------------------------------UserSignup----------------------------------->
@app.route('/usersignup', methods = ['GET', 'POST'])
def user_signup():
        pool = Pool()
        pool_new(pool)
        logger.info('Entered into user_signup')
        with app.app_context():
            userRegForm = UserRegistration()
        if request.method == 'POST' and userRegForm.validate() :
            username = request.form['username']
            email=request.form['email']
            std_isd=request.form['std_isd']
            mobile=request.form['mobile']
            password = request.form['password']
            usertype = request.form['usertype']
            isEmailExist=UserSignup.objects(email=email)
            isMobileExist=UserSignup.objects(mobile=mobile)
            if isEmailExist.count()>0:
                 logger.info(' failed to signup because %s already existed!',email)
                 userRegForm.email.errors.append("Email already existed!")
            elif isMobileExist.count()>0:
                 logger.info(' failed to signup because %s already existed!',mobile)
                 userRegForm.mobile.errors.append("Mobile already existed!")
            else:
                createUser = UserSignup(username=username, email=email.lower(),std_isd=std_isd, mobile=mobile, password =generate_password_hash(password),usertype=usertype)# Insert form data in collection
                createUser.save()
                registeredUser = UserSignup.objects(email=email.lower())
                urldata=''
                emails=email.lower()
                if registeredUser.count() > 0:
                    ts = int(round(time.time() * 1000))
                    userid = registeredUser[0].id
                    urldata = str(ts)+':'+str(userid)
                    fo = open("./static/mailtemp/thankyoumail.html", "r+")
                    htmlbody = fo.read()
                    fo.close()
                    htmlbody = htmlbody.replace("$$username$$",username)
                    htmlbody = htmlbody.replace("$$urldata$$",urldata)
                    #sendMail(email,'Signed up successful',htmlbody)
                    
                    pool.apply_async(sendMail,[emails,'Signed up successful',htmlbody])
                    logger.info('Sucessfully signup')
                    return render_template('error.html',userRegForm=userRegForm,reportsof = 'Thank you for registering with us!',msg="Mail sent for completing registration process. Check spam if not found in inbox and click on confirm button.<br>The Email will be expired in 2 Hrs.",userinfo=current_user)
                else:
                  userRegForm.email.errors.append("Email not available with us!")   
            return render_template('signup.html', userRegForm=userRegForm)   
        else:
            return render_template('signup.html', userRegForm=userRegForm)

@app.route('/emailverification/<urldata>')
def emailverification(urldata):
        with app.app_context():
            userRegForm = UserRegistration()
        data = urldata.split(':')
        pts = data[1]
        userstatus = UserSignup.objects.get(id=pts)
        if userstatus.status == 'Inactive':
            userstatus.status = 'Process'
            userstatus.save()
            return render_template('emailverifiedsuccess.html',reportsof = 'Status',msg="Congratulations! Dear user, you have successfully become part of ShopMyTools. Kindly <a href="+app.config['Mainurl']+">login</a>")
        else:
            data = urldata.split(':')
            pts = int(data[0])
            cts = int(round(time.time() * 1000))
            dts = cts-pts
            hours=(dts/(1000*60*60))%24
            if hours<2:
                userRegForm.userid.data = data[1]
                return render_template('emailverifiedsuccess.html',reportsof = 'Status',msg="Dear User, you have already completed the process. Kindly <a href="+app.config['Mainurl']+">login</a>.",userinfo=current_user)
            else:
                return render_template('error.html',msg="Sorry!<br> The verification link is Expired.<br>Please <a href="+app.config['Mainurl']+">login</a> here." ,userinfo=current_user)

#-----------------------------------------------------------------dashboard-------------------------------------------------------				
@app.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():
    if current_user.usertype=='Admin':
       sup=UserSignup.objects(status='Active',usertype="Supplier").count()
       supplier= "{:,}".format(sup)
       dealers=UserSignup.objects(status='Active',usertype="Distributor/Dealer").count()
       dealer= "{:,}".format(dealers)
       services=Reg_Service.objects(status='Active').count()
       service= "{:,}".format(services)
       warehouses=Warehouse.objects().count()
       warehouse= "{:,}".format(warehouses)
       product=Sup_Upload.objects(status='Accept').count()
       products= "{:,}".format(product)
       couponcounts=OrderCoupons.objects(status='Active').count()
       couponcount= "{:,}".format(couponcounts)
       shops=Shopsetup.objects().count()
       shop= "{:,}".format(shops)
       whstocks=0
      
       for wh in ProdinvWH.objects():
         whstocks+=int(wh.quantity)
       whstock="{:,}".format(whstocks)
       
       pos_stocks=0
       for prod_inv_obj in ProdInvShop.objects():
         #print prod_inv_obj.inqty
         pos_stocks+=int(prod_inv_obj.inqty)
       pos_stock="{:,}".format(pos_stocks)
       #print 'hii'
       
       fromdates=date.today()
       six_months = date.today() - relativedelta(months=6)
       confirm_products=[]
       wh_products=[]
       waste_prod=[]
       n_m_p=[]
       for prod in ConfirmInvoice.objects():
            for inv_prod in prod.orderitem:
                confirm_products.append(inv_prod.productdesp)
       final_prod=list(set(confirm_products))
       for prod in ProdinvWH.objects():
            wh_products.append(prod.prod_desc)
       for del_prod in final_prod:
            if del_prod in wh_products:
                wh_products.remove(del_prod)
            else:
                waste_prod.append(del_prod)
       non_moving=ProdinvWH.objects().filter(prod_desc__in=wh_products,created_date__gte=six_months,created_date__lte=fromdates)
       for non_moving_prod in non_moving:
            for invdate in non_moving_prod.invoice_smtlist:
                n_m_p.append({'prod_desc':non_moving_prod.prod_desc,'modelno':non_moving_prod.modelno,'brand':non_moving_prod.brand,'quantity':non_moving_prod.quantity,'invoice_date':non_moving_prod.created_date.strftime("%d/%m/%y")})
       total_prod= len(n_m_p)

       #total_prod="{:,}".format(str(n_m_p))
       wh_stock_value=0
       for prod in ProdinvWH.objects():
           for price in prod.prices:
                wh_stock_value+=int(prod.quantity)*float(price.landing_price)
       #wh_stocks= "{:,}".format(wh_stock_value)
       final_wh_stock_values=wh_stock_value/100000
       wh_stock_values= format(final_wh_stock_values, '.2f')
       

       wh_sales_value=0
       for prod in ProdinvWH.objects():
         for price in prod.prices:
            wh_sales_value+=int(prod.outqty)*float(price.dealer_price)
       #wh_sales_values= "{:,}".format(wh_sales_value)
       final_wh_sales_value=wh_sales_value/100000
       wh_sales_values= format(final_wh_sales_value, '.2f')

       pos_stock_value=0
       for prod in ProdInvShop.objects():
         for prices in prod.price:
             pos_stock_value+=int(prod.inqty)*float(prices.dealer_price)
       #pos_stock_values= "{:,}".format(pos_stock_value)
       final_pos_stock_value=pos_stock_value/100000
       pos_stock_values= format(final_pos_stock_value, '.2f')

       pos_sales_value=0
       for prod in ProdInvShop.objects():
          for prices in prod.price:
             pos_sales_value+=int(prod.outqty)*float(prices.offer_price)
       #pos_sales_values= "{:,}".format(pos_sales_value)
       final_pos_sales_value=pos_sales_value/100000
       pos_sales_values= format(final_pos_sales_value, '.2f')
             
       logger.info('Entered into dashboard')
       return render_template('dashboard.html',supplier=supplier,dealer=dealer,service=service,warehouse=warehouse,products=products,whstock=whstock,pos_stock=pos_stock,shop=shop,
                              couponcount=couponcount,total_prod=total_prod,wh_stock_value=wh_stock_values,wh_sales_value=wh_sales_values,pos_stock_value=pos_stock_values,pos_sales_value=pos_sales_values)

'''
@app.route('/active_dealer_details', methods = ['GET', 'POST'])
@login_required
def active_dealer_details():
        dealer=[]
        for detail in UserSignup.objects(usertype = 'Distributor/Dealer',status='Active'):
          for info in Reg_Dealer.objects(dealer_mail=detail.email):
            data={}
            data['id']=detail.id
            data['username']=detail.username
            data['email']=detail.email
            data['mobile']=detail.mobile
            data['registered_on']=detail.registered_on
            data['status']=detail.status
            data['userid']=detail.userid
            data['shopname']=info.dealer_shopname
            dealer.append(data)
        logger.info('Entered into Supplier details ')        
        return render_template('dealer-details.html',dealer=dealer)
    

@app.route('/active_supplier_details', methods = ['GET', 'POST'])
@login_required
def active_supplier_details():
        supplier=[]
        for detail in UserSignup.objects(usertype = 'Supplier',status='Active'):
          for info in Reg_Supplier.objects(supplier_mail=detail.email):
            data={}
            data['id']=detail.id
            data['username']=detail.username
            data['email']=detail.email
            data['mobile']=detail.mobile
            data['registered_on']=detail.registered_on
            data['status']=detail.status
            data['userid']=detail.userid
            data['companyname']=info.supplier_companyname
            supplier.append(data)
        logger.info('Entered into Supplier details ')        
        return render_template('supplier-details.html',supplier=supplier)
    
'''


@app.route('/active_service_center_details', methods = ['GET', 'POST'])
@login_required
def active_service_center_details():
        dealer= Reg_Service.objects(status='Active')
        logger.info('Entered into Dealer details ')        
        return render_template('service_details.html',dealer=dealer)

@app.route('/active_productlist',methods = ['GET', 'POST'])
@login_required
def active_productlist():
    logger.info('Admin Entered into productlist')
    product= Sup_Upload.objects(status='Accept')    
    return render_template('product-list.html',product=product)
   

@app.route('/wh_stock_data', methods=['GET', 'POST'])
def wh_stock_data():
    wh_list=[]
    for prod in ProdinvWH.objects():
        wh_list.append(prod.warehouse)
    final_wh=list(set(wh_list))
    #print final_wh
    wh_data=[]
    for wh in final_wh:
        wh_details={}
        prod_wh=ProdinvWH.objects(warehouse=wh)
        total_qty=0
        for wh_qty in prod_wh:
            wh_details['warehouse']=wh_qty.warehouse
            total_qty+=int(wh_qty.quantity)
        wh_details['total_qty']=total_qty
        wh_data.append(wh_details)
    return render_template('wh_stock_data.html',wh_data=wh_data)


@app.route('/wh_stock_data_viewmore/<wh>', methods=['GET', 'POST'])
def wh_stock_data_viewmore(wh):
    prod_wh=ProdinvWH.objects(warehouse=wh)
    return render_template('wh_stock_data_viewmore.html',prod_wh=prod_wh,wh=wh)


@app.route('/pos_stock_data', methods=['GET', 'POST'])
def pos_stock_data():
    shop_list=[]
    for prod in ProdInvShop.objects():
        shop_list.append(prod.shop)
    final_shop=list(set(shop_list))
    #print shop_list
    shop_data=[]
    for shop in final_shop:
        shop_details={}
        prod_shop=ProdInvShop.objects(shop=shop)
        total_qty=0
        for shop_qty in prod_shop:
            shop_details['shop']=shop_qty.shop
            total_qty+=int(shop_qty.inqty)
        shop_details['total_qty']=total_qty
        for reg in Reg_Dealer.objects(dealer_shopname=shop):
            shop_details['dealer_name']=reg.dealer_name
            shop_data.append(shop_details)
    return render_template('pos_stock.html',shop_data=shop_data)

@app.route('/pos_stock_viewmore', methods=['GET', 'POST'])
def pos_stock_viewmore():
     shops=request.args.get('shop')
     dealer_name=request.args.get('dealer_name')
     shop=shops.replace('_',' ')
     prod_data=ProdInvShop.objects(shop=shop)
     return render_template('pos_stock_viewmore_data.html',prod_data=prod_data,shop=shop,dealer_name=dealer_name)


@app.route('/non_moving_product_viewmore', methods=['GET', 'POST'])
def non_moving_product_viewmore():
    return  render_template('non-moving-product.html')
    
@app.route('/non_moving_products', methods=['GET', 'POST'])
def non_moving_products():
    json_data = request.get_json(force=True)
    duration = json_data['duration']
    #print duration
    fromdates=date.today()
    six_months = date.today() - relativedelta(months=int(duration))
    #print fromdates
    #print six_months
    confirm_products=[]
    wh_products=[]
    waste_prod=[]
    n_m_p=[]
    for prod in ConfirmInvoice.objects():
        for inv_prod in prod.orderitem:
            confirm_products.append(inv_prod.productdesp)
    final_prod=list(set(confirm_products))
    for prod in ProdinvWH.objects():
        wh_products.append(prod.prod_desc)
    for del_prod in final_prod:
        if del_prod in wh_products:
            wh_products.remove(del_prod)
        else:
            waste_prod.append(del_prod)
    #print wh_products
    non_moving=ProdinvWH.objects().filter(prod_desc__in=wh_products,created_date__gte=six_months,created_date__lte=fromdates)
    for non_moving_prod in non_moving:
         n_m_p.append({'prod_desc':non_moving_prod.prod_desc,'modelno':non_moving_prod.modelno,'brand':non_moving_prod.brand,'quantity':non_moving_prod.quantity,'invoice_date':non_moving_prod.created_date.strftime("%d/%m/%y")})
   # print len(n_m_p)
    return jsonify(n_m_p)
#--------------------------------------------------------------------wh stock/sales value------------------------------------------------------------
@app.route('/stock_value_data', methods=['GET', 'POST'])
def stock_value_data():
    wh_list=[]
    for prod in ProdinvWH.objects():
        wh_list.append(prod.warehouse)
    final_wh=list(set(wh_list))
    #print final_wh
    wh_data=[]
    for wh in final_wh:
        wh_details={}
        prod_wh=ProdinvWH.objects(warehouse=wh)
        total_qty=0
        for wh_qty in prod_wh:
            wh_details['warehouse']=wh_qty.warehouse
            total_qty+=int(wh_qty.quantity)
        wh_details['total_qty']=total_qty
        wh_data.append(wh_details)
    return render_template('stock_value.html',wh_data=wh_data)



@app.route('/stock_value_viewmore/<wh>', methods=['GET', 'POST'])
def stock_value_viewmore(wh):
    prod_wh=[]
    total_amount=0
    for prod in ProdinvWH.objects(warehouse=wh):        
        for prices in prod.prices:
            data={}
            data['prod_desc']=prod.prod_desc
            data['brand']=prod.brand
            data['modelno']=prod.modelno
            data['quantity']=prod.quantity
            data['landing_price']=prices.landing_price
            data['subtotal']=int(prod.quantity)*float(prices.landing_price)
            total_amount+=int(prod.quantity)*float(prices.landing_price)
            
            prod_wh.append(data)
    return render_template('stock_value_viewmore.html',prod_wh=prod_wh,wh=wh,total_amount=total_amount)

@app.route('/sales_value_data', methods=['GET', 'POST'])
def sales_value_data():
    wh_list=[]
    for prod in ProdinvWH.objects():
        wh_list.append(prod.warehouse)
    final_wh=list(set(wh_list))
    #print final_wh
    wh_data=[]
    for wh in final_wh:
        wh_details={}
        prod_wh=ProdinvWH.objects(warehouse=wh)
        total_qty=0
        for wh_qty in prod_wh:
            wh_details['warehouse']=wh_qty.warehouse
            total_qty+=int(wh_qty.outqty)
        wh_details['total_qty']=total_qty
        wh_data.append(wh_details)
    return render_template('sales_value.html',wh_data=wh_data)


@app.route('/sales_value_viewmore/<wh>', methods=['GET', 'POST'])
def sales_value_viewmore(wh):
    prod_wh=[]
    total_amount=0
    for prod in ProdinvWH.objects(warehouse=wh):        
        for prices in prod.prices:
            data={}
            data['prod_desc']=prod.prod_desc
            data['brand']=prod.brand
            data['modelno']=prod.modelno
            data['outqty']=prod.outqty
            data['dealer_price']=prices.dealer_price
            data['subtotal']=int(prod.outqty)*float(prices.dealer_price)
            total_amount+=int(prod.outqty)*float(prices.dealer_price)
            
            prod_wh.append(data)
    return render_template('sales_value_viewmore.html',prod_wh=prod_wh,wh=wh,total_amount=total_amount)

#-----------------------------------------------------------------------pos stock/sales---------------------------------------------------------

@app.route('/pos_stock_value_data', methods=['GET', 'POST'])
def pos_stock_value_data():
    shop_list=[]
    for prod in ProdInvShop.objects():
        shop_list.append(prod.shop)
    final_shop=list(set(shop_list))
    #print shop_list
    shop_data=[]
    for shop in final_shop:
        shop_details={}
        prod_shop=ProdInvShop.objects(shop=shop)
        total_qty=0
        for shop_qty in prod_shop:
            shop_details['shop']=shop_qty.shop
            total_qty+=int(shop_qty.inqty)
        shop_details['total_qty']=total_qty
        shop_data.append(shop_details)
    return render_template('pos_stock_value.html',shop_data=shop_data)




@app.route('/pos_stock_value_viewmore/<shop>', methods=['GET', 'POST'])
def pos_stock_value_viewmore(shop):
    prod_shop=[]
    total_amount=0
    for prod in ProdInvShop.objects(shop=shop):
        
        for prices in prod.price:
            data={}
            data['proddescription']=prod.proddescription
            data['brand']=prod.brand
            data['model']=prod.model
            data['inqty']=prod.inqty
            data['dealer_price']=prices.dealer_price
            data['subtotal']=int(prod.inqty)*float(prices.dealer_price)
            total_amount+=int(prod.inqty)*float(prices.dealer_price)
            
            prod_shop.append(data)
    #print total_amount
    return render_template('pos_stock_value_viewmore.html',prod_shop=prod_shop,shop=shop,total_amount=total_amount)

@app.route('/pos_sales_value_data', methods=['GET', 'POST'])
def pos_sales_value_data():
    shop_list=[]
    for prod in ProdInvShop.objects(shop__ne='web'):
        shop_list.append(prod.shop)
    final_shop=list(set(shop_list))
    shop_data=[]
    for shop in final_shop:
        prod_shop=ProdInvShop.objects(shop=shop)
        total_qty=0
        for shop_qty in prod_shop:
            shop_details={}
            shop_details['shop']=shop_qty.shop
            total_qty+=int(shop_qty.outqty)
        shop_details['total_qty']=total_qty
        shop_data.append(shop_details)
    #return jsonify(shop_data)
    return render_template('pos_sales_value.html',shop_data=shop_data)


@app.route('/pos_sales_value_viewmore/<shop>', methods=['GET', 'POST'])
def pos_sales_value_viewmore(shop):
    prod_shop=[]
    total_amount=0
    for prod in ProdInvShop.objects(shop=shop):
        for prices in prod.price:
            data={}
            data['proddescription']=prod.proddescription
            data['brand']=prod.brand
            data['model']=prod.model
            data['outqty']=prod.outqty
            data['offer_price']=prices.offer_price
            data['subtotal']=int(prod.outqty)*float(prices.offer_price)
            total_amount+=int(prod.outqty)*float(prices.offer_price)
            prod_shop.append(data)
    return render_template('pos_sales_value_viewmore.html',prod_shop=prod_shop,shop=shop,total_amount=total_amount)


@app.route('/coupon_info_viewmore', methods=['GET', 'POST'])
def coupon_info_viewmore():
    cu_info= OrderCoupons.objects()    
    return render_template('coupon-info-list.html',cu_info=cu_info)


@app.route('/editprofile', methods = ['GET', 'POST'])
@login_required
def editprofile():
      with app.app_context():
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
               #controler =DashboardLink() 
               #result=controler.dashboardLink(request)
               if current_user.usertype=='Admin':
                  return redirect(url_for('dashboard'))
               elif current_user.usertype=='Supplier':
                  return redirect(url_for('supplier_dashboard'))
               elif current_user.usertype=='Distributor/Dealer':
                  return redirect(url_for('dealer_dashboard'))
               elif current_user.usertype=='Purchase-Manager':
                  return redirect(url_for('purchase_dashboard'))
               elif current_user.usertype=='WH-Manager':
                  return redirect(url_for('warehouse_dashboard'))
               elif current_user.usertype=='Accountant':
                  return redirect(url_for('account_dashboard'))
               elif  current_user.usertype=='Market Manager':
                  return redirect(url_for('marketing_dashboard')) 
      else:
            User = UserSignup.objects.get(id=current_user.id)
            userEditForm.username.data = User.username
            userEditForm.email.data = User.email
            userEditForm.mobile.data = User.mobile
            logger.info('Entered into editprofile')
            return render_template('edit_profile.html',userEditForm=userEditForm)
    

@app.route('/userlist', methods = ['GET', 'POST'])
@login_required
def userlist():
        logger.info('Entered into userlist')
        with app.app_context():
            form = UserList()
        if request.method == 'POST':
          if current_user.usertype=="Admin":
            username = request.form['username']
            email=request.form['email']
            mobile=request.form['mobile']
            password = request.form['password']
            usertype = request.form.get('usertype')
            isEmailExist=UserSignup.objects.filter(Q(email=email.lower()) | Q(mobile=mobile))
            status=request.form.get('purchasehide')
            if status=='yes':
                    pmlist = UserSignup.objects.get(email=email.lower())
                    pmlist.username=username
                    pmlist.mobile=mobile
                    pmlist.usertype=usertype
                    pmlist.password=generate_password_hash(password)
                    pmlist.save()
                    return redirect(url_for('userlist'))
            else:
                if isEmailExist.count()>0:
                     return render_template('emailmobile.html')
                createUser = UserSignup(username=username, email=email.lower(), mobile=mobile, password =generate_password_hash(password),usertype=usertype)# Insert form data in collection
                createUser.save()
                return redirect(url_for('userlist'))
        else:
            lists = UserSignup.objects()
            types=Usertype.objects()
            logger.info('Sucessfully Created new in Userlist')
            return render_template('userlist.html', form=form,lists=lists,types=types)

@app.route('/user_delete/', methods=['GET', 'POST'])
@login_required
def user_delete():
    if current_user.usertype=="Admin":
        logger.info('Entered into user_delete')
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="i"):
            brand_info = UserSignup.objects.get(id=docid)
            brand_info.delete()
        logger.info('Sucessfully Deleted  %s  in Userlist',type)
        return redirect(url_for('userlist'))

@app.route('/usertype', methods=['GET', 'POST'])
@login_required
def usertype():
        logger.info('Entered into usertype')
        with app.app_context():
            form = UsertypeForm()
        if request.method == 'POST' and form.validate():
          if current_user.usertype=="Admin":  
            usertype = request.form['usertype']
            userrole=request.form['userrole']
            status=request.form.get('hide')
            if status=='yes':
                userlist = Usertype.objects.get(usertype=usertype)
                userlist.userrole=userrole
                userlist.save()
            elif status!='yes':
                createUser = Usertype(usertype=usertype,userrole=userrole)# Insert form data in collection
                createUser.save()
            logger.info('Sucessfully Created  new in Usertype')
            return redirect(url_for('usertype'))
        else:
            types=Usertype.objects()
            return render_template('usertype.html',form=form,types=types)


@app.route('/usertypedelete/', methods=['GET', 'POST'])
@login_required
def usertypedelete():
    if current_user.usertype=="Admin":
        logger.info('Entered into usertypedelete')
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="i"):
            quickview = Usertype.objects.get(id=docid)
            quickview.delete()
        logger.info('Sucessfully Deleted  %s  in Usertype',type)
        return redirect(url_for('usertype'))
    
 #------------------------------------------------------------Home page-------------------------------

@app.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
         logger.info('Entered into home')
         if current_user.usertype == 'Admin':
             logger.info('Admin Entered into Admin dashboard')
             return redirect(url_for('dashboard'))
         if current_user.usertype == 'Support':
             logger.info('Entered into Support dashboard')
             return redirect(url_for('support_dashboard'))
         if current_user.usertype == 'Data-Entry-Manager':
             logger.info('Entered into Data-Entry-Manager dashboard')
             return redirect(url_for('data_entry_dashboard'))
         if current_user.usertype == 'Market Manager':
             logger.info('Market Manager Entered into Market Manager dashboard')
             return redirect(url_for('marketing_dashboard'))
         if current_user.usertype == 'Accountant':
             logger.info('Accountant Entered into Accountant dashboard')
             return redirect(url_for('account_dashboard'))
         if current_user.usertype == 'Purchase-Manager':
             logger.info('Purchase-Manager Entered into Purchase-Manager dashboard')
             return redirect(url_for('purchase_dashboard'))
         if current_user.usertype == 'WH-Manager':
             logger.info('WH-Manager Entered into WH-Manager dashboard')
             return redirect(url_for('warehouse_dashboard'))    
         if current_user.usertype=='Distributor/Dealer':
            something = Reg_Dealer.objects(user_id=str(current_user.id))
            if something.count>0:
               if something.count>0:
                userstatus = UserSignup.objects.get(id=current_user.id)
                if userstatus.status == 'Process':
                    return redirect(app.config['Register']+'reg_dealer/'+str(current_user.id))
                elif userstatus.status == 'Inactive':
                    return render_template('home.html',userinfo=current_user)
                elif userstatus.status == 'Review':
                    return render_template('home.html',userinfo=current_user)
                elif userstatus.status == 'Active':
                    logger.info('Dealer Entered into Dealer dashboard')
                    return redirect(app.config['Dealer_Dashboard']+'dealer_dashboard/'+str(current_user.id))
            else:
                return render_template('home.html',userinfo=current_user)
         elif  current_user.usertype=='Supplier':
            something = Reg_Supplier.objects(user_id=str(current_user.id))
            if something.count>0:
               userstatus = UserSignup.objects.get(id=current_user.id)
               if userstatus.status == 'Process':
                 return redirect(app.config['Register']+'reg_supplier/'+str(current_user.id))
               elif userstatus.status == 'Inactive':
                 return render_template('home.html',userinfo=current_user)
               elif userstatus.status == 'Review':
                  return render_template('home.html',userinfo=current_user)
               elif userstatus.status == 'Active':
                 logger.info('Supplier Entered into Supplier dashboard')
                 return redirect(app.config['Supplier_Dashboard']+'supplier_dashboard/'+str(current_user.id))
            else:
                return render_template('home.html',userinfo=current_user)

     #-----------------------------------Registration Forms------------------------------------------------------------------>

@app.route('/reg_dealer', methods = ['GET', 'POST'])
@login_required
def reg_dealer():
      if current_user.usertype=='Distributor/Dealer':
        with app.app_context():
            form = DealerForm()
        if request.method == 'POST' and form.validate():
            controler  = SignUpControler()
            result = controler.regDealerCotrl(request)
            if result=="Fail":
                 return render_template('error.html',msg=str('ShopName Existed'))
            return render_template('reg_success.html')
        else:
            empDetails = UserSignup.objects.get(email = current_user.email)
            form.dealer_name.data = empDetails.username
            form.dealer_mail.data = empDetails.email
            form.dealer_mobile.data = empDetails.mobile
            return render_template('dealer-register.html',form=form)
      return render_template('error.html',reportsof = 'Unauthorized out ....')


@app.route('/reg_supplier', methods = ['GET', 'POST'])
@login_required
def reg_supplier():
       if current_user.usertype=='Supplier':   
        with app.app_context():
            form = SupplierForm()
        if request.method == 'POST' and form.validate():
            controler  = SignUpControler()
            result = controler.regSupplierCotrl(request)
            if result=="Fail":
                return render_template('error.html',reportsof = 'Registration Failed')
            return render_template('reg_success.html')
        else:
            empDetails = UserSignup.objects.get(email = current_user.email)
            form.supplier_name.data = empDetails.username
            form.supplier_mail.data = empDetails.email
            form.supplier_mobile.data = empDetails.mobile
            return render_template('supplier-register.html',form=form)
       return render_template('error.html',reportsof = 'Unauthorized out ....')


#-------------------------User have to create own credentials to login direct admin dashbord--------------------------------------

@app.route('/createadmin', methods = ['GET', 'POST','PUT'])
def createAdmin():
        logger.info('Entered into createAdmin')
        createUser = UserSignup(username="admin", email="smthub.2017@gmail.com",std_isd="91", mobile="8885060326", password =generate_password_hash("Admin#123"),usertype="Admin")
        createUser.save()
        return "Admin created successfully."

#------------------------purchase info------------------------------------------------------------------------
@app.route('/purchase_dashboard', methods = ['GET', 'POST'])
@login_required
def purchase_dashboard():
    logger.info('Entered into Purchase manager dashboard')
    purchase_orders=PurchaseOrders.objects(user_id=str(current_user.id)).count()
    purchase_invoice= PurchaseInvoice.objects(purchase_manager_id=current_user.username).count()
    return render_template('purchase-manager-dashboard.html',purchase_orders=purchase_orders,purchase_invoice=purchase_invoice)


    
@app.route('/admin_purchaselist')
@login_required
def admin_purchaselist():
        if current_user.usertype=='Admin':
           logger.info('Admin Entered into purchaselist')
           purchase= PurchaseOrders.objects().order_by('-id')
           return render_template('admin_purchaselist.html',purchase=purchase)
        elif current_user.usertype=='Purchase-Manager':
            purchase=PurchaseOrders.objects(user_id=str(current_user.id)).order_by('-id')
            logger.info('Purchase manager Entered into purchaselist')
            return render_template('admin_purchaselist.html',purchase=purchase)
        elif current_user.usertype=='Accountant':
            purchase=PurchaseOrders.objects().order_by('-id')
            logger.info('Accountant Entered into purchaselist')
            return render_template('admin_purchaselist.html',purchase=purchase)
    
@app.route('/adminpurchaseinformation/<id>',methods = ['GET', 'POST'])
@login_required
def adminpurchaseinformation(id):
       if current_user.usertype=='Admin' or current_user.usertype=='Purchase-Manager'or current_user.usertype=='Accountant':
        detailes = PurchaseOrders.objects.filter(id=id).first()
        number= num2words(detailes.totalvalue)
        company=Company_Setup.objects()
        billing=Billing_Setup.objects()
        warehouse=Warehouse.objects()
        headerlist = Header_Setup.objects()
        header=Header.objects()
        logo=header[0].headerlogo
        regsup=Reg_Supplier.objects(user_id=detailes.supplier_id)
        logger.info('Entered into Purchase Information')
        return render_template('admin-orderviewmore.html',detailes=detailes,company=company[0],billing=billing[0],warehouse=warehouse[0],logo=logo,regsup=regsup[0],headerlist=headerlist[0],number=number)
       else:
           if current_user.usertype=='Supplier':
            detailes = PurchaseOrders.objects.filter(id=id).first()
            number= num2words(detailes.totalvalue)
            company=Company_Setup.objects()
            billing=Billing_Setup.objects()
            header=Header.objects()
            logo=header[0].headerlogo
            warehouse=Warehouse.objects()
            headerlist = Header_Setup.objects()
            regsup=Reg_Supplier.objects(user_id=detailes.supplier_id)
            if request.method == 'POST':
                comment=request.form.get('comment')
                detailes.remarks=comment
                if request.form.get('submit') == 'Accept':
                    detailes.status = 'Accept'
                    detailes.save()
                    return redirect(url_for('/purchase_invoice',id=id))
                else:
                    detailes.status='Reject'
                    detailes.save()
            logger.info('Entered into Purchase Information')
            return render_template('admin-orderviewmore.html',detailes=detailes,company=company[0],billing=billing[0],logo=logo,warehouse=warehouse[0],regsup=regsup[0],headerlist=headerlist[0],number=number)


@app.route('/purchase_delete/', methods=['GET', 'POST'])
@login_required
def purchase_delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="em"):
            quickview = PurchaseOrders.objects.get(id=docid)
            quickview.delete()
        logger.info('Deleted Purchase information')
        return redirect(url_for('admin_purchaselist'))


@app.route('/admin_purchaseinvoice')
@login_required
def admin_purchaseinvoice():
        if current_user.usertype=='Admin':
           logger.info('Admin Entered into admin_purchaseinvoice')
           purchaseinvoice=PurchaseInvoice.objects()  
           return render_template('admin_purchaseinvoice.html',purchaseinvoice=purchaseinvoice)
        elif current_user.usertype=='Purchase-Manager':
           logger.info('Purchase-Manager Entered into admin_purchaseinvoice')
           purchaseinvoice= PurchaseInvoice.objects(purchase_manager_id=current_user.username)   
           return render_template('admin_purchaseinvoice.html',purchaseinvoice=purchaseinvoice)


@app.route('/adminpurchaseinvoiceinfo/<id>',methods = ['GET', 'POST'])
@login_required
def adminpurchaseinvoiceinfo(id):
        if current_user.usertype=='Admin':
           logger.info('Admin Entered into adminpurchaseinvoiceinfo')
           detailess = PurchaseInvoice.objects.filter(id=id).first()
           purchase_data=PurchaseOrders.objects(purchaseOrder_no=detailess.purchaseOrder_no)
           company=Company_Setup.objects()
           billing=Billing_Setup.objects()
           warehouse=Warehouse.objects()
           headerlist = Header_Setup.objects()
           regsup=Reg_Supplier.objects()
           number= num2words(float((detailess.total_value)))
           return render_template('purchaseinvoice-viewmore.html',purchase_data=purchase_data,detailess=detailess,company=company[0],billing=billing[0],warehouse=warehouse[0],headerlist=headerlist[0],regsup=regsup[0],number=number)
        elif current_user.usertype=='Purchase-Manager':
           logger.info('Purchase-Manager Entered into adminpurchaseinvoiceinfo')
           detailess = PurchaseInvoice.objects.filter(id=id).first()
           purchase_data=PurchaseOrders.objects(purchaseOrder_no=detailess.purchaseOrder_no)
           company=Company_Setup.objects()
           billing=Billing_Setup.objects()
           warehouse=Warehouse.objects()
           headerlist = Header_Setup.objects()
           regsup=Reg_Supplier.objects()
           header=Header.objects()
           logo=header[0].headerlogo
           number= num2words(float((detailess.total_value)))
           return render_template('purchaseinvoice-viewmore.html',purchase_data=purchase_data,detailess=detailess,company=company[0],logo=logo,billing=billing[0],warehouse=warehouse[0],headerlist=headerlist[0],regsup=regsup[0],number=number)
 
#---------------supplier and dealer details---------------------------------------------------------------------

@app.route('/service_center_details', methods = ['GET', 'POST'])
@login_required
def service_center_details():
        dealer= Reg_Service.objects()
        logger.info('Entered into Dealer details ')        
        return render_template('service_details.html',dealer=dealer)

  
@app.route('/serviceviewmore/<id>', methods = ['GET', 'POST'])
@login_required
def serviceviewmore(id):
        userstatus = Reg_Service.objects.get(id=id)
        detail = Reg_Dealer.objects.get(user_id=userstatus.user_id)# Fetching Query
        logger.info('Entered into Dealer Viewmore ')
        return render_template('service_centerviewmore-details.html',detail=detail)

@app.route('/serviceactive/<id>')
@login_required
def serviceactive(id):
        userstatus = Reg_Service.objects.get(id=id)
        if userstatus.status == 'Inactive':
            userstatus.status = 'Active'
           
            dealer=Reg_Dealer.objects.get(user_id=userstatus.user_id)
            dealer.dealer_authority='True'
            dealer.save()
            userstatus.save()
            return redirect(url_for('service_center_details'))

@app.route('/service_delete/', methods=['GET', 'POST'])
@login_required
def service_delete():
        logger.info('Entered into user_delete')
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="i"):
            service = Reg_Service.objects.get(id=docid)
            service.delete()
        logger.info('Sucessfully Deleted  %s  in service',type)
        return redirect(url_for('service_center_details'))

 

@app.route('/dealer_details', methods = ['GET', 'POST'])
@login_required
def dealer_details():
        dealer=[]
        for detail in UserSignup.objects(usertype = 'Distributor/Dealer'):
           info = Reg_Dealer.objects(dealer_mail=detail.email)
           if info.count()>0:
                data={}
                data['id']=detail.id
                data['username']=detail.username
                data['email']=detail.email
                data['mobile']=detail.mobile
                data['registered_on']=detail.registered_on
                data['status']=detail.status
                data['userid']=detail.userid
                data['shopname']=info[0].dealer_shopname
                dealer.append(data)
            
           else:
                data={}
                data['id']=detail.id
                data['username']=detail.username
                data['email']=detail.email
                data['mobile']=detail.mobile
                data['registered_on']=detail.registered_on
                data['status']=detail.status
                data['userid']=detail.userid
                data['shopname']='None'
                dealer.append(data)  
        
        logger.info('Entered into Dealer details ')        
        return render_template('dealer-details.html',dealer=dealer)
'''
@app.route('/dealer_details', methods = ['GET', 'POST'])
@login_required
def dealer_details():
        dealer= UserSignup.objects(usertype = 'Distributor/Dealer')
        logger.info('Entered into Dealer details ')        
        return render_template('dealer-details.html',dealer=dealer)
'''
@app.route('/dealerviewmore/<email>', methods = ['GET', 'POST'])
@login_required
def dealerviewmore(email):
        detail = Reg_Dealer.objects.filter(dealer_mail=email).first()# Fetching Query
        logger.info('Entered into Dealer Viewmore ')
        return render_template('dealerviewmore-details.html',detail=detail)
    

@app.route('/supplier_details', methods = ['GET', 'POST'])
@login_required
def supplier_details():
        supplier=[]
        for detail in UserSignup.objects(usertype = 'Supplier'):
           info = Reg_Supplier.objects(supplier_mail=detail.email)
           if info.count()>0:
                data={}
                data['id']=detail.id
                data['username']=detail.username
                data['email']=detail.email
                data['mobile']=detail.mobile
                data['registered_on']=detail.registered_on
                data['status']=detail.status
                data['userid']=detail.userid
                data['companyname']=info[0].supplier_companyname
                supplier.append(data)
                
           else:
            data={}
            data['id']=detail.id
            data['username']=detail.username
            data['email']=detail.email
            data['mobile']=detail.mobile
            data['registered_on']=detail.registered_on
            data['status']=detail.status
            data['userid']=detail.userid
            data['companyname']='None'
            supplier.append(data)
        logger.info('Entered into Supplier details ')        
        return render_template('supplier-details.html',supplier=supplier)
'''
@app.route('/supplier_details', methods = ['GET', 'POST'])
@login_required
def supplier_details():
        supplier=UserSignup.objects(usertype = 'Supplier')
        logger.info('Entered into Supplier details ')        
        return render_template('supplier-details.html',supplier=supplier)
'''    

@app.route('/supplierviewmore/<name>', methods = ['GET', 'POST'])
@login_required
def supplierviewmore(name):
        info = Reg_Supplier.objects(supplier_mail=name).first()# Fetching Query
        logger.info('Entered into Supplier Viewmore ')
        return render_template('supplierviewmore-details.html',info=info)


@app.route('/actives/<email>')
@login_required
def actives(email):
        pool = Pool()
        pool_new(pool)
        userstatus = UserSignup.objects.get(email=email)
        if userstatus.status == 'Inactive':
            userstatus.status = 'Process'
            userstatus.save()
            return render_template('success.html')
        elif userstatus.status == 'Review':
            userstatus.status = 'Active'
            userstatus.save()
            if userstatus.usertype=='Supplier':
                supUser = Reg_Supplier.objects(supplier_mail=email)
                s= supUser[0].supplier_companyname
                sup=s[0]
                numbers =  Number().get()
                number=sup+numbers
                Number().put(numbers)
                userstatus.userid = number
                userstatus.save()
                registeredUser = Reg_Supplier.objects(supplier_mail=email)
                if registeredUser.count() > 0:
                  fo = open("./static/mailtemp/suppliermailtemp.html", "r+")
                  htmlbody = fo.read()
                  fo.close()
                  urldata='Dear '+registeredUser[0].supplier_name+',<br> Your registration process is done. Login using registered e mail Id/mobile number. Thank you.'
                  htmlbody = htmlbody.replace("$$urldata$$",urldata)
                  #sendMail(email,'Supplier Verification & Approval',htmlbody)
                  pool.apply_async(sendMail,[email,'Your registration is successful',htmlbody])
                  msg="Dear "+registeredUser[0].supplier_name+", Your registration process is done. Login using registered e mail Id/mobile number. Thank you."
                  mobileList=[]
                  mobileList.append(registeredUser[0].supplier_isd+registeredUser[0].supplier_mobile)
                  #SMS(msg,mobileList)
                  pool.apply_async(SMS,[msg,mobileList])
                  return render_template('success.html')
                  
            else:
                registeredUser = Reg_Dealer.objects(dealer_mail=email)
                s= registeredUser[0].dealer_gstin
                sup=s[0:2]
                numbers =  DealerNumber().get()
                number=sup+numbers
                DealerNumber().put(numbers)
                userstatus.userid = number
                userstatus.save()
                if registeredUser.count() > 0:
                      fo = open("./static/mailtemp/dealermailtemp.html", "r+")
                      htmlbody = fo.read()
                      fo.close()
                      urldata='Dear '+registeredUser[0].dealer_name+',<br> Your registration process is done. Login using registered e mail Id/mobile number. Thank you.'
                      htmlbody = htmlbody.replace("$$urldata$$",urldata)
                      #sendMail(email,'Dealer Verification & Approval',htmlbody)
                      pool.apply_async(sendMail,[email,'Your registration is successful',htmlbody])
                      msg="Dear "+registeredUser[0].dealer_name+", Your registration process is done. Login using registered e mail Id/mobile number. Thank you." 
                      #mobile='91'+registeredUser[0].dealer_mobile
                      #SMS(msg,mobile)
                      mobileList=[]
                      mobileList.append(registeredUser[0].dealer_isd+registeredUser[0].dealer_mobile)
                      #print mobileList
                      pool.apply_async(SMS,[msg,mobileList])
                return render_template('success.html')
        else:
            userstatus.status = 'Active'
            userstatus.save()
            return render_template('success.html')


@app.route('/reject/<email>')
@login_required
def reject(email):
        pool = Pool()
        pool_new(pool)
        userstatus = UserSignup.objects.get(email=email)
        if userstatus.status == 'Review':
            userstatus.status = 'Reject'
            userstatus.save()
            if userstatus.usertype=='Supplier':
                registeredUser = Reg_Supplier.objects(supplier_mail=email)
                if registeredUser.count() > 0:
                  fo = open("./static/mailtemp/suppliermailtemp.html", "r+")
                  htmlbody = fo.read()
                  fo.close()
                  urldata='Dear '+registeredUser[0].supplier_name+',Regret to inform that the details are incorrect. Thank you for signing with us. <br> For any further assistance, contact us at <Customer care contact number> or write to us at <Customer care mail id> on all days between 9am to 10pm.'
                  htmlbody = htmlbody.replace("$$urldata$$",urldata) 
                  #sendMail(email,'Supplier Verification & rejected',htmlbody)
                  pool.apply_async(sendMail,[email,'Supplier Verification & rejected',htmlbody])
                  msg="Dear "+registeredUser[0].supplier_name+",We regret to inform you that currently we are not interested to associated with you. Thank you for signing with us." 
                  mobileList=[]
                  mobileList.append(registeredUser[0].supplier_isd+registeredUser[0].supplier_mobile) 
                  #SMS(msg,mobile)
                  pool.apply_async(SMS,[msg,mobileList])
            else: 
                registeredUser = Reg_Dealer.objects(dealer_mail=email)
                
                if registeredUser.count() > 0:
                      fo = open("./static/mailtemp/dealermailtemp.html", "r+")
                      htmlbody = fo.read()
                      fo.close()
                      urldata='Dear '+registeredUser[0].dealer_name+',<br>We regret to inform you that currently we are not interested to associated with you. Thank you for signing with us. '
                      htmlbody = htmlbody.replace("$$urldata$$",urldata)
                      htmlbody = '<html><body><table><tr><td></td></tr></body></html>'
                      #sendMail(email,'Dealer Verification & rejected',htmlbody)
                      pool.apply_async(sendMail,[email,'Dealer Verification & rejected',htmlbody])
                      msg="Dear "+registeredUser[0].dealer_name+",We regret to inform you that currently we are not interested to associated with you. Thank you for signing with us."
                      #mobile='91'+registeredUser[0].dealer_mobile
                      mobileList=[]
                      mobileList.append(registeredUser[0].dealer_isd+registeredUser[0].dealer_mobile) 
                      #SMS(msg,mobile)
                      pool.apply_async(SMS,[msg,mobileList])
            return render_template('success.html')
        else:
            userstatus.status = 'Active'
            userstatus.save()
            return render_template('success.html')  

@app.route('/delete/', methods=['GET', 'POST'])
@login_required
def delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="em"):
            quickview = UserSignup.objects.get(id=docid)
            quickview.delete()
        logger.info(' User Deleted Sucessfully')
        return render_template('delete.html')
#-------------------------------------------------supplierinfo----------------------------------------------------------------------------------------------
@app.route('/productlist',methods = ['GET', 'POST'])
@login_required
def productlist():
    logger.info('Admin Entered into productlist')
    product= Sup_Upload.objects()    
    return render_template('product-list.html',product=product)

@app.route('/productviewmore/<id>',methods = ['GET', 'POST'])
@login_required
def productviewmore(id):
        pool = Pool()
        pool_new(pool)
        detailes = Sup_Upload.objects.filter(id=id).first()
        sup=Reg_Supplier.objects(user_id=detailes.user_id)
        if request.method == 'POST':
            comment=request.form.get('comment')
            detailes.remarks=comment
            if request.form.get('submit') == 'Accept':
                detailes.status = 'Accept'
                detailes.save()
                registeredUser = Sup_Upload.objects(id=id)
                if registeredUser.count() > 0:
                  fo = open("./static/mailtemp/suppliermailtemp.html", "r+")
                  htmlbody = fo.read()
                  fo.close()
                  urldata='Your product is reviewed successfully. Login to check details..'
                  htmlbody = htmlbody.replace("$$urldata$$",urldata)
                  #sendMail(sup[0].supplier_mail,'Product is reviewed- Accepted',htmlbody)
                  pool.apply_async(sendMail,[sup[0].supplier_mail,'Product reviewed by admin',htmlbody])
                  msg="Your product(s) are reviewed successfully. Login for the status." 
                  #mobile='91'+sup[0].supplier_mobile
                  mobileList=[]
                  mobileList.append(sup[0].supplier_isd+sup[0].supplier_mobile)
                  #SMS(msg,mobile)
                  pool.apply_async(SMS,[msg,mobileList])
                  registeredUser1 = UserSignup.objects(usertype='Market Manager')
                  fo = open("./static/mailtemp/suppliermailtemp.html", "r+")
                  htmlbody = fo.read()
                  fo.close()
                  adminmail=registeredUser1[0].email
                  urldata='Product is reviewed and accepted. Need to set the prices.'
                  htmlbody = htmlbody.replace("$$urldata$$",urldata)
                  #sendMail(email,'Supplier Verification & Approval',htmlbody)
                  pool.apply_async(sendMail,[adminmail,'Product price required',htmlbody])
                  msg='Product is reviewed and accepted. Need to set the prices.'
                  mobileList=[]
                  mobileList.append("91"+registeredUser1[0].mobile)
                  #SMS(msg,mobileList)
                  pool.apply_async(SMS,[msg,mobileList])
                return redirect(url_for("productlist"))
            else:
                detailes.status='Reject'
                detailes.save()
                wh=ProdinvWH.objects.get(prod_desc=detailes.upload_name)
                #print detailes.upload_name
                #print wh
                wh.delete()
                registeredUser = Sup_Upload.objects(id=id)
                if registeredUser.count() > 0:
                  fo = open("./static/mailtemp/suppliermailtemp.html", "r+")
                  htmlbody = fo.read()
                  fo.close()
                  urldata='Your product(s) are reviewed successfully. Login for the status.'
                  htmlbody = htmlbody.replace("$$urldata$$",urldata)
                  #sendMail(sup[0].supplier_mail,'Product is reviewed- Rejected',htmlbody)
                  pool.apply_async(sendMail,[sup[0].supplier_mail,'Product reviewed by admin',htmlbody])
                  msg="Your product(s) are reviewed successfully. Login for the status." 
                  mobileList=[]
                  mobileList.append(sup[0].supplier_isd+sup[0].supplier_mobile)
                  #SMS(msg,mobile)
                  pool.apply_async(SMS,[msg,mobileList])
                return redirect(url_for("productlist"))
        logger.info('Entered into Product Viewmore')
        return render_template('product-viewmore.html',detailes=detailes,supname=sup[0].supplier_name)

@app.route('/productdelete/', methods=['GET', 'POST'])
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
#------------------------master products----------------------------------------------------------------   
@app.route('/master_products', methods = ['GET', 'POST'])
@login_required
def master_products():
        with app.app_context():
         form1 = MasterproductForm1()
         form2 = MasterproductForm2()
         form3 = MasterproductForm3()
         if request.method == 'POST':
            #print request.form.get('categoryname')
            #print request.form['subcategoryid']
            #print request.form['subcategory']
            
            if form1.validate():
                print "HIIII"
                categoryid =request.form['categoryid']              
                categoryname=request.form['categoryname']                
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
                    
                iscategoryid=Category.objects(categoryid=categoryid)
                iscategoryname=Category.objects(categoryname=categoryname)
                status=request.form.get('cathide')
                if status=='yes':
                    catlist = Category.objects.get(categoryid=categoryid)
                    catlist.categoryname=categoryname
                    catlist.save()
                elif status !='yes' :
                  if iscategoryid.count()>0 or iscategoryname.count()>0:
                     return render_template('categoryy.html')
                  CatNumber().put(categoryid)   
                  
                  cat = Category(categoryid=categoryid, categoryname=categoryname.strip(),tags=tagsinfo,metadescription=metatagsinfo,keywords=keywordsinfo) 
                  cat.save()
                    
                logger.info('Category Entered sucessfully')
                return redirect(url_for('master_products'))
            elif form2.validate():
                print "Hi"
                categoryname=request.form.get('categoryname')
                print categoryname
                subcategoryid = request.form['subcategoryid']
                print subcategoryid
                subcategory = request.form['subcategory']
                print subcategory
                issubcategoryid=Sub_Category.objects(subcategoryid=subcategoryid)
                issubcategory=Sub_Category.objects(subcategory=subcategory)
                status=request.form.get('cathide')
                if status=='yes':
                    catlist = Sub_Category.objects.get(subcategoryid=subcategoryid)
                    catlist.subcategory=subcategory
                    catlist.save()
                elif status !='yes' :
                    if issubcategoryid.count()>0:
                       return render_template('categoryy.html')
                    SubcatNumber().put(subcategoryid) 
                    subcat = Sub_Category(categoryname=categoryname.strip(),subcategoryid=subcategoryid,subcategory=subcategory.strip()) 
                    subcat.save()
                logger.info('SubCategory Entered sucessfully')
                return redirect(url_for('master_products'))  
            else:
                productid = request.form['productid']
                categoryname = request.form.get('categoryname')
                subcategory = request.form.get('subcategory')
                productname = request.form['productname']
                description = request.form['description']
                atrname = request.form.getlist('attributeName')
                isproductid=Product.objects(productid=productid)
                isproductname=Product.objects(productname=productname)
                status=request.form.get('cathide')
                if status=='yes':
                    catlist = Product.objects.get(productid=productid)
                    catlist.productname=productname
                    catlist.description=description
                    #catlist.attribute=[]
                    catlist.save()
                    for x in range(len(atrname)):
                      atrs = Atname(atrname[x])
                      catlist.attribute.append(atrs)
                    catlist.save()
                elif status !='yes' :
                    if isproductid.count()>0 or isproductname.count()>0:
                       return render_template('categoryy.html')
                    pdct = Product(productid=productid, categoryname=categoryname,subcategory=subcategory,productname=productname,description=description) 
                    pdct.save()
                    for x in range(len(atrname)):
                      atrs = Atname(atrname[x])
                      pdct.attribute.append(atrs)
                      pdct.save()
                logger.info('Product Entered sucessfully')
                return redirect(url_for('master_products'))
        categorylist = Category.objects()
        categorylist1 = Sub_Category.objects()
        categorylist2= Product.objects()
        categorynumber=CatNumber().get()
        subcategorynumber=SubcatNumber().get()
        logger.info('Entered cat ,subcat and product sucessfully')
        return render_template('master-products.html',form1=form1,form2=form2,form3=form3,categorylist=categorylist,categorylist1=categorylist1,categorylist2=categorylist2,
                               categorynumber=categorynumber,subcategorynumber=subcategorynumber)

    
@app.route('/master_product_delete/', methods=['GET', 'POST'])
@login_required
def master_product_delete():

            type = request.args.get('type')
            docid = request.args.get('docid')
            categoryname1 = request.args.get('categoryname')
            if(type=="cat"):
                exists=Sub_Category.objects(categoryname=categoryname1)
                if exists:
                    return "the category is not deleted"
                else:
                    user=Category.objects.get(id=docid)
                    user.delete()
                    logger.info('Category Deleted sucessfully')
                    return redirect(url_for('master_products'))
            elif(type=="subcat"):
                exists=Product.objects(categoryname=categoryname1)
                if exists:
                    return "the category is not deleted"
                else:
                    user=Sub_Category.objects.get(id=docid)
                    user.delete()
                    logger.info('Subcategory Deleted sucessfully')
                    return redirect(url_for('master_products'))
            else:
                user=Product.objects.get(id=docid)
                user.delete()
                logger.info('Product Deleted sucessfully')
                return redirect(url_for('master_products'))     
            
@app.route('/catsubatr_post/', methods=['GET', 'POST'])
@login_required
def catsubatr_post():
    try:
        logger.info('Entered into catsubatr_post')
        subcat=request.args.get('catname')
        subcategory=[]
        for subcat in Sub_Category.objects(categoryname=subcat):
            subcategory.append(subcat.subcategory)
        sub=sorted(subcategory)
        return jsonify(sub)   
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')    

@app.route('/attribute_post/', methods=['GET', 'POST'])
@login_required
def attribute_post():
    try:
       logger.info('Entered into attribute_post')
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

@app.route('/countries', methods = ['GET', 'POST'])
@login_required
def countries():
        with app.app_context():
         form1 = CountryForm1()
         form2 = CountryForm2()
         form3 = CountryForm3()
         if request.method == 'POST':
            if form1.validate():
                countryname = request.form['countryname']
                country_std_isd=request.form['country_std_isd']
                countryinfo = Country(countryname=countryname,country_std_isd=country_std_isd) 
                countryinfo.save()
                return redirect(url_for('countries'))
            elif form3.validate():
                #return 'hi'
                countryname = request.form.get('countryname')
                state = request.form.get('state')
                city = request.form['city']
                cityinfo = City(countryname=countryname, state=state,city=city) 
                cityinfo.save()
                return redirect(url_for('countries'))    
            else:
                countryname=request.form.get('countryname')
                state = request.form['state']
                stateinfo = State(countryname=countryname,state=state) 
                stateinfo.save()
                return redirect(url_for('countries'))
        countrylist = Country.objects()
        countrylist1 = State.objects()
        countrylist2= City.objects()
        return render_template('country.html',form1=form1,form2=form2,form3=form3,countrylist=countrylist,countrylist1=countrylist1,countrylist2=countrylist2)

@app.route('/country_state_city_delete/', methods=['GET', 'POST'])
@login_required
def country_state_city_delete():

            type = request.args.get('type')
            docid = request.args.get('docid')
            countryname = request.args.get('countryname')
            if(type=="country"):
                exists=State.objects(countryname=countryname)
                if exists:
                    return "the country is not deleted"
                else:
                    user=Country.objects.get(id=docid)
                    user.delete()
                    logger.info('Country Deleted sucessfully')
                    return redirect(url_for('countries'))
            elif(type=="state"):
                exists=City.objects(countryname=countryname)
                if exists:
                    return "the country is not deleted"
                else:
                    user=State.objects.get(id=docid)
                    user.delete()
                    logger.info('State Deleted sucessfully')
                    return redirect(url_for('countries'))
            else:
                user=City.objects.get(id=docid)
                user.delete()
                logger.info('City Deleted sucessfully')
                return redirect(url_for('countries'))    

@app.route('/countrystate_post/', methods=['GET', 'POST'])
@login_required
def countrystate_post():
    try:
        logger.info('Entered into catsubatr_post')
        subcat=request.args.get('catname')
        subcategory=[]
        for subcat in State.objects(countryname=subcat):
            subcategory.append(subcat.state)
        sub=sorted(subcategory)
        return jsonify(sub)   
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')
    
#------------------------------------------------------------------Purchase dept-------------------------------------------------------------------------------------------------
@app.route('/purchase_order', methods=['GET', 'POST'])
@login_required
def Purchase_order():
        with app.app_context():
            form = PurchaseOrderForm()
        if request.method == 'POST' and form.validate():
            supplier_docid=request.form.get('supplier_docid')
            warehouse_docid = request.form.get('warehouse_docid')
            return redirect(url_for('purchaseorder_viewmore'))    
        else:
            warehouselist = Warehouse.objects()
            supplierlist = UserSignup.objects(status='Active',usertype='Supplier')
            logger.info('Entered into purchase order ')
            return render_template('purchase_orders_login.html', form=form,supplierlist=supplierlist,warehouselist=warehouselist)
                
@app.route('/purchaseorder_viewmore', methods=['GET', 'POST'])
@login_required
def purchaseorder_viewmore():
        with app.app_context():
            form = PurchaseOrderviewForm()
        if request.method == 'POST':
            supplier_docid=request.form.get('supplier_docid')
            warehouse_docid = request.form.get('warehouse_docid')
            if supplier_docid=='0' or warehouse_docid =='0':
                return redirect(url_for('Purchase_order'))
            warehouselist = Warehouse.objects.get(id=warehouse_docid)
            supplierlist = UserSignup.objects.get(status='Active',usertype='Supplier',id=supplier_docid)
            user=current_user
            supplier=Reg_Supplier.objects(user_id=supplier_docid)
            if len(supplier)==0:
                return render_template('error.html',reportsof = 'Exception',msg='No Supplier Available')
            supplierinfo = supplier[0]
            productinfo=Sup_Upload.objects(user_id=supplierinfo.user_id,status="Accept")
            productinventory = []
            purchaseNumber = PurchaseNumber().get()
            #purchaseNumbers=PurchaseNumber().put(purchaseNumber)
            for product in productinfo:
                whproducts= ProdinvWH.objects(prod_desc=product.upload_name)
                avlqty = '0'
                if whproducts.count() >0: 
                    if whproducts[0].quantity != '0':
                        avlqty = whproducts[0].quantity
                data = {}
                data['upload_id'] = product.upload_id
                data['upload_name'] = product.upload_name
                data['upload_brand'] = product.upload_brand
                data['upload_modelno'] = product.upload_modelno
                data['upload_hsncode'] = product.upload_hsncode
                data['avlqty'] = avlqty
                netval=product.upload_netPrice
                #netprice=
                #(netval, '.f')
                data['upload_netPrice']=netval
                json_data = json.dumps(data)
                test=json.loads(json_data)
                productinventory.append(test)
            logger.info('Entered into purchase order Viewmore')
            return render_template('purchase-orders.html',form=form,warehouselist=warehouselist,supplierlist=supplierlist
                              ,warehouse_docid=warehouse_docid,supplier_docid=supplier_docid,supplierinfo=supplierinfo,user=user,productinventory=productinventory, purchaseNumber = purchaseNumber)
        return redirect(url_for('purchaseorder_viewmore'))                    
   
@app.route('/purchase_post', methods=['GET', 'POST'])
@login_required
def purchase_post():
    pool = Pool()
    pool_new(pool)
    try:      
      if request.method == 'POST':
       logger.info('Entered into purchase Post')
       
       json_data = request.get_json(force=True)
       warehouse_name = json_data['ware_house']
       
       supplier_name = json_data['supplier_name']
       supplier_id=json_data['supplier_id']
       supplier_address = json_data['supplier_address']
       purchaseManager = json_data['purchase_manager_id']
       #purchaseOrder_no = json_data['purchaseOrder_no']
       po_date = json_data['po_date']
       totalitems = json_data['total_items']
       totalqty = json_data['total_quantity']
       if totalitems =='0' or totalqty == '0':
           return redirect(url_for('purchaseorder_viewmore'))
       elif totalitems=='NaN' or totalqty =='NaN':
           return 'Fail'
       totalvalue = json_data['total_value']
       purchaseNumber = PurchaseNumber().get()
       purchaseinfo = PurchaseOrders(user_id=str(current_user.id),warehouse_name=warehouse_name, supplier_name=supplier_name,supplier_id=supplier_id,
                                        supplier_address=supplier_address, purchaseManager=purchaseManager,purchaseOrder_no=purchaseNumber,
                                        po_date =po_date,totalitems=totalitems,totalqty=totalqty,totalvalue=totalvalue)
       purchaseinfo.save()
       item=0
       for i in json_data['items']:
            item += 1
            var=str(item)
            #item = i['item']
            order_id = i['item_id']
            name=i['item_name']
            model_no = i['item_model']
            hsn = i['item_hsn']
            quantity = i['item_quntity']
            netprice = i['item_price']
            value = i['item_value']
            order = WHOrders(var, order_id,name,model_no,hsn,quantity ,netprice,value)
            purchaseinfo.orderslist.append(order)
            purchaseinfo.save()
       PurchaseNumber().put(purchaseNumber)

       user=Reg_Supplier.objects(user_id=supplier_id)
       usersmail=UserSignup.objects.get(id=user[0].user_id)
       emailList=[]
       emailList.append(usersmail.email)
       fo = open("./static/mailtemp/suppliermailtemp.html", "r+")
       htmlbody = fo.read()
       fo.close()
       urldata='Supplier has received a purchase order from Purchase manager and need an acknowledgement.'
       htmlbody = htmlbody.replace("$$urldata$$",urldata)
       
       sendMail(emailList,"Acknowledgement for purchase order"+purchaseNumber,htmlbody)
       #pool.apply_async(sendMail,[emailList,"Acknowledgement for purchase order",htmlbody])
       msg="Supplier has received a purchase order from Purchase manager and need an acknowledgement."
       mobileList=[]
       mobileList.append('91'+usersmail.mobile)
       #print mobileList         
       SMS(msg,mobileList)
       #pool.apply_async(SMS,[msg,mobileList])

       return 'Success'
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')

#-------------------------bank info----------------------------------------------------------------------------
@app.route('/bankinfo', methods=['GET', 'POST'])
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

#--------------------------------------------------------------------WH Dept-----------------------------------------------------------------

@app.route('/warehouse_dashboard', methods = ['GET', 'POST'])
@login_required
def warehouse_dashboard():
       logger.info('Entered into warehouse dashboard')
       warehouses=Warehouse.objects().count()
       warehouse= "{:,}".format(warehouses)
       purchase=PurchaseOrders.objects(status="Accept").count()
       purchasedata= "{:,}".format(purchase)
       purchaseinv=PurchaseInvoice.objects().count()
       purchaseinvoice= "{:,}".format(purchaseinv)
       shop = ShopOrders.objects().count()
       shoporders="{:,}".format(shop)
       shopinv = ShopOrderInvoice.objects().count()
       #shop_purchaseorderno=current_user.id
       shopinvoice="{:,}".format(shopinv)
       wh_stock_value=0
       for prod in ProdinvWH.objects(user_id=str(current_user.id)):
           for price in prod.prices:
                wh_stock_value+=int(prod.quantity)*float(price.landing_price)
       #wh_stock_values= "{:,}".format(wh_stock_value)
       final_wh_stock_values=wh_stock_value/100000
       wh_stock_values= format(final_wh_stock_values, '.2f')
       
       wh_sales_value=0
       for prod in ProdinvWH.objects(user_id=str(current_user.id)):
         for price in prod.prices:
            wh_sales_value+=int(prod.outqty)*float(price.dealer_price)
       #wh_sales_values= "{:,}".format(wh_sales_value)
       final_wh_sales_values=wh_sales_value/100000
       wh_sales_values= format(final_wh_sales_values, '.2f')
            
       whstocks=0
       for wh in ProdinvWH.objects(user_id=str(current_user.id)):
         whstocks+=int(wh.quantity)
       whstock="{:,}".format(whstocks)
       return render_template('warehouse-dashboard.html',purchasedata=purchasedata,purchaseinvoice=purchaseinvoice,shoporders=shoporders,
                              shopinvoice=shopinvoice,wh_stock_values=wh_stock_values,wh_sales_values=wh_sales_values,whstock=whstock)  


@app.route('/warehouse', methods = ['GET', 'POST','PUT'])
@login_required
def warehouse():
        with app.app_context():
            form = WHRegistration()
        if request.method == 'POST' and form.validate():
            warehouse_id= request.form['warehouse_id']
            warehouse_name=request.form['warehouse_name']
            warehouse_address=request.form['warehouse_address']
            warehouse_email = request.form['warehouse_email']
            warehouse_phone = request.form['warehouse_phone']
            warehouse_manager=request.form.get('warehouse_manager')
            status=request.form.get('wrhousehide')
            if status=='yes':
                wrhouse = Warehouse.objects.get(warehouse_id=warehouse_id)
                wrhouse.warehouse_name=warehouse_name
                wrhouse.warehouse_address=warehouse_address
                wrhouse.warehouse_manager=warehouse_manager
                wrhouse.save()
            elif status !='yes' :
                iswarehouse=Warehouse.objects(warehouse_name=warehouse_name)
                isUseridExist=Warehouse.objects(warehouse_id=warehouse_id)
                isemail=Warehouse.objects(warehouse_email=warehouse_email)
                isphone=Warehouse.objects(warehouse_phone=warehouse_phone)
                if isUseridExist.count()>0:
                     return render_template('whidexist.html')
                elif isemail.count()>0:
                     return render_template('whemail.html')
                elif isphone.count()>0:
                     return render_template('whphone.html')
                elif iswarehouse.count()>0:
                     return render_template('whwarehouse.html')     
                warehouseUser = Warehouse(user_id=str(current_user.id),warehouse_id=warehouse_id, warehouse_name=warehouse_name, warehouse_address=warehouse_address
                                       ,warehouse_email=warehouse_email, warehouse_phone=warehouse_phone,warehouse_manager=warehouse_manager)# Insert form data in 
                warehouseUser.save()
            return redirect(url_for('warehouse'))
        else:
            if current_user.usertype=='WH-Manager':
                  wh = Warehouse.objects(user_id=str(current_user.id))
            elif  current_user.usertype=='Admin' or  current_user.usertype=='WH-Manager':
                wh = Warehouse.objects()
            logger.info('Created Warehouse manager ')
            return render_template('warehouse-manager-setup.html',wh=wh, form=form)


@app.route('/ware_delete/', methods=['GET', 'POST'])
@login_required
def ware_delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="whouse"):
            quickview1 = Warehouse.objects.get(id=docid)
            quickview1.delete()
        logger.info('Deleted Warehouse manager')
        return redirect(url_for('warehouse'))
   

@app.route('/wh_history')
@login_required
def wh_history():
        if current_user.usertype=='WH-Manager':
           details=ProdinvWH.objects(user_id=str(current_user.id))
           invoicesList =[]
           for document in details:
               for inv in document.invoice_smtlist:
                   data={}
                   data['supplier']=document.supplier
                   data['warehouse']=document.warehouse
                   data['invoiceid']=inv.invoiceid
                   data['invoicedate']=inv.invoicedate
                   inlistFlag = True
                   for inlist in invoicesList:
                      if(inlist['invoiceid']==inv.invoiceid):
                           inlistFlag=False       
                   if inlistFlag:
                       invoicesList.append(data)  
           return render_template('wh-product-inv-history.html',detailslist=invoicesList)
        else:
           details=ProdinvWH.objects()
           invoicesList =[]
           for document in details:
               for inv in document.invoice_smtlist:
                   data={}
                   data['supplier']=document.supplier
                   data['warehouse']=document.warehouse
                   data['invoiceid']=inv.invoiceid
                   data['invoicedate']=inv.invoicedate
                   inlistFlag = True
                   for inlist in invoicesList:
                      if(inlist['invoiceid']==inv.invoiceid):
                           inlistFlag=False     
                   if inlistFlag:
                       invoicesList.append(data)
           return render_template('wh-product-inv-history.html',detailslist=invoicesList)
           
@app.route('/wh_historyviewmore/<invoiceid>')
@login_required
def wh_historyviewmore(invoiceid):

        if current_user.usertype=='WH-Manager':
           values=[]
           for details in ProdinvWH.objects():
               for i in details.invoice_smtlist:
                   if i.invoiceid==invoiceid:
                           data={}
                           fromsmt= i.fromsmt
                           tosmt= i.tosmt
                           start=str(fromsmt[9:15])
                           end=str(tosmt[9:15])
                           qty= int(end)-int(start)
                           smtqty=qty+1
                           data['supplier']=details.supplier
                           data['warehouse']=details.warehouse
                           data['invoiceid']=i.invoiceid
                           data['invoicedate']=i.invoicedate
                           data['hsn']=details.hsn
                           #data['modelno']=details.modelno
                           data['modelno']=details.modelno
                           data['brand']=details.brand
                           data['prod_desc']=details.prod_desc
                           data['quantity']=smtqty
                           #data['outqty']=details.outqty
                           data['fromsmt']=i.fromsmt
                           data['tosmt']=i.tosmt
                           data['barcode']=details.barcode     
                           values.append(data)     
           return render_template('whi-product-inv-viewmore.html',detail=values)
        else:
           details=ProdinvWH.objects()
           logger.info('Entered into Warehouse History Viewmore')
           return render_template('whi-product-inv-viewmore.html',detail=details)
           
@app.route('/wh_barcode', methods=['GET', 'POST'])
def wh_barcode():
    try:
        logger.info('Entered into Warehouse Barecode')
        return render_template('wh-barcode.html')
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')   

@app.route('/wh_barcodeprint', methods=['GET', 'POST'])
def wh_barcodeprint():
    try:
           if request.method == 'POST':
             logger.info('Entered into Warehouse Barecode Print')
             json_data = request.get_json(force=True)
             invoiceid = json_data['invoiceid']
             detail=[]
             wh=ProdinvWH.objects(invoice_smtlist__invoiceid=invoiceid)
             if wh.count()==0:
                 data={}
                 data['barcode']='false'
                 detail.append(data)
                 return jsonify(detail)
             for prodinv in wh:
                 for j in prodinv.invoice_smtlist:
                     if j.invoiceid == invoiceid :
                        data={}
                        fromsmt= j.fromsmt
                        tosmt= j.tosmt
                        start=str(fromsmt[11:15])
                        end=str(tosmt[11:15])
                        qty= int(end)-int(start)
                        smtqty=qty+1
                        data['modelno']=prodinv.modelno                
                        data['quantity']=smtqty
                        data['fromsmtid']= j.fromsmt
                        data['tosmtid']= j.tosmt
                        data['invoiceid']=invoiceid
                        data['barcode']=prodinv.barcode
                        test=ast.literal_eval(json.dumps(data))
                        #value=test.values()                        
                        detail.append(test)                
             return jsonify(detail) 
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')   

@app.route('/smtbarcode/<modelno>', methods = ['GET', 'POST'])
def smtbarcode(modelno):
    try:
        #modelno=reruest.args.get('modelno')
        bartype=ProdinvWH.objects(modelno=modelno)
        bartypes=bartype[0]
        bartypes.status='Print'
        bartypes.save()
        a=[]
        for i in bartype:
            data={}
            data['smtids']= i.smtids
            test=ast.literal_eval(json.dumps(data))
            value=test.values()
            a.append(test)
            b=[]
            for i in value[0]:
                files = os.listdir(os.path.join(app.static_folder, 'barcode'))
                for filename in files:
                    if filename.startswith(i):
                        b.append(filename)
        logger.info('Generated barcodes for SMT ids')
        return render_template('wh -barcodeprint.html',barcodeimg=b)    
    except Exception as e:
       return render_template('error.html',reportsof = 'Exception',msg=str(e))


@app.route('/whpack', methods=['GET', 'POST'])
@login_required
def whpack():
    try:
        logger.info('Entered into Warehouse Packing')
        return render_template('warehouseto-shopproductspacking.html')
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')   

@app.route('/whpackdata', methods=['GET', 'POST'])
def whpackdata():
    try:
        if request.method == 'POST':
             logger.info('Entered into Warehouse Pack Data')
             json_data = request.get_json(force=True)
             invoiceid=json_data['invoice']
             detail=[]
             prodinv=ShopOrderInvoice.objects(shopinvoice_number=invoiceid,status="Approve")
             if prodinv.count()==0:
                 data={}
                 data['warehouse']='false'
                 detail.append(data)
                 return jsonify(detail)
             
             for detailes in prodinv:
                print 'hi'
                for i in detailes.invoice:
                    whdata=ProdinvWH.objects(prod_desc=i.prod_desc)
                    data={}
                    data['warehouse']=detailes.ware_house
                    data['shopname']=detailes.shop_name
                    data['items']=i.items
                    data['model_no']=i.model_no
                    data['brand']=whdata[0].brand
                    data['quantity']=i.quantity
                    item1=int(str(i.quantity))               
                    a=whdata[0].smtids
                    qty=int(str(whdata[0].quantity))
                    if range(qty)>= range(item1):
                        smt=[]
                        for j in range(item1):
                            smt.append(a[j])
                            data['smtids']= smt
                        test=ast.literal_eval(json.dumps(data))
                        detail.append(test)
                    
                    else :
                        data={}
                        data['warehouse']='fail'
                        data['modelname']=i.model_no
                        detail.append(data)
       
             return jsonify(detail)     
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')

        
@app.route('/whpackpost',methods = ['GET', 'POST'])
def whpackpost():
    pool = Pool()
    pool_new(pool)
    try:
     if request.method == 'POST':
       json_data = request.get_json(force=True)       
       ware_house = json_data['ware_house']
       shop_name = json_data['shop_name']
       invoice = json_data['invoice']
       po_date = json_data['po_date']
       receiptno = json_data['receiptNo']
       shippingdetail = json_data['shippingDetail']
       remarks = json_data['remarksId']
       shopship = ProdInvShipping(warehouse=ware_house,shop=shop_name,invoice=invoice,startdate=po_date,receiptid=receiptno,shippingdetails=shippingdetail,remarks=remarks)
       shopship.save()
       logger.info('Entered into Warehouse Packpost')
       for i in json_data['items']:
            items = i['item']            
            model=i['item_model']
            brand = i['item_brand']
            smtid = i['item_smtid']    
            qty = i['item_quntity']
            s=smtid.split(',')
            ids=[]
            for j in s:
                ids.append(j)
            ships = ShipData(items,model,brand,ids,qty)
            shopship.orderslist.append(ships)
            shopship.save()
            whdatas=ProdinvWH.objects(modelno=model,brand=brand)
            whdata=whdatas[0]
            whqty= int(str(whdata.outqty))
            inwhqty=int(str(whdata.quantity))
            shopqty=int(qty)
            totalqty = whqty+shopqty
            whdata.outqty=str(totalqty)
            quantity=inwhqty-shopqty
            whdata.quantity=str(quantity)            
            for k in s:
                whdata.smtids.remove(k)
            whdata.save()
       prodinv=ShopOrderInvoice.objects(shopinvoice_number=invoice)
       user=UserSignup.objects(usertype='Accountant')
       user1=UserSignup.objects(usertype='Market Manager')
       usermail=UserSignup.objects(userid=prodinv[0].dealer_id)
       emailList=[]
       emailList.append(user[0].email)
       emailList.append(usermail[0].email)
       emailList.append(user1[0].email)
       fo = open("./static/mailtemp/whmailtemp.html", "r+")
       htmlbody = fo.read()
       fo.close()
       urldata='Your order '+ invoice+ " is packed and ready for shipping through " + shippingdetail+'.'
       htmlbody = htmlbody.replace("$$urldata$$",urldata)
       #htmlbody = '<html><body><table><tr><td>Dear user your order '+ invoice+ " is packed and ready for shipping via Vehicle " + shippingdetail +'</td></tr></body></html>'
       #sendMail(emailList,'packing the products',htmlbody)
       pool.apply_async(sendMail,[emailList,'Packing products in progress',htmlbody])
       msg="Your order "+ invoice +"is packed and ready for shipping through " +" "+ shippingdetail+'.'
       mobileList=[]
       mobileList.append('91'+usermail[0].mobile)
       mobileList.append('91'+user[0].mobile)
       mobileList.append('91'+user1[0].mobile)
       #SMS(msg,mobileList)
       pool.apply_async(SMS,[msg,mobileList])
       shopinvoice=ShopOrderInvoice.objects.get(shopinvoice_number=invoice)
       shopinvoice.status = 'Shipping'
       shopinvoice.save()
       
       shoporder=ShopOrders.objects.get(shop_purchaseorderno=shopinvoice.shop_purchaseorderno)
       shoporder.status='Shipping'
       shoporder.save()
       return 'Success'                     
    except Exception as e:
        return render_template('error.html',reportsof = 'Exception',msg=str(e)) 


@app.route('/wh_data', methods=['GET', 'POST'])
@login_required
def wh_data():
    try:
        if current_user.usertype=='WH-Manager':
           logger.info('Warehouse Manager Entered into Warehouse Data')
           sup=UserSignup.objects(status='Active',usertype='Supplier')
           warehouselist = Warehouse.objects(user_id=str(current_user.id))
           #print sup[0].username
           if  warehouselist.count()==0:
              return render_template('wh-nodta.html')
           return render_template('wh-product-inv-entry.html',sup=sup,warehouselist=warehouselist[0].warehouse_name)
        else:
           sup=UserSignup.objects(status='Active',usertype='Supplier')
           logger.info('Entered into Warehouse Data')
           warehouselist = Warehouse.objects(user_id=str(current_user.id))
           if  warehouselist.count()==0:
               return render_template('wh-nodta.html')
           return render_template('wh-product-inv-entry.html',sup=sup,warehouselist=warehouselist[0].warehouse_name)     
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')   

@app.route('/wh_invoice', methods=['GET', 'POST'])
@login_required
def wh_invoice():
    try:
        inv=request.args.get('invname')
        invoice=PurchaseInvoice.objects.get(invoice_no=inv)
        invdate=invoice.invoice_date
        return jsonify(invdate)
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')


@app.route('/wh_invoice_get', methods=['GET', 'POST'])
@login_required
def wh_invoice_get():
    try:
        json_data = request.get_json(force=True)
        invno = json_data['invoice']
        supid = json_data['supplier']
        #print supid,"su"
        #print current_user.id 
        invdate = json_data['invoicedate']
        #print invdate
        sups=Sup_Upload.objects(user_id=supid)
        #print sup[0].user_id
        detailslist=[]
        if sups:
            order=invno.replace('POIN','PO')
            total_qty=0
            invinfo=PurchaseInvoice.objects(invoice_no=invno,invoice_date=invdate)
            #print invinfo
            #purchase=PurchaseOrders.objects(purchaseOrder_no=order,po_date=invdate)
            if invinfo.count()>0:      
             if invinfo[0].supplier_id==sups[0].user_id:
              for inv in PurchaseOrders.objects(purchaseOrder_no=invinfo[0].purchaseOrder_no):
                for detail in inv.orderslist:
                    sup=Sup_Upload.objects(upload_name=detail.name)
                    data={}
                    data['hsn']=detail.hsn
                    data['model']=detail.model_no
                    data['brand']=sup[0].upload_brand
                    data['productname']=detail.name
                    data['quantity']=detail.quantity
                    total_qty+=int(detail.quantity)
                    detailslist.append(data)                   
            else:
                data={}
                data['invoice']="fail"
                detailslist.append(data)
            return jsonify(detailslist)
        else:
          return 'error'
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')   


@app.route('/wh_remarks_post', methods=['GET', 'POST'])
@login_required
def wh_remarks_post():
    pool = Pool()
    pool_new(pool)
    try:      
      if request.method == 'POST':
       json_data = request.get_json(force=True)
       supplierid = json_data['supplier']
       invoice = json_data['invoice']
       purchaseorderno=json_data['poid']
       ware_house = json_data['warehouse']
       invoicedate = json_data['invoicedate']
       purchaseorderdate = json_data['podate']
       remarks = json_data['remarks']
       #return remarks
       user=UserSignup.objects(usertype='Purchase-Manager')
       #user=UserSignup.objects(usertype='Admin')
       user1=UserSignup.objects(usertype='Market Manager')
       usermail=UserSignup.objects.get(id=supplierid)
       emailList=[]
       emailList.append(user[0].email)
       #emailList.append(usermail.email)
       emailList.append(user1[0].email)
       fo = open("./static/mailtemp/whremarktemp.html", "r+")
       htmlbody = fo.read()
       fo.close()
       supplier=usermail.username
       htmlbody = htmlbody.replace("$$invoice$$",invoice)
       htmlbody = htmlbody.replace("$$supplier$$",supplier)
       htmlbody = htmlbody.replace("$$ware_house$$",ware_house)
       htmlbody = htmlbody.replace("$$invoicedate$$",invoicedate)
       htmlbody = htmlbody.replace("$$remarks$$",remarks)
       #sendMail(emailList,'Remarks the products from WH',htmlbody)
       pool.apply_async(sendMail,[emailList,'Remarks for the purchase from warehouse for order '+ str(invoice),htmlbody])
       return 'Success'
    except Exception as e:
        return jsonify('{"mesg":' + str +'}')

       
@app.route('/whdata_post', methods=['GET', 'POST'])
@login_required
def whdata_post():
    pool = Pool()
    pool_new(pool)
    try:
      if request.method == 'POST':
       json_data = request.get_json(force=True)
       supplierid = json_data['supplier']
       invoice = json_data['invoice']
       purchaseorderno=json_data['poorder']
       ware_house = json_data['ware_house']
       invoicedate = json_data['invoiceDate']
       purchaseorderdate = json_data['poDate']
       total_quantity = json_data['total_quantity']
       if  supplierid == '0' or invoice == '0' or invoicedate =='0' or total_quantity == '0':
           return redirect(url_for('wh_data'))
       totalqty=''
       data=[]
       for i in json_data['products']:
             item_hsn = i['item_hsn']
             item_model = i['item_model']
             item_brand=i['item_brand']
             item_productDesc = i['item_productDesc']
             item_quntity = i['item_quntity']
             item1=int((str(item_quntity)))
             data.append(str(item_model))
             data.append(str(item_brand))
             data.append(str(item_productDesc))
             data.append(str(item_quntity))
             numbers=[]
             for i in range(item1):
                 smtnumber =  SMTIdNumber().get()
                 SMTIdNumber().put(smtnumber)
                 numbers.append(smtnumber)
             data.append(str(numbers))
             smtpnumbers=str(numbers)
             fromsmt=numbers[0]
             tosmt=numbers[-1]
             prodinvobj1=ProdinvWH.objects(supplier=supplierid,warehouse=ware_house,brand=item_brand,prod_desc=item_productDesc)
             print prodinvobj1.count()
             sup=Sup_Upload.objects(upload_name=item_productDesc,upload_brand=item_brand)
             if prodinvobj1.count()==0:
                   print 'insert'+item_model
                   prodinvobj=ProdinvWH(user_id=str(current_user.id),supplier=supplierid,warehouse=ware_house,hsn=item_hsn,modelno=item_model,brand=item_brand,prod_desc=item_productDesc,smtids=numbers,
                                        quantity=item_quntity,outqty='0',barcode=sup[0].upload_id)
                   
                   inv=InvoiceList(invoiceid=invoice,fromsmt=fromsmt,tosmt=tosmt,invoicedate=invoicedate)
                   prodinvobj.invoice_smtlist.append(inv)
                   prodinv0WH = ProdinvWH.objects(supplier=supplierid,modelno=item_model,brand=item_brand,prod_desc=item_productDesc)
                   if  prodinv0WH.count()==0:	
                       sup_data=Sup_Upload.objects(upload_name=item_productDesc,upload_brand=item_brand)
                       price = PriceList(landing_price=sup_data[0].prices[0].landing_price, dealer_price=sup_data[0].prices[0].dealer_price,offer_price=sup_data[0].prices[0].offer_price,enduser_price=sup_data[0].prices[0].enduser_price,bulk_unit_price=sup_data[0].prices[0].bulk_unit_price,bulk_qty=sup_data[0].prices[0].bulk_qty,landing_price_gst=sup_data[0].prices[0].landing_price_gst, dealer_price_gst=sup_data[0].prices[0].dealer_price_gst,offer_price_gst=sup_data[0].prices[0].offer_price_gst,enduser_price_gst=sup_data[0].prices[0].enduser_price_gst)  
                       prodinvobj.prices.append(price)		
                       prodinvobj.save()
                   else:
                       if prodinv0WH[0].warehouse=="Default":
                           #print 'default'
                           price = PriceList(landing_price=prodinv0WH[0].prices[0].landing_price, dealer_price=prodinv0WH[0].prices[0].dealer_price,offer_price=prodinv0WH[0].prices[0].offer_price,enduser_price=prodinv0WH[0].prices[0].enduser_price,bulk_unit_price=prodinv0WH[0].prices[0].bulk_unit_price,bulk_qty=prodinv0WH[0].prices[0].bulk_qty,landing_price_gst=prodinv0WH[0].prices[0].landing_price_gst, dealer_price_gst=prodinv0WH[0].prices[0].dealer_price_gst,offer_price_gst=prodinv0WH[0].prices[0].offer_price_gst,enduser_price_gst=prodinv0WH[0].prices[0].enduser_price_gst)  
                           prodinvobj.prices.append(price)		
                           prodinvobj.save()                        
                           whdelete = ProdinvWH.objects(warehouse="Default",prod_desc=item_productDesc)
                           whdelete.delete()
                       else:
                           sup_data=Sup_Upload.objects(upload_name=item_productDesc,upload_brand=item_brand)
                           #print'sup'
                           price = PriceList(landing_price=sup_data[0].prices[0].landing_price, dealer_price=sup_data[0].prices[0].dealer_price,offer_price=sup_data[0].prices[0].offer_price,enduser_price=sup_data[0].prices[0].enduser_price,bulk_unit_price=sup_data[0].prices[0].bulk_unit_price,bulk_qty=sup_data[0].prices[0].bulk_qty,landing_price_gst=sup_data[0].prices[0].landing_price_gst, dealer_price_gst=sup_data[0].prices[0].dealer_price_gst,offer_price_gst=sup_data[0].prices[0].offer_price_gst,enduser_price_gst=sup_data[0].prices[0].enduser_price_gst)  
                           prodinvobj.prices.append(price)		
                           prodinvobj.save()
                       
                   
                       
                   
             else:
                  #prodinv=ProdinvWH.objects(modelno=item_model,warehouse=ware_house,supplier=supplierid)
                  print 'update'+item_model
                  prodinvobject=prodinvobj1[0]
                  smt=[]
                  for i in prodinvobject.smtids:
                      smt.append(i)
                  smtid=smt+numbers
                  fromsmt=numbers[0]
                  tosmt=numbers[-1]
                  qty= int(str(prodinvobject.quantity))
                  totalqty = str(qty+item1)
                  inv=InvoiceList(invoiceid=invoice,fromsmt=fromsmt,tosmt=tosmt,invoicedate=invoicedate)
                  prodinvobject.invoice_smtlist.append(inv)                   
                  prodinvobject.smtids=smtid                 
                  prodinvobject.quantity=totalqty
                  prodinvobject.save()
       quantity=totalqty
       user=UserSignup.objects(usertype='Admin')
       user1=UserSignup.objects(usertype='Accountant')
       user2=UserSignup.objects(usertype='Market Manager')
       emailList=[]
       emailList.append(user1[0].email)
       emailList.append(user[0].email)
       emailList.append(user2[0].email)
       fo = open("./static/mailtemp/whmailtemp.html", "r+")
       htmlbody = fo.read()
       fo.close()
       urldata=quantity +"products were received at warehouse "+ware_house+" with invoice"+invoice +"of "+item_brand+"need to be updated with prices."
       htmlbody = htmlbody.replace("$$urldata$$",urldata)
       #sendMail(emailList,'Products are arrived @ '+ ware_house,htmlbody) 
       pool.apply_async(sendMail,[emailList,'Products arrived at '+ware_house,htmlbody])
       msg=quantity +"products were received at warehouse "+ware_house+" with invoice"+invoice +"of "+item_brand+"need to be updated with prices."
       mobileList=[]
       mobileList.append('91'+user[0].mobile)
       mobileList.append('91'+user1[0].mobile)
       mobileList.append('91'+user2[0].mobile)
       #SMS(msg,mobileList)
       pool.apply_async(SMS,[msg,mobileList])
       logger.info('Entered into Warehouse Data Post') 
       return 'Success'
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')

@app.route('/whhsn_post', methods=['GET', 'POST'])
@login_required
def whhsn_post():
    try:
        supid=request.args.get('supId')
        hsn=request.args.get('hsn')
        logger.info('Entered into Warehouse HSN Post')   
        if supid:
            hsn=[]
            for products in Sup_Upload.objects(user_id=supid,status='Accept'):
                hsn.append(products.upload_hsncode)
            sub=sorted(set(hsn))    
        elif hsn:
            model=[]
            for products in Sup_Upload.objects(upload_hsncode=hsn,status='Accept'):
                model.append(products.upload_modelno)
            sub=sorted(set(model)) 
        return jsonify(sub)  
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')    


@app.route('/whbrand_post/', methods=['GET', 'POST'])
@login_required
def whbrand_post():
    try:
        hsn=request.args.get('hsn')
        modelNo=request.args.get('modelNo')
        logger.info('Entered into Warehouse Brand Post')   
        brand=[]
        for products in Sup_Upload.objects(upload_hsncode=hsn,upload_modelno=modelNo,status='Accept'):
            brand.append(products.upload_brand)
        sub=sorted(set(brand))
        return jsonify(sub)  
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')    

@app.route('/whproduct_post/', methods=['GET', 'POST'])
@login_required
def whproduct_post():
    try:
        hsn=request.args.get('hsn')
        modelNo=request.args.get('modelNo')
        brand=request.args.get('brand')
        logger.info('Entered into Warehouse Product Post')   
        if hsn=='0' or modelNo =='0' or brand =='0':
            return 'no data available'
        product=Sup_Upload.objects(upload_hsncode=hsn,upload_modelno=modelNo,upload_brand=brand,status='Accept')
        return product[0].upload_name   
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')    

#-----------------------------------------more info-------------------------------
@app.route('/header_setup', methods = ['GET', 'POST'])
@login_required
def header_setup():
        with app.app_context():
         form = HeaderForm()
        if request.method == 'POST' and form.validate():
            companyname = request.form['companyname']
            address=request.form['address']
            companylogo= request.files['companylogo']
            contactno=request.form['contactno']
            companylogo.save(os.path.join(app.config['UPLOAD_LOGO'], companylogo.filename))
            headeinfo =Header_Setup(user_id=str(current_user.id),companyname=companyname, address=address,companylogo=companylogo.filename,contactno=contactno) 
            headeinfo.save()
            return redirect(url_for('header_setup'))
        else:
            Headerlist = Header_Setup.objects()
            logger.info('Sucessfully setup header')
            return render_template('headerinfo.html',form=form,Headerlist=Headerlist)
            

@app.route('/headersetup_delete/', methods=['GET', 'POST'])
@login_required
def headersetup_delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="head"):
            header_info = Header_Setup.objects.get(id=docid)
            header_info.delete()
        logger.info('Deleted header in header setup')
        return redirect(url_for('header_setup'))

@app.route('/company_setup', methods = ['GET', 'POST'])
@login_required
def company_setup():
        with app.app_context():
         form = CompanyForm()
        if request.method == 'POST':
            companyname = request.form['companyname']
            address=request.form['address']
            pan = request.form['pan']
            gstin=request.form['gstin']
            cin=request.form['cin']
            state=request.form.get('state')
            a= str(state.split("-")[0])
            statecode=request.form['statecode']
            status=request.form.get('billhide')
            if status=='yes':
                billinfo = Company_Setup.objects.get(companyname=companyname)
                billinfo.address=address
                billinfo.pan=pan
                billinfo.gstin=gstin
                billinfo.cin=cin
                billinfo.state=state
                billinfo.statecode=statecode
                billinfo.save()
                return redirect(url_for('company_setup'))
            elif status !='yes':
                companyinfo =Company_Setup(user_id=str(current_user.id),companyname=companyname, address=address , pan=pan , gstin=gstin,cin=cin,state=a,statecode=statecode) 
                companyinfo.save()
                logger.info('Created Company in Company Setup')
                return redirect(url_for('company_setup'))
        else:
           Companylist = Company_Setup.objects()
           return render_template('company-setup.html',form=form,Companylist=Companylist)
    
@app.route('/companysetup_delete/', methods=['GET', 'POST'])
@login_required
def companysetup_delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="company"):
            company_info = Company_Setup.objects.get(id=docid)
            company_info.delete()
        logger.info('Deleted Company in Company Setup')
        return redirect(url_for('company_setup'))
    

@app.route('/billing_setup', methods = ['GET', 'POST'])
@login_required
def billing_setup():
        with app.app_context():
         form = BillingForm()
        if request.method == 'POST':
            companyname = request.form['companyname']
            address=request.form['address']
            pan = request.form['pan']
            gstin=request.form['gstin']
            cin=request.form['cin']
            state=request.form.get('state')
            b= str(state.split("-")[0])
            statecode=request.form['statecode']
            companylogo= request.files['companylogo']
            contactno=request.form['contactno']
            companylogo.save(os.path.join(app.config['UPLOAD_LOGO'], companylogo.filename))
            billinginfo =Billing_Setup(user_id=str(current_user.id),companyname=companyname, address=address , pan=pan , gstin=gstin,cin=cin,state=b,statecode=statecode,companylogo=companylogo.filename,contactno=contactno) 
            billinginfo.save()
            logger.info('Created Billing in Billing Setup')
            return redirect(url_for('billing_setup'))
        else:
            Billinglist = Billing_Setup.objects()
            logger.info('Entered into billing setup')
            return render_template('billing-setup.html',form=form,Billinglist=Billinglist)
            

@app.route('/billingsetup_delete/', methods=['GET', 'POST'])
@login_required
def billingsetup_delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="billing"):
            billing_info = Billing_Setup.objects.get(id=docid)
            billing_info.delete()
        logger.info('Deleted Billing in Billing Setup')
        return redirect(url_for('billing_setup'))
        

@app.route('/tax_discount', methods = ['GET', 'POST'])
@login_required
def tax_discount():
        with app.app_context():
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
        taxlist = Supplier_Tax.objects()
        discountlist = Supplier_Discount.objects()              
        return render_template('tax-discount-configuration.html',form1=form1,form2=form2,taxlist=taxlist,discountlist=discountlist)

@app.route('/tax_discountt_delete/', methods=['GET', 'POST'])
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
 
@app.route('/bank_configuration', methods = ['GET', 'POST'])
@login_required
def bank_configuration():
        with app.app_context():
         form = BankForm()
        if request.method == 'POST':
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
               company=Reg_Dealer.objects()
               form.ac_holdername.data = company[0].dealer_shopname   
            else:
               bankdetailes = Bank_Setup.objects(user_id=str(current_user.id))
            return render_template('bank-configuration.html',form=form,bankdetailes=bankdetailes)

@app.route('/bankdelete/', methods=['GET', 'POST'])
@login_required
def bankdelete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="bank"):
            bankinfo=Bank_Setup.objects.get(id=docid)
            bankinfo.delete()
        logger.info('Deleted Bank Deatils')
        return redirect(url_for('bank_configuration'))

#---------------------------- Dealer Dashbord-------------------------------
@app.route('/shophistory', methods = ['GET', 'POST','PUT'])
@login_required
def shophistory():
        shop=[]
        for i in ProdInvShop.objects(user_id=str(current_user.id)):
          for j in i.price:              
            data={}
            data['supplier']=i.supplier
            data['warehouse']=i.warehouse
            data['shop']=i.shop
            data['category']=i.category
            data['subcategory']=i.subcategory
            data['brand']=i.brand
            data['model']=i.model
            data['barcode']=i.barcode                       
            data['inqty']=i.inqty
            data['outqty']=i.outqty
            data['avlsmtid']=', '.join(i.avlsmtid)
            data['dealer_price']=j.dealer_price
            data['enduser_price']=j.enduser_price
            data['status']=i.status
            test=ast.literal_eval(json.dumps(data))
            shop.append(test)
        logger.info('Entered into shophistory')
        return render_template('shophistory.html',shop=shop)

@app.route('/shopuser', methods = ['GET', 'POST','PUT'])
@login_required
def shopuser():
    user=ShopUser.objects()
    return render_template('shopuser.html',user=user)

@app.route('/shopuserdelete/', methods=['GET'])
@login_required
def shopuserdelete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="shopuser"):
            quickview = ShopUser.objects.get(id=docid)
            quickview.delete()
        return redirect(url_for('shopuser'))


@app.route('/shopsetup', methods = ['GET', 'POST'])
@login_required
def shopsetup():
    shop = Shopsetup.objects()
    return render_template('shop-setup.html',shop=shop)

    
@app.route('/shopsetup_delete/', methods=['GET'])
@login_required
def shopsetup_delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="setup"):
            quickview = Shopsetup.objects.get(id=docid)
            quickview.delete()
        return redirect(url_for('shopsetup'))


@app.route('/shoporderinvoice',methods=['GET'])
@login_required
def shoporderinvoice():
        shop=[]
        for i in ShopOrders.objects(status__ne= 'Pending').order_by("-id"):
                 shop.append(i)
        return render_template('shoporder-inv.html',shop=shop)
   
@app.route('/shoporderlist',methods=['GET'])
@login_required
def shoporderlist():
        if current_user.usertype=='Admin' or current_user.usertype=='Accountant'  or current_user.usertype=='WH-Manager'  or current_user.usertype=='Market Manager':
            shop=ShopOrders.objects().order_by('-id')
            return render_template('shop-orderlist.html',shop=shop)
        else:
            if current_user.usertype=='Distributor/Dealer':
                shop=ShopOrders.objects(user_id==str(current_user.id)).order_by('-id')  
                return render_template('shop-orderlist.html',shop=shop)


@app.route('/shoporderviewmore/<id>',methods = ['GET', 'POST'])
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
            header=Header.objects()
            logo=header[0].headerlogo
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
                        elif request.form.get('submit') == 'Edit':
                               return render_template('shoporder-qty-edit.html',detailes=detailes,billing=billing[0],company=company[0],logo=logo,warehouse=warehouse[0],qty=whdata,regdealer=regdealer[0])  
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

@app.route('/shoporderviewmorepost',methods = ['GET', 'POST'])
@login_required
def shoporderviewmorepost():
            json_data = request.get_json(force=True)
            warehouse_name = json_data['ware_house']
            shop_name = json_data['shop_name']
            shop_id=json_data['shop_id']
            shop_address = json_data['shop_address']
            dealer_id = json_data['dealer_id']
            shop_po = json_data['shop_po']
            po_date = json_data['po_date']
            total_value = json_data['total_value']
            order_edit_by = current_user.username
            order_edited_date=json_data['currentdate']
            qtyval=0
            for i in json_data['items']:
                item = i['item']
                brand=i['brand']
                item_hsn = i['item_hsn']
                item_model=i['item_model']
                item_quntity=i['item_quntity']
                item_price = i['item_price']
                item_value = i['item_value']
                qtyval=qtyval+int(item_quntity)
                
                data=ShopOrders.objects.get(shop_purchaseorderno=shop_po)
                data.totalvalue=total_value
                data.order_edit_by=order_edit_by
                data.order_edited_date=order_edited_date
                data.status="Edited"
                data.totalqty=str(qtyval)
                data.save()
                
                for price in data.orderslist:
                    if price.supplier==brand and price.model_no==item_model:
                        #return item_quntity
                        price.quantity=item_quntity
                        price.value=item_value
                        price.save()
                        
            shopuser=ShopOrders.objects(dealer_id=dealer_id)         
            User=UserSignup.objects(userid=shopuser[0].dealer_id)
            emailList=[]
            emailList.append(User[0].email)
            fo = open("./static/mailtemp/marketingmailtemp.html", "r+")
            htmlbody = fo.read()
            fo.close()
            urldata='This order with no '+ shop_po +' is modified with quantity .Login to Accept or Reject to confirm the order.'
            htmlbody = htmlbody.replace("$$urldata$$",urldata)
            sendMail(emailList,'Order modified',htmlbody)
            #pool.apply_async(sendMail,[emailList,'Accounts Manger will raise an Invoice for the approved orders',htmlbody])
            msg='This order with no '+ shop_po +' is modified with quantity'
            mobileList=[]
            mobileList.append('91'+User[0].mobile)    
            return "Success"
        


@app.route('/whqty',methods = ['GET', 'POST'])
@login_required
def whqty():
    try:
        wh =request.args.get('selectedValue')
        supplier =request.args.get('supplier')
        item_hsn =request.args.get('item_hsn')
        item_model =request.args.get('item_model')
        item_qty =request.args.get('item_qty')
        item =request.args.get('item')
        item_price =request.args.get('item_price')
        item_value =request.args.get('item_value')
        qty=[]
        for i in ProdinvWH.objects(supplier=supplier,hsn=item_hsn,modelno=item_model):
            data={}
            data['item']=item
            data['supplier']=i.supplier
            data['hsn']=i.hsn
            data['modelno']=i.modelno            
            data['warehouse']=i.warehouse
            data['avl_quantity']=i.quantity
            data['qty']=item_qty
            data['item_price']=item_price
            data['item_value']=item_value
            test=json.loads(json.dumps(data))
            qty.append(test)
        return jsonify(qty)       
    except Exception as e:
        return render_template('error.html',reportsof = 'Exception',msg=str(e)) 
        
@app.route('/whqty_post',methods = ['GET', 'POST'])
def whqty_post():
    try:
     if request.method == 'POST':
       json_data = request.get_json(force=True)
       warehouse_name = json_data['warehouse']
       shop_purchageno = json_data['shop_purchageno']
       for i in json_data['whitems']:
            item = i['item']
            supplier=i['supplier']
            hsn = i['item_hsn']
            model_no = i['item_model']
            quantity = i['item_quntity']
            avl_quantity = i['item_avlquntity']
            netprice = i['item_price']
            value = i['item_value']
       data = ShopOrders.objects.get(shop_purchaseorderno=shop_purchageno)
       #print data.status
       data.status = 'Accept'  
       data.warehouse_name=warehouse_name
       data.save()
       return 'Success'
    except Exception as e:
        return render_template('error.html',reportsof = 'Exception',msg=str(e)) 


@app.route('/shoporder_delete', methods=['GET'])
@login_required
def shoporder_delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="em"):
            quickview = ShopOrders.objects.get(id=docid)
            quickview.delete()
        return redirect(url_for('shoporderlist'))

@app.route('/shop_invoice/<id>', methods = ['GET'])
@login_required
def shop_invoice(id):
        sum=0
        orders=ShopOrders.objects(id=id)
        orderdata=[]
        item=0
        totalitems=[]
        for detailes in orders :
           for i in detailes.orderslist:
            if i.quantity !='0':
                totalitems.append(i.quantity)
                item += 1
                var=str(item)
                spoinvoice=detailes.shop_purchaseorderno.replace('SPO','SPOIN')
                supvalues = Sup_Upload.objects(upload_modelno=i.model_no,upload_brand=i.supplier)
                #print supvalues
                if supvalues.count()==0:
                        return render_template('supinv.html')
                data={}
                data['warehouse_name']=detailes.warehouse_name
                data['shop_name']=detailes.shop_name
                data['shop_id']=detailes.shop_id
                data['dealer_id']=detailes.dealer_id
                data['shop_purchaseorderno']=detailes.shop_purchaseorderno
                #data['totalitems']=detailes.totalitems
                data['totalqty']=detailes.totalqty
                data['totalvalue']=detailes.totalvalue                       
                data['items']=var
                data['hsn']=i.hsn
                data['model_no']=i.model_no
                data['quantity']=i.quantity
                data['netprice']=i.netprice             
                qty=int(i.quantity)
                price=supvalues[0].prices[0].dealer_price_gst
                #print type(price),"price"
                finalvalue=format(price, '.2f')
                #print type(finalvalue)
                taxv=float(finalvalue)*qty
                taxvalue=format(taxv, '.2f')
                #print taxvalue
                data['value']=taxvalue
                sum=sum+float(taxvalue)
                #print totalsum
                data['upload_name']=supvalues[0].upload_name
                data['upload_mrp']=supvalues[0].upload_mrp
                data['upload_tax']=supvalues[0].upload_tax
                tvalue=float(detailes.totalvalue)
                orderdata.append(data)
        totalval=format(sum, '.2f')
        return render_template('shoporder-invoice.html',detailes=orderdata,totalval=totalval,spoinvoice=spoinvoice,totalitems=len(totalitems))    

@app.route('/shopinvoice_post', methods = ['GET', 'POST'])
@login_required
def shopinvoice_post():
    pool = Pool()
    pool_new(pool)
    try:
        #return 'hi'
        if request.method == 'POST':
           json_data = request.get_json(force=True)
           ware_house= json_data['ware_house']
           shop_name=json_data['shop_name']
           shop_id=json_data['shop_id']
           dealer_id = json_data['shopdealer_id']
           shop_po = json_data['shoppurchaseOrder_no']
           shopinvoice_no = json_data['shopinvoice_number']
           invoice_date = json_data['shopinvoice_date']
           expected_date=json_data['expected_date']  
           total_items= json_data['total_items']
           total_quantity = json_data['total_quantity']
           total_value = json_data['total_value']
           invoicenum=ShopOrderInvoice.objects(shopinvoice_number=shopinvoice_no)
           if invoicenum.count()>0:
                 return 'Invoice Already Existed'
           shopinvoiceinfo = ShopOrderInvoice(user_id=str(current_user.id),ware_house=ware_house,shop_name=shop_name,shop_id=shop_id,
                                         dealer_id=dealer_id,shop_purchaseorderno=shop_po,shopinvoice_number=shopinvoice_no,invoice_date=invoice_date,
                                        expected_date =expected_date,total_items=total_items,total_quantity=total_quantity,total_value=total_value)
           #shopinvoiceinfo.save()    
           for i in json_data['items']:
            item = i['item']
            hsn = i['item_hsn']
            prod_desc = i['item_proDesc']
            model_no = i['item_model']
            quantity = i['item_quntity']
            mrp  = i['item_mrp']
            netprice = i['item_netPrice']
            tax  = i['item_tax']
            value = i['item_value']
            invoice = ShopInvoice(item,hsn,prod_desc,model_no,quantity,mrp,netprice,tax,value)
            shopinvoiceinfo.invoice.append(invoice)
            #shopinvoiceinfo.save()
           for j in json_data['othercharges']:
                   charge_name = j['charge_name']
                   charge_value = j['charge_value']
                   charges = ShopCharges(charge_name, charge_value)
                   shopinvoiceinfo.othercharges.append(charges)
           shopinvoiceinfo.save()
           data = ShopOrders.objects.get(shop_purchaseorderno=shop_po)
           data.status = 'Approve'
           data.save()
           shopuser=ShopOrderInvoice.objects(dealer_id=dealer_id)         
           User=UserSignup.objects(userid=shopuser[0].dealer_id)
           user=UserSignup.objects(usertype='WH-Manager')
           user1=UserSignup.objects(usertype='Accountant')

           emailList=[]
           emailList.append(User[0].email)
           emailList.append(user[0].email)
           emailList.append(user1[0].email)
           if shopuser.count() > 0:
               fo = open("./static/mailtemp/accountmailtemp.html", "r+")
               htmlbody = fo.read()
               fo.close()
               urldata='Your order '+ shop_po +' was accepted and invoice is generated INV '+ shopinvoice_no +' kindly make payments if any.'
               htmlbody = htmlbody.replace("$$urldata$$",urldata)
               #sendMail(emailList,'Invoice generated',htmlbody)
               pool.apply_async(sendMail,[emailList,'Accounts Manger will raise an Invoice for the approved orders',htmlbody])
               msg='Your order '+ shop_po +' was accepted and invoice is generated INV '+ shopinvoice_no +' kindly make payments if any.'
               mobileList=[]
               mobileList.append('91'+User[0].mobile)
               mobileList.append('91'+user[0].mobile)
               mobileList.append('91'+user1[0].mobile)
               #SMS(msg,mobileList)
               pool.apply_async(SMS,[msg,mobileList])
           return 'Success'        
                    
    except Exception as e:
       return jsonify('{"mesg":' + str(e) +'}')

#-----------------------------------Forgot Password--------------------------------------->
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
        pool = Pool()
        pool_new(pool)
        with app.app_context():
                form = ForgotPassword()
        if request.method == 'POST' and form.validate():
          email = request.form['email']
          registeredUser = UserSignup.objects(email=email)
          urldata=''
          if registeredUser.count() > 0:
              ts = int(round(time.time() * 1000))
              userid = registeredUser[0].id
              urldata = str(ts)+':'+str(userid)
              restlint = "<a href="+app.config['Mainurl']+'passwordreset/'+urldata+" style='background-color: #068693; color: #ffffff; padding: 10px;text-decoration:none;'>Reset Password</a>"
              fo = open("./static/mailtemp/forgotmailtemp.html", "r+")
              htmlbody = fo.read()
              fo.close()
              urldata='Dear '+registeredUser[0].username+',<br> We received a request to reset the password for your account.If you have made the request,please click on the following button.<br> This link will be expire in 2hrs.</td></tr><tr><td><br><br>'+restlint+'<br><br><br>In case the above link does not work, please copy and paste the link in your browser.<br>If you did not raise the request, please ignore the email.'
              htmlbody = htmlbody.replace("$$urldata$$",urldata)
              #sendMail(email,'Reset your ShopMyTools account password',htmlbody)
              pool.apply_async(sendMail,[email,'reset password',htmlbody])
              logger.info('Sent mail to reset the password')
              return render_template('error.html',form=form,reportsof = 'Reset Password',msg="Thank you, <br> Please check your Email and click on the link to reset password.<br>Link will be expired in 2hrs.",userinfo=current_user)
          else:
              logger.info('Failed to send mail because Email not available with us!')
              form.email.errors.append("This email Id is not registered with us")
              return render_template('forgot-password.html',form=form,reportsof = 'Reset Password')
        else:
            logger.info('Entered into forgot  password')
            return render_template('forgot-password.html',form=form,reportsof = 'Reset Password',userinfo=current_user)

@app.route('/passwordreset/<urldata>', methods=['GET', 'POST'])
def passwordreset(urldata):
        with app.app_context():
                form = ResetPassword()
        if request.method == 'POST' and form.validate():
          password = request.form['password']
          userid = request.form['userid']
          registeredUser = UserSignup.objects.get(id=userid)
          registeredUser.password=generate_password_hash(password)
          registeredUser.save()
          logger.info('Your Password reset done successfully!')
          return render_template('error.html',form=form,reportsof = 'Reset Password Success',msg="Your Password reset done successfully!",userinfo=current_user)
        else:
            data = urldata.split(':')
            pts = int(data[0])
            cts = int(round(time.time() * 1000))
            dts = cts-pts
            hours=(dts/(1000*60*60))%24
            if hours<2:
                form.userid.data = data[1]
                return render_template('reset-password.html',form=form,reportsof = 'Reset Password',userinfo=current_user)
            else:
                logger.info('Failed to reset Password')
                return render_template('error.html',form=form,reportsof = 'Reset Password',msg="Sorry, Reset Password link Expaired.<br><a href='/forgot'>Reset Password</a>",userinfo=current_user)


@app.route('/data_entry_dashboard', methods = ['GET', 'POST'])
@login_required
def data_entry_dashboard():
       logger.info('Entered into Data Entry dashboard')
       return render_template('data-entry-dashboard.html')

#-----------------Marketing dept-------------------------------------------------------------------------------------
@app.route('/marketing_dashboard', methods = ['GET', 'POST'])
@login_required
def marketing_dashboard():
    shop=ShopOrders.objects.count()
    purchaseinvoice= ShopOrderInvoice.objects.count()
    order_coupon = OrderCoupons.objects(status='Active').count()
    return render_template('marketing-dashboard.html',shop=shop,purchaseinvoice=purchaseinvoice,order_coupon=order_coupon)
'''
@app.route('/shoporderlist_viewmore',methods=['GET'])
@login_required
def shoporderlist_viewmore():
    shop=ShopOrders.objects(status='Accept')
    return render_template('shop-orderlist.html',shop=shop)
         

@app.route('/purchaseinvoice_viewmore',methods=['GET'])
@login_required
def purchaseinvoice_viewmore():
    purchaseinvoice= ShopOrderInvoice.objects(status='Approve')
    return render_template('invoicehistory.html',purchaseinvoice=purchaseinvoice)
'''
@app.route('/coupon_order_viewmore',methods=['GET'])
@login_required
def coupon_order_viewmore():
    cu_info= OrderCoupons.objects(status='Active')    
    return render_template('coupon-info-list.html',cu_info=cu_info)
 

@app.route('/order_coupons', methods = ['GET', 'POST'])
@login_required
def order_coupons():
        with app.app_context():
            form = CouponsForm()
        if request.method == 'POST':
            #return 'Hi'
            coupon_name=request.form['coupon_name']
            coupon_code = request.form['coupon_code']
            typef=request.form.get('disType')
            discount=request.form['discount']
            maxvalue=request.form['maxvalue']
            from_date=request.form.get('fromDate')
            end_date = request.form.get('endDate')
            min_order_value = request.form['min_order_value']
            created_date=request.form.get('createDate')
            createdBy=request.form.get('createBy')
            terms_conditions=request.form.get('termsConditions')
            imageurl=request.form.get('imageUrl')
            #return str(imageurl)
            status=request.form.get('couponhide')
            if status=='yes':
                coupon_edit = OrderCoupons.objects.get(coupon_code=coupon_code)
                coupon_edit.coupon_name=coupon_name
                coupon_edit.typef=typef
                coupon_edit.discount=discount
                coupon_edit.from_date=from_date
                coupon_edit.end_date=end_date
                coupon_edit.min_order_value=min_order_value
                coupon_edit.terms_conditions=terms_conditions
                coupon_edit.imageurl=imageurl
                coupon_edit.save()
            else:
                coupons = OrderCoupons(user_id=str(current_user.id),coupon_name=coupon_name,coupon_code=coupon_code, typef=typef, discount=discount,maxvalue=maxvalue,from_date=from_date, end_date =end_date,
                            min_order_value=min_order_value,created_date=created_date,createdBy=createdBy,terms_conditions=terms_conditions,imageurl=imageurl)# Insert form data in collection
                coupons.save()   
            return redirect(url_for('order_coupons'))
        else:
            coupon=OrderCoupons.objects()
            return render_template('order-coupons.html', form=form,coupon=coupon)

@app.route('/coupondelete/', methods=['GET'])
@login_required
def coupondelete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="coup"):
            coupon = OrderCoupons.objects.get(id=docid)
            coupon.delete()
        return redirect(url_for('order_coupons'))

@app.route('/couponactive/<id>')
@login_required
def couponactive(id):
    userstatus = OrderCoupons.objects.get(id=id)
    if userstatus.status == 'Inactive':
        userstatus.status = 'Active'
        userstatus.save()
    return redirect(url_for('order_coupons'))    

@app.route('/market_price_setup', methods = ['GET','POST'])#drop down WH values
def market_price_setup():
    try:
        logger.info('Entered into Market price setup')
        whdata=Warehouse.objects()
        return render_template('price-setup.html',whdata=whdata)
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')        

@app.route('/market_brand_post', methods=['GET', 'POST'])
def market_brand_post():
    try:
        logger.info('Entered into Market Brand post')
        whid=request.args.get('supId') #WH
        sup=Warehouse.objects(id=whid)
        #brand=request.args.get('brand')  
        brand=[]
        for supplier in Sup_Upload.objects(status__ne='Inprocess'):
            for products in ProdinvWH.objects(warehouse=sup[0].warehouse_name,prod_desc=supplier.upload_name):#drop down brand based on wh
            #if products.prod_desc==supplier[0].upload_name:
                #print 'hi'
                brand.append(products.brand)
        sub=sorted(set(brand))  
        return jsonify(sub)     
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')

@app.route('/market_model_post', methods=['GET', 'POST'])
def market_model_post():
    try:
        whid=request.args.get('supId') #WH
        sup=Warehouse.objects(id=whid)
        brand=request.args.get('brand')
        model=[]
        #print sup[0].warehouse_name
        for supplier in Sup_Upload.objects(status__ne='Inprocess',upload_brand=brand):
            for products in ProdinvWH.objects(warehouse=sup[0].warehouse_name,brand=brand,prod_desc=supplier.upload_name):#drop down nodelNo based on brand
            #if products.prod_desc==supplier[0].upload_name:
                 model.append(products.modelno)
        sub=sorted(set(model))  
        return jsonify(sub)
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')
@app.route('/market_get_values', methods = ['GET','POST'])
def market_get_values():
    try:
        json_data = request.get_json(force=True)
        logger.info('Entered into Market Values')
        brand=json_data['brand']
        modelno = json_data['modelNo']
        warehouseid= json_data['supplierId']
        br=[]
        for i in Sup_Upload.objects(status='Accept',upload_modelno=modelno,upload_brand=brand):
          wh = Warehouse.objects(id=warehouseid)
          for data in ProdinvWH.objects(modelno=modelno,brand=brand,warehouse=wh[0].warehouse_name):
            for j in data.prices:
                data={}
                data['upload_mrp']=i.upload_mrp
                data['upload_discount']=i.upload_discount
                data['upload_tax']=i.upload_tax
                data['upload_netPrice']=i.upload_price
                data['landing_price']=i.upload_price
                data['dealer_price']=j.dealer_price
                data['offer_price']=j.offer_price
                data['enduser_price']=j.enduser_price
                data['bulk_unit_price']=j.bulk_unit_price
                data['bulk_qty']=j.bulk_qty
                data['landing_price_gst']=j.landing_price_gst
                data['dealer_price_gst']=j.dealer_price_gst
                data['offer_price_gst']=j.offer_price_gst
                data['enduser_price_gst']=j.enduser_price_gst
                data['description']=i.upload_name
                br.append(data)     
        return jsonify(br)
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')

@app.route('/market_price_post', methods=['GET', 'POST'])
def market_price_post():
    pool = Pool()
    pool_new(pool)
    try:
        if request.method == 'POST':#insert values into collection from ajax call
            logger.info('Entered into Market Price Post')
            json_data = request.get_json(force=True)
            warehouseid= json_data['supplierId']
            brand=json_data['brand']
            modelno = json_data['modelNo']
            for i in json_data['prices']:
                wh = Warehouse.objects.get(id=warehouseid)
                landing_price=i['landing_price']
                #print landing_price
                dealer_price=i['dealer_price']
                offer_price=i['offer_price']
                enduser_price=i['endUser_price']
                bulk_unit_price=i['bulk_price']
                bulk_qty=i['bulk_qty']
                landing_price_gst=i['landing_price_gst']
                dealer_price_gst=i['dealer_price_gst']
                offer_price_gst=i['offer_price_gst']
                enduser_price_gst=i['enduser_price_gst']
                #return offer_price
                pval=(float(offer_price)/float(enduser_price))*100
                pval=100-float(pval)
                #percentage=format(pval, '.2f')
                #print type(percentage)
                for data in ProdinvWH.objects(modelno=modelno,brand=brand):
                    for j in data.prices:
                        j.landing_price=landing_price
                        j.dealer_price=dealer_price
                        j.offer_price=offer_price
                        j.enduser_price=enduser_price
                        j.bulk_unit_price=bulk_unit_price
                        j.bulk_qty=bulk_qty
                        j.landing_price_gst=float(landing_price_gst)
                        j.dealer_price_gst=float(dealer_price_gst)
                        j.offer_price_gst=float(offer_price_gst)
                        j.enduser_price_gst=float(enduser_price_gst)
                        j.save()
                       

            for data in Sup_Upload.objects(upload_modelno=modelno,upload_brand=brand):
                 for k in data.prices:
                        k.landing_price=landing_price
                        k.dealer_price=dealer_price
                        k.offer_price=offer_price
                        k.enduser_price=enduser_price
                        k.bulk_unit_price=bulk_unit_price
                        k.bulk_qty=bulk_qty
                        k.landing_price_gst=float(landing_price_gst)
                        k.dealer_price_gst=float(dealer_price_gst)
                        k.offer_price_gst=float(offer_price_gst)
                        k.enduser_price_gst=float(enduser_price_gst)
                        percentage=format(float(pval),'.2f')
                        k.percentage=float(percentage)
                        k.doubleoffer_price=float(offer_price)
                        k.save()
           
            json_data['product_name']= data.upload_name
            json_data['offer_price']= k.offer_price
            user = UserSignup.objects(usertype='Accountant')
            fo = open("./static/mailtemp/marketingmailtemp.html", "r+")
            htmlbody = fo.read()
            fo.close()
            urldata='Dear '+user[0].username+',<br>Product prices are updated sucessfully.'
            htmlbody = htmlbody.replace("$$urldata$$",urldata)
            #sendMail(user[0].email,'Update the product prices',htmlbody)
            pool.apply_async(sendMail,[user[0].email,'Update the product prices',htmlbody])
            msg='Dear '+user[0].username+' Product prices are updated sucessfully.'
            #mobile='91'+user[0].mobile
            mobileList=[]
            mobileList.append('91'+user[0].mobile)
            #SMS(msg,mobile)
            pool.apply_async(SMS,[msg,mobileList])
            product_name=json_data['product_name']
            offer_price=json_data['offer_price']
            UpdateInitiateOrder(product_name,offer_price)
            #jar = cookielib.FileCookieJar("cookie")
            #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
            #url = 'http://157.119.108.135:8005/updateinitiateorder'
            #user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            #data = {"product_name":product_name,"offer_price":offer_price}
            #data1=json.dumps(data)
            #data = urllib.urlencode(data)
            #login_request = urllib2.Request(url,data1)
            #login_reply = opener.open(login_request)
            #login_reply_data = login_reply.read()
            return 'Success'
    except Exception as e:
       return jsonify('{"mesg":' + str(e) +'}')
'''    
@app.route('/customer_order_tracking', methods=['GET', 'POST'])
def customer_order_tracking():
    json_data = request.get_json(force=True)
    print json_data
    product_name = 'jhgiyguguhgvhj'
    offer_price='54654'
    jar = cookielib.FileCookieJar("cookie")
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
    url = 'http://192.168.20.68:80/sample'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    data = {"product_name":product_name,"offer_price":offer_price}
    data1=json.dumps(data)
    #data = urllib.urlencode(data)
    login_request = urllib2.Request(url,data1)
    print login_request,'login_request'
    login_reply = opener.open(login_request)
    login_reply_data = login_reply.read()
    print type(login_reply)
    return jsonify(ast.literal_eval(login_reply_data))
'''
@app.route('/price_list', methods = ['GET','POST'])
def price_list():
    try:
        logger.info('Entered into Price List')
        dt=ProdinvWH.objects()           
        return render_template('product-price-list.html',dt=dt)
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')

@app.route('/settlement', methods=['GET', 'POST'])
def settlement():
    shop=request.args.get('shop')
    br=[]
    for prod in CustomerOrders.objects():
        data={}
        data['shop']=prod.shop
        inlistFlag = True
        for inlist in br:
            if(inlist['shop']==prod.shop):
                inlistFlag=False
        if inlistFlag:
                br.append(data) 
    return render_template('dealer-settlement.html',shp=br)
    


@app.route('/dealer_settlement', methods=['GET', 'POST'])
def dealer_settlement():
    try:
      if request.method == 'POST':
        json_data = request.get_json(force=True)
        shop = json_data['shop']
        '''
        tax_amount=0
        total=0
    
        details=[]
        detail=CustomerOrders.objects(shop=shop,settelmentAmount__ne='0',order_settlement=False,status="Complete").only('orderid','transactionid','discountAmount','order_settlement','settelmentAmount','orderitems__tax_amount','orderitems__total')
        invoicesList=json.loads(detail.to_json())
        print invoicesList
        for orders in invoicesList:
            print orders
            info={}
            info['orderid']=orders.orderid
            #info['transactionid']=orders.transactionid                    
            info['discount_amount']=orders.discountAmount            
            print "hi"
            print invoicesList['orderitems']
            for price in orders['orderitems']:
                data={}
                data['taxAmount']=tax_amount+price.tax_amount
                data['total']=total+price.total
                info['prices']=data
            details.append(info)
        print details    
        return jsonify(details)
        '''
        
        invoicesList=[]
        
        for prodinv in CustomerOrders.objects(shop=shop,order_settlement=False,status="Complete",settelmentAmount__ne='0'):
            #settelmentAmount__ne='0'
            data={}
            data['orderid']=prodinv.orderid
            data['transactionid']=prodinv.transactionid            
            data['discount_amount']=prodinv.discountAmount
            data['settelmentAmount']=prodinv.settelmentAmount
            total=0.0
            tax=0.0
            #print type(total)
            for amount in prodinv.orderitems:
                #print float(amount.tax_amount)
                info={}
                tax=tax+float(amount.tax_amount)
                total=total+float(amount.total)
                info['taxAmount']=tax
                info['total']=total
            data['amount']=info
            invoicesList.append(data)
                       
        return jsonify(invoicesList)
                  
     
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')

    

@app.route('/settlementpost',methods = ['GET', 'POST'])
def settlementpost():
    try:
     if request.method == 'POST':
       json_data = request.get_json(force=True)       
       shop = json_data['shop']
       settleTotalAmount = json_data['settleTotalAmount']
       shopship = DealerSettlement(user_id=str(current_user.id),shop=shop,settleTotalAmount=settleTotalAmount).save()
       for i in json_data['items']:
            item = i['item']
            orderid=i['orderid']
            transactionid = i['transactionid']
            taxAmount = i['taxAmount']
            total = i['total']
            discountAmount=i['discount_amount']
            ships = Settlement(item,orderid,transactionid,taxAmount,discountAmount,total)
            shopship.settlement_items.append(ships)
            shopship.save()
            for prodinv in CustomerOrders.objects(shop=shop,order_settlement=False):
               prodinv.order_settlement=True
               prodinv.save()
       return 'Success'                     
    except Exception as e:
        return render_template('error.html',reportsof = 'Exception',msg=str(e))


@app.route('/settlement_report', methods=['GET', 'POST'])
def settlement_report():
    shop=request.args.get('shop')
    br=[]
    for prod in CustomerOrders.objects():
        data={}
        data['shop']=prod.shop
        inlistFlag = True
        for inlist in br:
            if(inlist['shop']==prod.shop):
                inlistFlag=False
        if inlistFlag:
                br.append(data) 
    return render_template('settlement_history.html',shp=br)


@app.route('/settlement_history', methods=['GET', 'POST'])
def settlement_history():
    try:
        if request.method == 'POST':
             json_data = request.get_json(force=True)
             shop = json_data['shop']                
             invoicesList=[]
             '''
             detail=DealerSettlement.objects(shop=shop,flag='True').only('orderid','transactionid','discountAmount','order_settlement','settelmentAmount')
             cus_ord_histy=json.loads(detail.to_json())
             return jsonify(cus_ord_histy)
             '''
             for i in DealerSettlement.objects(shop=shop):
                  data={}
                  data['shop']=shop
                  data['settlementid']=i.user_id
                  data['settleTotalAmount']=i.settleTotalAmount
                  data['date']=(i.settlement_date).strftime('%d-%m-%Y')
                  '''
                  inlistFlag = True
                  for inlist in invoicesList:
                      if(inlist['orderid']==prodinv.orderid):
                           inlistFlag=False       
                  if inlistFlag:
                  '''
                  invoicesList.append(data)   
             return jsonify(invoicesList) 
             
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')

@app.route('/dealer_settlement_viewmore/<shop>/<date>',methods = ['GET', 'POST'])
@login_required
def dealer_settlement_viewmore(shop,date):
        #date= request.args.get('date') datetime.datetime.strptime('03:55', '%H:%M').time()
        dates=str(date)
        dat = datetime.datetime.strptime(dates,'%d-%m-%Y').strftime("%Y-%m-%d")
        orderslist=[]
        for detailss in DealerSettlement.objects():
            for order_info in detailss.settlement_items:
                dbdate= (detailss.settlement_date).strftime("%Y-%m-%d")
                if detailss.shop==shop and dbdate==dat:
                    data={}
                    data['orderid']=order_info.orderid
                    data['transactionid']=order_info.transactionid
                    data['taxAmount']=order_info.taxAmount
                    data['discountAmount']=order_info.discountAmount
                    data['total']=order_info.total
                    orderslist.append(data)
        return render_template('dealer-settlement-viewmore.html',orderslist=orderslist)    

#----------------------Account dept-----------------------------------

@app.route('/account_dashboard', methods = ['GET', 'POST'])
@login_required
def account_dashboard():
       logger.info('Entered into account dashboard')
       pur_orders=PurchaseOrders.objects(status='Accept').count()
       purchase_orders="{:,}".format(pur_orders)
       shop_order=ShopOrders.objects(status__ne="Pending").count()
       shop_orders="{:,}".format(shop_order)
       shop_invoice=ShopOrderInvoice.objects().count()
       shop_invoices="{:,}".format(shop_invoice)
       settle=DealerSettlement.objects().count()
       settlement="{:,}".format(settle)
       return render_template('account-dashboard.html',purchase_orders=purchase_orders,shop_orders=shop_orders,shop_invoices=shop_invoices,settlement=settlement)


@app.route('/invoicehistory',methods=['GET'])
@login_required
def invoicehistory():
           logger.info('Entered into Invoice History')
           purchaseinvoice= ShopOrderInvoice.objects.order_by("-id")    
           return render_template('invoicehistory.html',purchaseinvoice=purchaseinvoice)


@app.route('/invoiceviewmore/<id>',methods = ['GET', 'POST'])
@login_required
def invoiceviewmore(id):
        logger.info('Entered into Invoice Viewmore')
        detailess = ShopOrderInvoice.objects.filter(id=id).first()
        regdealer=Reg_Dealer.objects()
        company=Company_Setup.objects()
        billing=Billing_Setup.objects(dealerid=detailess.dealer_id)
        warehouse=Warehouse.objects()
        header=Header.objects()
        logo=header[0].headerlogo
        number= num2words(float((detailess.total_value)))
        return render_template('invoice-viewmore.html',detailess=detailess,company=company[0],logo=logo,billing=billing[0],warehouse=warehouse[0],regdealer=regdealer[0],number=number)


#-------------------------------------------------Fair Contacts--------------------------------------------------------------------------
    
@app.route('/fair_contact', methods=['GET', 'POST'])
@login_required
def fair_contact():
    try:
     if request.method == 'POST':
           logger.info('Entered into Fair Contact')
           json_data = request.get_json(force=True)
           username = json_data['username']
           email = json_data['email']
           business_type=json_data['business_type']
           mobile_no = json_data['mobile_no']
           
           if business_type == 'Others':
              others = json_data['others']
           else:
              others = "None"
           isEmail=Fair_Contact.objects(email=email)
           isMobile=Fair_Contact.objects(mobile_no = mobile_no)
           if isEmail.count()>0:
               return 'Email already existed!'
           elif isMobile.count()>0:
               return 'Mobile already existed!'
           fair = Fair_Contact(username=username,email=email,business_type=business_type,mobile_no=mobile_no,others=others)
           fair.save()
           return 'Success' 
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')

@app.route('/fair_contactlist',methods = ['GET', 'POST'])
@login_required
def fair_contactlist():
        logger.info('Entered into Fair Contact List')
        contact=[]
        for i in Fair_Contact.objects():
            contact.append(i)    
        return render_template('fair-contact.html',contact=contact)


@app.route('/fair_contact_delete/<id>', methods=['GET'])
@login_required
def fair_contact_delete(id):
        quickview = Fair_Contact.objects.get(id=id)
        quickview.delete()
        logger.info('Deleted Fair Contact')
        return redirect(url_for('fair_contactlist'))
    
@app.route('/notifications',methods = ['GET', 'POST'])
def notifications():
    logger.info('Entered into Notification')
    detailes = Notifications.objects()
    dt=[]
    for i in detailes:
        message=i.message
    return render_template('dashboard.html',message=message)


@app.route('/userorders',methods = ['GET', 'POST'])
def userorders():
     try:
        if request.method == 'POST':   #insert values into collection from ajax call
            logger.info('Entered into User Orders')
            json_data = request.get_json(force=True)
            order_created_date= json_data['order_created_date']
            order_id=json_data['order_id']
            customer_email = json_data['customer_email']
            firstname = json_data['firstname']
            lastname = json_data['lastname']
            mobile = json_data['mobile']
            ordered_items= json_data['ordered_items']
            shipping_address=json_data['shipping_address']
            billing_address = json_data['billing_address']
            base_subtotal = json_data['base_subtotal']
            shipping_amount = json_data['shipping_amount'] 
            orders = UserOrders(order_created_date=order_created_date,order_id=order_id,customer_email=customer_email,firstname=firstname,lastname=lastname,mobile=mobile,
                                  ordered_items=ordered_items,shipping_address=shipping_address,billing_address=billing_address,base_subtotal=base_subtotal,shipping_amount=shipping_amount)
            orders.save()
            for i in json_data['ordered_items']:
                product_id=i['product_id']
                product_name=i['product_name']
                modelnumber=i['modelnumber']
                sku=i['sku']
                price=i['price']
                offer_price=i['offer_price']
                brand=i['brand']
                quantity=i['quantity']
                items = UserOrderList(product_id=product_id,product_name=product_name,modelnumber=modelnumber,sku=sku,price=price,offer_price=offer_price,brand=brand,quantity=quantity)  
                orders.ordered_items.append(items)
                orders.save()
        return 'Success'
     except Exception as e:
         return jsonify('{"mesg":' + str(e) +'}')       
#----------------------------------------------Error templates-------------------------------------------------------------->
@app.errorhandler(401)
def page_not_found(e):
    return render_template('error.html',reportsof = 'Error: 401',msg=str(e))

@app.errorhandler(404)
def page_not_available(e):
    return render_template('error.html',reportsof = 'Error: 404',msg=str(e))

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html',reportsof = 'Error: 500',msg=str(e))

#---------------------------------Logout---------------------------------------------------------------------------->
# somewhere to logout
@app.route("/logout")
def logout():
    logout_user()
    logger.info('Loggedout Sucessfully')
    return redirect(url_for('login'))

#------------------------------------------------------------Extra Pages------------------------------------------------->
@app.route('/how_it_works', methods=['GET'])
def how_it_works():
    logger.info('Entered into How It works')
    return render_template('how-it-works.html')

@app.route('/faq', methods=['GET'])
def faq():
    logger.info('Entered into  Faq')
    return render_template('faq.html')

@app.route('/test1', methods=['GET','POST'])
def test1():
     json_data = request.get_json(force=True)
     warehouse_name = json_data['username']
     supplier_name = json_data['firstname']
     mobile = json_data['mobile']
     return warehouse_name+supplier_name+mobile


@app.route('/shop_ajax', methods = ['GET', 'POST'])
#@login_required
def shop_ajax():
        shop=Shopsetup.objects()
        shops=[]
        for shoinfo in shop:
            data={}
            data['shop_id']=shoinfo.shop_id
            data['shop_name']=shoinfo.shop_name
            data['shop_address']=shoinfo.shop_address
            data['pincode']=shoinfo.pincode
            data['latitude']=shoinfo.lat_long[0]
            data['longitude']=shoinfo.lat_long[1]
            data['email']=shoinfo.email
            data['shop_name']=shoinfo.shop_name
            data['phone']=shoinfo.phone
            data['password']=shoinfo.password
            shops.append(data)
        return jsonify({'status':'success','data':shops})  

@app.route('/ser_ajax', methods = ['GET', 'POST'])
#@login_required
def ser_ajax():
        shop=Shopsetup.objects()
        shops=[]
        for shoinfo in shop:
            data={}
            data['shop_id']=shoinfo.shop_id
            data['shop_name']=shoinfo.shop_name
            data['shop_address']=shoinfo.shop_address
            data['pincode']=shoinfo.pincode
            data['latitude']=shoinfo.latitude
            data['longitude']=shoinfo.longitude
            data['email']=shoinfo.email
            data['shop_name']=shoinfo.shop_name
            data['phone']=shoinfo.phone
            data['password']=shoinfo.password
            shops.append(data)
        return jsonify({'status':'success','data':shops})

@app.route('/support_dashboard', methods = ['GET', 'POST'])
def support_dashboard():
        logger.info('Entered into Support Dashboard')
        return render_template('support-dashboard.html')

@app.route('/customer_report', methods = ['GET', 'POST'])
def customer_report():
        logger.info('Entered into Customer Report')
        return render_template('order-check.html')

@app.route('/customerdata', methods=['GET', 'POST'])
def customerdata():
    try:
        if request.method == 'POST':
             logger.info('Entered into Customer data')
             json_data = request.get_json(force=True)
             orderid=json_data['ordersearch']
             prodinv=CustomerOrders.objects(orderid=orderid)
             detail=[]
             for customer in prodinv:
                for i in customer.orderitems:                   
                    data={}
                    data['orderno']=customer.orderid
                    data['orderdate']=customer.createddate
                    data['personinfo']=customer.customermobile
                    data['orderstatus']=customer.status
                    data['sno']=i.sno
                    data['prodesc']=i.productdesp
                    data['quantity']=i.qty
                    data['unitprice']=i.unitprice
                    data['total']=i.total
                    data['totalamount']=customer.totalamount
                    data['shippingaddr']=customer.shippingaddress
                    data['shippingtype']=customer.shippingtype
                    detail.append(data)   
             return jsonify(detail)     
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')

#---------------------------------csv files download from browser------------------------------------------------------------------>
def get_whinformation(url):
        wh= ProdinvWH.objects()
        product=[]
        for products in wh:
            for j in products.prices:
                if j['enduser_price']>0:     
                    data={}
                    data['id']=str(products.id)
                    data['user_id']=products.user_id
                    data['supplier']=products.supplier
                    data['warehouse']=products.warehouse
                    data['hsn']=products.hsn
                    data['modelno']=products.modelno
                    data['brand']=products.brand
                    data['prod_desc']=products.prod_desc
                    data['smtids']=ast.literal_eval(json.dumps(products.smtids))
                    data['quantity']=products.quantity
                    data['barcode']=products.barcode
                    data['status']=products.status
                    em=[]
                    for i in products.invoice_smtlist:
                        data1={}
                        data1['invoiceid']=i.invoiceid
                        data1['fromsmt']=i.fromsmt
                        data1['tosmt']=i.tosmt
                        data1['invoicedate']=i.invoicedate
                        #return str(data1['invoicedate'])
                        em.append(data1)
                    #return str(em)
                    data['property']=json.dumps(em)
                    pm=[]
                    for j in products.prices:
                        data2={}
                        data2['landing_price']=j.landing_price
                        data2['dealer_price']=j.dealer_price
                        data2['offer_price']=j.offer_price
                        data2['enduser_price']=j.enduser_price
                        data2['bulk_unit_price']=j.bulk_unit_price
                        data2['bulk_qty']=j.bulk_qty
                        pm.append(data2)
                    data['pricelist']=json.dumps(pm)
                    product.append(data)
        with open('whout.csv', 'wb+') as f:
             dict_writer = csv.DictWriter(f, fieldnames=['id','user_id','supplier','warehouse', 'hsn','modelno','brand','prod_desc','smtids','quantity','barcode','property','pricelist','status'])
             dict_writer.writeheader()
             dict_writer.writerows(product)
        return 'Download completely'
                    

@app.route("/wh_download.csv")
def whdownload():
    url = ""
    get_whinformation(url)
    logger.info('Warehouse Downloaded successfully!')
    return send_file("whout.csv")


def get_shopinformation(url):
    shopinfo= ProdInvShop.objects()
    product=[]
    for products in shopinfo:
        data={}
        data['name']=products.proddescription
        data['qty']=products.inqty
        data['image']=products.image
        data['model']=products.model
        em=[]
        for j in Sup_Upload.objects.filter(upload_modelno=products.model):
            data['image']=j.upload_photo
            for k in j.attributes:
                data1={}
                data1['atrname']=k['atrname']
                data1['atrvalue']=k['atrvalue']
                em.append(data1)
        data2={}        
        for i in products.price:
            data2['enduser_price']=i.enduser_price
            data2['offer_price']=i.offer_price
            data['enduser_price']=data2['enduser_price']
            data['offer_price']=data2['offer_price']
            data['attributes']=json.dumps(em)
            product.append(data)
    #return str(product)
    with open('out.csv', 'wb+') as f:
         dict_writer = csv.DictWriter(f, fieldnames=['name','model','enduser_price','offer_price','qty','image','attributes'])
         dict_writer.writeheader()
         dict_writer.writerows(product)
    return 'Download completely'
        

@app.route("/shop_download.csv")
def shopdownload():
    url = ""
    get_shopinformation(url)
    logger.info('Shop Downloaded successfully!')
    return send_file("out.csv")

@app.route('/service_tax', methods = ['GET', 'POST'])
def service_tax():
        with app.app_context():
         form = ServicetaxForm()
        if request.method == 'POST':
            taxid = request.form['taxid']
            taxname=request.form['taxname']
            taxrate=request.form['taxrate']
            tax = ServiceTax(user_id=str(current_user.id),taxid=taxid,taxname=taxname,taxrate=taxrate) 
            tax.save()
            return redirect(url_for('service_tax'))
        servicelist = ServiceTax.objects(user_id=str(current_user.id))              
        return render_template('service-tax.html',form=form,servicelist=servicelist)

@app.route('/service_tax_delete/', methods=['GET', 'POST'])
@login_required
def service_tax_delete():
            type = request.args.get('type')
            docid = request.args.get('docid')
            if(type=="tax"):
                user=ServiceTax.objects.get(id=docid)
                user.delete()
                logger.info('Deleted Tax')
            return redirect(url_for('service_tax'))

@app.route('/Resource', methods = ['GET', 'POST'])
def Resource(): 
        #json_data = request.get_json(force=True)
        confirm_shop=ServiceTax.objects.get(tax_rate='50')
        if confirm_shop:
            return "true"
        else:
            return "False"
#--------------------Wh reports----------------------------------------------------------------------------------
@app.route('/whpurchase_orderreport', methods = ['GET', 'POST'])
def whpurchase_orderreport():
        logger.info('Entered into Customer Report')
        return render_template('whpurchase-order-reports.html')

@app.route('/whpurchase_orderget', methods = ['GET', 'POST'])
def whpurchase_orderget():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        fromdate=json_data['fromdate']
        todate=json_data['todate']
        fromdates = datetime.datetime.strptime(fromdate, "%Y-%m-%d")
        to = datetime.datetime.strptime(todate, "%Y-%m-%d")
        todates=to+timedelta(1)
        wh=[]
        purchasedata=PurchaseOrders.objects(created_date__lte=todates,created_date__gte=fromdates)
        if purchasedata.count()==0:
                    data={}
                    data['status']="fail"
                    wh.append(data)
                    return jsonify(wh)
        for i in purchasedata:
            data={}
            data['shoppono']=i.purchaseOrder_no
            data['warehousename']=i.warehouse_name
            data['podate']=i.po_date
            data['status']=i.status            
            wh.append(data)
        return jsonify(wh)


@app.route('/whpurchase_orderviewmore/<pono>',methods = ['GET', 'POST'])
@login_required
def whpurchase_orderviewmore(pono):
        detailes = PurchaseOrders.objects.filter(purchaseOrder_no=pono).first()
        number= num2words(float((detailes.totalvalue)))
        company=Company_Setup.objects()
        billing=Billing_Setup.objects()
        warehouse=Warehouse.objects()
        headerlist = Header_Setup.objects()
        regsup=Reg_Supplier.objects(user_id=detailes.supplier_id)
        header=Header.objects()
        logo=header[0].headerlogo
        return render_template('whpurchaseorde-reportrviewmore.html',detailes=detailes,company=company[0],billing=billing[0],logo=logo,warehouse=warehouse[0],regsup=regsup[0],headerlist=headerlist[0],number=number)


@app.route('/whinvoice_orderreport', methods = ['GET', 'POST'])
def whinvoice_orderreport():
        logger.info('Entered into Customer Report')
        return render_template('whpurchaseorder-invoicereport.html')

@app.route('/whpurchase_invoiceget', methods = ['GET', 'POST'])
def whpurchase_invoiceget():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        prevdate=json_data['prevdate']
        currentdate=json_data['currentdate']
        fromdates = datetime.datetime.strptime(prevdate, "%Y-%m-%d")
        to = datetime.datetime.strptime(currentdate, "%Y-%m-%d")
        todates=to+timedelta(1)
        invoice=[]
        invoicedata=PurchaseInvoice.objects(created_date__lte=todates,created_date__gte=fromdates)
        if invoicedata.count()==0:
                data={}
                data['status']="fail"
                invoice.append(data)
                return jsonify(invoice)
        for i in invoicedata :
            data={}
            data['warehousename']=i.ware_house
            data['invoiceno']=i.invoice_no
            data['indate']=i.invoice_date
            data['status']=i.status            
            invoice.append(data)
        return jsonify(invoice)

@app.route('/whinvoice_orderviewmore/<invno>',methods = ['GET', 'POST'])
@login_required
def whinvoice_orderviewmore(invno):
    detailess = PurchaseInvoice.objects.filter(invoice_no=invno).first()
    purchase_data=PurchaseOrders.objects(purchaseOrder_no=detailess.purchaseOrder_no)
    company=Company_Setup.objects()
    billing=Billing_Setup.objects()
    warehouse=Warehouse.objects()
    headerlist = Header_Setup.objects()
    regsup=Reg_Supplier.objects(user_id=detailess.supplier_id)
    number= num2words(float((detailess.total_value)))
    header=Header.objects()
    logo=header[0].headerlogo
    #return detailes.warehouse_name    
    return render_template('whpurchaseorder-invoiceviewreport.html',purchase_data=purchase_data,detailess=detailess,company=company[0],billing=billing[0],warehouse=warehouse[0],logo=logo,headerlist=headerlist[0],regsup=regsup[0],number=number)


@app.route('/whcustomer_report', methods = ['GET', 'POST'])
def whcustomer_report():
        logger.info('Entered into Customer Report')
        return render_template('wh-customerorder-reports.html')

@app.route('/whcustomerdata', methods=['GET', 'POST'])
def whcustomerdata():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        fromdate=json_data['fromdate']
        todate=json_data['todate']
        fromdates = datetime.datetime.strptime(fromdate, "%Y-%m-%d")
        to = datetime.datetime.strptime(todate, "%Y-%m-%d")
        todates=to+ timedelta(1)
        shop=[]
        orderdata=ShopOrders.objects(created_date__lte=todates,created_date__gte=fromdates)
        if orderdata.count()==0:
            data={}
            data['status']="fail"
            shop.append(data)
            return jsonify(shop)
        for i in orderdata:
            data={}
            data['dealer_id']=i.dealer_id
            data['shop_purchaseorderno']=i.shop_purchaseorderno
            data['warehouse_name']=i.warehouse_name
            data['po_date']=i.po_date
            data['status']=i.status            
            shop.append(data)
        return jsonify(shop)


@app.route('/wh-customer_orderviewmore/<id>',methods = ['GET', 'POST'])
@login_required
def whcustomer_orderviewmore(id):
    
        detailess = ShopOrders.objects.filter(shop_purchaseorderno=id).first()
        billing=Billing_Setup.objects(dealerid=detailess.dealer_id)
        company=Company_Setup.objects()
        warehouse=Warehouse.objects()
        number= num2words(float((detailess.totalvalue)))
        regdealer=Reg_Dealer.objects()
        header=Header.objects()
        logo=header[0].headerlogo
        return render_template('wh-customer-orderreport-viewmore.html',detailes=detailess,billing=billing[0],logo=logo,company=company[0],warehouse=warehouse[0],regdealer=regdealer[0],number=number)


@app.route('/whorder_invoice', methods = ['GET', 'POST'])
def whorder_invoice():
        logger.info('Entered into Customer Report')
        return render_template('wh-customer-invoice-reports.html')

@app.route('/whorder_invoicedata', methods=['GET', 'POST'])
def whorder_invoicedata():
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
             invoicedata=ShopOrderInvoice.objects(created_date__lte=todates,created_date__gte=fromdates)
             if invoicedata.count()==0:
                data={}
                data['status']="fail"
                detail.append(data)
                return jsonify(detail)
             for inv in invoicedata:                 
                    data={}
                    data['dealer_id']=inv.dealer_id
                    data['ware_house']=inv.ware_house
                    data['shop_purchaseorderno']=inv.shop_purchaseorderno
                    data['shopinvoice_number']=inv.shopinvoice_number
                    data['invoice_date']=inv.invoice_date
                    data['expected_date']=inv.expected_date
                    data['status']=inv.status
                    detail.append(data)
                    
             return jsonify(detail)     
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')



@app.route('/whcustomer_invoiceorderviewmore/<id>',methods = ['GET', 'POST'])
@login_required
def whcustomer_invoiceorderviewmore(id):
    
        detailess = ShopOrderInvoice.objects.filter(shop_purchaseorderno=id).first()
        number= num2words(float((detailess.total_value)))
        company=Company_Setup.objects()
        billing=Billing_Setup.objects(dealerid=detailess.dealer_id)
        warehouse=Warehouse.objects()
        regdealer=Reg_Dealer.objects()
        header=Header.objects()
        logo=header[0].headerlogo
        return render_template('wh-customerinvoice-viewmore.html',detailes=detailess,company=company[0],logo=logo,billing=billing[0],warehouse=warehouse[0],regdealer=regdealer[0],number=number)
    

@app.route('/wh_stock_reports', methods = ['GET', 'POST'])
def wh_stock_reports():
        shop=[]
        for i in ProdinvWH.objects(user_id=str(current_user.id)):
            data={}
            data['brand']=i.brand
            inlistFlag = True
            for inlist in shop:
                if(inlist['brand']==i.brand):
                        inlistFlag=False
            if inlistFlag:
                shop.append(data)
        logger.info('Entered into Customer Report')
        return render_template('wh-stock-reports.html',shop=shop)


@app.route('/wh_brand_post/', methods=['GET', 'POST'])
@login_required
def wh_brand_post():
       brand=request.args.get('brand')
       br=[]
       for i in ProdinvWH.objects(brand=brand,user_id=str(current_user.id)):
                 br.append(i.modelno)
       modelnos=sorted(set(br))
       logger.info('Entered into new brand post')
       return jsonify(modelnos)


@app.route('/whstockreportsdata', methods=['GET', 'POST'])
@login_required
def whstockreportsdata():
      if request.method == 'POST':
          logger.info('Entered into shoporder')
          json_data = request.get_json(force=True)
          brand = json_data['brand']
          modelno = json_data['modelno']
          wh=[]
          if brand == '0' and modelno == '0':
              wh= ProdinvWH.objects(user_id=str(current_user.id))
          elif brand == '0':
              wh=ProdinvWH.objects(user_id=str(current_user.id),modelno=modelno)
          elif modelno == '0':
             wh= ProdinvWH.objects(user_id=str(current_user.id),brand=brand)
          else:
             wh= ProdinvWH.objects(user_id=str(current_user.id),modelno=modelno,brand=brand)
          product=[]
          for products in wh:
              data={}
              data['prod_desc']=products.prod_desc
              data['quantity']=products.quantity
              data['outqty']=products.outqty
              bal=int(products.quantity)+int(products.outqty)
              data['balqty']=bal
              product.append(data)
             
          return jsonify(product)   
      else:
          return 'fail'


@app.route('/wh_advanced_reports', methods = ['GET', 'POST'])
def wh_advanced_reports():
        shop=[]
        for i in ProdInvShop.objects():
            data={}
            data['brand']=i.brand
            inlistFlag = True
            for inlist in shop:
                if(inlist['brand']==i.brand):
                        inlistFlag=False
            if inlistFlag:
                shop.append(data)
        logger.info('Entered into Customer Report')
        return render_template('wh-advance-reports.html',shop=shop)


@app.route('/whadv_brand_post/', methods=['GET', 'POST'])
def whadv_brand_post():
       brand=request.args.get('brand')
       br=[]
       for i in ProdInvShop.objects(brand=brand):
                 br.append(i.model)
       modelnos=sorted(set(br))
       logger.info('Entered into new brand post')
       return jsonify(modelnos)
 
@app.route('/whadvancedreportsdata', methods=['GET', 'POST'])
@login_required
def whadvancedreportsdata():
      if request.method == 'POST':
          logger.info('Entered into shoporder')
          json_data = request.get_json(force=True)
          brand = json_data['brand']
          model = json_data['modelno']
          shop=[]
          if brand == '0' and model == '0':
              shop= ProdInvShop.objects() 
          elif brand == '0':
              shop=ProdInvShop.objects(model=model)
          elif model == '0':
             shop= ProdInvShop.objects(brand=brand)
          else:
             shop= ProdInvShop.objects(model=model,brand=brand)
          product=[]
          for products in shop:
              data={}
              data['prod_desc']=products.proddescription
              data['quantity']=products.inqty
              data['outqty']=products.outqty
              product.append(data)
          return jsonify(product)   
      else:
          return 'fail'
        
@app.route('/exchange_policy', methods = ['GET', 'POST'])
def exchange_policy():
    with app.app_context():
     form = ExchangeForm()
    prod_inv_obj=ProdInvShop.objects()
    data=[]
    for obj in prod_inv_obj:
        dt={}
        dt['model']=obj.model
        dt['brand']=obj.brand
        inlistFlag = True
        for inlist in data:
            if inlist['model']==obj.model:
                inlistFlag=False
            elif inlist['brand']==obj.brand:
                inlistFlag=False
        if inlistFlag:
            data.append(dt)
    if request.method == 'POST':
        invoice_no = request.form.get('invoice_no')
        brand = request.form.get('brand')
        model = request.form.get('model')
        oldsmt_id = request.form.get('oldsmt_id')
        newsmt_id = request.form.get('newsmt_id')
        prod_inv_wh=ProdinvWH.objects(modelno=model,brand=brand)
        prod_inv_shp=ProdInvShop.objects(model=model,brand=brand)
        for i in prod_inv_shp:
            for j in i.avlsmtid:
                if j==oldsmt_id:
                    index=i.avlsmtid.index(oldsmt_id)
                    i.avlsmtid[index]=newsmt_id
                    i.save()
                    for a in prod_inv_wh:
                        for b in a.smtids:
                            if b==newsmt_id:
                                index=a.smtids.index(newsmt_id)
                                a.smtids[index]=oldsmt_id
                                a.save()
                            return render_template('exchange-success.html')
    return render_template('exchange-policy.html',form=form,data=data)

#--------------------------------------site setup----------------------------------------------------
@app.route('/collection', methods = ['GET', 'POST'])
@login_required
def collection():
        logger.info('Entered into userlist')
        with app.app_context():
            form = CollectionForm()
        if request.method == 'POST' and form.validate():
          if current_user.usertype=="Admin":
            collectionname = request.form['collectionname']
            collectionurl=request.form['collectionurl']
            collectionlink=request.form['collectionlink']
            createcollection = Collections(name=collectionname, imageurl=collectionurl, imagelink=collectionlink)# Insert form data in collection
            createcollection.save()
            return redirect(url_for('collection'))
        else:
            info = Collections.objects()
            logger.info('Sucessfully Created new in Collections')
            return render_template('collection.html', form=form,info=info)


@app.route('/collection_delete/', methods=['GET', 'POST'])
@login_required
def collection_delete():
    if current_user.usertype=="Admin":
        logger.info('Entered into user_delete')
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="i"):
            collection_info = Collections.objects.get(id=docid)
            collection_info.delete()
        logger.info('Sucessfully Deleted  %s  in Collection',type)
        return redirect(url_for('collection'))

    
@app.route('/brand', methods = ['GET', 'POST'])
@login_required
def brand():
        logger.info('Entered into brand')
        with app.app_context():
            form = BrandForm()
        if request.method == 'POST':
          if current_user.usertype=="Admin":
            
            brandname = request.form['brandname']
            brandurl=request.form['brandurl']
            brandlink=request.form['brandlink']
            brandfooterurl=request.form['brandfooterurl']
            brandtype=request.form['brandtype']           
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
                
            createcollection = Brand(brandname=brandname, brandurl=brandurl, brandlink=brandlink,brandfooterurl=brandfooterurl,brandtype=brandtype,tags=tagsinfo,metadescription=metatagsinfo,keywords=keywordsinfo)# Insert form data in collection
            createcollection.save()
            logger.info('Sucessfully Created new in brand Collections')
            return redirect(url_for('brand'))
        else:
            info = Brand.objects()
            logger.info('Sucessfully Created new in brand Collections')
            return render_template('brand.html', form=form,info=info)


@app.route('/brand_delete/', methods=['GET', 'POST'])
@login_required
def brand_delete():
    if current_user.usertype=="Admin":
        logger.info('Entered into user_delete')
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="i"):
            brand_info = Brand.objects.get(id=docid)
            brand_info.delete()
        logger.info('Sucessfully Deleted  %s  in Brand',type)
        return redirect(url_for('brand'))



@app.route('/banner', methods = ['GET', 'POST'])
@login_required
def banner():
        logger.info('Entered into banner')
        with app.app_context():
            form = BannerForm()
        if request.method == 'POST' and form.validate():
          if current_user.usertype=="Admin":
            bannername = request.form['bannername']
            bannerurl=request.form.getlist('bannerurl')
            bannerlink=request.form.getlist('bannerlink')
            createbanner = Banner(bannername=bannername)# Insert form data in collection
            createbanner.save()
            for x in range(len(bannerurl)):
                urls = BannerUrlLink(bannerurl[x],bannerlink[x])
                createbanner.imageurllink.append(urls)
                createbanner.save()
            logger.info('Sucessfully Created new in Collections')
            return redirect(url_for('banner'))
        else:
            db=[]
            for info in Banner.objects():
              for i in info.imageurllink:
                data={}
                data['id']=info.id
                data['bannername']=info.bannername
                data['bannerimageurl']=i.bannerimageurl
                data['bannerimagelink']=i.bannerimagelink
                db.append(data)
            logger.info('Sucessfully Created new in Collections')
            return render_template('banner.html', form=form,info=db)

@app.route('/banner_delete/', methods=['GET', 'POST'])
@login_required
def banner_delete():
    if current_user.usertype=="Admin":
        logger.info('Entered into user_delete')
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="i"):
            brand_info = Banner.objects.get(id=docid)
            brand_info.delete()
        logger.info('Sucessfully Deleted  %s  in Userlist',type)
        return redirect(url_for('banner'))

@app.route('/footer', methods = ['GET', 'POST'])
@login_required
def footer():
        logger.info('Entered into banner')
        with app.app_context():
            form = FooterForm()
        if request.method == 'POST' and form.validate():
          if current_user.usertype=="Admin":
            #return request.form['footername']
            footername = request.form['footername']
            footerurl=request.form.getlist('footerurl')
            footerlink=request.form.getlist('footerlink')
            #return footername
            createbanner = Footer(footername=footername)# Insert form data in collection
            createbanner.save()
            for x in range(len(footerurl)):
                urls = FooterUrlLink(footerurl[x],footerlink[x])
                createbanner.imageurllink.append(urls)
                createbanner.save()
            logger.info('Sucessfully Created new in Collections')
            return redirect(url_for('footer'))
        else:
            db=[]
            for info in Footer.objects():
              for i in info.imageurllink:
                data={}
                data['id']=info.id
                data['footername']=info.footername
                data['footerimageurl']=i.footerimageurl
                data['footerimagelink']=i.footerimagelink
                db.append(data)
            logger.info('Sucessfully Created new in Collections')
            return render_template('sitefooter.html', form=form,info=db)

@app.route('/footer_delete/', methods=['GET', 'POST'])
@login_required
def footer_delete():
    logger.info('Entered into footer delete')  
    if current_user.usertype=="Admin":
        logger.info('Entered into user_delete')
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="i"):
            brand_info = Footer.objects.get(id=docid)
            brand_info.delete()
        logger.info('Sucessfully Deleted  %s  in footer',type)
        return redirect(url_for('footer'))



@app.route('/header', methods = ['GET', 'POST'])
@login_required
def header():
        with app.app_context():
         form = HeadForm()
        if request.method == 'POST' and form.validate():
            headername = request.form['headername']
            headercontactno=request.form['headercontactno']
            headerlogo= request.form['headerlogo']
            headeinfo =Header(headername=headername,headercontactno=headercontactno,headerlogo=headerlogo) 
            headeinfo.save()
            logger.info('Sucessfully setup site header')
            return redirect(url_for('header'))
        else:
            Headerlist = Header.objects()
            logger.info('Sucessfully setup site header')
            return render_template('header.html',form=form,Headerlist=Headerlist)
            
@app.route('/header_delete/', methods=['GET', 'POST'])
@login_required
def header_delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="head"):
            header_info = Header.objects.get(id=docid)
            header_info.delete()
        logger.info('Deleted header in Site header setup')
        return redirect(url_for('header'))

@app.route('/review_verification', methods=['GET', 'POST'])
def review_verification():
    reviews=Reviews_info.objects()
    logger.info('Entered into review_verification')
    return render_template('reviews-varification.html',reviews=reviews)


@app.route('/review_actives/<id>')
def review_actives(id):
        userstatus = Reviews_info.objects.get(id=id)
        if userstatus.status == 'Created':
            userstatus.status = 'Active'
            userstatus.save()
        logger.info('Entered into review activation')
        return redirect(url_for('review_verification'))
    
@app.route('/review_reject/<id>')
def review_reject(id):
        userstatus = Reviews_info.objects.get(id=id)
        if userstatus.status == 'Created':
            userstatus.status = 'Reject'
            userstatus.save()
        logger.info('Entered into review reject')
        return redirect(url_for('review_verification'))


@app.route('/review_delete', methods=['GET', 'POST'])
def review_delete():
        type = request.args.get('type')
        docid = request.args.get('docid')
        if(type=="rev"):
            rev_info = Reviews_info.objects.get(id=docid)
            rev_info.delete()
        logger.info('Entered into review delete')
        return redirect(url_for('review_verification'))



#-------------------------------------------------------------------------------bulk prices download and upload-------------------
def get_priceinformation(url):
    sup=Sup_Upload.objects(status='Accept')
    prod_data=[]
    for prod in sup:
        if ProdinvWH.objects(prod_desc=prod.upload_name).count()>0:
            data={}
            data['Productname']=prod.upload_name
            for i in prod.prices:
                data['Landing_price']=i.landing_price
                data['Dealer_price']=i.dealer_price
                data['Enduser_price']=i.offer_price
                data['MRP']=i.enduser_price
                data['Bulkunit_price']=i.bulk_unit_price
                data['Bulk_qty']=i.bulk_qty
                data['Landing_price_gst']=i.landing_price_gst
                data['Dealer_price_gst']=i.dealer_price_gst
                data['Enduser_price_gst']=i.offer_price_gst
                data['MRP_gst']=i.enduser_price_gst
                data['Enduser_Discount']=i.percentage
                prod_data.append(data)      
    
    #print prod_data
    with open('pricesdownload.csv', 'wb+') as f:
         dict_writer = csv.DictWriter(f, fieldnames=['Productname','Landing_price','Dealer_price','Enduser_price','MRP','Bulkunit_price','Bulk_qty','Landing_price_gst','Dealer_price_gst','Enduser_price_gst','MRP_gst','Enduser_Discount'])
         dict_writer.writeheader()
         dict_writer.writerows(prod_data)
    return 'Download completely'

    
@app.route("/prices_download.csv")
def pricesdownload():
    url = ""
    get_priceinformation(url)
    logger.info('prices Downloaded successfully!')
    return send_file("pricesdownload.csv")

@app.route('/pricesbulkupload', methods = ['GET', 'POST'])
def pricesbulkupload():
    try:
        with app.app_context():
            form = PricesUploadfileForm()
        if request.method == 'POST':
            f = request.files['upload_file']
            stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
            reader = csv.DictReader(stream)
            header= ['Productname','Landing_price','Dealer_price','Enduser_price','MRP','Bulkunit_price','Bulk_qty','Landing_price_gst','Dealer_price_gst','Enduser_price_gst','MRP_gst','Enduser_Discount']
            for each  in reader:
                Productname=each['Productname']
                landing_price=each['Landing_price']
                dealer_price=each['Dealer_price']
                offer_price=each['Enduser_price']
                enduser_price=each['MRP']
                bulkunit_price=each['Bulkunit_price']
                bulk_qty=each['Bulk_qty']
                landing_price_gst=each['Landing_price_gst']
                dealer_price_gst=each['Dealer_price_gst']
                offer_price_gst=each['Enduser_price_gst']
                enduser_price_gst=each['MRP_gst']
                percentage=each['Enduser_Discount']
                #print type(percentage)
                for data in ProdinvWH.objects(prod_desc=Productname):
                    for j in data.prices:
                        j.landing_price=landing_price
                        j.dealer_price=dealer_price
                        j.offer_price=offer_price
                        j.enduser_price=enduser_price
                        j.bulk_unit_price=bulkunit_price
                        j.bulk_qty=bulk_qty
                        j.landing_price_gst=float(landing_price_gst)
                        j.dealer_price_gst=float(dealer_price_gst)
                        j.offer_price_gst=float(offer_price_gst)
                        j.enduser_price_gst=float(enduser_price_gst)
                        j.save()
                        
                for data in Sup_Upload.objects(upload_name=Productname):
                 for k in data.prices:
                        k.landing_price=landing_price
                        k.dealer_price=dealer_price
                        k.offer_price=offer_price
                        k.enduser_price=enduser_price
                        k.bulk_unit_price=bulkunit_price
                        k.bulk_qty=bulk_qty
                        k.landing_price_gst=float(landing_price_gst)
                        k.dealer_price_gst=float(dealer_price_gst)
                        k.offer_price_gst=float(offer_price_gst)
                        k.enduser_price_gst=float(enduser_price_gst)
                        k.percentage=float(percentage)
                        k.doubleoffer_price=float(offer_price)
                        k.save()
                
            return render_template('pricesupload_success.html')
        logger.info('Entered into Bulk Products upload')
        return render_template('bulk-prices-upload.html',form=form)
    except Exception as e:
       return jsonify('{"mesg":' + str(e) +'}')
    

#--------------------------------------------------------------latest order--------------------------------
@app.route('/latest_order', methods = ['GET', 'POST'])
def latest_order():
        logger.info('Entered into Customer Report')
        dealer=UserSignup.objects(usertype = 'Distributor/Dealer',status='Active')
        dealerlist=[]
        for i in dealer:
            #print i.id
            user=str(i.id)
            shop=Shopsetup.objects(user_id=user)
            #print shop.count()
            if shop.count()>0:
                #print 'hi'
                data={}
                data['id']=i.id
                data['username']=i.username
                dealerlist.append(data)
        #print dealerlist
        return render_template('latest-order.html',dealer=dealerlist)

@app.route('/latestorder_data', methods=['GET', 'POST'])
def latestorder_data():
    try:
        if request.method == 'POST':
             logger.info('Entered into Customer data')
             json_data = request.get_json(force=True)
             fromdate=json_data['fromdate']
             todate=json_data['todate']
             dealerid=json_data['dealer']
             #print dealerid
             fromdates = datetime.datetime.strptime(fromdate, "%Y-%m-%d")
             to = datetime.datetime.strptime(todate, "%Y-%m-%d")
             todates=to+ timedelta(1)
             detail=[]
             if dealerid=='0':
                 
                 customerdata=CustomerOrders.objects(created_date__lte=todates,created_date__gte=fromdates)
                 if customerdata.count()==0:
                        data={}
                        data['status']="fail"
                        detail.append(data)
                        return jsonify(detail) 
                 address=[]
                 for customer in customerdata:
                        shop=Shopsetup.objects(shop_name=customer.shop)
                        data={}
                        data['orderno']=customer.orderid
                        data['date']=customer.created_date.strftime('%d-%m-%Y')
                        data['shopid']=shop[0].shop_id
                        data['shopname']=shop[0].shop_name
                        data['status']=customer.status                    
                        detail.append(data)
             else:
                 shop=Shopsetup.objects(user_id=dealerid)
                 customerdata=CustomerOrders.objects(shop=shop[0].shop_name,created_date__lte=todates,created_date__gte=fromdates)
                 if customerdata.count()==0:
                        data={}
                        data['status']="fail"
                        detail.append(data)
                        return jsonify(detail) 
                 address=[]
                 for customer in customerdata:
                        data={}
                        data['orderno']=customer.orderid
                        data['date']=customer.created_date.strftime('%d-%m-%Y')
                        data['shopid']=shop[0].shop_id
                        data['shopname']=shop[0].shop_name
                        data['status']=customer.status
                        detail.append(data)

             return jsonify(detail)     
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')

		
@app.route('/latestorder_viewmore/<orderno>',methods = ['GET', 'POST'])
def latestorder_viewmore(orderno):
    
        detailess = CustomerOrders.objects.filter(orderid=orderno).first()
        shop=Shopsetup.objects(shop_name=detailess.shop)
        shopinfo= shop[0].dealer+','+shop[0].phone+','+shop[0].shop_address
        address=[]
        for j in detailess.shippingaddress:
            data={}
            data['shippingaddress']=j.firstname+','+j.lastname+','+j.house_no+','+j.street_address+','+j.city+','+j.state+','+j.postal_code+','+j.country+','+j.mobile+','+j.alt_mobile                        
            address.append(data)
        for k in detailess.billingaddress:
            data1={}
            data1['billingaddress']=k.firstname+','+k.lastname+','+k.house_no+','+k.street_address+','+k.city+','+k.state+','+k.postal_code+','+k.country+','+k.mobile+','+k.alt_mobile                        
            address.append(data1)
        #print address
        return render_template('latest-orderreport-viewmore.html',detailes=detailess,address=address,shopaddress=shopinfo)
#-----------------------cart list---------------------------

@app.route('/cartlist', methods = ['GET', 'POST'])
def cartlist():
        logger.info('Entered into Customer Report')
        data=CustomerDetails.objects()
        cartlist=[]
        item=0
        for info in data: 
            for cartdata in InitiateOrders.objects(user_id=str(info.id)):
                    item += 1
                    data={}
                    data['sno']=item
                    data['name']=info.firstname
                    data['id']=str(info.id)
                    data['email']=info.email
                    data['mobile']=info.mobile
                    cartlist.append(data)               
        return render_template('cartlist.html',cartlist=cartlist)


@app.route('/cartviewmore/<id>',methods = ['GET', 'POST'])
def cartviewmore(id):
    
        data= InitiateOrders.objects.filter(user_id=id).first()  
        return render_template('cartlist-viewmore.html',data=data)

@app.route('/promotion',methods = ['GET', 'POST'])
def promotion():
        with app.app_context():
            form = Promotions()
        if request.method == 'POST':
            content= request.form['content']
            user=CustomerDetails.objects(user_type__ne='shop',email="sivajitc@gmail.com")       
            emailList=[]
            for i in user:
                data={}
                data['email']=i.email
                data['username']=i.firstname
                emailList.append(data)
            for mail in  emailList:
                
                fo = open("./static/mailtemp/promotionmailtemp.html", "r+")
                htmlbody = fo.read()
                fo.close()
                urldata=content
                username=mail['username']
                #print username
                htmlbody = htmlbody.replace("$$username$$",username)
                htmlbody = htmlbody.replace("$$urldata$$",urldata)
                sendMail(mail['email'],'Shop My Tools Promotions',htmlbody)
            #print content
            return redirect(url_for('promotion'))
        return render_template('promotions.html',form=form)



#----------------------------------------------------for care------------------------------------------------------
@app.route('/user_data', methods=['GET', 'POST'])
def user_data():
    json_data = request.get_json(force=True)
    user=json_data['loginid']
    password=json_data['password']
    user_type=json_data['usertype']
    user_data=[]
    if '@' in user:
        dbUser = UserSignup.objects(email=user,usertype=user_type)
        if dbUser.count()==0:
            print "fhsdjfh"
            return jsonify({"status":"Fail"})
        dbPassword = str(dbUser[0].password)
        print dbPassword
        if check_password_hash(dbPassword,password):
            user_details={}
            user_details['username']=dbUser[0].username
            user_details['mobile']=dbUser[0].mobile
            user_details['email']=user
            user_data.append(user_details)
            return jsonify({"status":"Success","data":user_data})
        else:
            print "fail"
            return jsonify({"status":"Fail"})
          
    else:
         dbUser = UserSignup.objects(mobile=user)
         if dbUser.count()==0:
             return jsonify({"status":"Fail"})
         dbPassword = str(dbUser[0].password)
         if check_password_hash(dbPassword,password):
              user_details={}
              user_details['username']=dbUser[0].username
              user_details['email']=dbUser[0].email
              user_details['mobile']=user
              user_data.append(user_details)
              return jsonify({"status":"Success","data":user_data})
         else:
               return jsonify({"status":"Fail"})

            
@app.route('/shop_user_data', methods=['GET', 'POST'])
def shop_user_data():
    json_data = request.get_json(force=True)
    user=json_data['loginid']
    password=json_data['password']
    user_data=[]
    if '@' in user:
        dbUser = ShopUser.objects(email=user)
        if dbUser.count()==0:
            print "fhsdjfh"
            return jsonify({"status":"Fail"})
        dbPassword = str(dbUser[0].password)
        print dbPassword
        if check_password_hash(dbPassword,password):
            user_details={}
            user_details['username']=dbUser[0].username
            user_details['mobile']=dbUser[0].mobile
            user_details['email']=user
            user_data.append(user_details)
            return jsonify({"status":"Success","data":user_data})
        else:
            print "fail"
            return jsonify({"status":"Fail"})
          
    else:
         dbUser = ShopUser.objects(mobile=user)
         if dbUser.count()==0:
             return jsonify({"status":"Fail"})
         dbPassword = str(dbUser[0].password)
         if check_password_hash(dbPassword,password):
              user_details={}
              user_details['username']=dbUser[0].username
              user_details['email']=dbUser[0].email
              user_details['mobile']=user
              user_data.append(user_details)
              return jsonify({"status":"Success","data":user_data})
         else:
               return jsonify({"status":"Fail"})

#----------------------------------------------------for care------------------------------------------------------    

if __name__ == '__main__':
    now = datetime.date.today().strftime("%Y_%m_%d")
    handler = RotatingFileHandler("loggers/applogs/"+"app_" + str(now) + ".log", maxBytes=100000, backupCount=3)
    logger = logging.getLogger('__name__')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    app.run(host="127.0.0.1",port=8000,threaded=True)
