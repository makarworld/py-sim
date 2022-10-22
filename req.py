import requests
import json

from exceptions import BadCountryError, BadOperatorError, HostingOrderError, IncorrectCountryError, IncorrectProductError, NoProductError, NotEnoughRatingError, NotEnoughUserBalanceError, OrderNoSMSError, OrderNotFoundError, RecordNotFoundError, ReuseExpiredError, ReuseFalseError, ReuseNotPossibleError, SelectCountryError, SelectOperatorError, ServerOfflineError, UnauthorizedError, NoFreePhonesError
from logger import log
from data import URL, ReqType, ReqResponse, Errors

class Session:
    def __init__(self):
        self.session = requests.Session()

    def headers(self, *args, **kwargs):
        self.session.headers.update(*args, **kwargs)

    def cookies(self, *args, **kwargs):
        self.session.cookies.update(*args, **kwargs)

    def capture_errors(self, r: requests.Request) -> None:
        if r.text == Errors.NO_FREE_PHONES:
            raise NoFreePhonesError("No free phones")

        if r.status_code == 401:
            raise UnauthorizedError("Status Code: 401 Unauthorized")

        if r.status_code == 400:
            if r.text == Errors.COUNTRY_IS_INCORRECT:
                raise IncorrectCountryError("Country is incorrect")
            elif r.text == Errors.BAD_COUNTRY:
                raise BadCountryError("Bad country")
            elif r.text == Errors.PRODUCT_IS_INCORRECT:
                raise IncorrectProductError("Product is incorrect")
            elif r.text == Errors.BAD_OPERATOR:
                raise BadOperatorError("Bad operator")
            elif r.text == Errors.NOT_ENOUGH_USER_BALANCE:
                raise NotEnoughUserBalanceError("Not enough user balance")
            elif r.text == Errors.NOT_ENOUGH_RATING:
                raise NotEnoughRatingError("Not enough user balance")
            elif r.text == Errors.SELECT_COUNTRY:
                raise SelectCountryError("Select country")
            elif r.text == Errors.SELECT_OPERATOR:
                raise SelectOperatorError("Select operator")
            elif r.text == Errors.NO_PRODUCT:
                raise NoProductError("No product")
            elif r.text == Errors.SERVER_OFFLINE:
                raise ServerOfflineError("Server is offline")
            elif r.text == Errors.NO_FREE_PHONES:
                raise NoFreePhonesError("No free phones")
            elif r.text == Errors.REUSE_NOT_POSSIBLE:
                raise ReuseNotPossibleError("Reuse not possible")
            elif r.text == Errors.REUSE_FALSE_POSSIBLE:
                raise ReuseFalseError("Reuse false")
            elif r.text == Errors.REUSE_EXPIRED:
                raise ReuseExpiredError("Reuse expired")
            elif r.text == Errors.ORDER_NO_SMS:
                raise OrderNoSMSError("Order no sms")
            elif r.text == Errors.HOSTING_ORDER:
                raise HostingOrderError("Hosting order")
            elif r.text == Errors.ORDER_NOT_FOUND:
                raise OrderNotFoundError("Order not found")
            else:
                log.info(f"Uncaptured 400 Error: {r.text}")

        if r.status_code == 404:
            if r.text == Errors.ORDER_NOT_FOUND or r.text == Errors.ERROR_404:
                raise OrderNotFoundError("Order not found")
            elif r.text == Errors.RECORD_NOT_FOUND:
                raise RecordNotFoundError("Order not found")
            else:
                log.info(f"Uncaptured 404 Error: {r.text}")

        

    # < main function for requests >
    def send(self,
        url: URL, 
        _type: ReqType = ReqType.GET,
         **kwargs):

        r = self.session.request(_type, url, **kwargs)
        log.debug(f"New Request | {_type} - {url}, kwargs={kwargs} | Response<{r.status_code}>: {r.text}")

        self.capture_errors(r)

        return ReqResponse(req=r, json=r.json(), text=r.text, content=r.content)

    # < END >

    def post(self,
        url: URL, 
        _type: ReqType = ReqType.POST,
         **kwargs):
        
        return self.send(url, _type, **kwargs)

    def get(self,
        url: URL, 
        _type: ReqType = ReqType.GET,
         **kwargs):
        
        return self.send(url, _type, **kwargs)

    def head(self,
        url: URL, 
        _type: ReqType = ReqType.HEAD,
         **kwargs):
        
        return self.send(url, _type, **kwargs)

    def options(self,
        url: URL, 
        _type: ReqType = ReqType.OPTIONS,
         **kwargs):
        
        return self.send(url, _type, **kwargs)