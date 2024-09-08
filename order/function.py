import time
import random

def generate_transaction_id():
    timestamp = int(time.time() * 1000)  
    random_number = random.randint(1000, 9999)  
    return f"{timestamp}{random_number}"