from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AirlineCompanies(db.Model):
    __tablename__ = "airline_companies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=True)
    address_info = db.Column(db.String(45), nullable=True)
    phone_number = db.Column(db.String(45), nullable=True)
    planes = db.relationship('Planes', backref='airline_company', lazy=True)


class Planes(db.Model):
    __tablename__ = "planes"
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(45), nullable=True)
    total_flight_hours = db.Column(db.Float, nullable=True)
    serial_number = db.Column(db.Integer, nullable=False)
    airline_company_id = db.Column(db.Integer, db.ForeignKey('airline_companies.id'), nullable=False)


class Countries(db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    regions = db.relationship('Regions', backref='country', lazy=True)


class Regions(db.Model):
    __tablename__ = "regions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    cities = db.relationship('Cities', backref='region', lazy=True)


class RoutePoints(db.Model):
    __tablename__ = "route_points"
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, nullable=True)
    datetime = db.Column(db.DateTime, nullable=True)
    longitude_latitude = db.Column(db.String(45), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    current_speed = db.Column(db.Float, nullable=True)


class Cities(db.Model):
    __tablename__ = "cities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=False)


class Flights(db.Model):
    __tablename__ = "flights"
    id = db.Column(db.Integer, primary_key=True)
    departure_datetime = db.Column(db.DateTime, nullable=False)
    arriving_datetime = db.Column(db.DateTime, nullable=False)
    airport_from = db.Column(db.String(45), nullable=False)
    airport_to = db.Column(db.String(45), nullable=False)
    flight_number = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Float, nullable=True)
    passengers_list_id = db.Column(db.Integer, nullable=False)  # Add this line
    route_points_id = db.Column(db.Integer, db.ForeignKey('route_points.id'), nullable=False)
    plane_id = db.Column(db.Integer, db.ForeignKey('planes.id'), nullable=False)
    passengers = db.relationship('Passengers', secondary='flights_have_passengers', backref='flights')


class Airports(db.Model):
    __tablename__ = "airports"
    airport_id = db.Column(db.Integer, primary_key=True)
    name_index = db.Column(db.String(45), nullable=False)
    code = db.Column(db.String(45), nullable=False)
    region_id = db.Column(db.Integer, nullable=False)
    region_country_id = db.Column(db.Integer, nullable=False)


class Passengers(db.Model):
    __tablename__ = "passengers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    surname = db.Column(db.String(45), nullable=False)
    passport_data = db.Column(db.String(45), nullable=False)
    serial_passport_number = db.Column(db.Integer, nullable=False)


class FlightsHavePassengers(db.Model):
    __tablename__ = "flights_have_passengers"
    flights_id = db.Column(db.Integer, db.ForeignKey('flights.id'), primary_key=True)
    passengers_id = db.Column(db.Integer, db.ForeignKey('passengers.id'), primary_key=True)