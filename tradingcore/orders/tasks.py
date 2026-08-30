from celery import shared_task
from .market_maker import MarketMaker

@shared_task
def run_market_maker():
    bot = MarketMaker(inventory = 0)
    buy_order ,sell_order = bot.place_orders(quantity = 1)
    return f"Placed: BUY @ {buy_order.price} ],SELL @ {sell_order.price}"