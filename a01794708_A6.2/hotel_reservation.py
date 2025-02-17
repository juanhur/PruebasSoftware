"""clase de hoteles,clientes y reservaciones."""
import json
import os


class Hotel:
    """Clase que representa un hotel."""

    DATA_FILE = "hotels.json"

    def __init__(self, hotel_id, name, location, rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms = rooms

    def to_dict(self):
        """Convertiro objeto a dic"""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "rooms": self.rooms,
        }

    @classmethod
    def save_to_file(cls, hotels):
        """Guarda la lista de hoteles en un archivo JSON."""
        try:
            with open(cls.DATA_FILE, "w", encoding="utf-8") as file:
                json.dump([hotel.to_dict() for hotel in hotels], file)
        except IOError as e:
            print(f"Error al guardar los hoteles: {e}")

    @classmethod
    def load_from_file(cls):
        """Carga la lista de hoteles desde un archivo JSON."""
        if not os.path.exists(cls.DATA_FILE):
            return []
        try:
            with open(cls.DATA_FILE, "r", encoding="utf-8") as file:
                return [cls(**data) for data in json.load(file)]
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error al cargar los hoteles: {e}")
            return []

    @classmethod
    def create_hotel(cls, hotel_id, name, location, rooms):
        """Crea un nuevo hotel y lo guarda en archivo."""
        hotels = cls.load_from_file()
        hotels.append(cls(hotel_id, name, location, rooms))
        cls.save_to_file(hotels)

    @classmethod
    def delete_hotel(cls, hotel_id):
        """Elimina un hotel por su ID."""
        hotels = cls.load_from_file()
        hotels = [hotel for hotel in hotels if hotel.hotel_id != hotel_id]
        cls.save_to_file(hotels)

    @classmethod
    def display_hotel_info(cls, hotel_id):
        """Muestra la información de un hotel por su ID."""
        hotels = cls.load_from_file()
        for hotel in hotels:
            if hotel.hotel_id == hotel_id:
                print(f"Hotel ID: {hotel.hotel_id}")
                print(f"Nombre: {hotel.name}")
                print(f"Ubicación: {hotel.location}")
                print(f"Habitaciones: {hotel.rooms}")
                return
        print("Hotel no encontrado.")

    @classmethod
    def modify_hotel_info(cls, hotel_id, name=None, location=None, rooms=None):
        """Modifica la información de un hotel."""
        hotels = cls.load_from_file()
        for hotel in hotels:
            if hotel.hotel_id == hotel_id:
                if name:
                    hotel.name = name
                if location:
                    hotel.location = location
                if rooms:
                    hotel.rooms = rooms
                cls.save_to_file(hotels)
                print("Información del hotel modificada.")
                return
        print("Hotel no encontrado.")


class Customer:
    """Clase que representa un cliente."""

    DATA_FILE = "customers.json"

    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self):
        """regresa diccionario de custumer"""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def save_to_file(cls, customers):
        """Guarda la lista de clientes en un archivo JSON."""
        try:
            with open(cls.DATA_FILE, "w", encoding="utf-8") as file:
                json.dump([customer.to_dict() for customer in customers], file)
        except IOError as e:
            print(f"Error al guardar los clientes: {e}")

    @classmethod
    def load_from_file(cls):
        """Carga la lista de clientes desde un archivo JSON."""
        if not os.path.exists(cls.DATA_FILE):
            return []
        try:
            with open(cls.DATA_FILE, "r", encoding="utf-8") as file:
                return [cls(**data) for data in json.load(file)]
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error al cargar los clientes: {e}")
            return []

    @classmethod
    def create_customer(cls, customer_id, name, email):
        """Crea un nuevo cliente y lo guarda en archivo."""
        customers = cls.load_from_file()
        customers.append(cls(customer_id, name, email))
        cls.save_to_file(customers)

    @classmethod
    def delete_customer(cls, customer_id):
        """Elimina un cliente por su ID."""
        customers = cls.load_from_file()
        customers = [
            customer for customer
            in customers if customer.customer_id != customer_id
            ]
        cls.save_to_file(customers)

    @classmethod
    def display_customer_info(cls, customer_id):
        """Muestra la información de un cliente por su ID."""
        customers = cls.load_from_file()
        for customer in customers:
            if customer.customer_id == customer_id:
                print(f"Cliente ID: {customer.customer_id}")
                print(f"Nombre: {customer.name}")
                print(f"Email: {customer.email}")
                return
        print("Cliente no encontrado.")

    @classmethod
    def modify_customer_info(cls, customer_id, name=None, email=None):
        """Modifica la información de un cliente."""
        customers = cls.load_from_file()
        for customer in customers:
            if customer.customer_id == customer_id:
                if name:
                    customer.name = name
                if email:
                    customer.email = email
                cls.save_to_file(customers)
                print("Información del cliente modificada.")
                return
        print("Cliente no encontrado.")


class Reservation:
    """Clase que representa una reservación."""

    DATA_FILE = "reservations.json"

    def __init__(self, reservation_id, customer_id, hotel_id):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def to_dict(self):
        """regresa diccionario de reservacion"""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
        }

    @classmethod
    def save_to_file(cls, reservations):
        """Guarda la lista de reservaciones en un archivo JSON."""
        try:
            with open(cls.DATA_FILE, "w", encoding="utf-8") as file:
                json.dump([res.to_dict() for res in reservations], file)
        except IOError as e:
            print(f"Error al guardar las reservaciones: {e}")

    @classmethod
    def load_from_file(cls):
        """Carga la lista de reservaciones desde un archivo JSON."""
        if not os.path.exists(cls.DATA_FILE):
            return []
        try:
            with open(cls.DATA_FILE, "r", encoding="utf-8") as file:
                return [cls(**data) for data in json.load(file)]
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error al cargar las reservaciones: {e}")
            return []

    @classmethod
    def create_reservation(cls, reservation_id, customer_id, hotel_id):
        """Crea una nueva reservación."""
        reservations = cls.load_from_file()
        reservations.append(cls(reservation_id, customer_id, hotel_id))
        cls.save_to_file(reservations)

    @classmethod
    def cancel_reservation(cls, reservation_id):
        """Cancela una reservación por su ID."""
        reservations = cls.load_from_file()
        reservations = [res for res in reservations
                        if res.reservation_id != reservation_id]
        cls.save_to_file(reservations)
        print(f"Reserva {reservation_id} cancelada.")
