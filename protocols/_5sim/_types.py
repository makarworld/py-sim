from data import Order

class SimOrder:
    """Class for interaction with order"""
    def __init__(self, order: dict):
        self.__dict__.update(order)

    def __str__(self):
        return self.__dict__.__str__()

    def __repr__(self):
        return self.__dict__.__repr__()

    def set_protocol(self, protocol):
        """:protocol: class for interaction with sms-server"""
        self.protocol = protocol

        return self
    
    def check(self):
        self.__dict__.update(self.protocol.check(self.id).__dict__)
        return self

    def cancel(self):
        self.__dict__.update(self.protocol.cancel(self.id).__dict__)
        return self

    def inbox(self):
        return self.protocol.inbox(self.id)

    def finish(self):
        self.__dict__.update(self.protocol.finish(self.id).__dict__)
        return self
    
    def ban(self):
        self.__dict__.update(self.protocol.ban(self.id).__dict__)
        return self


if __name__ == "__main__":
    SO = SimOrder({"id":324062266,"phone":"+79852461218","operator":"mts","product":"tinder","price":1.5,"status":"PENDING","expires":"2022-06-17T21:38:48.876691Z","sms":[],"created_at":"2022-06-17T21:23:48.876691Z","country":"russia"})

