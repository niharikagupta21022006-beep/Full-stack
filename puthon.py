# order_id = 1
# symbol = "AAPL"
# price = 150.25
# quantity = 10
# side = "BUY"

# print("Order:",order_id,symbol,side,quantity,"@",price)

# quantity = 10
# available_stock = 5

# if quantity <= available_stock :
#     print("Order can be fully filled")

# elif quantity > available_stock and available_stock > 0:
#     print("Order can be partially filled")

# else:
#     print("No stock available")

# def check_match(buy_price,sell_price):
#     if sell_price <= buy_price:
#         return True

#     else:
#         return False

# sell_orders = [150.50,150.25,150.75,150.10]
# buy_price = 150.30

# for price in sell_orders:
    
#     matched = check_match(buy_price,price)
#     print(price,"->Match",matched)



class Order:
    def __init__(self,order_id,price,quantity,side):
       self.order_id = order_id
       self.price = price
       self.quantity = quantity
       self.side = side

class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self,order):
        if order.side == "BUY":
            self.buy_orders.append(order)
        else:
            self.sell_orders.append(order)

    def show_book(self):
        print("---BUY ORDERS---")
        for o in self.buy_orders:
            print(o.order_id,o.quantity,"@",o.price)

        print("---SELL ORDERS---")
        for o in self.sell_orders:
            print(o.order_id,o.quantity,"@",o.price)

    def match_orders(self):

        self.buy_orders.sort(key = lambda o:o.price , reverse = True)
        self.sell_orders.sort(key = lambda o:o.price)
        for buy in self.buy_orders[:]:
            for sell in self.sell_orders[:]:
                if buy.quantity == 0:
                    break
                if sell.price <= buy.price and sell.quantity > 0:
                    trade_qty = min(buy.quantity,sell.quantity)
                    print("TRADE:",trade_qty,"shares @",sell.price,"|buyer:",buy.order_id,"|seller",sell.order_id)
                    buy.quantity -= trade_qty
                    sell.quantity -= trade_qty

                    if sell.quantity == 0:
                        self.sell_orders.remove(sell)

            if buy.quantity == 0:
                    self.buy_orders.remove(buy)

    def cancel_order(self,order_id):
        for order in self.buy_orders:
            if order.order_id  == order_id:
                self.buy_orders.remove(order)
                print("Cancelled BUY order:",order_id)
                return

        for order in self.sell_orders:
            if order.order_id == order_id:
                self.sell_orders.remove(order)
                print("Cancelled SELL order:",order_id)
                return 

        print("Order not found:",order_id)

book = OrderBook()
book.add_order(Order(1,150.50,15,"BUY"))
book.add_order(Order(2,150.30,6,"SELL"))
book.add_order(Order(3,150.10,6,"SELL"))



book.show_book()
print()
book.cancel_order(2)
print()
book.show_book()
