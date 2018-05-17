#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from app import Flask, request, url_for, redirect, render_template, abort , Response,session,jsonify,flash
from form import DealerForm,SupplierForm,ContractorForm,ServiceForm
from models import Reg_Dealer,UserSignup,Reg_Supplier,Goods,Reg_Service,Reg_Contractor,Sup_Upload,atr,Country,State,City
from controler import SignUpControler
from flask_login  import login_user , logout_user , current_user , login_required
from flask_login  import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import json,time, os,ast,sys
import PIL.Image
sys.modules['Image'] = PIL.Image
from os import path
sys.setrecursionlimit(1000)
import requests
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
import datetime
import urllib2,urllib
from multiprocessing import Pool
import traceback
import threading
import functools

regapp = Flask(__name__)
regapp.secret_key = 'secret'

login_manager = LoginManager()
login_manager.init_app(regapp)
login_manager.session_protection = "strong"
regapp.config['Mainurl']='http://127.0.0.1:8000/'

regapp.config['NOTIFICATIONS']='True'
regapp.config['SMS']='True'

def synchronized(wrapped):
    lock = threading.Lock()
    @functools.wraps(wrapped)
    def _wrap(*args, **kwargs):
        with lock:
            return wrapped(*args, **kwargs)
    return _wrap

def sendMail(email,subject,htmlbody):
    if regapp.config['NOTIFICATIONS']=='True':
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
        
    if(regapp.config['SMS'])=='True':
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

@regapp.after_request
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

@regapp.errorhandler(Exception)
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


@regapp.route('/reg_dealer/<userid>', methods = ['GET', 'POST'])
#@login_required
def reg_dealer(userid):
        pool = Pool()
        pool_new(pool)
        uservalue = UserSignup.objects.get(id=userid)
        login_user(uservalue, remember=True)
        if current_user.usertype=='Distributor/Dealer':
         with regapp.app_context():
            form = DealerForm()
        if request.method == 'POST' and form.validate():
            controler  = SignUpControler()
            result = controler.regDealerCotrl(request)
            if result=="Fail":
                 logger.info('Failed to Dealer Registration ')
                 return render_template('error.html',msg=str('ShopName Existed'))
            registeredUser = Reg_Dealer.objects(dealer_mail=current_user.email)
            if registeredUser.count() > 0:
              fo = open("./static/mailtemp/signup_email.html", "r+")
              htmlbody = fo.read()
              fo.close()
              urldata='Your registration process is  in progress. Our marketing team will contact and update shortly. '
              url=urldata.encode('ascii','ignore')
              htmlbody = htmlbody.replace("$$urldata$$",url)
              #sendMail(registeredUser[0].dealer_mail,'Dealer have registered successfully',htmlbody)
              pool.apply_async(sendMail,[registeredUser[0].dealer_mail,'Our marketing team is verifying the details. Will get back to you shortly',htmlbody])
              msg="Your registration process is  in progress. Our marketing team will contact and update shortly. "
              
              #mobile='91'+registeredUser[0].dealer_mobile
              mobileList=[]
              mobileList.append(registeredUser[0].dealer_isd+registeredUser[0].dealer_mobile)
              #SMS(msg,mobile)
              pool.apply_async(SMS,[msg,mobileList])
              registeredUser1 = UserSignup.objects(usertype="Admin")
              fo = open("./static/mailtemp/suppliermailtemp.html", "r+")
              htmlbody = fo.read()
              fo.close()
              adminmail=registeredUser1[0].email
              urldata='New user '+registeredUser[0].dealer_name+' is registered. Login and confirm the user details.'
              htmlbody = htmlbody.replace("$$urldata$$",urldata)                 
              pool.apply_async(sendMail,[adminmail,'New user registration under review',htmlbody])
              msg='New user '+registeredUser[0].dealer_name+' is registered. Login and confirm the user details.'
              mobileList=[]
              mobileList.append("91"+registeredUser1[0].mobile)             
              pool.apply_async(SMS,[msg,mobileList])
              logger.info('Dealer Registration Sucessfully')
              return render_template('error.html',form=form,reportsof = 'Dealer have registered sucessfully',msg="Thank you, <br> Please check your Email and Mobile.",userinfo=current_user)
            else:
              form.email.errors.append("Email not available with us!")
              return render_template('error.html',form=form,reportsof = 'Email not available with us!')
        else:
            empDetails = UserSignup.objects.get(email = current_user.email)
            form.dealer_name.data = empDetails.username
            form.dealer_mail.data = empDetails.email
            form.dealer_mobile.data = empDetails.mobile
            form.dealer_email.data = empDetails.email
            country=Country.objects()
            return render_template('dealer-register.html',form=form,countrylist=country)        
        return render_template('error.html',reportsof = 'Unauthorized out ....')
 
@regapp.route('/reg_supplier/<userid>', methods = ['GET', 'POST'])
#@login_required
def reg_supplier(userid):
       pool = Pool()
       pool_new(pool)
       uservalue = UserSignup.objects.get(id=userid)
       login_user(uservalue, remember=True)
       if current_user.usertype=='Supplier':    
        with regapp.app_context():
            form = SupplierForm()
        if request.method == 'POST' and form.validate():
            controler  = SignUpControler()
            result = controler.regSupplierCotrl(request)
            if result=="Fail":
                logger.info('Failed to Supplier Registration ')
                return render_template('error.html',reportsof = 'Registration Failed')
            registeredUser = Reg_Supplier.objects(supplier_mail=current_user.email)
            if registeredUser.count() > 0:
              fo = open("./static/mailtemp/suppliermailtemp.html", "r+")
              htmlbody = fo.read()
              fo.close()
              urldata="Your registration process is  in progress. Our marketing team will contact and update shortly. "
              htmlbody = htmlbody.replace("$$urldata$$",urldata)
              #sendMail(registeredUser[0].supplier_mail,'Supplier have registered successfully',htmlbody)
              pool.apply_async(sendMail,[registeredUser[0].supplier_mail,'Our marketing team is verifying the details. Will get back to you shortly',htmlbody])
              msg="Your registration process is  in progress. Our marketing team will contact and update shortly. "
              #mobile='91'+registeredUser[0].supplier_mobile
              mobileList=[]
              mobileList.append(registeredUser[0].supplier_isd+registeredUser[0].supplier_mobile)
              #SMS(msg,mobile)
              pool.apply_async(SMS,[msg,mobileList])
              logger.info('Supplier Registration Sucessfully')
              registeredUser1 = UserSignup.objects(usertype="Admin")
              fo = open("./static/mailtemp/suppliermailtemp.html", "r+")
              htmlbody = fo.read()
              fo.close()
              adminmail=registeredUser1[0].email
              #print adminmail
              urldata='New user '+registeredUser[0].supplier_name+' is registered. Login and confirm the user details.'
              htmlbody = htmlbody.replace("$$urldata$$",urldata)
              #sendMail(email,'Supplier Verification & Approval',htmlbody)
              pool.apply_async(sendMail,[adminmail,'New user registration under review',htmlbody])
              msg='New user '+registeredUser[0].supplier_name+' is registered. Login and confirm the user details.'
              mobileList=[]
              mobileList.append("91"+registeredUser1[0].mobile)
              #SMS(msg,mobileList)
              pool.apply_async(SMS,[msg,mobileList])
              return render_template('error.html',form=form,reportsof = 'Supplier have registered sucessfully',msg="Thank you, <br> Please check your Email and Mobile.",userinfo=current_user)
            else:
              form.email.errors.append("Email not available with us!")
              return render_template('error.html',form=form,reportsof = 'Email not available with us!')
        else:
            empDetails = UserSignup.objects.get(email = current_user.email)
            form.supplier_name.data = empDetails.username
            form.supplier_mail.data = empDetails.email
            form.supplier_mobile.data = empDetails.mobile
            form.supplier_email.data = empDetails.email
            country=Country.objects()
            #print i.country_std_isd    
            return render_template('supplier-register.html',form=form,country=country)
       return render_template('error.html',reportsof = 'Unauthorized out ....')

@regapp.route('/state_service', methods=['GET', 'POST'])
def state_service():
    try:
        country=request.args.get('countryname')
        countyname=country.split("_")[0]
        statelist=[]
        for statename in State.objects(countryname=countyname):
            statelist.append(statename.state)
            
        states=sorted(statelist)
        return jsonify(statelist)
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')    

@regapp.route('/city_post/', methods=['GET', 'POST'])
@login_required
def city_post():
    try:
       country=request.args.get('country')
       countyname=country.split("_")[0]
       state=request.args.get('state')
       citylist=[]
       for cityname in City.objects(countryname=countyname,state=state):
                citylist.append(cityname.city)
       cities=sorted(citylist)
       return jsonify(cities)
           
    except Exception as e:
        return jsonify('{"mesg":' + str(e) +'}')    

'''    
@regapp.route('/reg_service/<userid>', methods = ['GET', 'POST'])
def reg_service(userid):
      uservalue = UserSignup.objects.get(id=userid)
      login_user(uservalue, remember=True)
      if current_user.usertype=='Service Center':
        with regapp.app_context():
            serviceForm = ServiceForm()
        if request.method == 'POST' and serviceForm.validate():
            controler  = SignUpControler()
            result = controler.regServiceCotrl(request)
            if result=="Fail":
                logger.info('Failed to Service Registration ')
                return render_template('error.html',reportsof = 'Registration Failed')
            logger.info('Service Registration Sucessfully')
            return render_template('reg_success.html')
        else:
            empDetails = UserSignup.objects.get(email = current_user.email)
            serviceForm.service_name.data = empDetails.username
            serviceForm.service_mail.data = empDetails.email
            serviceForm.service_mobile.data = empDetails.mobile
            return render_template('servicecenter-register.html',serviceForm=serviceForm)
      return render_template('error.html',reportsof = 'Unauthorized out ....')
  
@regapp.route('/reg_contractor/<userid>', methods = ['GET', 'POST'])
def reg_contractor(userid):
      uservalue = UserSignup.objects.get(id=userid)
      login_user(uservalue, remember=True)
      if current_user.usertype=='Contractor/Industrialist':
        with regapp.app_context():
            contractorForm = ContractorForm()
        if request.method == 'POST' and contractorForm.validate():
            controler  = SignUpControler()
            result = controler.regContractorCotrl(request)
            if result=="Fail":
                logger.info('Failed to Contractor Registration ')
                return render_template('error.html',reportsof = 'Registration Failed')
            logger.info('Contractor Registration Sucessfully')
            return render_template('reg_success.html')       
        else:
            empDetails = UserSignup.objects.get(email = current_user.email)
            contractorForm.contractor_name.data = empDetails.username
            contractorForm.contractor_mail.data = empDetails.email
            contractorForm.contractor_mobile.data = empDetails.mobile
            return render_template('contractor-register.html',contractorForm=contractorForm)
      return render_template('error.html',reportsof = 'Unauthorized out ....')
 '''  
# somewhere to logout
@regapp.route("/logout")
def logout():
    logout_user()
    logger.info('User Logout Sucessfully')
    return redirect(regapp.config['Mainurl'])



if __name__ == '__main__':
    now = datetime.date.today().strftime("%Y_%m_%d")
    handler = RotatingFileHandler("loggers/regapplogs/"+"regapp_" + str(now) + ".log", maxBytes=100000, backupCount=3)
    logger = logging.getLogger('__name__')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    regapp.run(host='127.0.0.1',port='5002',threaded=True)
