import json
import time
import os
import requests

from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from nameko_tracer import Tracer
from nameko_structlog import StructlogDependency

HEALTH_CHECK_PERIOD = 60 # in seconds

def _check_get_200( url ):
    status = True
    message = 'Ok'
    try:
        response = requests.get(url, timeout = 5 )
        if response.status_code != 200: raise Exception()
    except:
            status = False
            message = 'Unknown'
    return status , message 

def check_airports( instance ):
    return _check_get_200( os.environ.get( 'AIRPORTS_HEALTH_CHECK' ) )


def check_trips( instance ):
    return _check_get_200( os.environ.get( 'TRIPS_HEALTH_CHECK' ) )

class GatewayService:
    name = 'gateway'

    airports_rpc = RpcProxy('airports_service')
    trips_rpc = RpcProxy('trips_service')

    tracer = Tracer()
    log = StructlogDependency()

    health_check_func = {
        'trips': check_trips,
        'gateways': check_airports
    }

    @http('GET', '/bum')
    def bum(self, request):
        raise Exception("bang!")

    @http('GET', '/trip-bum')
    def trip_bum(self, request):
        ans = self.trips_rpc.bum()
        return json.dumps({'Trip': ans})

    @http('GET', '/ping')
    def ping(self, request):
        self.log.info(message=f"Your name is {self.name}", type="greeting")
        return "Pong!"

    @http('GET', '/airport-ping')
    def airport_ping(self, request):
        ans = self.airports_rpc.ping()
        return json.dumps({'Airport': ans})

    @http('GET', '/trip-ping')
    def trip_ping(self, request):
        ans = self.trips_rpc.ping()
        return json.dumps({'Trip': ans})

    @http('GET', '/airport/<string:airport_id>')
    def get_airport(self, request, airport_id):
        airport = self.airports_rpc.get(airport_id)
        return json.dumps({'airport': airport})

    @http('POST', '/airport')
    def post_airport(self, request):
        data = json.loads(request.get_data(as_text=True))
        airport_id = self.airports_rpc.create(data['airport'])

        return airport_id

    @http('GET', '/trip/<string:trip_id>')
    def get_trip(self, request, trip_id):
        trip = self.trips_rpc.get(trip_id)
        return json.dumps({'trip': trip})

    @http('POST', '/trip')
    def post_trip(self, request):
        data = json.loads(request.get_data(as_text=True))
        trip_id = self.trips_rpc.create(data['airport_from'], data['airport_to'])

        return trip_id

    @http('GET', '/health')
    def health_check(self, request):
        healthy = True
        message = []

        for k,check in self.health_check_func.items():
            func_status_ok , func_message = check(self)
            message.append( f'    {k} status: {"OK" if func_status_ok else "Error. "+func_message}' )
            healthy &= func_status_ok
        message.insert(0, f"{self.name} status: {'OK' if healthy else 'Error'}\nDependencies:")
        message.append(f'Last update: {time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime() )}')

        return (200 if healthy else 500 ) , '\n'.join(message)