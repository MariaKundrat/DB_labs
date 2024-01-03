from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from model import db, Planes, Countries, Regions, Cities, RoutePoints, Flights, Airports, Passengers, \
    FlightsHavePassengers, AirlineCompanies

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cairocoders-ednalan'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:120403@localhost/lab_4'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

CORS(app, supports_credentials=True)

db.init_app(app)

with app.app_context():
    db.create_all()

ma = Marshmallow(app)


class AirlineCompaniesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'city_id', 'address_info', 'phone_number')


class PlanesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'model', 'total_flight_hours', 'serial_number', 'airline_company_id')


class CountriesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


class RegionsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'country_id')


class CitiesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'region_id')


class RoutePointsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'flight_id', 'datetime', 'longitude_latitude', 'latitude', 'current_speed')


class FlightsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'departure_datetime', 'arriving_datetime', 'airport_from', 'airport_to',
                  'flight_number', 'distance', 'passengers_list_id', 'route_points_id', 'plane_id')


class AirportsSchema(ma.Schema):
    class Meta:
        fields = ('airport_id', 'name_index', 'code', 'region_id', 'region_country_id')


class PassengersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'surname', 'passport_data', 'serial_passport_number')


class FlightsHavePassengersSchema(ma.Schema):
    class Meta:
        fields = ('flights_id', 'passengers_id')


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


airline_company_schema = AirlineCompaniesSchema()
airline_companies_schema = AirlineCompaniesSchema(many=True)


@app.route('/airline_companies', methods=['GET'])
def get_airline_companies():
    all_airline_companies = AirlineCompanies.query.all()
    result = airline_companies_schema.dump(all_airline_companies)
    return jsonify(result)


@app.route('/airline_companies/<int:id>', methods=['GET'])
def get_airline_companies_by_id(id):
    airline_company = AirlineCompanies.query.get_or_404(id)
    result = airline_company_schema.dump(airline_company)
    return jsonify(result)


@app.route('/add_airline_companies', methods=['POST'])
def add_airline_companies():
    data = request.get_json()
    new_airline_companies = AirlineCompanies(
        id=data['id'],
        name=data['name'],
        city_id=data['city_id'],
        address_info=data['address_info'],
        phone_number=data['phone_number']
    )
    db.session.add(new_airline_companies)
    db.session.commit()
    return 'New airline company added'


@app.route('/update_airline_company/<int:id>', methods=['PUT'])
def update_airline_company(id):
    airline_company = AirlineCompanies.query.get(id)

    name = request.json.get('name')
    city_id = request.json.get('city_id')
    address_info = request.json.get('address_info')
    phone_number = request.json.get('phone_number')

    if airline_company:
        airline_company.name = name
        airline_company.city_id = city_id
        airline_company.address_info = address_info
        airline_company.phone_number = phone_number

        db.session.commit()
        return jsonify({'message': 'Airline Company updated successfully'})
    else:
        return jsonify({'message': 'Airline Company not found'}), 404


@app.route('/airlinecompanydelete/<int:id>', methods=['DELETE'])
def airline_company_delete(id):
    company = AirlineCompanies.query.get(id)

    if company:
        planes_of_company = Planes.query.filter_by(airline_company_id=id).all()
        for plane in planes_of_company:
            flights_of_plane = Flights.query.filter_by(plane_id=plane.id).all()
            for flight in flights_of_plane:
                db.session.delete(flight)
            db.session.delete(plane)

        db.session.delete(company)
        db.session.commit()
        return jsonify({'message': f'Airline company with ID {id} deleted successfully'})
    else:
        return jsonify({'message': 'Airline company not found'}), 404


plane_schema = PlanesSchema()
planes_schema = PlanesSchema(many=True)


@app.route('/planes', methods=['GET'])
def list_planes():
    all_planes = Planes.query.all()
    results = planes_schema.dump(all_planes)
    return jsonify(results)


@app.route('/planes/<id>', methods=['GET'])
def plane_details(id):
    plane = Planes.query.get(id)
    return plane_schema.jsonify(plane)


@app.route('/add_planes', methods=['POST'])
def add_plane():
    data = request.get_json()
    new_plane = Planes(
        id=data['id'],
        model=data['model'],
        total_flight_hours=data['total_flight_hours'],
        serial_number=data['serial_number'],
        airline_company_id=data['airline_company_id']
    )
    db.session.add(new_plane)
    db.session.commit()
    return 'New plane added'


@app.route('/update_plane/<int:id>', methods=['PUT'])
def update_plane(id):
    plane = Planes.query.get(id)

    model = request.json.get('model')
    total_flight_hours = request.json.get('total_flight_hours')
    serial_number = request.json.get('serial_number')
    airline_company_id = request.json.get('airline_company_id')

    if plane:
        plane.model = model
        plane.total_flight_hours = total_flight_hours
        plane.serial_number = serial_number
        plane.airline_company_id = airline_company_id

        db.session.commit()
        return jsonify({'message': 'Plane updated successfully'})
    else:
        return jsonify({'message': 'Plane not found'}), 404


@app.route('/planesdelete/<int:company_id>', methods=['DELETE'])
def planes_delete(company_id):
    planes_of_company = Planes.query.filter_by(airline_company_id=company_id).all()

    if planes_of_company:
        for plane in planes_of_company:
            flights_of_plane = Flights.query.filter_by(plane_id=plane.id).all()
            for flight in flights_of_plane:
                db.session.delete(flight)
            db.session.commit()

        for plane in planes_of_company:
            db.session.delete(plane)
        db.session.commit()

        return jsonify({'message': f'Planes of Airline company with ID {company_id} deleted successfully'})
    else:
        return jsonify({'message': 'No planes found for the specified Airline company'}), 404


country_schema = CountriesSchema()
countries_schema = CountriesSchema(many=True)


@app.route('/countries', methods=['GET'])
def list_countries():
    all_countries = Countries.query.all()
    results = countries_schema.dump(all_countries)
    return jsonify(results)


@app.route('/countries/<id>', methods=['GET'])
def country_details(id):
    country = Countries.query.get(id)
    return country_schema.jsonify(country)


@app.route('/add_countries', methods=['POST'])
def add_country():
    data = request.get_json()
    new_country = Countries(
        id=data['id'],
        name=data['name']
    )
    db.session.add(new_country)
    db.session.commit()
    return 'New country added'


@app.route('/update_country/<int:id>', methods=['PUT'])
def update_country(id):
    country = Countries.query.get(id)

    name = request.json.get('name')

    if country:
        country.name = name

        db.session.commit()
        return jsonify({'message': 'Country updated successfully'})
    else:
        return jsonify({'message': 'Country not found'}), 404


@app.route('/countriesdelete/<int:country_id>', methods=['DELETE'])
def countries_delete(country_id):
    country = Countries.query.get(country_id)

    if country:
        regions_of_country = Regions.query.filter_by(country_id=country_id).all()

        if regions_of_country:
            for region in regions_of_country:
                cities_of_region = Cities.query.filter_by(region_id=region.id).all()
                for city in cities_of_region:
                    db.session.delete(city)
                db.session.delete(region)

        db.session.delete(country)
        db.session.commit()
        return jsonify({'message': f'Country with ID {country_id} deleted successfully'})
    else:
        return jsonify({'message': 'Country not found'}), 404


region_schema = RegionsSchema()
regions_schema = RegionsSchema(many=True)


@app.route('/regions', methods=['GET'])
def list_regions():
    all_regions = Regions.query.all()
    results = regions_schema.dump(all_regions)
    return jsonify(results)


@app.route('/regions/<id>', methods=['GET'])
def region_details(id):
    region = Regions.query.get(id)
    return region_schema.jsonify(region)


@app.route('/add_regions', methods=['POST'])
def add_region():
    data = request.get_json()
    new_region = Regions(
        id=data['id'],
        name=data['name'],
        country_id=data['country_id']
    )
    db.session.add(new_region)
    db.session.commit()
    return 'New region added'


@app.route('/update_region/<int:id>', methods=['PUT'])
def update_region(id):
    region = Regions.query.get(id)

    name = request.json.get('name')
    country_id = request.json.get('country_id')

    if region:
        region.name = name
        region.country_id = country_id

        db.session.commit()
        return jsonify({'message': 'Region updated successfully'})
    else:
        return jsonify({'message': 'Region not found'}), 404


@app.route('/regionsdelete/<int:region_id>', methods=['DELETE'])
def regions_delete(region_id):
    region = Regions.query.get(region_id)

    if region:
        airports_in_region = Airports.query.filter_by(region_id=region_id).all()

        if airports_in_region:
            for airport in airports_in_region:
                db.session.delete(airport)

        db.session.delete(region)
        db.session.commit()
        return jsonify({'message': f'Region with ID {region_id} deleted successfully'})
    else:
        return jsonify({'message': 'Region not found'}), 404


city_schema = CitiesSchema()
cities_schema = CitiesSchema(many=True)


@app.route('/cities', methods=['GET'])
def list_cities():
    all_cities = Cities.query.all()
    results = cities_schema.dump(all_cities)
    return jsonify(results)


@app.route('/cities/<id>', methods=['GET'])
def city_details(id):
    city = Cities.query.get(id)
    return city_schema.jsonify(city)


@app.route('/add_cities', methods=['POST'])
def add_city():
    data = request.get_json()
    new_city = Cities(
        id=data['id'],
        name=data['name'],
        region_id=data['region_id']
    )
    db.session.add(new_city)
    db.session.commit()
    return 'New city added'


@app.route('/update_city/<int:id>', methods=['PUT'])
def update_city(id):
    city = Cities.query.get(id)

    name = request.json.get('name')
    region_id = request.json.get('region_id')

    if city:
        city.name = name
        city.region_id = region_id

        db.session.commit()
        return jsonify({'message': 'City updated successfully'})
    else:
        return jsonify({'message': 'City not found'}), 404


@app.route('/citiesdelete/<int:city_id>', methods=['DELETE'])
def cities_delete(city_id):
    city = Cities.query.get(city_id)

    if city:
        db.session.delete(city)
        db.session.commit()
        return jsonify({'message': f'City with ID {city_id} deleted successfully'})
    else:
        return jsonify({'message': 'City not found'}), 404


route_points_schema = RoutePointsSchema()
route_points_list_schema = RoutePointsSchema(many=True)


@app.route('/route_points', methods=['GET'])
def list_route_points():
    all_route_points = RoutePoints.query.all()
    results = route_points_list_schema.dump(all_route_points)
    return jsonify(results)


@app.route('/route_points/<id>', methods=['GET'])
def route_point_details(id):
    route_point = RoutePoints.query.get(id)
    return route_points_schema.jsonify(route_point)


@app.route('/add_route_point', methods=['POST'])
def add_route_point():
    data = request.get_json()
    new_route_point = RoutePoints(
        id=data['id'],
        flight_id=data['flight_id'],
        datetime=data['datetime'],
        longitude_latitude=data['longitude_latitude'],
        latitude=data['latitude'],
        current_speed=data['current_speed']
    )
    db.session.add(new_route_point)
    db.session.commit()
    return 'New route point added'


@app.route('/update_route_point/<int:id>', methods=['PUT'])
def update_route_point(id):
    route_point = RoutePoints.query.get(id)

    flight_id = request.json.get('flight_id')
    datetime = request.json.get('datetime')
    longitude_latitude = request.json.get('longitude_latitude')
    latitude = request.json.get('latitude')
    current_speed = request.json.get('current_speed')

    if route_point:
        route_point.flight_id = flight_id
        route_point.datetime = datetime
        route_point.longitude_latitude = longitude_latitude
        route_point.latitude = latitude
        route_point.current_speed = current_speed

        db.session.commit()
        return jsonify({'message': 'Route Point updated successfully'})
    else:
        return jsonify({'message': 'Route Point not found'}), 404


@app.route('/routepointsdelete/<int:route_point_id>', methods=['DELETE'])
def route_points_delete(route_point_id):
    route_point = RoutePoints.query.get(route_point_id)

    if route_point:
        flights_with_route_point = Flights.query.filter_by(route_points_id=route_point_id).all()

        if flights_with_route_point:
            for flight in flights_with_route_point:
                db.session.delete(flight)
            db.session.commit()

        db.session.delete(route_point)
        db.session.commit()
        return jsonify({'message': f'Route point with ID {route_point_id} deleted successfully'})
    else:
        return jsonify({'message': 'Route point not found'}), 404


flights_schema = FlightsSchema()
flights_list_schema = FlightsSchema(many=True)


@app.route('/flights', methods=['GET'])
def list_flights():
    all_flights = Flights.query.all()
    results = flights_list_schema.dump(all_flights)
    return jsonify(results)


@app.route('/flights/<id>', methods=['GET'])
def flights_details(id):
    flight = Flights.query.get(id)
    return flights_schema.jsonify(flight)


@app.route('/add_flights', methods=['POST'])
def add_flight():
    data = request.get_json()
    new_flight = Flights(
        id=data['id'],
        departure_datetime=data['departure_datetime'],
        arriving_datetime=data['arriving_datetime'],
        airport_from=data['airport_from'],
        airport_to=data['airport_to'],
        flight_number=data['flight_number'],
        distance=data['distance'],
        passengers_list_id=data['passengers_list_id'],
        route_points_id=data['route_points_id'],
        plane_id=data['plane_id']
    )
    db.session.add(new_flight)
    db.session.commit()
    return 'New flight added'


@app.route('/update_flight/<int:id>', methods=['PUT'])
def update_flight(id):
    flight = Flights.query.get(id)

    departure_datetime = request.json.get('departure_datetime')
    arriving_datetime = request.json.get('arriving_datetime')
    airport_from = request.json.get('airport_from')
    airport_to = request.json.get('airport_to')
    flight_number = request.json.get('flight_number')
    distance = request.json.get('distance')
    passengers_list_id = request.json.get('passengers_list_id')
    route_points_id = request.json.get('route_points_id')
    plane_id = request.json.get('plane_id')

    if flight:
        flight.departure_datetime = departure_datetime
        flight.arriving_datetime = arriving_datetime
        flight.airport_from = airport_from
        flight.airport_to = airport_to
        flight.flight_number = flight_number
        flight.distance = distance
        flight.passengers_list_id = passengers_list_id
        flight.route_points_id = route_points_id
        flight.plane_id = plane_id

        db.session.commit()
        return jsonify({'message': 'Flight updated successfully'})
    else:
        return jsonify({'message': 'Flight not found'}), 404


@app.route('/flightsdelete/<int:flight_id>', methods=['DELETE'])
def flights_delete(flight_id):
    flight = Flights.query.get(flight_id)

    if flight:
        db.session.delete(flight)
        db.session.commit()
        return jsonify({'message': f'Flight with ID {flight_id} deleted successfully'})
    else:
        return jsonify({'message': 'Flight not found'}), 404


airport_schema = AirportsSchema()
airport_list_schema = AirportsSchema(many=True)


@app.route('/airports', methods=['GET'])
def list_airports():
    all_airports = Airports.query.all()
    results = airport_list_schema.dump(all_airports)
    return jsonify(results)


@app.route('/airports/<id>', methods=['GET'])
def airport_details(id):
    airport = Airports.query.get(id)
    return airport_schema.jsonify(airport)


@app.route('/add_airports', methods=['POST'])
def add_airport():
    data = request.get_json()
    new_airport = Airports(
        airport_id=data['airport_id'],
        name_index=data['name_index'],
        code=data['code'],
        region_id=data['region_id'],
        region_country_id=data['region_country_id']
    )
    db.session.add(new_airport)
    db.session.commit()
    return 'New airport added'


@app.route('/update_airport/<int:id>', methods=['PUT'])
def update_airport(id):
    airport = Airports.query.get(id)

    name_index = request.json.get('name_index')
    code = request.json.get('code')
    region_id = request.json.get('region_id')
    region_country_id = request.json.get('region_country_id')

    if airport:
        airport.name_index = name_index
        airport.code = code
        airport.region_id = region_id
        airport.region_country_id = region_country_id

        db.session.commit()
        return jsonify({'message': 'Airport updated successfully'})
    else:
        return jsonify({'message': 'Airport not found'}), 404


@app.route('/airportsdelete/<int:airport_id>', methods=['DELETE'])
def airports_delete(airport_id):
    airport = Airports.query.get(airport_id)

    if airport:
        db.session.delete(airport)
        db.session.commit()
        return jsonify({'message': f'Airport with ID {airport_id} deleted successfully'})
    else:
        return jsonify({'message': 'Airport not found'}), 404


passengers_schema = PassengersSchema()
passengers_list_schema = PassengersSchema(many=True)


@app.route('/passengers', methods=['GET'])
def list_passengers():
    all_passengers = Passengers.query.all()
    results = passengers_list_schema.dump(all_passengers)
    return jsonify(results)


@app.route('/passengers/<id>', methods=['GET'])
def passenger_details(id):
    passenger = Passengers.query.get(id)
    return passengers_schema.jsonify(passenger)


@app.route('/add_passengers', methods=['POST'])
def add_passenger():
    data = request.get_json()
    new_passenger = Passengers(
        id=data['id'],
        name=data['name'],
        surname=data['surname'],
        passport_data=data['passport_data'],
        serial_passport_number=data['serial_passport_number']
    )
    db.session.add(new_passenger)
    db.session.commit()
    return 'New passenger added'


@app.route('/update_passenger/<int:id>', methods=['PUT'])
def update_passenger(id):
    passenger = Passengers.query.get(id)

    name = request.json.get('name')
    surname = request.json.get('surname')
    passport_data = request.json.get('passport_data')
    serial_passport_number = request.json.get('serial_passport_number')

    if passenger:
        passenger.name = name
        passenger.surname = surname
        passenger.passport_data = passport_data
        passenger.serial_passport_number = serial_passport_number

        db.session.commit()
        return jsonify({'message': 'Passenger updated successfully'})
    else:
        return jsonify({'message': 'Passenger not found'}), 404


@app.route('/passengersdelete/<int:passenger_id>', methods=['DELETE'])
def passengers_delete(passenger_id):
    passenger = Passengers.query.get(passenger_id)

    if passenger:
        db.session.delete(passenger)
        db.session.commit()
        return jsonify({'message': f'Passenger with ID {passenger_id} deleted successfully'})
    else:
        return jsonify({'message': 'Passenger not found'}), 404


flights_have_passengers_schema = FlightsHavePassengersSchema()
flights_have_passengers_list_schema = FlightsHavePassengersSchema(many=True)


@app.route('/flights_have_passengers', methods=['GET'])
def list_flights_passengers():
    all_flights_passengers = FlightsHavePassengers.query.all()
    results = flights_have_passengers_list_schema.dump(all_flights_passengers)
    return jsonify(results)


@app.route('/flights_have_passengers/<flight_id>/<passenger_id>', methods=['GET'])
def flight_passenger_details(flight_id, passenger_id):
    flight_passenger = FlightsHavePassengers.query.filter_by(flights_id=flight_id, passengers_id=passenger_id).first()
    return flights_have_passengers_schema.jsonify(flight_passenger)


@app.route('/add_flights_have_passengers', methods=['POST'])
def add_flight_have_passenger():
    data = request.get_json()
    new_flight_have_passenger = FlightsHavePassengers(
        flights_id=data['flights_id'],
        passengers_id=data['passengers_id']
    )
    db.session.add(new_flight_have_passenger)
    db.session.commit()
    return 'New flight has passenger added'


@app.route('/update_flight_passenger/<int:flight_id>/<int:passenger_id>', methods=['PUT'])
def update_flight_passenger(flight_id, passenger_id):
    flight_passenger = FlightsHavePassengers.query.filter_by(flights_id=flight_id, passengers_id=passenger_id).first()

    new_flight_id = request.json.get('new_flight_id')
    new_passenger_id = request.json.get('new_passenger_id')

    if flight_passenger:
        flight_passenger.flights_id = new_flight_id
        flight_passenger.passengers_id = new_passenger_id

        db.session.commit()
        return jsonify({'message': 'Flight-Passenger association updated successfully'})
    else:
        return jsonify({'message': 'Flight-Passenger association not found'}), 404


@app.route('/flightspassengersdelete/<int:flight_id>/<int:passenger_id>', methods=['DELETE'])
def flights_passengers_delete(flight_id, passenger_id):
    flight_passenger = FlightsHavePassengers.query.filter_by(flights_id=flight_id, passengers_id=passenger_id).first()

    if flight_passenger:
        db.session.delete(flight_passenger)
        db.session.commit()
        return jsonify({'message': f'Flight-Passenger relationship deleted successfully'})
    else:
        return jsonify({'message': 'Flight-Passenger relationship not found'}), 404


@app.route('/connections', methods=['GET'])
def get_connections():
    flights = Flights.query.all()
    connections = []

    for flight in flights:
        plane = Planes.query.filter_by(id=flight.plane_id).first() if flight.plane_id else None
        airline_company_id = plane.airline_company_id if plane else None
        plane_model = plane.model if plane else None

        passengers = [{
            'passenger_id': passenger.id,
            'passenger_name': passenger.name,
            'passenger_surname': passenger.surname
        } for passenger in flight.passengers]

        flight_data = {
            'flight_id': flight.id,
            'airline_company_id': airline_company_id,
            'plane_model': plane_model,
            'passengers': passengers
        }
        connections.append(flight_data)

    return jsonify(connections)
