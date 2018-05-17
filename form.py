#!/usr/bin/env python2.7
from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField,PasswordField,FileField, SelectMultipleField,FieldList,StringField
from wtforms import validators, ValidationError, HiddenField
import datetime
from flask_wtf.file import FileField, FileAllowed, FileRequired,DataRequired
from flask_ckeditor import CKEditorField

myChoices = [('User Type','User Type'),('Distributor/Dealer','Distributor/Dealer'),('Supplier', 'Supplier')]
typef = [('Flat','Flat'),('%','%')]
country = [('Select Country', 'Select Country'),('India','India'),('China','China')]
state= [('Select State', 'Select State'),('ANDAMAN AND NICOBAR ISLANDS', 'ANDAMAN AND NICOBAR ISLANDS'),('ANDHRA PRADESH','ANDHRA PRADESH'),('ARUNACHAL PRADESH','ARUNACHAL PRADESH'),('ASSAM','ASSAM'),('BIHAR','BIHAR'),('CHANDIGARH','CHANDIGARH'),('CHHATTISGARH','CHHATTISGARH'),('DADRA AND NAGAR HAVELI','DADRA AND NAGAR HAVELI'),('DAMAN AND DIU','DAMAN AND DIU'),('DELHI','DELHI'),('GOA','GOA'),('GUJARAT','GUJARAT'),('HARYANA','HARYANA'),('HIMACHAL PRADESH','HIMACHAL PRADESH'),('JAMMU AND KASHMIR','JAMMU AND KASHMIR'),('JHARKHAND','JHARKHAND'),('KARNATAKA','KARNATAKA'),('KERALA','KERALA'),('LAKSHADWEEP','LAKSHADWEEP'),('MADHYA PRADESH','MADHYA PRADESH'),('MAHARASHTRA','MAHARASHTRA'),('MANIPUR','MANIPUR'),('MEGHALAYA','MEGHALAYA'),('MIZORAM','MIZORAM'),('NAGALAND','NAGALAND'),('ORISSA','ORISSA'),('PONDICHERRY','PONDICHERRY'),('PUNJAB','PUNJAB'),('RAJASTHAN','RAJASTHAN'),('SIKKIM','SIKKIM'),('TAMIL NADU','TAMIL NADU'),('TELANGANA','TELANGANA'),('TRIPURA','TRIPURA'),('UTTAR PRADESH','UTTAR PRADESH'),('UTTARANCHAL','UTTARANCHAL'),('WEST BENGAL','WEST BENGAL')]
area=[('Select area of work', 'Select area of work'),('Airport','Airport'),('Construction','Construction'),('Harbours','Harbours'),('Highways','Highways'),('Manufacture','Manufacture'),('Mining','Mining'),('Oil & Refinery','Oil & Refinery'),('Roads','Roads'),('Others','Others')]
work= [('Select work period', 'Select work period'),('< 6 M','< 6 M'),(' 6 M','6 M'),(' > 6 M',' > 6 M')]
Category=[('Select Category', 'Select Category'),('Option1', 'Option1'),('Option2','Option2')]
Subcategory=[('Select Sub category', 'Select Sub category'),('Option1', 'Option1'),('Option2','Option2'),('Option3','Option3')]
brand=[('Select brand', 'Select brand'),('Option1', 'Option1'),('Option2','Option2'),('Option3','Option3')]
location=[('0', 'Select Location'),('Hyderabad', 'Hyderabad')]
SelectTax=[('Select Tax', 'Select Tax'),('VAT', 'VAT'),('GST','GST')]
SelectDiscount=[('Select Discount', 'Select Discount'),('Special Discount', 'Special Discount')]
frequency=[('0', 'Select Frequency'),('Fast Moving', 'Fast Moving'),('Medium','Medium'),('Slow','Slow'),('N/A','N/A')]
userlist= [('User Type','User Type'),('Director','Director'),('Manager', 'Manager'),('Puchase Manager', 'Purchase Manager'),('WH-Manager', 'WH-Manager'),('Marketing-Manager', 'Marketing-Manager')]
brandtypelist= [('Brand Type','Brand Type'),('Top Brands','Top Brands'),('Emerging Brands', 'Emerging Brands')]

class UserRegistration(FlaskForm):
    userid = HiddenField("userid")
    #id=TextField("ID",[validators.Required("Please enter your ID."),validators.Length(min=3, max=10,message=("ID must be between 3 to 10"))])
    username = TextField("User Name",[validators.Required("Enter user name (e.g. James)"),validators.Length(min=3, max=15,message=("Minimum 3 to Maximum 15 characters"))])
    email = TextField("Email",[validators.Required("Enter email id (e.g. abcd@gmail.com)"),validators.Email("Invalid email id")])
    std_isd = TextField("std_isd",[validators.Required("Enter STD/ISD (e.g. 91)"),validators.length(min=2, max=3,message=("Minimum 2 to Maximum 3 digits"))])
    mobile = TextField("Mobile",[validators.Required("Enter mobile number (e.g. 98888888881)")])
    password = PasswordField("Password",[validators.Required("Enter password"),validators.Length(min=8,message=("Enter a combination of atleast 8 letters (1 upper case, 1 lower case), 1 number and 1 special character (_ ! @ # - $ % ^ . & * =)")),validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm password')
    usertype = SelectField('Department', choices=myChoices)

    
class LoginForm(FlaskForm):
    loginid = TextField("Login ID",[validators.Required("Enter your mobile number or email")])
    password = PasswordField("Password",[validators.Required("Password"),validators.Length(min=8,message=("Wrong password"))])
   
class DealerForm(FlaskForm):
   dealer_name = TextField(" Name",[validators.Required("Enter name"),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
   #dealer_shopname = TextField(" Shop Name",[validators.Required("Enter shop name"),validators.Length(min=3, max=50,message=("Shop Name Minimum 3 to Maximum 50 characters"))])
   dealer_cin = TextField("CIN")
   dealer_shopname = TextField("Shop Name",[validators.Required("Enter shop name"),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
   reg_shopname = TextField("Shop Name",[validators.Required("Enter shop name"),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 150 characters (Symbols .,#&/- allowed)"))])
   dealer_address = TextAreaField("Address",[validators.Required("Enter address (Plot No., Street Name, Area Name, City, State, PIN Code, Country) "),validators.Length(min=3, max=150,message=("Minimum 3 to Maximum 150 characters"))])
   country= TextField("Country",[validators.Required("Select country.")])
   state= TextField("State",[validators.Required("Select state.")])
   city = TextField("City",[validators.Required("Select city.")])
   dealer_town= TextField("Town",[validators.Required("Enter district."),validators.Length(max=15,message=("Minimum 3 to Maximum 25 characters  "))])
   dealer_pin = TextField("Pin",[validators.Required("Enter pin code (e.g. 500036)"),validators.Length(max=6,message=("Invalid pincode"))])
   dealer_phone=TextField("Enter  mobile or land line number")
   dealer_mail=TextField("Mail",[validators.Required("Enter email"),validators.Email("Enter email")])
   dealer_gstin = TextField(" GSTIN ",[validators.Required("Enter GSTIN number (e.g. 36AAGCG4402R3ZA)"),validators.Length(max=15,message=("Invalid number"))])
   dealer_pan = TextField(" Pan",[validators.Required("Enter PAN number ( e.g. CDBPP4936L)"),validators.Length(max=10,message=("Invalid PAN number"))])
   dealer_contactname=TextField(" Name",[validators.Required("Enter name"),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 25 characters"))])
   dealer_mobile=TextField("Mobile",[validators.Required("Enter mobile number")])
   dealer_email=TextField("Email",[validators.Required("Enter email"),validators.Email("Enter email")])

class SupplierForm(FlaskForm):
   supplier_name = TextField(" Name",[validators.Required("Enter name"),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
   supplier_companyname = TextField(" supplier_companyname",[validators.Required("Enter company name"),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
   supplier_cin = TextField("CIN")
   supplier_address = TextAreaField("Address",[validators.Required("Enter address (Plot No., Street Name, Area Name, City, State, PIN Code, Country)"),validators.Length(max=150,message=("Minimum 3 to Maximum 150 characters"))])
   country= TextField("Country",[validators.Required("Select country.")])
   state= TextField("State",[validators.Required("Select state.")])
   city = TextField(" City",[validators.Required("Select city.")])
   supplier_town= TextField(" Town",[validators.Required("Enter district."),validators.Length(max=15,message=("Minimum 3 to Maximum 25 characters "))])
   supplier_pin = TextField(" Pin",[validators.Required("Enter pin code (e.g. 500036)"),validators.Length(max=6,message=("Invalid pincode"))])
   supplier_phone=TextField("Phone")
   supplier_mail=TextField("Mail",[validators.Required("Enter email "),validators.Email("Enter email ")])
   supplier_gstin = TextField(" supplier_gstin",[validators.Required("Enter GSTIN number (e.g. 36AAGCG4402R3ZA)"),validators.Length(max=15,message=("Invalid number"))])
   supplier_pan = TextField(" Pan",[validators.Required("Enter PAN number ( e.g. CDBPP4936L)"),validators.Length(max=10,message=("Invalid PAN number"))]) 
   brand = TextField(" Brand",[validators.Required("Enter brand.")])
   supplier_tm = TextField(" TM No",[validators.Required("Enter trade mark number"),validators.Length(max=7,message=("Only 7 digits are allowed"))])
   supplier_contactname=TextField(" Name",[validators.Required("Enter name"),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
   supplier_mobile=TextField("Mobile",[validators.Required("Enter mobile number")])
   supplier_email=TextField("Email",[validators.Required("Enter email "),validators.Email("Enter email ")])
   
class ServiceForm(FlaskForm):
   service_center = TextField("Service Center",[validators.Required("Enter service center")])
   service_center_area = TextField("Service Center Area",[validators.Required("Enter service center area")])
   

class ContractorForm(FlaskForm):
   contractor_name = TextField(" Name",[validators.Required("Please enter your Name."),validators.Length(min=2, max=25,message=("Name must be between 2 to 25"))])
   contractor_cin = TextField(" CIN",[validators.Required("Please enter valid CIN Number"),validators.Length(max=21,message=("CIN must be 21"))])
   contractor_address = TextAreaField("Address",[validators.Required("Please enter the Permanent Address"),validators.Length(max=60,message=("Address Should be max 60 Characters"))])
   contractor_country = SelectField('Country', choices=country)
   contractor_state = SelectField('State:', choices=state)
   contractor_city = TextField(" City",[validators.Required("Enter City."),validators.Length(min=2, max=20,message=("City must be between 2 to 20"))])
   contractor_town = TextField(" Town",[validators.Required("Enter Town."),validators.Length(max=15,message=("Town must be 15"))])
   contractor_pin = TextField(" Pin",[validators.Required("Enter valid Pin Code"),validators.Length(max=6,message=("Pin Code should be 6 digits"))])
   contractor_phone=TextField("Phone",[validators.Required("Please provide the valid Mobile Number of 10 digits/Please provide the valid Landline Number of 11 digits")])
   contractor_pan = TextField(" Pan",[validators.Required("Please enter valid PAN Number"),validators.Length(max=10,message=("Please enter valid PAN Number"))])
   contractor_tin = TextField(" Tin",[validators.Required("Please enter valid TIN Number"),validators.Length(max=11,message=("Only  11 digits are allowed"))])
   contractor_mail=TextField("Mail",[validators.Required("Please enter your Email "),validators.Email("Please enter your Email ")])
   contractor_worklocation=TextField("ExpWorklocation",[validators.Required("Please enter Work Location"),validators.Length(max=20,message=("Please enter Work Location"))])
   contractor_areaofwork=SelectField('Areaofwork', choices=area)
   contractor_workperiod=SelectField('WorkPeriod', choices=work)
   contractor_contactname=TextField(" Name",[validators.Required("Please enter your Name"),validators.Length(min=3, max=50,message=("Name Should be between 3 to 50 Characters"))])
   contractor_mobile=TextField("Mobile",[validators.Required("Please provide the valid Mobile Number of 10 digits")])
   contractor_email=TextField("Email",[validators.Required("Please enter your Email "),validators.Email("Please enter your Email ")])


class ForgotPassword(FlaskForm):
    email = TextField("Email",[validators.Required("Enter email id"),validators.Email("This email Id is not registered with us")])

class ResetPassword(FlaskForm):
    userid = HiddenField("userid")
    password = PasswordField("Set Password",[validators.Required("Enter password."),validators.Length(min=8, max=32,message=("Enter a combination of atleast 8 letters (1 upper case, 1 lower case), 1 number and 1 special character (_ ! @ # - $ % ^ . & * =)")),validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm password')

class MasterproductForm1(FlaskForm):
   categoryid = TextField(" categoryid",[validators.Required("Enter ID no."),validators.Length(min=3, max=21,message=("Minimum 3 to Maximum 21 characters"))])
   categoryname = TextField(" Categoryname",[validators.Required("Enter category"),validators.Length(min=3,max=50,message=("Minimum 3 to Maximum 50 characters"))])
   tags=TextAreaField("tags")
   metadescription=TextAreaField("metadescription")
   keywords=TextAreaField("keywords")
   

class MasterproductForm2(FlaskForm):
   categoryname = TextField(" categoryname",[validators.Required("Select category")])
   subcategoryid = TextField(" subcategoryid",[validators.Required("Enter sub category ID"),validators.Length(min=3, max=21,message=("Minimum 3 to Maximum 21 characters"))])
   subcategory = TextField(" subcategory",[validators.Required("Select sub category")])
      
class MasterproductForm3(FlaskForm):
   productid = TextField(" productid",[validators.Required("Enter product ID."),validators.Length(min=3, max=21,message=("Minimum 3 to Maximum 21 characters"))])
   categoryname = TextField(" categoryname",[validators.Required("Select category")])
   subcategory = TextField(" subcategory",[validators.Required("Select sub category")])
   productname = TextField(" productname",[validators.Required("Enter product name"),validators.Length(min=3,max=50,message=("Minimum 3 to Maximum 50 characters"))])
   description = TextAreaField(" description",[validators.Required("Enter description") ,validators.Length(min=3,max=100,message=("Minimum 3 to Maximum 100 characters"))])
   atrname=TextField(" atrname",[validators.Required("Enter attribute name") ,validators.Length(min=3,max=15,message=("Minimum 3 to Maximum 15 characters"))])

class CountryForm1(FlaskForm):
   country_std_isd = TextField(" country_std_isd",[validators.Required("Enter STD and ISD"),validators.Length(max=3,message=("Minimum 2 to Maximum 3 characters"))])
   countryname = TextField("countryname",[validators.Required("Enter country name"),validators.Length(min=2,max=21,message=("Minimum 3 to Maximum 21 characters"))])
   

class CountryForm2(FlaskForm):
   countryname = TextField("countryname",[validators.Required("Select country")])
   state = TextField("state",[validators.Required("Enter state name"),validators.Length(min=3, max=21,message=("Minimum 3 to Maximum 21 characters"))])
      
class CountryForm3(FlaskForm):
   countryname = TextField("countryname",[validators.Required("Please enter country name."),validators.Length(min=3, max=21,message=("Minimum 3 to Maximum 21 characters"))])
   state = TextField("state",[validators.Required("Select state")])
   city = TextField("city",[validators.Required("Enter city name")])

class UploadForm(FlaskForm):
   upload_id = TextField(" upload_id",[validators.Required(" Enter product Id"),validators.Length(min=3, max=21,message=("Minimum 3 to 21 characters"))])
   categoryname = TextField(" categoryname")
   subcategory = TextField(" subcategory")
   upload_name= TextField(" upload_name",[validators.Required("Enter product name."),validators.Length(min=3, max=75,message=("Minimum 3 to Maximum 75 characters"))])
   upload_modelno= TextField(" upload_modelno",[validators.Required("Enter model no."),validators.Length(min=3, max=40,message=("Minimum 3 to Maximum 40 characters"))])
   brand = TextField(" brand")
   upload_hsncode=TextField(" upload_hsncode",[validators.Required("Enter HSNcode."),validators.Length(min=8,message=("Minimum 8 digits "))])
   upload_warranty= TextField(" upload_warranty")
   upload_pieceperCarton =TextField(" upload_pieceperCarton",[validators.Required("Enter piece per carton."),validators.Length(min=1, max=3,message=("Minimum 1 to Maximum 3 characters"))])
   upload_minimumOrder=TextField(" upload_minimumOrder",[validators.Required("Enter order."),validators.Length(min=1, max=3,message=("Minimum 1 to Maximum 3 characters"))])
   upload_netWeight =TextField(" upload_netWeight")
   upload_mrp=TextField(" upload_mrp",[validators.Required("Enter MRP "),validators.Length(min=1, max=10,message=("Minimum 1 to Maximum 10 characters"))])
   discount = TextField(" discount")
   upload_discount=TextField(" upload_discount",[validators.Required("Enter discount."),validators.Length(min=1, max=5,message=("Minimum 1 to Maximum 5 characters"))]) 
   upload_price = TextField(" upload_price",[validators.Required("Enter price."),validators.Length(min=1, max=9999999999,message=("Minimum 1 to Maximum 9999999999 characters"))])
   tax = TextField(" tax")
   upload_tax=TextField(" upload_tax",[validators.Required("Enter tax."),validators.Length(min=1, max=5,message=("Minimum 1 to Maximum 5 characters"))])
   upload_netPrice=TextField(" upload_netPrice",[validators.Required("Enter net price."),validators.Length(min=1, max=25,message=("Minimum 1 to Maximum 25 characters"))])
   #upload_locations=SelectField('location:', choices=location)
   #frequency=SelectField('frequency:', choices=frequency)
   upload_photo=TextField("upload_photo")
   manual_video=TextField("manual_video")
   manual_pdf=TextField("manual_pdf")
   tags=TextAreaField("tags")
   metadescription=TextAreaField("metadescription")
   keywords=TextAreaField("keywords")
   description = TextAreaField("Description")
   atrname=TextField(" atrname",[validators.Required("Enter attribute name."),validators.Length(min=1, max=25,message=("Minimum 1 to Maximum 25 characters"))])
   atrvalue=TextField(" atrname",[validators.Required("Enter attribute value."),validators.Length(min=1, max=25,message=("Minimum 1 to Maximum 25 characters"))])


class ShippingForm(FlaskForm):
    vehiclenumber = TextField(" Vehiclenumber",[validators.Required("Enter vehicle number."),validators.Length(min=10, max=10,message=("Minimum 10 to Maximum 10 characters"))])
    drivername = TextField(" Drivername",[validators.Required("Enter driver name"),validators.Length(min=3, max=21,message=("Minimum 3 to Maximum 21 characters"))])
    contactnumber = TextField(" Contactnumber",[validators.Required("Enter contact number"),validators.Length(max=21,message=("Maximum 21 characters"))])
    alternativecontact = TextField(" Alternativecontact",[validators.Required("Enter Alternative contact number") ,validators.Length(max=21,message=("Maximum 21 characters"))])


class SuppliertaxForm(FlaskForm):
    taxId = TextField(" taxId",[validators.Required("Enter tax Id."),validators.Length(min=3, max=10,message=("Minimum 3 to Maximum 10 characters"))])
    taxName= TextField(" taxName",[validators.Required("Enter tax name"),validators.Length(min=3, max=10,message=("Minimum 3 to Maximum 10 characters"))])
    taxRate = TextField(" TaxRate",[validators.Required("Enter tax rate"),validators.Length(min=1,max=5,message=("Minimum 1 to Maximum 5 characters"))])

   
class SupplierdiscountForm(FlaskForm):
    discountId = TextField(" DiscountId",[validators.Required("Enter discount Id."),validators.Length(min=3, max=10,message=("Discount Id Minimum 3 to Maximum 10 characters"))])
    discountName= TextField(" DiscountName",[validators.Required("Enter discount name"),validators.Length(min=3,max=21,message=("Discount name Minimum 3 to Maximum 21 characters "))])
    discountRate = TextField(" DiscountRate",[validators.Required("Enter discount rate"),validators.Length(min=1,max=5,message=("Enter discount rate (0 to 100%)"))])
    
class EditForm(FlaskForm):
    username = TextField("User Name",[validators.Required("Enter name."),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
    email = TextField("Email",[validators.Required("Enter email"),validators.Email("Enter email ")])
    mobile = TextField("Mobile",[validators.Required("Enter mobile number")])
    oldpassword=PasswordField("Password",[validators.Required("Enter password"),validators.Length(min=8,message=("Password Minimum 8 characters "))])
    password = PasswordField("Password",[validators.Required("Confirm password"),validators.Length(min=8,message=("Password Minimum 8 characters")),validators.EqualTo('confirm', message='Password do not match')])
    confirm = PasswordField('Confirm password')
    
class WHRegistration(FlaskForm):
    warehouse_id = TextField(" Warehouse Id",[validators.Required("Enter valid number "),validators.Length(min=3,max=21,message=("Minimum 3 to Maximum 21 digits"))])
    warehouse_name = TextField(" Warehouse Name",[validators.Required("Enter name"),validators.Length(min=3,max=50,message=("Minmum 3 to Maximum 50 characters"))])
    warehouse_address= TextAreaField("Warehouse Address",[validators.Required("Enter address (House No., Street Name, Area Name, City, State, PIN Code, Country)"),validators.Length(min=3,max=100,message=("Minimum 3 to Maximum 100 characters"))])
    warehouse_email = TextField("Email",[validators.Required("Enter email Id (example: abcd@gmail.com)"),validators.Email("Invalid email Id ")])
    warehouse_phone = TextField(" Warehouse Phone",[validators.Required("Enter 10 digit mobile number"),validators.Length(max=10,message=("Enter 10 digit mobile number"))])
    #warehouse_password =PasswordField("Password",[validators.Required("Password  should contain minimum 8 characters"),validators.Length(min=8, max=20,message=("Password must be between 8 to 20 "))])   
    warehouse_manager= TextField(" Warehouse Manager",[validators.Required("Select warehouse manager"),validators.Length(min=3,max=21,message=("Minimum 3 to Maximum 21 characters"))])

class PurchaseOrderForm(FlaskForm):
    supplier_docid = TextField(" Supplier Name",[validators.Required("Enter supplier name"),validators.Length(max=21,message=("Maximum 21 characters"))])
    warehouse_docid = TextField(" Warehouse Name",[validators.Required("Enter warehouse name"),validators.Length(max=21,message=("Maximum 21 characters"))])

class PurchaseOrderviewForm(FlaskForm):
    warehouse_name = TextField(" Warehouse Name",[validators.Required("Enter warehouse name"),validators.Length(max=21,message=("Maximum 21 characters"))])
    supplier_name = TextField(" Supplier Name",[validators.Required("Enter supplier name"),validators.Length(max=21,message=("Maximum 21 characters"))])
    supplier_id = TextField(" Supplier Id",[validators.Required("Enter supplier Id"),validators.Length(max=21,message=("Maximum 21 characters"))])
    supplier_address = TextField(" Supplier Address",[validators.Required("Enter address"),validators.Length(max=21,message=("Maximum 21 characters"))])
    pm_id = TextField(" Pm Id",[validators.Required("Enter purchase manager Id"),validators.Length(max=21,message=("Maximum 21 characters"))])
    po_no = TextField(" Po No",[validators.Required("Enter  purchase number"),validators.Length(max=21,message=("Maximum 21 characters"))])
    po_date = TextField(" Po Date",[validators.Required("Enter purchase order date"),validators.Length(max=21,message=("Maximum 21 characters"))])
        
class UserList(FlaskForm):
    username = TextField("User Name",[validators.Required("Enter user name."),validators.Length(min=3, max=21,message=("Minmum 3 to Maximum 21 characters"))])
    email = TextField("Email",[validators.Required("Enter email "),validators.Email("Enter email")])
    mobile = TextField("Mobile",[validators.Required("Enter 10 digit mobile number"),validators.Length( max=10,message=("Enter 10 digit mobile number"))])
    password = PasswordField("Password",[validators.Required("Enter password"),validators.Length(min=8,message=("Enter a combination of atleast 8 letters (1 upper case, 1 lower case), 1 number and 1 special character (_ ! @ # - $ % ^ . & * =)"))])
    usertype = TextField('Department')

class UsertypeForm(FlaskForm):
    usertype= TextField(" User Type",[validators.Required("Enter user type"),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
    userrole = TextField(" User Role",[validators.Required("Enter user role"),validators.Length(min=3,max=50,message=("Minimum 3 to Maximum 50 characters"))])

class BarCodeCartonForm(FlaskForm):
   barcode = TextField("Barcode List",[validators.Required("Enter barcode")])       
   mainbarcode=TextField("Main bar code",[validators.Required("Enter main barcode")])
   
class BarcodeForm(FlaskForm):
  barcode = TextField("Barcode Id",[validators.Required("Enter barcode Id"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
  barcode_type = TextField(" Barcode Type",[validators.Required("Enter barcode type"),validators.Length(max=21,message=("Maximum 21 characters"))])
  todayDate=TextField("Today Date",[validators.Required("Enter today date")])

class ProductsInHouseForm(FlaskForm):
     barcode = TextField("Barcode",[validators.Required("Enter barcode")])
     wh_id = TextField("Wh Id",[validators.Required("Enter warehouse Id"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 digits"))])
     invoice_id = TextField("Invoice Id",[validators.Required("Enter invoice Id")])
     smt_id = TextField("Smt Id",[validators.Required("Enter smt Id"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 digits"))])
     hsn_number = TextField("HSN",[validators.Required("Enter HSN number"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 digits"))])
     supplier_id = TextField("Supplier Id",[validators.Required("Enter supplier Id"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 digits"))])
     category = TextField("Category",[validators.Required("Enter category"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     sub_category = TextField("Sub Category",[validators.Required("Enter sub category"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     product_name = TextField("Product Name",[validators.Required("Enter product name"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     brand = TextField("Brand",[validators.Required("Enter brand"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     model_number = TextField("Model Number",[validators.Required("Enter model number"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     hotsale = TextField("Hot Sale",[validators.Required("Enter hot sale"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     avl_qty = TextField("Avl Quantity",[validators.Required("Enter available quantity"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     soldout_qty = TextField("Sold out Quantity",[validators.Required("Enter soldout quantity"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     netprice = TextField("Net Price",[validators.Required("Enter net price"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     landingprice = TextField("Landing Price",[validators.Required("Enter landing price"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     dealerprice = TextField("Dealer Price",[validators.Required("Enter dealer price"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     enduserprice = TextField("Enduser price",[validators.Required("Enter enduser price"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     mrp = TextField("MRP",[validators.Required("Enter MRP"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     discount = TextField("Discount",[validators.Required("Enter discount"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     warenty = TextField("Warenty",[validators.Required("Enter warrenty"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     dofmk = TextField("Date of manufacture",[validators.Required("Enter date of manufacture"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     dofsale = TextField("Date of sale",[validators.Required("Enter date of sale"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     shop_tag = TextField("Shop Tag",[validators.Required("Enter shop tag"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     user_tag = TextField("User Tag",[validators.Required("Enter user tag"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])
     user_check = TextField("User Check",[validators.Required("Enter user check"),validators.Length(min=10, max=15,message=("Minimum 10 to Maximum 15 characters"))])

class ShopUserForm(FlaskForm):
    userid=TextField("User Id",[validators.Required("Enter Id."),validators.Length(min=3, max=21,message=("Minimum 3 to Maximum 21 characters"))])
    username = TextField("User Name",[validators.Required("Enter name."),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
    email = TextField("Email",[validators.Required("Enter email "),validators.Email("Enter email ")])
    mobile = TextField("Mobile",[validators.Required("Enter 10 digits mobile number"),validators.Length( max=10,message=("Enter 10 digits mobile number"))])
    shop=TextField("Shop",[validators.Required("Enter shop."),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
    password = PasswordField("Password",[validators.Required("Enter password "),validators.Length(min=3, max=10,message=("Minimum 3 to Maximum 10 characters "))])
    createdby = TextField("Created By",[validators.Required("Enter created by."),validators.Length(min=3, max=21,message=("Minimum 3 to Maximum 21 characters"))]) 
    date= TextField("Createdby",[validators.Required("Enter created date "),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])

    
class ShopsetupForm(FlaskForm):
    shop_id = TextField(" Shop Id",[validators.Required("Enter shop Id"),validators.Length(min=3, max=21,message=("Minimum 3 to Maximum 21 digits"))])
    shop_name = TextField(" Shop Name",[validators.Required("Enter shop name"),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
    reg_shop_name=TextField(" Shop Name",[validators.Required("Enter shop name"),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
    shop_address= TextAreaField("Address",[validators.Required("Enter shop address"),validators.Length(min=3, max=100,message=("Minimum 3 to Maximum 100 characters"))])
    pincode = TextField(" Pincode",[validators.Required("Enter pin code (e.g. 500036) "),validators.Length(max=21,message=("Maximum 21 digits"))])
    latitude = TextField(" Latitude",[validators.Required("Enter latitude")])
    longitude = TextField(" Longitude",[validators.Required("Enter longitude")])
    email =  TextField("Email",[validators.Required("Enter Email "),validators.Email("Enter Email ")])
    phone = TextField(" Phone",[validators.Required("Enter 10 digits mobile number")])
    dealer =TextField(" Dealer",[validators.Required("Enter dealer name"),validators.Length(max=21,message=("Maximum 21 characters"))])
    email = TextField("Email",[validators.Required("Enter email "),validators.Email("Enter email")])
    phone = TextField(" phone",[validators.Required("Enter 10 digits mobile number")])
    dealer =TextField(" dealer",[validators.Required("Enter dealer name"),validators.Length(max=21,message=("Maximum 21 characters"))])
    password =PasswordField("Password",[validators.Required("Enter password"),validators.Length(min=8,max=20, message=("Minimum 8 to Maximum 20 characters"))])   

class ShopOrderForm(FlaskForm):
    warehouse_name = TextField(" Warehouse Name",[validators.Required("Enter warehouse name"),validators.Length(max=21,message=("Maximum 21 characters"))])
    shop_name = TextField(" Shop Name",[validators.Required("Enter shop name"),validators.Length(max=21,message=("Maximum 21 characters"))])

class ShopOrderviewForm(FlaskForm):
    warehouse_name = TextField(" Warehouse_name",[validators.Required("Enter warehouse name"),validators.Length(max=21,message=("Maximum 21 characters"))])
    shop_name = TextField(" Shop Name",[validators.Required("Enter shop name"),validators.Length(max=21,message=("Maximum 21 characters"))])
    shop_id = TextField(" Shop Id",[validators.Required("Enter shop Id"),validators.Length(max=21,message=("Maximum 21 digits"))])
    shop_address = TextField(" Shop Address",[validators.Required("Enter  shop address"),validators.Length(max=21,message=("Maximum 21 characters"))])
    pm_id = TextField(" Pm Id",[validators.Required("Enter purchase manager Id"),validators.Length(max=21,message=("Maximum 21 digits"))])
    po_no = TextField(" Po No",[validators.Required("Enter Purchase numbaer"),validators.Length(max=21,message=("Maximum 21 digits"))])
    po_date = TextField(" Po Date",[validators.Required("Enter  purchase order date"),validators.Length(max=21,message=("Maximum 21 digits"))])
        

class CompanyForm(FlaskForm):
    companyname = TextField(" company Name",[validators.Required("Enter company name"),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
    address = TextAreaField(" Address",[validators.Required("Enter address"),validators.Length(min=3, max=100,message=("Minimum 3 to Maximum 100 characters"))])
    pan= TextField("PAN",[validators.Required("Enter the PAN"),validators.Length(max=60,message=("Maximum 60 characters"))])
    gstin =TextField(" GSTIN",[validators.Required("Enter GSTIN"),validators.Length(max=21,message=("Maximum 21 digits"))])
    cin = TextField(" CIN",[validators.Required("Enter CIN"),validators.Length(max=21,message=("Maximum 21 characters"))])
    state =TextField("State",[validators.Required("Enter state "),validators.Length(min=8,message=("Minimum 8 characters "))])   
    statecode= TextField(" State Code",[validators.Required("Enter state code"),validators.Length(max=21,message=("Maximum 21 characters"))])

class BillingForm(FlaskForm):
    dealerid = TextField(" Dealer Id")
    companyname = TextField(" company Name",[validators.Required("Enter company name"),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
    address = TextAreaField(" Address",[validators.Required("Enter address"),validators.Length(min=3, max=100,message=("Minimum 3 to Maximum 100 characters"))])
    pan= TextField("PAN",[validators.Required("Enter PAN"),validators.Length(max=60,message=("Maximum 60 characters"))])
    gstin =TextField("GSTIN",[validators.Required("Enter GSTIN"),validators.Length(max=21,message=("Maximum 21 characters"))])
    cin = TextField(" CIN",[validators.Required("Enter CIN"),validators.Length(max=21,message=("Maximum 21 characters"))])
    state =TextField("State",[validators.Required("Enter state "),validators.Length(min=8,message=("Minimum 8 characters "))])   
    statecode= TextField(" State Code",[validators.Required("Enter state code"),validators.Length(max=21,message=("Maximum 21 characters"))])
    companylogo= FileField("Logo ",validators=[FileRequired(),FileAllowed(['png', 'jpg', 'jpeg'], 'Images only! jpg/png')])
    contactno=TextField(" Contact Number",[validators.Required("Enter contact number"),validators.Length(max=10,message=("Maximum 10 characters"))])

class MasterBrandEditForm(FlaskForm):
    supplier_id = TextField(" Supplier Id",[validators.Required("Enter supplier Id."),validators.Length(min=3, max=24,message=("Minimum 3 to Maximum 24 characters"))])
    brand = TextField(" Brand",[validators.Required("Enter brand."),validators.Length(min=2, max=50,message=("Minimum 2 to Maximum 50 characters"))])
    supplier_tm = TextField(" TM No",[validators.Required("Enter valid trade mark number"),validators.Length(min=7,max=7,message=("Only 7 digits are allowed"))])
   
    
class BankForm(FlaskForm):
    bankac_number = TextField(" Bank Account number",[validators.Required("Enter bank account number"),validators.Length(min=6, max=17,message=("Minimum 6 to Maximum 17 characters"))])
    ac_holdername = TextField("Account Holder Name",[validators.Required("Enter account holder name"),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
    accountType = TextField(" Account Type",[validators.Required("Enter account type"),validators.Length(max=21,message=("Maximum 21 characters"))])
    bank_name = TextField(" Bank Name",[validators.Required("Enter bank name"),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
    ifsc_code= TextField(" IFSC Code",[validators.Required("Enter the IFSC code"),validators.Length(min=11, max=11,message=("Minimum 11 to Maximum 11 characters"))])
    micr_code =TextField(" MICR Code",[validators.Required("Enter MICR code"),validators.Length(min=9, max=9,message=("Minimum 9 to Maximum 9 characters"))])
    vpa =TextField(" VPA Code")
    branch_name = TextField("  Branch Name",[validators.Required("Enter branch name"),validators.Length(min=3, max=50,message=("Minimum 3 to Maximum 50 characters"))])
    branch_address =TextAreaField("Branch Address",[validators.Required("Enter branch address"),validators.Length(min=3, max=150,message=("Minimum 3 to Maximum 150 characters"))]) 

class HeaderForm(FlaskForm):
    companyname = TextField(" company Name",[validators.Required("Enter company name"),validators.Length(min=3, max=30,message=("Minimum 3 to Maximum 30 characters"))])
    address = TextAreaField(" Address",[validators.Required("Enter address"),validators.Length(min=3, max=100,message=("Minimum 3 to Maximum 100 characters"))])
    companylogo= FileField("Logo ",validators=[FileRequired(),FileAllowed(['png', 'jpg', 'jpeg'], 'Images only! jpg/png')])
    contactno=TextField(" Contact Number",[validators.Required("Enter contact number"),validators.Length(max=10,message=("Maximum 10 characters"))])

class UploadfileForm(FlaskForm):
      upload_file = FileField("file ",validators=[FileRequired(),FileAllowed(['csv'], 'CSV Files only! ')])

class CouponsForm(FlaskForm):
      coupon_name = TextField(" coupon_name",[validators.Required("Enter coupon name")])
      coupon_code =TextField(" coupon_code",[validators.Required("Enter coupon code")])
      discount = TextField(" discount",[validators.Required("Enter discount")])
      discount_type = usertype = SelectField('typef', choices=typef)
      maxvalue=TextField(" max_value",[validators.Required("Enter maxvalue")])
      from_date = TextField(" from_date",[validators.Required("Enter from date")])
      end_date = TextField(" end_date",[validators.Required("Enter end date")])
      min_order_value = TextField("min_order_value",[validators.Required("Enter minimum order value")])
      created_date = TextField(" created_date",[validators.Required("Enter created date")])
      createdBy = TextField(" createdBy",[validators.Required("Enter created by")])
      terms_conditions= TextAreaField("terms_conditions",[validators.Required("Enter terms and conditions")])
      imageurl = TextAreaField("imageurl",[validators.Required("Enter image url")])
      
class ServicetaxForm(FlaskForm):
    taxid = TextField(" taxId",[validators.Required("Enter tax Id."),validators.Length(min=3, max=10,message=("Minimum 3 to Maximum 10 characters"))])
    taxname= TextField(" taxName",[validators.Required("Enter tax name"),validators.Length(min=3, max=10,message=("Minimum 3 to Maximum 10 characters"))])
    taxrate = TextField(" TaxRate",[validators.Required("Enter tax rate"),validators.Length(min=1,max=5,message=("Minimum 1 to Maximum 5 characters"))])

class ExchangeForm(FlaskForm):
    invoice_no = TextField(" invoice_no",[validators.Required("Enter invoice number.")])
    brand= TextField(" brand",[validators.Required("Enter brand")])
    model = TextField(" model",[validators.Required("Enter model")])
    oldsmt_id= TextField(" oldsmt_id",[validators.Required("Enter old smt Id")])
    newsmt_id = TextField(" newsmt_id",[validators.Required("Enter new smt Id")])    

class CollectionForm(FlaskForm):
    collectionname = TextField(" Collection Name",[validators.Required("Enter collection name"),validators.Length(min=3, max=30,message=("Minimum 3 to Maximum 30 characters"))])
    collectionurl = TextAreaField(" Collection Url",[validators.Required("Enter collection url")])
    collectionlink= TextAreaField(" Collection Link",[validators.Required("Enter collection link")])

class BrandForm(FlaskForm):
    brandname = TextField(" Brand Name",[validators.Required("Enter collection name"),validators.Length(min=3, max=30,message=("Minimum 3 to Maximum 30 characters"))])
    brandurl = TextAreaField(" Collection Url",[validators.Required("Enter brand url")])
    brandlink= TextAreaField(" Collection Link",[validators.Required("Enter brand link")])
    brandfooterurl= TextAreaField(" Collection Link",[validators.Required("Enter brand footer url")])
    brandtype= SelectField('Brand Type', choices=brandtypelist)
    tags=TextAreaField("tags")
    metadescription=TextAreaField("metadescription")
    keywords=TextAreaField("keywords")

class BannerForm(FlaskForm):
    bannername = TextField(" Banner Name",[validators.Required("Enter banner name"),validators.Length(min=3, max=30,message=("Minimum 3 to Maximum 30 characters"))])
    bannerurl = TextAreaField(" Banner Url",[validators.Required("Enter banner url")])
    bannerlink= TextAreaField(" Banner Link",[validators.Required("Enter banner link")])    

class FooterForm(FlaskForm):
    footername = TextField(" Footer Name",[validators.Required("Enter footer name"),validators.Length(min=3, max=30,message=("Minimum 3 to Maximum 30 characters"))])
    footerurl = TextAreaField(" Footer Url",[validators.Required("Enter footer url")])
    footerlink= TextAreaField(" Footer Link",[validators.Required("Enter footer link")])    
    
class HeadForm(FlaskForm):
    headername = TextField(" Header Name",[validators.Required("Enter name"),validators.Length(min=3, max=30,message=("Minimum 3 to Maximum 30 characters"))])
    headercontactno=TextField(" Contact Number",[validators.Required("Enter contact number")])
    headerlogo= TextAreaField(" Header Logo",[validators.Required("Enter logo")])
    
class ImageForm(FlaskForm):
    supplier_id = TextField(" Supplier Id",[validators.Required("Enter supplier Id."),validators.Length(min=3, max=21,message=("Minimum 3 to Maximum 21 characters"))])
    productname = TextField(" company Name",[validators.Required("Enter company name"),validators.Length(min=3, max=30,message=("Minimum 3 to Maximum 30 characters"))])
    image= FileField("image ",validators=[FileRequired(),FileAllowed(['png', 'jpg', 'jpeg'], 'Images only! jpg/png')])


class PricesUploadfileForm(FlaskForm):
      upload_file = FileField("file ",validators=[FileRequired(),FileAllowed(['csv'], 'CSV Files only! ')])

class Promotions(FlaskForm):
    content = CKEditorField("content")
