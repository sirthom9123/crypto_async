from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from .models import Test, Position
from .utils import get_random_code
import requests

@shared_task
def get_crypto_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    data = requests.get(url).json()
    
    for item in data:
        p, _ = Position.objects.get_or_create(name=item['name'])
        p.image = item['image']
        p.price = item['current_price']
        p.rank = item['market_cap_rank']  
        p.market_cap = item['market_cap']  
        p.save()
        
@periodic_task(run_every=(crontab(minute='*/1')))
def get_crypto_current():
    get_crypto_data.delay()
        
        
# @shared_task
# def create_test_object(name):
#     Test.objects.create(name=name)
    

# @shared_task
# def create_all_code():
#     for test in Test.objects.all():
#         test.code = get_random_code()
#         test.save()    
    
# @periodic_task(run_every=(crontab(minute='*/1')))
# def run_create_obj():
#     create_test_object.delay(name='new2020')