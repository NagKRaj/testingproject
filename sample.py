class UpdateInitiateOrder(Resource):
    def post(self):
		json_data = request.get_json(force=True)
        pool = Pool()
        init_orders=InitiateOrders.objects()
        for order in init_orders:
            for item in order.orderitem:
                old_price=item.offer_price
                #req_orderitem=[{'product_name':"1800W Speed Heat Gun Black and Decker KX1800-B1","offer_price":"1100"}]
                print req_orderitem
                for req_items in req_orderitem:
                    if item.productdescription == json_data['product_name']:
                        item.offer_price = json_data['offer_price']
                        item.save()
                        if len(order.user_id) > 20:
                            customer_data=CustomerDetails.objects(id=order.user_id)
                            fo = open("./static/smt-site-notifications/dealer_mail.html", "r+"
                            htmlbody = fo.read()
                            fo.close()
                            urldata ='Dear '+customer_data[0].firstname.encode('ascii','ignore')+', few products in your cart were updated with prices. New prices for  '+(item.productdescription).encode('ascii','ignore')+ ' are '+old_price+' and  '+item.offer_price+ 'respectively.'
                            htmlbody = htmlbody.replace("$$urldata$$",urldata)
                            email_list=[]
                            email_list.append(customer_data[0].email)
                            print email_list
                            pool.apply_async(sendMail,[email_list,'Price changes for products in your cart',htmlbody])
        return {"status":"email sent"}
