"""
Chatchana Chaenban
683040487-6
P2
"""
from abc import ABC, abstractmethod
class Vehicle(ABC):
    """
    Abstract base class representing a vehicle.
    """
    def __init__(self, make, model, year):
        if not make or not model:
            raise ValueError("Make or Model must be Non-Empty String.")
        if year <= 0:
            raise ValueError("Year must be Positive integer.")
        
        self.make = make
        self.model = model
        self.year = year
        self.is_running = False

    @abstractmethod
    def start_engine(self):
        """Returns a string a start engines"""
        pass

    @abstractmethod
    def stop_engine(self):
        """ Retruns a string a stop engines"""
        pass

    def get_info(self) -> str: # concrete methods
        return f"Vehicle's year as {self.year}, make with {self.make}, and model by {self.model}."
    
class CommercialVehicle(Vehicle):
    """
    Represents a commercial vehicle capable of carrying cargo.
    """

    def __init__(self, make, model, year, license_number: str, max_load: float):
        super().__init__(make, model, year)

        if max_load <= 0:
            raise ValueError("Max load must be Positive.")

        self.license_number = license_number
        self.max_load = max_load
        self.current_load = 0.0

    def start_engine(self):
        self.is_running = True
        print("Commercial vehicle engine starting!!!!....")

    def stop_engine(self):
        self.is_running = False
        print("Commercial vehicle engine stop!!!!!....")

    def load_cargo(self, weight: float) -> bool:
        if weight <= 0:
            raise ValueError("Weight must be Positive.")

        if self.current_load + weight <= self.max_load:
            self.current_load += weight
            return True
        return False

    def unload_cargo(self, weight: float) -> float:
        if weight <= 0:
            raise ValueError("Weight must be Positive.")

        if weight >= self.current_load:
            self.current_load = 0.0
        else:
            self.current_load -= weight

        return self.current_load
    
class Car(Vehicle):
    """
    Represents a passenger car.
    """

    def __init__(self, make, model, year, num_doors: int):
        super().__init__(make, model, year)

        if num_doors <= 0:
            raise ValueError("doors must be Positive.")

        self.num_doors = num_doors

    def start_engine(self):
        self.is_running = True
        print("Car engine's starting!!!!")

    def stop_engine(self):
        self.is_running = False
        print("Car engine's stopped!!!!")

class Trailer(CommercialVehicle):
    """
    Represents a trailer used for hauling cargo.
    """

    def __init__(self, make, model, year, license_number, max_load, num_axles: int = 2):
        super().__init__(make, model, year, license_number, max_load)

        if num_axles <= 0:
            raise ValueError("Number of axles must be Positive.")

        self.num_axles = num_axles

    def get_weight_per_axle(self) -> float:
        if self.num_axles == 0:
            return 0
        return self.current_load / self.num_axles

class DeliveryVan(Car, CommercialVehicle):
    """
    Represents a delivery van using multiple inheritance.
    """
    def __init__(
            self, 
            make, 
            model, 
            year, 
            num_doors,
            license_number,
            max_load
    ):
        Vehicle.__init__(self, make, model, year)
        self.num_doors = num_doors
        self.license_number = license_number
        self.max_load = max_load
        self.current_load = 0.0

        self.delivery_mode = False
    
    def toggle_delivery_mode(self) -> str:
        self.delivery_mode = not self.delivery_mode
        return f"Delivery Mode {'ON' if self.delivery_mode else 'OFF'}"
    
    def begin_service(self):
        print("Starting Delivery at your service...!!!")
        print(self.get_info())

        print("Loadinf Cargo.....")
        self.load_cargo(50)

        self.start_engine()

        print(self.toggle_delivery_mode())

        self.stop_engine()

        print("Unloading Cargo.....!!")
        self.unload_cargo(50)

        print(self.toggle_delivery_mode())
        print("Delivery Service DONE COMPLETE!!!")

    def get_info(self) -> str:
        return (
            f"{self.year} {self.make} {self.model}"
            f"Doors: {self.num_doors}"
            f"License: {self.license_number}"
            f"Load: {self.current_load} / {self.max_load}"
        )
        

if __name__ == "__main__":
    print("=== Testing Car ===")
    car = Car("Toyota", "Corolla", 2022, 4)
    car.start_engine()
    car.stop_engine()
    print(car.get_info())

    print("\n=== Testing Trailer ===")
    trailer = Trailer("Volvo", "XT", 2021, "TRL123", 1000, 4)
    trailer.load_cargo(400)
    print("Weight per axle:", trailer.get_weight_per_axle())

    print("\n=== Testing Delivery Van ===")
    van = DeliveryVan("Ford", "Transit", 2023, 4, "VAN999", 500)
    van.begin_service()