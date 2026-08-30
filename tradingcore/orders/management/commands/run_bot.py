import time
from django.core.management.base import BaseCommand
from orders.market_maker import MarketMaker

class Command(BaseCommand):
    help = 'Rums the market making bot continuously'

    def handle(self,*args,**kwargs):
        while True:
            bot = MarketMaker(inventory = 0)
            buy_order,sell_order = bot.place_orders(quantity=1)

            self.stdout.write(f"Placed: BUY @ {buy_order.price},SELL @ {sell_order.price}")

            time.sleep(5)