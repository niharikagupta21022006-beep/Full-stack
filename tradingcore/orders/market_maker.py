from .models import Order

class MarketMaker:
    def __init__(self,inventory,risk_factor = 0.1,spread = 2):
        self.inventory = inventory
        self.risk_factor = risk_factor
        self.spread = spread
        self.mid_price = self.calculate_mid_price()

    def calculate_mid_price(self):
        best_bid = Order.objects.filter(side = 'BUY').order_by('-price').first()
        best_ask = Order.objects.filter(side = 'SELL').order_by('price').first()

        if best_bid and best_ask:
            return(best_bid.price + best_ask.price)/2

        else:
            return 100

    def reservation_price(self):
        return float(self.mid_price) - (self.inventory*self.risk_factor)

    def bid_price(self):
        return self.reservation_price() - (self.spread / 2)

    def ask_price(self):
        return self.reservation_price() + (self.spread/2)

    def place_orders(self,quantity = 1):
        buy_order = Order.objects.create(
            price = self.bid_price(),
            quantity = quantity,
            side='BUY'
        ) 

        sell_order = Order.objects.create(
            price = self.ask_price(),
            quantity = quantity,
            side = 'SELL'
        )

        return buy_order,sell_order
    