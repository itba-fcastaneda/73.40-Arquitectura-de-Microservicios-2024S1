import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http


class GatewayService:
    name = 'gateway'

    airports_rpc = RpcProxy('airports_service')
    trips_rpc = RpcProxy('trips_service')

    @http('GET', '/ping')
    def ping(self, request):
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
