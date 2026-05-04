from abc import ABC, abstractmethod


class RefuelableMixin:
    def refuel(self):
        print(f"Refueling vehicle {self.model}...")


class Vehicle(ABC):
    def __init__(self, brand, model, year, mileage):
        self.brand = brand
        self.model = model
        self.year = year
        self._mileage = mileage


    @property
    def mileage(self):
        return self._mileage


    @mileage.setter
    def mileage(self, value):
        if value < self._mileage:
            raise ValueError("Mileage cannot be rolled back!")
        self._mileage = value


    @abstractmethod
    def calculate_maintenance_cost(self):
        pass

    def display_info(self):
        print(f"[{self.__class__.__name__}] {self.brand} {self.model} ({self.year}) | Mileage: {self.mileage} km")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class Car(Vehicle, RefuelableMixin):
    def __init__(self, brand, model, year, mileage, doors_count):
        super().__init__(brand, model, year, mileage)
        self.doors_count = doors_count

    def calculate_maintenance_cost(self):
        return self.mileage * 0.5


class Motorcycle(Vehicle, RefuelableMixin):
    def __init__(self, brand, model, year, mileage, has_sidecar):
        super().__init__(brand, model, year, mileage)
        self.has_sidecar = has_sidecar

    def calculate_maintenance_cost(self):
        return self.mileage * 0.3

def service_fleet(vehicles):
    print("--- FLEET SERVICE STARTED ---")
    for v in vehicles:
        v.display_info()
        v.refuel()
        cost = v.calculate_maintenance_cost()
        print(f"Estimated maintenance cost: {cost:.2f} PLN")
        print("-" * 30)


if __name__ == "__main__":
    fleet = [
        Car("Toyota", "Corolla", 2020, 50000, 5),
        Motorcycle("Honda", "CB500F", 2022, 12000, False)
    ]

    service_fleet(fleet)

    try:
        fleet[0].mileage = 40000 
    except ValueError as e:
        print(f"Error: {e}")