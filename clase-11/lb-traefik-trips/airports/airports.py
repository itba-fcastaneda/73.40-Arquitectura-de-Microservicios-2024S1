import uuid
import time 

from nameko.rpc import rpc
from nameko_redis import Redis
from nameko.web.handlers import http

HEALTH_CHECK_PERIOD = 60 # in seconds

class AirportsService:
    name = "airports_service"

    redis = Redis('development')

    def __init__(self):
        self.health_check_func = {}
        self.health_check_time = int( time.time() )


    @rpc
    def get(self, airport_id):
        airport = self.redis.get(airport_id)
        return airport

    @rpc
    def create(self, airport):
        airport_id = uuid.uuid4().hex
        self.redis.set(airport_id, airport)
        return airport_id

    @http('GET', '/health')
    def health_check(self, request):
        now = int(time.time())
        healthy = True
        message = []
        if (now - self.health_check_time) > HEALTH_CHECK_PERIOD:
            for k,check in self.health_check_func.items():
                func_status_ok , func_message = check(self)
                message.append( f'{k} status: {"OK" if func_status_ok else "Error. "+func_message}' )
                healthy &= func_status_ok
            self.health_check_time = now

        message.insert(0, f"{self.name} status: {'OK' if healthy else 'Error'}\nDependencies:")

        return (200 if healthy else 500 ) , '\n'.join(message)