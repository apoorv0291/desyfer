

def check_product_no(product_no):
    print "In Check_PRODUCT_NO"
    try:
        product_no = int(product_no.strip())
        if product_no <9999999 or  product_no > 99999999:
            error_msg = "Product Code Should be an 8 digit number"
            return error_msg , False
        else:
            return None,True
    except Exception, e:
        print e
        error_msg = "Product Code Should be an integer not a String"
        print "error_msg", error_msg
        return error_msg, False



