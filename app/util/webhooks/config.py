from requests import post


# Example message: {'content':str({'ID':appID, 'status':'server start'})}
class Webhook:
    def __init__(self, server: str):
        self.server = server

    def msg(self, m: str) -> dict:
        return post(self.server, m)
