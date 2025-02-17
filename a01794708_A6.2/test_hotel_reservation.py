"""Pruebas unitarias"""
import unittest
from hotel_reservation import Hotel, Customer, Reservation


class TestHotelReservation(unittest.TestCase):
    """Pruebas unitarias para el sistema de reservas."""

    def setUp(self):
        """Configura el entorno antes de cada prueba."""
        self.hotel = Hotel(1, "el dorado Hotel", "cuenca", 50)
        self.customer = Customer(1, "pedro hurtado", "pedrohurtado@gmail.com")
        self.reservation = Reservation(1, 1, 1)

    def test_create_hotel(self):
        """Prueba la creación de un hotel."""
        print("Prueba la creación de un hotel.")
        print("--------------------------------")
        hotels = [self.hotel]
        Hotel.save_to_file(hotels)
        loaded_hotels = Hotel.load_from_file()
        self.assertEqual(loaded_hotels[0].name, "el dorado Hotel")

    def test_create_customer(self):
        """Prueba la creación de un cliente."""
        print("Prueba la creación de un cliente.")
        print("--------------------------------")
        customers = [self.customer]
        Customer.save_to_file(customers)
        loaded_customers = Customer.load_from_file()
        self.assertEqual(loaded_customers[0].email, "pedrohurtado@gmail.com")

    def test_create_reservation(self):
        """Prueba la creación de una reserva."""
        print("Prueba la creación de una reserva.")
        print("--------------------------------")
        reservations = [self.reservation]
        Reservation.save_to_file(reservations)
        loaded_reservations = Reservation.load_from_file()
        self.assertEqual(loaded_reservations[0].reservation_id, 1)

    def test_hotel_persistence(self):
        """Prueba la persistencia de hoteles en archivo."""
        print("Prueba la persistencia de hoteles en archivo.")
        print("--------------------------------")
        Hotel.create_hotel(2, "Test Hotel", "LA", 30)
        hotels = Hotel.load_from_file()
        self.assertTrue(
            any(hotel.hotel_id == 2 for hotel in hotels)
            )

    def test_save_to_file_permission_error(self):
        """Prueba qué sucede si ocurre un error
        de permisos al guardar en el archivo."""
        print("error permisos al guardar en el archivo")
        print("--------------------------------")
        original_file = Hotel.DATA_FILE
        Hotel.DATA_FILE = "/root/readonly_hotels.json"
        hotels = [self.hotel]
        try:
            Hotel.save_to_file(hotels)
        except IOError as e:
            self.assertIn("Error al guardar los hoteles", str(e))
        finally:
            Hotel.DATA_FILE = original_file

    def test_load_from_file_not_found(self):
        """Prueba qué sucede si el archivo no existe."""
        print("prueba el archiov no existe")
        print("--------------------------------")
        original_file = Hotel.DATA_FILE
        Hotel.DATA_FILE = "/root/nonexistent_hotels.json"
        hotels = Hotel.load_from_file()
        self.assertEqual(hotels, [])
        Hotel.DATA_FILE = original_file

    def test_load_from_file_json_error(self):
        """Prueba qué sucede si el archivo JSON está corrupto."""
        print("prueba json corrupto")
        print("--------------------------------")
        # Crea un archivo corrupto
        a = "{ hotel_id: 1, name:"
        b = "'el dorado Hotel',"
        c = "location: 'cuenca', rooms: 50 }"
        with open(Hotel.DATA_FILE, "w", encoding="utf-8") as file:
            file.write(
                a+b+c
                )  # JSON inválido
        hotels = Hotel.load_from_file()
        self.assertEqual(hotels, [])

    def test_delete_hotel(self):
        """Prueba la eliminación de un hotel por su ID."""
        print("prueba eliminar hotel")
        print("--------------------------------")
        hotels = [self.hotel]
        Hotel.save_to_file(hotels)
        Hotel.delete_hotel(1)
        loaded_hotels = Hotel.load_from_file()
        self.assertEqual(len(loaded_hotels), 0)

    def test_display_hotel_info(self):
        """Prueba la visualización de la información de un hotel."""
        print("prueba visualizar hoteles")
        print("--------------------------------")
        hotels = [self.hotel]
        Hotel.save_to_file(hotels)
        with self.assertLogs(level='INFO') as log:
            Hotel.display_hotel_info(1)
        self.assertIn("Hotel ID: 1", log.output[0])

    def test_modify_hotel_info(self):
        """Prueba la modificación de la información de un hotel."""
        print("prueba modificar info hotel")
        print("--------------------------------")
        hotels = [self.hotel]
        Hotel.save_to_file(hotels)
        Hotel.modify_hotel_info(
            1, name="Nuevo Hotel", location="Quito", rooms=100
            )
        modified_hotels = Hotel.load_from_file()
        self.assertEqual(modified_hotels[0].name, "Nuevo Hotel")
        self.assertEqual(modified_hotels[0].location, "Quito")
        self.assertEqual(modified_hotels[0].rooms, 100)

    def test_delete_customer(self):
        """Prueba la eliminación de un cliente por su ID."""
        print("pruea eliminar cliente")
        print("--------------------------------")
        customers = [self.customer]
        Customer.save_to_file(customers)
        Customer.delete_customer(1)
        loaded_customers = Customer.load_from_file()
        self.assertEqual(len(loaded_customers), 0)

    def test_display_customer_info(self):
        """Prueba la visualización de la información de un cliente."""
        print("prueva visualizar cliente")
        print("--------------------------------")
        customers = [self.customer]
        Customer.save_to_file(customers)
        with self.assertLogs(level='INFO') as log:
            Customer.display_customer_info(1)
        self.assertIn("Cliente ID: 1", log.output[0])

    def test_modify_customer_info(self):
        """Prueba la modificación de la información de un cliente."""
        print("prueba modificar cliente")
        print("--------------------------------")
        customers = [self.customer]
        Customer.save_to_file(customers)
        Customer.modify_customer_info(
            1, name="Juan Pérez", email="juanperez@gmail.com"
            )
        modified_customers = Customer.load_from_file()
        self.assertEqual(modified_customers[0].name, "Juan Pérez")
        self.assertEqual(modified_customers[0].email, "juanperez@gmail.com")

    def test_cancel_reservation(self):
        """Prueba la cancelación de una reservación."""
        print("prueba cancelar reserva")
        print("--------------------------------")
        reservations = [self.reservation]
        Reservation.save_to_file(reservations)
        Reservation.cancel_reservation(1)
        loaded_reservations = Reservation.load_from_file()
        self.assertEqual(len(loaded_reservations), 0)


if __name__ == "__main__":
    unittest.main()
