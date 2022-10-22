
class UnauthorizedError(Exception):
    """
    401 https://docs.5sim.net/#balance-request\n
    401 https://docs.5sim.net/#vendor-statistic\n
    401 https://docs.5sim.net/#wallets-reserve\n
    """
    pass

class IncorrectCountryError(Exception):
    """
    400 [country is incorrect] https://docs.5sim.net/#prices-by-country\n
    400 [country is incorrect] https://docs.5sim.net/#prices-by-country-and-product"""
    pass

class BadCountryError(Exception):
    """
    400 [bad country] https://docs.5sim.net/#buy-activation-number\n
    400 [bad country] https://docs.5sim.net/#buy-hosting-number\n
    400 [bad country] https://docs.5sim.net/#re-buy-number"""
    pass

class IncorrectProductError(Exception):
    """
    400 [product is incorrect] https://docs.5sim.net/#prices-by-country\n
    400 [product is incorrect] https://docs.5sim.net/#prices-by-country-and-product"""
    pass

class BadOperatorError(Exception):
    """
    400 [bad operator] https://docs.5sim.net/#buy-activation-number\n
    400 [bad operator] https://docs.5sim.net/#buy-hosting-number\n
    400 [bad operator] https://docs.5sim.net/#re-buy-number"""
    pass
class NotEnoughUserBalanceError(Exception):
    """
    400 [not enough user balance] https://docs.5sim.net/#buy-activation-number\n
    400 [not enough user balance] https://docs.5sim.net/#buy-hosting-number\n
    400 [not enough user balance] https://docs.5sim.net/#re-buy-number"""
    pass

class NotEnoughRatingError(Exception):
    """
    400 [not enough rating] https://docs.5sim.net/#buy-activation-number\n
    400 [not enough rating] https://docs.5sim.net/#buy-hosting-number\n
    400 [not enough rating] https://docs.5sim.net/#re-buy-number"""
    pass

class SelectCountryError(Exception):
    """
    400 [select country] https://docs.5sim.net/#buy-activation-number\n
    400 [select country] https://docs.5sim.net/#buy-hosting-number"""
    pass

class SelectOperatorError(Exception):
    """
    400 [select operator] https://docs.5sim.net/#buy-activation-number\n
    400 [select operator] https://docs.5sim.net/#buy-hosting-number\n
    400 [select operator] https://docs.5sim.net/#re-buy-number"""
    pass

class NoProductError(Exception):
    """
    400 [no product] https://docs.5sim.net/#buy-activation-number\n
    400 [no product] https://docs.5sim.net/#buy-hosting-number\n
    400 [no product] https://docs.5sim.net/#re-buy-number"""
    pass

class ServerOfflineError(Exception):
    """
    400 [server offline] https://docs.5sim.net/#buy-activation-number\n
    400 [server offline] https://docs.5sim.net/#buy-hosting-number\n
    400 [server offline] https://docs.5sim.net/#re-buy-number"""
    pass

class NoFreePhonesError(Exception):
    """
    200 [no free phones] https://docs.5sim.net/#buy-activation-number
    400 [no free phones] https://docs.5sim.net/#re-buy-number"""
    pass

class ReuseNotPossibleError(Exception):
    """400 [reuse not possible] https://docs.5sim.net/#re-buy-number"""
    pass

class ReuseFalseError(Exception):
    """400 [reuse false] https://docs.5sim.net/#re-buy-number"""
    pass

class ReuseExpiredError(Exception):
    """400 [reuse expired] https://docs.5sim.net/#re-buy-number"""
    pass

class OrderNotFoundError(Exception):
    """
    404 [order not found] https://docs.5sim.net/#check-order-get-sms\n
    404 [<html><head><title>not found</title></head><body>not found</body></html>] https://docs.5sim.net/#finish-order\n
    404 [<html><head><title>not found</title></head><body>not found</body></html>] https://docs.5sim.net/#cancel-order\n
    404 [<html><head><title>not found</title></head><body>not found</body></html>] https://docs.5sim.net/#ban-order\n
    404 [<html><head><title>not found</title></head><body>not found</body></html>] https://docs.5sim.net/#sms-inbox-list"""
    pass

class OrderExpiredError(Exception):
    """
    400 [order expired] https://docs.5sim.net/#finish-order\n
    400 [order expired] https://docs.5sim.net/#cancel-order\n
    400 [order expired] https://docs.5sim.net/#ban-order"""
    pass

class OrderNoSMSError(Exception):
    """
    400 [order no sms] https://docs.5sim.net/#finish-order\n
    400 [order no sms] https://docs.5sim.net/#cancel-order\n
    400 [order no sms] https://docs.5sim.net/#ban-order"""
    pass

class HostingOrderError(Exception):
    """
    400 [hosting order] https://docs.5sim.net/#finish-order\n
    400 [hosting order] https://docs.5sim.net/#cancel-order\n
    400 [hosting order] https://docs.5sim.net/#ban-order"""
    pass

class RecordNotFoundError(Exception):
    """404 [<html><head><title>not found</title></head><body>not found</body></html>] https://docs.5sim.net/#sms-inbox-list"""
    pass

class RequestLimitByIPError(Exception):
    """503 https://docs.5sim.net/#structure-of-sms"""
    pass

class RequestLimitByApiKeyError(Exception):
    """429 https://docs.5sim.net/#structure-of-sms"""
    pass

class RequestLimitBuyNumberError(Exception):
    """503 https://docs.5sim.net/#structure-of-sms"""
    pass

class RequestLimitBanError(Exception):
    """https://docs.5sim.net/#structure-of-sms"""
    pass
