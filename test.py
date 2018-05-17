from models import Sup_Upload,atr,PriceLists,Search_Keywords
import re

import itertools


for i in Sup_Upload.objects():
    for j in Sup_Upload.objects(upload_name=i.upload_name):
        searchkeywords_list=[]
        product_name_list=j.upload_name.split(' ')
        searchkeywords_list.append(j.upload_name)
        searchkeywords_list.append(j.upload_brand.replace(' ','')+j.upload_subcategory.replace(' ',''))
        searchkeywords_list.append(j.upload_brand+' '+j.upload_subcategory)
        searchkeywords_list.append(j.upload_brand.replace(' ','')+j.upload_category.replace(' ',''))
        searchkeywords_list.append(j.upload_brand+' '+j.upload_category)
        searchkeywords_list.append(''.join(product_name_list))
        searchkeywords_list.append(' '.join(reversed(product_name_list)))
        searchkeywords_list.append(''.join(reversed(product_name_list)))
        searchkeywords_list.append(''.join(e for e in j.upload_name if e.isalnum()))
        searchkeywords_list.append(' '.join(re.sub('[^a-zA-Z0-9]+', '', _) for _ in product_name_list))
        uploadUser = Sup_Upload(user_id=j.user_id,upload_id=j.upload_id, upload_category=j.upload_category,
                                    upload_subcategory=j.upload_subcategory,upload_name=j.upload_name.strip(), upload_modelno=j.upload_modelno,
                                    upload_brand =j.upload_brand,upload_warranty=j.upload_warranty,upload_pieceperCarton=j.upload_pieceperCarton,
                                    upload_minimumOrder=j.upload_minimumOrder,search_keywords=searchkeywords_list,
                                    upload_netWeight=j.upload_netWeight,upload_mrp=j.upload_mrp,discount=j.discount,upload_discount=j.upload_discount,
                                    upload_price=j.upload_price,tax=j.tax,upload_tax=j.upload_tax,upload_netPrice=j.upload_netPrice,
                                    upload_hsncode=j.upload_hsncode,upload_locations=j.upload_locations,frequency=j.frequency,upload_photo=j.upload_photo,
                                    extraimages=j.extraimages,description=j.description,manual_video=j.manual_video,manual_pdf=j.manual_pdf,salesqty=j.salesqty,avgrating=j.avgrating,
                                tags=j.tags,metadescription=j.metadescription,keywords=j.keywords,status=j.status,lastweeksales=j.lastweeksales,remarks=j.remarks)
        uploadUser.save()
        for k in j.prices:
            price = PriceLists(landing_price=k.landing_price, dealer_price=k.dealer_price,offer_price=k.offer_price,enduser_price=k.enduser_price,
                               bulk_unit_price=k.bulk_unit_price,bulk_qty=k.bulk_qty,percentage=k.percentage,doubleoffer_price=k.doubleoffer_price,landing_price_gst=k.landing_price_gst,
                               dealer_price_gst=k.dealer_price_gst,offer_price_gst=k.offer_price_gst,enduser_price_gst=k.enduser_price_gst)  
            uploadUser.prices.append(price)
            uploadUser.save()
        for l in j.attributes:
            attribute=atr(atrname=l.atrname,atrvalue=l.atrvalue)
            uploadUser.attributes.append(attribute)
            uploadUser.save()
        j.delete()
    
print 'success'    

'''
#-----------------------------------search keywords------------
for i in Sup_Upload.objects():
            searchkeywords_list=[]
            product_name_list=i.upload_name.split(' ')
            searchkeywords_list.append(i.upload_brand.replace(' ','')+i.upload_subcategory.replace(' ',''))
            searchkeywords_list.append(i.upload_brand+' '+i.upload_subcategory)
            searchkeywords_list.append(i.upload_brand.replace(' ','')+i.upload_category.replace(' ',''))
            searchkeywords_list.append(i.upload_brand+' '+i.upload_category)
            searchkeywords_list.append(''.join(product_name_list))
            searchkeywords_list.append(' '.join(reversed(product_name_list)))
            searchkeywords_list.append(''.join(reversed(product_name_list)))
            searchkeywords_list.append(''.join(e for e in i.upload_name if e.isalnum()))
            searchkeywords_list.append(' '.join(re.sub('[^a-zA-Z0-9]+', '', _) for _ in product_name_list))
            product_name=i.upload_name+' '+i.upload_subcategory
            perm_list= list(itertools.permutations(product_name.split(' ')))
            without_space_list=[]
            new_list = []
            for words in perm_list:
               new_list.append(' '.join(words))
               without_space_list.append(''.join(words))
            #print new_list
            #print without_space_list
            final_list=new_list+without_space_list
            #print final_list
            final_search_list=final_list+searchkeywords_list
            search=Search_Keywords(upload_name=i.upload_name,search_keywords=final_search_list).save()
print 'success'
            #-----------------------------------------------------------end search keywords----------------
'''
