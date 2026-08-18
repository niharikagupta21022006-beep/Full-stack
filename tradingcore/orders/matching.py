from .models import Order

def match_orders():
    buy_orders = Order.objects.filter(side = "BUY").order_by('-price')
    sell_orders = Order.objects.filter(side = "SELL").order_by('price')

    for buy in buy_orders:
        for sell in sell_orders:
            if buy.quantity == 0:
                break

            if sell.price <= buy.price and sell.quantity > 0:
                trade_qty = min(buy.quantity,sell.quantity)
                print("TRADE:",trade_qty,"shares@",sell.price,"|buyer:",buy.id,"|seller:",sell.id)

                buy.quantity -= trade_qty
                sell.quantity -= trade_qty

                if sell.quantity == 0:
                    sell.delete()

                else:
                    sell.save()

            if buy.quantity == 0:
                buy.delete()

            else:
                buy.save()