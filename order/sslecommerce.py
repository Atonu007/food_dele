
from sslcommerz_lib import SSLCOMMERZ 


def ssl(transaction_id,total_price):
        setting = { 'store_id': 'moonw663b9ebca1d88', 'store_pass': 'moonw663b9ebca1d88@ssl', 'issandbox': True }
        sslcz = SSLCOMMERZ(setting)

        post_body = {}
        post_body['total_amount'] = total_price
        post_body['currency'] = "BDT"
        post_body['tran_id'] = transaction_id
        post_body['success_url'] = "your success url"
        post_body['fail_url'] = "your fail url"
        post_body['cancel_url'] = "your cancel url"
        post_body['emi_option'] = 0
        post_body['cus_name'] = "test"
        post_body['cus_email'] = "test@test.com"
        post_body['cus_phone'] = "01700000000"
        post_body['cus_add1'] = "customer address"
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"
        response = sslcz.createSession(post_body)
        return response 