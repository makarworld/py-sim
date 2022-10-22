from pysim.logger import log
from req import Session
from data import (
    Service, URL, ApiKey, Category, 
    Limit, Offset, Order, Country, 
    Operator, Product, Number, OrderId,
    Lang
)
from _types import SimOrder

class Type_5simProtocol(Service):
    """
    Service: 5sim
    link: https://5sim.net/
    docs: https://docs.5sim.net

    """
    def __init__(self, key: ApiKey, rpc: URL = "https://5sim.net/v1"):
        self.session = Session()
        self.session.headers({
            "Authorization": f"Bearer {key}",
            "Accept": "application/json"
        })

        self.rpc = rpc
    
    # < User >

    def balance(self) -> dict:
        """Provides profile data: email, balance and rating..
        Returns :class:`dict` object.\n
        Docs: https://docs.5sim.net/#user\n

        :rtype: dict\n
        :response example: { "id":1, "email":"mail@gmail.com", "vendor":"demo", "default_forwarding_number":"78009005040", "balance":100, "rating":96, "default_country": { "name":"russia","iso":"ru","prefix":"+7" }, "default_operator": { "name":"" }, "frozen_balance":0 }
        """
        # ;; Balance ;; 
        #     
        # GET - https://5sim.net/v1/user/profile
        # https://docs.5sim.net/#user

        return self.session.get(
            self.rpc + "/user/profile"
            ).json

    def profile(self) -> dict:
        """Hook to balance()"""
        return self.balance()

    def orders(self, 
        category: Category, 
        limit: Limit = None, 
        offset: Offset = None, 
        order: Order = None, 
        reverse: bool = None) -> dict:
        """Provides orders history by choosen :class:`Category`..
        Returns :class:`dict` object.\n
        Docs: https://docs.5sim.net/#orders-history\n

        :category:  :class:`Category` can be 'Category.HOSTING' or 'Category.ACTIVATION'.\n
        :limit: (optional) Pagination :class:`Limit`.\n
        :offset: (optional) Pagination :class:`Offset`.\n
        :order: (optional) Pagination :class:`Order`, should be field name.\n
        :reverse: (optional) Is reversed history, true / false.\n
        :rtype: dict\n
        :response example: { "Data": [ { "id":53533933, "phone":"+79085895281", "operator":"tele2", "product":"aliexpress", "price":2, "status":"BANNED", "expires":"2020-06-28T16:32:43.307041Z", "sms":[], "created_at":"2020-06-28T16:17:43.307041Z", "country":"russia" } ], "ProductNames":[], "Statuses":[], "Total":3 }
        """
        # ;; Orders history ;;
        # 
        # GET - https://5sim.net/v1/user/orders?category=$category
        # https://docs.5sim.net/#orders-history

        params = {
            "category": category,
            "limit": limit,
            "offset": offset,
            "order": order,
            "reverse": reverse
        }

        return self.session.get(
            self.rpc + "/user/orders",
            params = {k: v for k, v in params.items() if v is not None} # remove None items
            ).json

    def payments(self, 
        limit: Limit = None, 
        offset: Offset = None, 
        order: Order = None, 
        reverse: bool = None) -> dict:
        """Provides payments history..
        Returns :class:`dict` object.\n
        Docs: https://docs.5sim.net/#payments-history\n

        :limit: (optional) Pagination :class:`Limit`.\n
        :offset: (optional) Pagination :class:`Offset`.\n
        :order: (optional) Pagination :class:`Order`, should be field name.\n
        :reverse: (optional) Is reversed history, true / false.\n
        :rtype: dict\n
        :response example: { "Data": [ { "ID":30011934, "TypeName":"charge", "ProviderName":"admin", "Amount":100, "Balance":100, "CreatedAt":"2020-06-24T15:37:08.149895Z" } ], "PaymentTypes": [{"Name":"charge"}], "PaymentProviders":[{"Name":"admin"}], "Total":1 }
        """
        # ;; Payments history ;;
        # 
        # GET - https://5sim.net/v1/user/payments
        # https://docs.5sim.net/#payments-history

        params = {
            "limit": limit,
            "offset": offset,
            "order": order,
            "reverse": reverse
        }

        return self.session.get(
            self.rpc + "/user/payments",
            params = {k: v for k, v in params.items() if v is not None} # remove None items
            ).json

    # < END User >

    # < Products and prices >
    def products(self, country: Country, operator: Operator) -> dict:
        """To receive the name, the price, quantity of all products, available to buy..
        Returns :class:`dict` object.\n
        Docs: https://docs.5sim.net/#products-and-prices\n

        :country: The :class:`Country`, "Country.ANY" - any country.\n
        :operator: The :class:`Operator`, "Operator.ANY" - any operator.\n
        :rtype: dict\n
        :response example: {"1day":{"Category":"hosting","Qty":14,"Price":80},"vkontakte":{"Category":"activation","Qty":133,"Price":21}}
        """
        # ;; Products request ;;
        # 
        # GET - https://5sim.net/v1/guest/products/$country/$operator
        # https://docs.5sim.net/#products-and-prices

        return self.session.get(
            self.rpc + f"/guest/products/{country}/{operator}",
            ).json

    def prices(self, country: Country=None, product: Product=None) -> dict:
        """Returns product prices (optional by country or/and product)..
        Returns :class:`dict` object.\n
        Docs1: https://docs.5sim.net/#prices-request\n
        Docs2: https://docs.5sim.net/#prices-by-country\n
        Docs3: https://docs.5sim.net/#prices-by-product\n
        Docs4: https://docs.5sim.net/#prices-by-country-and-product\n

        :country: (optional) :class:`Country` name\n
        :product: (optional) :class:`Product` name\n
        :rtype: dict\n
        :response example: {"russia":{"1688":{"beeline":{"cost":4,"count":1260},"lycamobile":{"cost":4,"count":935},"matrix":{"cost":4,"count":0}}}}
        """
        # ;; Prices request ;;
        # 
        # GET - https://5sim.net/v1/guest/prices
        # https://docs.5sim.net/#products-and-prices
        params = {
            'country': country,
            'product': product
        }
        return self.session.get(
            self.rpc + f"/guest/prices",
            params = {k:v for k, v in params.items() if v is not None} # remove None items
            ).json

    # < END Products and prices >

    # < Purchase >

    def buy(self, 
        product: Product,
        country: Country = Country.ANY, 
        operator: Operator = Operator.ANY, 
        forwarding: str = None,
        number: Number = None,
        reuse: int = None,
        voice: int = None,
        ref: str = None) -> SimOrder:
        """Buy activation number..
        Returns :class:`SimOrder` object.\n
        Docs: https://docs.5sim.net/#buy-activation-number\n

        :country: The :class:`Country`, "Country.ANY" - any country\n
        :operator: The :class:`Operator`, "Operator.ANY" - any operator\n
        :product:  :class:`Product` name\n
        :forwarding: (optional) Whether or not to enable forwarding\n
        :number: (optional) :class:`Number` for which the call will be forwarded, only the Russian numbers, 11 digits, without the + sign\n
        :reuse: (optional) If equal to "1" buy with the ability to reuse the number, if available\n
        :voice: (optional) If equal to "1" buy with the ability to receive a call from the robot, if available\n
        :ref: (optional) Your referral key if you have it.\n

        :rtype: SimOrder\n
        :response example: SimOrder({"id":11631253,"phone":"+79000381454","operator":"beeline","product":"vkontakte","price":21,"status":"PENDING","expires":"2018-10-13T08:28:38.809469028Z","sms":null,"created_at":"2018-10-13T08:13:38.809469028Z","forwarding":false,"forwarding_number":"","country":"russia"})
        """
        # ;; Buy activation number ;;
        # 
        # GET - https://5sim.net/v1/user/buy/activation/$country/$operator/$product
        # GET - https://5sim.net/v1/user/buy/activation/$country/$operator/$product?forwarding=$forwarding&number=$number&reuse=$reuse&voice=$voice&ref=$ref
        # https://docs.5sim.net/#buy-activation-number
        params = {
            'forwarding': forwarding,
            'number': number,
            'reuse': reuse,
            'voice': voice,
            'ref': ref
        }

        # wrap response to class SimOrder for easy interaction with order 
        SO = SimOrder(self.session.get(
            self.rpc + f"/user/buy/activation/{country}/{operator}/{product}",
            params = {k:v for k, v in params.items() if v is not None} # remove None items
            ).json)

        SO.set_protocol(self)

        return SO
        
        
        

    def buy_hosting(self, 
        product: Product,
        country: Country = Country.ANY, 
        operator: Operator = Operator.ANY, 
        ) -> SimOrder:
        """Buy hosting number..
        Returns :class:`SimOrder` object.\n
        Docs: https://docs.5sim.net/#buy-hosting-number\n

        :country: The :class:`Country`, "Country.ANY" - any country\n
        :operator: The :class:`Operator`, "Operator.ANY" - any operator\n
        :product:  :class:`Product` name\n
       
        :rtype: SimOrder\n
        :response example: { "id": 1, "phone": "+79008001122", "product": "1day", "price": 1, "status": "PENDING", "expires": "1970-12-01T03:00:00.000000Z", "sms": [ { "id":3027531, "created_at":"1970-12-01T17:23:25.106597Z", "date":"1970-12-01T17:23:15Z", "sender":"Facebook", "text":"Use 415127 as your login code", "code":"415127" } ], "created_at": "1970-12-01T00:00:00.000000Z" }
        """
        # ;; Buy hosting number ;;
        # 
        # GET - https://5sim.net/v1/user/buy/hosting/$country/$operator/$product
        # https://docs.5sim.net/#buy-hosting-number

        SO = SimOrder(self.session.get(
            self.rpc + f"/user/buy/hosting/{country}/{operator}/{product}",
            ).json)

        SO.set_protocol(self)

        return SO

    def reuse(self, product: Product, number: Number) -> SimOrder:
        """Re-buy number..
        Returns :class:`SimOrder` object.\n
        Docs: https://docs.5sim.net/#re-buy-number\n

        :product: :class:`Product` name\n
        :number: Phone number, 4-15 digits (without the + sign)\n

        :rtype: SimOrder\n
        :response example: {} # No example on the site
        """
        # ;; Re-buy number ;;
        # 
        # GET - https://5sim.net/v1/user/reuse/$product/$number
        # https://docs.5sim.net/#re-buy-number

        SO = SimOrder(self.session.get(
            self.rpc + f"/user/reuse/{product}/{number}",
            ).json)

        SO.set_protocol(self)

        return SO

    # < END Purchase >

    # < Order managment >

    def check(self, id: OrderId) -> SimOrder:
        """Check order (Get SMS)..
        Returns :class:`SimOrder` object.\n
        Docs: https://docs.5sim.net/#check-order-get-sms\n

        :id: :class:`OrderId`\n

        :rtype: SimOrder\n
        :response example: { "id": 11631253, "created_at": "2018-10-13T08:13:38.809469028Z", "phone": "+79000381454", "product": "vkontakte", "price": 21, "status": "RECEIVED", "expires": "2018-10-13T08:28:38.809469028Z", "sms": [ { "id":3027531, "created_at":"2018-10-13T08:20:38.809469028Z", "date":"2018-10-13T08:19:38Z", "sender":"VKcom", "text":"VK: 09363 - use this code to reclaim your suspended profile.", "code":"09363" } ], "forwarding": false, "forwarding_number": "", "country":"russia" }
        """
        # ;; Check order (Get SMS) ;;
        # 
        # GET - https://5sim.net/v1/user/check/$id
        # https://docs.5sim.net/#check-order-get-sms

        SO = SimOrder(self.session.get(
            self.rpc + f"/user/check/{id}",
            ).json)

        SO.set_protocol(self)

        return SO

    def finish(self, id: OrderId) -> SimOrder:
        """Finish order..
        Returns :class:`SimOrder` object.\n
        Docs: https://docs.5sim.net/#finish-order\n

        :id: :class:`OrderId`\n

        :rtype: SimOrder\n
        :response example: { "id": 11631253, "created_at": "2018-10-13T08:13:38.809469028Z", "phone": "+79000381454", "product": "vkontakte", "price": 21, "status": "FINISHED", "expires": "2018-10-13T08:28:38.809469028Z", "sms": [ { "id":3027531, "created_at":"2018-10-13T08:20:38.809469028Z", "date":"2018-10-13T08:19:38Z", "sender":"VKcom", "text":"VK: 09363 - use this code to reclaim your suspended profile.", "code":"09363" } ], "forwarding": false, "forwarding_number": "", "country":"russia" }
        """
        # ;; Finish order ;;
        # 
        # GET - https://5sim.net/v1/user/finish/$id
        # https://docs.5sim.net/#finish-order

        SO = SimOrder(self.session.get(
            self.rpc + f"/user/finish/{id}",
            ).json)

        SO.set_protocol(self)

        return SO

    def cancel(self, id: OrderId) -> SimOrder:
        """Cancel order..
        Returns :class:`SimOrder` object.\n
        Docs: https://docs.5sim.net/#cancel-order\n

        :id: :class:`OrderId`\n

        :rtype: SimOrder\n
        :response example: { "id": 11631253, "created_at": "2018-10-13T08:13:38.809469028Z", "phone": "+79000381454", "product": "vkontakte", "price": 21, "status": "CANCELED", "expires": "2018-10-13T08:28:38.809469028Z", "sms": [ { "id":3027531, "created_at":"2018-10-13T08:20:38.809469028Z", "date":"2018-10-13T08:19:38Z", "sender":"VKcom", "text":"VK: 09363 - use this code to reclaim your suspended profile.", "code":"09363" } ], "forwarding": false, "forwarding_number": "", "country":"russia" }
        """
        # ;; Cancel order ;;
        # 
        # GET - https://5sim.net/v1/user/cancel/$id
        # https://docs.5sim.net/#cancel-order

        SO = SimOrder(self.session.get(
            self.rpc + f"/user/cancel/{id}",
            ).json)

        SO.set_protocol(self)

        return SO

    def ban(self, id: OrderId) -> dict:
        """Ban order..
        Returns :class:`SimOrder` object.\n
        Docs: https://docs.5sim.net/#ban-order\n

        :id: :class:`OrderId`\n

        :rtype: SimOrder\n
        :response example: { "id": 11631253, "created_at": "2018-10-13T08:13:38.809469028Z", "phone": "+79000381454", "product": "vkontakte", "price": 21, "status": "BANNED", "expires": "2018-10-13T08:28:38.809469028Z", "sms": [ { "id":3027531, "created_at":"2018-10-13T08:20:38.809469028Z", "date":"2018-10-13T08:19:38Z", "sender":"VKcom", "text":"VK: 09363 - use this code to reclaim your suspended profile.", "code":"09363" } ], "forwarding": false, "forwarding_number": "", "country":"russia" }
        """
        # ;; Ban order ;;
        # 
        # GET - https://5sim.net/v1/user/ban/$id
        # https://docs.5sim.net/#ban-order

        SO = SimOrder(self.session.get(
            self.rpc + f"/user/ban/{id}",
            ).json)

        SO.set_protocol(self)

        return SO

    def inbox(self, id: OrderId) -> dict:
        """Get SMS inbox list by order's id..
        Returns :class:`dict` object.\n
        Docs: https://docs.5sim.net/#sms-inbox-list\n

        :id: :class:`OrderId`\n

        :rtype: dict\n
        :response example: { "Data": [ { "ID":844928, "created_at":"2017-09-05T15:48:33.763297Z", "date":"2017-09-05T15:48:27Z", "sender":"+79998887060", "text":"12345", "code":"", "is_wave":false, "wave_uuid":"" } ], "Total":1 }
        """
        # ;; Ban order ;;
        # 
        # GET - https://5sim.net/v1/user/sms/inbox/$id
        # https://docs.5sim.net/#sms-inbox-list

        return self.session.get(
            self.rpc + f"/user/sms/inbox/{id}",
            ).json

    # < END Order managment >

    # < Notifications >

    def notifications(self, lang: Lang = Lang.EN) -> dict:
        """Get notifications..
        Returns :class:`dict` object.\n
        Docs: https://docs.5sim.net/#notifications\n

        :lang: :class:`Lang`of notification, Lang.RU or Lang.EN\n

        :rtype: dict\n
        :response example: { "text":"...notification text..." }
        """
        # ;; Get notifications ;;
        # 
        # GET - https://5sim.net/v1/guest/flash/$lang
        # https://docs.5sim.net/#notifications

        return self.session.get(
            self.rpc + f"/guest/flash/{lang}",
            ).json

    # < END Notifications >

    # < Vendors >

    def vendor(self) -> dict:
        """Vendor statistic..
        Returns :class:`dict` object.\n
        Docs: https://docs.5sim.net/#vendor-statistic\n

        :rtype: dict\n
        :response example: { "id":1, "email":"mail@gmail.com", "vendor":"demo", "default_forwarding_number":"78009005040", "balance":100, "rating":96, "default_country": { "name":"russia","iso":"ru","prefix":"+7" }, "default_operator": { "name":"" }, "frozen_balance":0 }
        """
        # ;; Vendor statistic ;;
        # 
        # GET - https://5sim.net/v1/user/vendor
        # https://docs.5sim.net/#vendor-statistic

        return self.session.get(
            self.rpc + f"/user/vendor",
            ).json

    def vendor_wallets(self) -> dict:
        """Available reserves currency for partner..
        Returns :class:`dict` object.\n
        Docs: https://docs.5sim.net/#wallets-reserve\n

        :rtype: dict\n
        :response example: {"fkwallet":43339.55,"payeer":2117.32,"unitpay":97.6}
        """
        # ;; Wallets reserve ;;
        # 
        # GET - https://5sim.net/v1/vendor/wallets
        # https://docs.5sim.net/#wallets-reserve

        return self.session.get(
            self.rpc + f"/vendor/wallets",
            ).json

    def vendor_orders(self,
        category: Category, 
        limit: Limit = None, 
        offset: Offset = None, 
        order: Order = None, 
        reverse: bool = None) -> dict:
        """Provides vendor's orders history by chosen :class:`Category`..
        Returns :class:`dict` object.\n
        Docs: https://docs.5sim.net/#vendor-orders-history\n

        :category:  :class:`Category` can be 'Category.HOSTING' or 'Category.ACTIVATION'.\n
        :limit: (optional) Pagination :class:`Limit`.\n
        :offset: (optional) Pagination :class:`Offset`.\n
        :order: (optional) Pagination :class:`Order`, should be field name.\n
        :reverse: (optional) Is reversed history, true / false.\n
        :rtype: dict\n
        :response example: { "Data": [], "ProductNames":[], "Statuses":[], "Total":3 }
        """
        # ;; Orders history ;;
        # 
        # GET - https://5sim.net/v1/vendor/orders?category=$category
        # https://docs.5sim.net/#vendor-orders-history

        params = {
            "category": category,
            "limit": limit,
            "offset": offset,
            "order": order,
            "reverse": reverse
        }

        return self.session.get(
            self.rpc + "/vendor/orders",
            params = {k: v for k, v in params.items() if v is not None} # remove None items
            ).json

    def vendor_payments(self,
        limit: Limit = None, 
        offset: Offset = None, 
        order: Order = None, 
        reverse: bool = None) -> dict:
        """Provides vendor's payments history..
        Returns :class:`dict` object.\n
        Docs: https://docs.5sim.net/#vendor-payments-history\n

        :limit: (optional) Pagination :class:`Limit`.\n
        :offset: (optional) Pagination :class:`Offset`.\n
        :order: (optional) Pagination :class:`Order`, should be field name.\n
        :reverse: (optional) Is reversed history, true / false.\n
        :rtype: dict\n
        :response example: { "Data": [], "PaymentProviders":null, "PaymentStatuses":null, "PaymentTypes":null, "Total":3 }
        """
        # ;; Vendor payments history ;;
        # 
        # GET - https://5sim.net/v1/vendor/payments
        # https://docs.5sim.net/#vendor-payments-history

        params = {
            "limit": limit,
            "offset": offset,
            "order": order,
            "reverse": reverse
        }

        return self.session.get(
            self.rpc + "/vendor/payments",
            params = {k: v for k, v in params.items() if v is not None} # remove None items
            ).json

    def vendor_withdraw(self,
        receiver: str, 
        method: str, 
        amount: int, 
        fee: str) -> dict:
        """Create payouts for a partner..
        Returns :class:`dict` object.\n
        Docs: https://docs.5sim.net/#create-payouts\n

        :receiver: Receiver.\n
        :method: Output method visa / qiwi / yandex.\n
        :amount: Amount.\n
        :fee: Payment system fkwallet / payeer / unitpay.\n
        :rtype: dict\n
        :response example: {} # No example on the site.
        """
        # ;; Create payouts ;;
        # 
        # POST - https://5sim.net/v1/vendor/withdraw
        # https://docs.5sim.net/#create-payouts

        data = {
            "receiver": receiver,
            "method": method,
            "amount": amount,
            "fee": fee
        }

        return self.session.post(
            self.rpc + "/vendor/withdraw",
            data = data
            ).json

    # < END Vendors >

    # < Countries list >

    def countries(self):
        """Returns a list of countries with available operators for purchase..
        Returns :class:`dict` object.\n
        Docs: https://docs.5sim.net/#countries-list\n

        :rtype: dict\n
        :response example: {"afghanistan":{"iso":{"af":1},"prefix":{"+93":1},"text_en":"Afghanistan","text_ru":"Афганистан","virtual18":{"activation":1},"virtual21":{"activation":1},"virtual23":{"activation":1},"virtual4":{"activation":1}}}
        """
        # ;; Get countries list ;;
        # 
        # GET - https://5sim.net/v1/guest/countries
        # https://docs.5sim.net/#countries-list

        return self.session.get(
            self.rpc + "/guest/countries",
            ).json

    # < END Countries list >

