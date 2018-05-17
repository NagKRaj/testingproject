
from models import Reg_Dealer,UserSignup,Reg_Supplier,Goods,Reg_Service,Reg_Contractor,Sup_Upload,atr
from flask_login  import current_user 

class SignUpControler(object):
        
    def regDealerCotrl(self,request):
        try:
            dealer_name = request.form['dealer_name']
            dealer_shopname = request.form['dealer_shopname']
            reg_shopname=request.form['reg_shopname']
            dealer_cin=request.form['dealer_cin']
            dealer_address=request.form['dealer_address']
            dealer_country = request.form.get('country')
            country=dealer_country.split("_")[0]
            isd=dealer_country.split("_")[1]
            dealer_state = request.form.get('state')
            dealer_city = request.form.get('city')
            dealer_town = request.form['dealer_town']
            dealer_pin = request.form['dealer_pin']
            dealer_phone = request.form['dealer_phone']
            dealer_mail = request.form['dealer_mail']
            dealer_gstin = request.form['dealer_gstin']
            dealer_pan = request.form['dealer_pan']
            dealer_contactname = request.form['dealer_contactname']
            dealer_mobile = request.form['dealer_mobile']
            dealer_email = request.form['dealer_email']

            iscompanyExist=Reg_Dealer.objects(dealer_shopname=dealer_shopname)
            iscinExist=Reg_Dealer.objects(dealer_cin=dealer_cin)
            isgstinExist=Reg_Dealer.objects(dealer_gstin=dealer_gstin)
            ispanExist=Reg_Dealer.objects(dealer_pan=dealer_pan)
            '''if iscompanyExist.count()>0:
                 return  'Fail'             
            elif iscinExist.count()>0:
                  return 'Fail'
            elif isgstinExist.count()>0:
                  return 'Fail'
            elif ispanExist.count()>0:
                  return 'Fail' '''
            dealerUser = Reg_Dealer(user_id=str(current_user.id),dealer_name=dealer_name,dealer_shopname=dealer_shopname,reg_shopname=reg_shopname, dealer_cin=dealer_cin, dealer_address=dealer_address,dealer_country=country,dealer_state=dealer_state,
                                    dealer_city =dealer_city,dealer_town=dealer_town,dealer_pin=dealer_pin,dealer_isd=isd,dealer_phone=dealer_phone,dealer_mail=dealer_mail.lower(),dealer_pan=dealer_pan,
                                    dealer_gstin=dealer_gstin,dealer_contactname=dealer_contactname,dealer_mobile=dealer_mobile,dealer_email=dealer_email.lower())# Insert form data in collection
            dealerUser.save()
            users = UserSignup.objects.get(id = current_user.id)
            users.status = 'Review'
            users.save()
            return str("Success")
            
        except Exception as e:
            return str("Fail")

    def regSupplierCotrl(self,request):
        try:
            supplier_name = request.form['supplier_name']
            supplier_companyname=request.form['supplier_companyname']
            supplier_cin=request.form['supplier_cin']
            supplier_address=request.form['supplier_address']
            supplier_country = request.form.get('country')
            country=supplier_country.split("_")[0]
            isd=supplier_country.split("_")[1]
            #print supplier_country
            supplier_state = request.form.get('state')
            supplier_city = request.form.get('city')
            supplier_town = request.form['supplier_town']
            supplier_pin = request.form['supplier_pin']
            supplier_phone = request.form['supplier_phone']
            supplier_mail = request.form['supplier_mail']
            supplier_gstin = request.form['supplier_gstin']
            supplier_pan = request.form['supplier_pan']
            supplier_brand = request.form.getlist('brand')
            supplier_tm = request.form.getlist('supplier_tm')
            supplier_contactname = request.form['supplier_contactname']
            supplier_mobile = request.form['supplier_mobile']
            supplier_email = request.form['supplier_email']
            #iscompanyExist=Reg_Supplier.objects(supplier_companyname=supplier_companyname)
            #iscinExist=Reg_Supplier.objects(supplier_cin=supplier_cin)
            #isgstinExist=Reg_Supplier.objects(supplier_gstin=supplier_gstin)
            #ispanExist=Reg_Supplier.objects(supplier_pan=supplier_pan)
            
            '''if iscompanyExist.count()>0:
                return  'Fail'
            elif iscinExist.count()>0:
                 return  'Fail'
            elif isgstinExist.count()>0:
                 return  'Fail'
            elif ispanExist.count()>0:
                 return  'Fail'''
            #return isd
            supplierUser = Reg_Supplier(user_id=str(current_user.id),supplier_name=supplier_name,supplier_companyname=supplier_companyname, supplier_cin=supplier_cin,
                                        supplier_address=supplier_address, supplier_country=country,supplier_state=supplier_state,
                                        supplier_city =supplier_city,supplier_town=supplier_town,supplier_pin=supplier_pin,supplier_isd=isd,supplier_phone=supplier_phone,
                                        supplier_mail=supplier_mail.lower(),supplier_gstin=supplier_gstin,supplier_pan=supplier_pan,supplier_contactname=supplier_contactname,
                                        supplier_mobile=supplier_mobile,supplier_email=supplier_email.lower(),supplier_id='0')# Insert form data in collection

            
            supplierUser.save()  
            for x in range(len(supplier_brand)):
                goods = Goods(supplier_brand[x], supplier_tm[x])
                supplierUser.supplier_brands.append(goods)
                supplierUser.save()
                
            user = UserSignup.objects.get(id = current_user.id)
            user.status = 'Review'
            user.save()
            return str("Success")
        except Exception as e:
            return str("Fail")



    

    def regContractorCotrl(self,request):
        try:
            contractor_name = request.form['contractor_name']
            contractor_cin=request.form['contractor_cin']
            contractor_address=request.form['contractor_address']
            contractor_country = request.form.get('country')
            contractor_state = request.form.get('state')
            contractor_city = request.form.get('city')
            contractor_town = request.form['contractor_town']
            contractor_pin = request.form['contractor_pin']
            contractor_phone = request.form['contractor_phone']
            contractor_pan = request.form['contractor_pan']
            contractor_tin = request.form['contractor_tin']
            contractor_mail = request.form['contractor_mail']
            contractor_worklocation = request.form['contractor_worklocation']
            contractor_areaofwork = request.form['contractor_areaofwork']
            contractor_workperiod = request.form['contractor_workperiod']
            contractor_contactname = request.form['contractor_contactname']
            contractor_mobile = request.form['contractor_mobile']
            contractor_email = request.form['contractor_email']
            contractorUser = Reg_Contractor(user_id=str(current_user.id),contractor_name=contractor_name, contractor_cin=contractor_cin, contractor_address=contractor_address,contractor_country=contractor_country,contractor_state=contractor_state,contractor_city =contractor_city,contractor_town=contractor_town,contractor_pin=contractor_pin,contractor_phone=contractor_phone,contractor_pan=contractor_pan,contractor_tin=contractor_tin,contractor_mail=contractor_mail,contractor_worklocation=contractor_worklocation,contractor_areaofwork=contractor_areaofwork,contractor_workperiod=contractor_workperiod,contractor_contactname=contractor_contactname,contractor_mobile=contractor_mobile,contractor_email=contractor_email)# Insert form data in 
            contractorUser.save()
            use = UserSignup.objects.get(id = current_user.id)
            use.status = 'Review'
            use.save()
            return str("Success")
        except Exception as e:
            return str("Fail")

       
class DashboardLink(object):
        
    def dashboardLink(self,request):
        try:
          return 'Hi'  
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
        except Exception as e:
            return str("Fail")    
            
