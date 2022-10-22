from lib2to3.pgen2.token import OP
from type_5simProtocol import Type_5simProtocol
from data import ApiKey, Category, Product, Operator, Country, OrderId, Status
from exceptions import *

APIKEY = ApiKey("eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjUyNjUzNTUsImlhdCI6MTYzMzcyOTM1NSwicmF5IjoiODUwMTk0MzYzOThlZGRhNDNlZWNiYmZiNWI2NzA2YmUiLCJzdWIiOjEwMjQxM30.SV5fnr5quVtA50rSbz1Dzfx9ZC2yS57pySSzHiELPjUw3Yt008US44q-mSn-zxka0a8n2EbWq2r5s0www_5QTaOimY__IyXqiYuAteLq-MbpahLPRWjqY10EDxeOVb-1Xb_U7QFu347xw6ZhL4LaRazVCmcq6pLUTWEDiMDGJ5GGEBGd_YF6N0AhvDnq90Bzc0vNu-ghU7IcQapM0fDSnCgZp7N4q50JPSS8yRSVVon3A-Ewoq8hxAjBpX7Z19Vf4sNm6y95WpT0gYCaLyr-uinheDoygXDczVsq-7EzhEKKmFlHbuwzEGwlUcdIYD2Za75IYrgLFbsU62M9twmDbw")

def test_balance():
    protocol = Type_5simProtocol(key=APIKEY)
    profile = protocol.balance()

    assert list(profile.keys()) == ['id', 'email', 'balance', 'rating', 'default_country', 'default_operator', 'frozen_balance']


def test_orders():
    protocol = Type_5simProtocol(key=APIKEY)
    orders = protocol.orders(Category.ACTIVATION, limit=1)

    assert list(orders.keys()) == ['Data', 'ProductNames', 'Statuses', 'Total']


def test_payments():
    protocol = Type_5simProtocol(key=APIKEY)
    payments = protocol.payments(limit=1)

    assert list(payments.keys()) == ['Data', 'PaymentTypes', 'PaymentProviders', 'Total']


def test_products():
    protocol = Type_5simProtocol(key=APIKEY)
    products = protocol.products(Country.RUSSIA, Operator.BEELINE)

    assert list(products.keys())[:5] == ['1688', '1day', '3hours', 'airbnb', 'alibaba']

def test_prices():
    protocol = Type_5simProtocol(key=APIKEY)
    prices = protocol.prices()

    assert list(prices.keys())[:5] == ['afghanistan', 'albania', 'algeria', 'angola', 'anguilla']

def test_prices_by_country():
    protocol = Type_5simProtocol(key=APIKEY)
    prices = protocol.prices(country=Country.AFGHANISTAN)

    assert list(prices.keys()) == ['afghanistan']

def test_prices_by_product():
    protocol = Type_5simProtocol(key=APIKEY)
    prices = protocol.prices(product=Product.AMAZON)

    assert list(prices.keys()) == ['amazon']

def test_prices_by_product_and_country():
    protocol = Type_5simProtocol(key=APIKEY)
    prices = protocol.prices(country=Country.AFGHANISTAN, product=Product.AMAZON)
    print(prices)
    assert list(prices.keys()) == ['afghanistan']

def test_buy_and_cancel():
    protocol = Type_5simProtocol(key=APIKEY)
    # test NoFreePhonesError
    try:
        order = protocol.buy(product=Product.TINDER, country=Country.RUSSIA, operator=Operator.ANY)
    except Exception as error:
        assert NoFreePhonesError == type(error)
        return

    order = order.check()
    assert order.status == Status.PENDING

    order = order.cancel()
    assert order.status == Status.CANCELED


    # test OrderNotFoundEror
    try:
        order = order.ban()

    except Exception as error:
        assert OrderNotFoundError == type(error)

def test_check():
    protocol = Type_5simProtocol(key=APIKEY)
    order_id = OrderId(-1)
    try:
        check = protocol.check(order_id)
    except Exception as error:
        assert OrderNotFoundError == type(error)

    

if __name__ == "__main__":
    test_buy_and_cancel()