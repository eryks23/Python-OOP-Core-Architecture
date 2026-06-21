# fleet-management

> A Python OOP reference implementation for vehicle fleet management — abstract classes, mixins, property validation, and polymorphism in a clean, extensible architecture.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

---

## Description

`fleet_management.py` is a self-contained Python module that models a vehicle fleet using core object-oriented programming patterns. It covers abstract base classes (ABC), mixin composition, property-based validation, and polymorphic dispatch — all within a minimal, readable codebase. The project serves as a clean reference implementation for developers learning Python OOP architecture or looking for a proven starting point for a fleet or asset-management domain model.

---

## Table of Contents

- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

---

## Key Features

- **ABC enforcement** — `Vehicle` is an abstract base class; any subclass that omits `calculate_maintenance_cost()` raises `TypeError` at instantiation time, not at runtime.
- **Odometer integrity via property validation** — the `mileage` setter rejects any value lower than the current reading, preventing accidental rollback.
- **Mixin-based behaviour composition** — `RefuelableMixin` adds `refuel()` to concrete vehicle classes through multiple inheritance, keeping the base class free of optional concerns.
- **Polymorphic fleet service** — `service_fleet()` operates on any `list[Vehicle]` regardless of concrete type; cost calculation and info display are dispatched dynamically.
- **Zero external dependencies** — uses only the Python standard library (`abc` module).

---

## Tech Stack

| Layer         | Technology                                    |
|---------------|-----------------------------------------------|
| Language      | Python 3.8+                                   |
| OOP patterns  | ABC, Mixin, Property, Polymorphism            |
| Dependencies  | stdlib only (`abc`)                           |

---

## Requirements

- **Python 3.8** or higher

Verify your version:

```bash
python --version
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/eryks23/Python-OOP-Core-Architecture.git
cd Python-OOP-Core-Architecture
```

No additional packages are required. Skip `pip install` entirely.

---

## Quick Start

Run the built-in demo:

```bash
python fleet_management.py
```

Expected output:

```
--- FLEET SERVICE STARTED ---
[Car] Toyota Corolla (2020) | Mileage: 50000 km
Refueling vehicle Corolla...
Estimated maintenance cost: 25000.00 PLN
------------------------------
[Motorcycle] Honda CB500F (2022) | Mileage: 12000 km
Refueling vehicle CB500F...
Estimated maintenance cost: 3600.00 PLN
------------------------------
Error: Mileage cannot be rolled back!
```

Use the module in your own script:

```python
from fleet_management import Car, Motorcycle, service_fleet

fleet = [
    Car("BMW", "320d", 2021, 80000, 4),
    Motorcycle("Yamaha", "MT-07", 2023, 5000, False),
]

service_fleet(fleet)

# Update mileage safely
fleet[0].mileage = 82000

# Invalid update — raises ValueError
fleet[0].mileage = 70000  # ValueError: Mileage cannot be rolled back!
```

---

## API Documentation

### `Vehicle` — Abstract Base Class

```python
Vehicle(brand: str, model: str, year: int, mileage: int)
```

| Parameter | Type  | Description                           |
|-----------|-------|---------------------------------------|
| `brand`   | `str` | Manufacturer name                     |
| `model`   | `str` | Model name                            |
| `year`    | `int` | Year of manufacture                   |
| `mileage` | `int` | Initial odometer reading in km        |

**Properties**

| Name      | Access    | Description                                                                 |
|-----------|-----------|-----------------------------------------------------------------------------|
| `mileage` | get / set | Returns the current odometer value. Setter raises `ValueError` if the new value is less than the current reading. |

**Methods**

| Method                        | Returns | Description                                                      |
|-------------------------------|---------|------------------------------------------------------------------|
| `display_info()`              | `None`  | Prints class name, brand, model, year, and mileage to stdout.    |
| `calculate_maintenance_cost()`| `float` | **Abstract.** Must be implemented by every subclass.             |
| `__str__()`                   | `str`   | Returns `"brand model (year)"`.                                  |

---

### `RefuelableMixin`

Attach to any vehicle class via multiple inheritance. Requires the host class to expose a `model` attribute.

| Method     | Returns | Description                                                |
|------------|---------|------------------------------------------------------------|
| `refuel()` | `None`  | Prints a refuelling confirmation message using `self.model`. |

---

### `Car(Vehicle, RefuelableMixin)`

```python
Car(brand: str, model: str, year: int, mileage: int, doors_count: int)
```

| Parameter     | Type  | Description              |
|---------------|-------|--------------------------|
| `doors_count` | `int` | Number of doors          |

| Method                        | Formula          | Returns                            |
|-------------------------------|------------------|------------------------------------|
| `calculate_maintenance_cost()`| `mileage × 0.5`  | `float` — estimated cost in PLN    |

---

### `Motorcycle(Vehicle, RefuelableMixin)`

```python
Motorcycle(brand: str, model: str, year: int, mileage: int, has_sidecar: bool)
```

| Parameter     | Type   | Description                    |
|---------------|--------|--------------------------------|
| `has_sidecar` | `bool` | Whether a sidecar is attached  |

| Method                        | Formula          | Returns                            |
|-------------------------------|------------------|------------------------------------|
| `calculate_maintenance_cost()`| `mileage × 0.3`  | `float` — estimated cost in PLN    |

---

### `service_fleet(vehicles)`

```python
service_fleet(vehicles: list[Vehicle]) -> None
```

Iterates over a list of `Vehicle` instances. For each vehicle, calls `display_info()`, `refuel()`, and `calculate_maintenance_cost()`, then prints the result. Works with any concrete subclass of `Vehicle`.

| Parameter  | Type           | Description                                |
|------------|----------------|--------------------------------------------|
| `vehicles` | `list[Vehicle]`| Any list of concrete `Vehicle` subclasses  |

---

## Project Structure

```
Python-OOP-Core-Architecture/
├── fleet_management.py   # Core module: all classes, mixin, and service_fleet()
├── requirements.txt      # Dependency declaration (stdlib only — intentionally empty)
├── LICENSE               # MIT License
└── README.md             # This file
```

To extend the project with tests, add:

```
Python-OOP-Core-Architecture/
└── tests/
    ├── __init__.py
    └── test_fleet.py
```

---

## Testing

No automated test suite is included. The `if __name__ == "__main__":` block in `fleet_management.py` provides a runnable smoke test:

```bash
python fleet_management.py
```

To add a proper test suite, install `pytest` and place tests under `tests/`:

```bash
pip install pytest
pytest tests/ -v
```

Example unit tests:

```python
# tests/test_fleet.py
import pytest
from fleet_management import Car, Motorcycle, service_fleet

def test_car_maintenance_cost():
    car = Car("Toyota", "Corolla", 2020, 50000, 5)
    assert car.calculate_maintenance_cost() == 25000.0

def test_motorcycle_maintenance_cost():
    moto = Motorcycle("Honda", "CB500F", 2022, 12000, False)
    assert moto.calculate_maintenance_cost() == 3600.0

def test_mileage_rollback_raises():
    car = Car("Toyota", "Corolla", 2020, 50000, 5)
    with pytest.raises(ValueError, match="Mileage cannot be rolled back"):
        car.mileage = 40000

def test_mileage_valid_update():
    car = Car("Toyota", "Corolla", 2020, 50000, 5)
    car.mileage = 60000
    assert car.mileage == 60000

def test_service_fleet_runs(capsys):
    fleet = [Car("BMW", "320d", 2021, 10000, 4)]
    service_fleet(fleet)
    captured = capsys.readouterr()
    assert "FLEET SERVICE STARTED" in captured.out
    assert "Refueling vehicle 320d" in captured.out
```

---

## Contributing

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Commit your changes using [Conventional Commits](https://www.conventionalcommits.org/):

   ```bash
   git commit -m "feat: add ElectricCar subclass with battery capacity"
   ```

4. Push to your fork:

   ```bash
   git push origin feature/your-feature-name
   ```

5. Open a Pull Request against `main`.

**Guidelines:**
- New vehicle types must extend `Vehicle` and implement `calculate_maintenance_cost()`.
- Keep the module importable without side effects (all demo code under `if __name__ == "__main__":`).
- Add unit tests for every new class or function.

---

## Author

GitHub: [@eryks23](https://github.com/eryks23)              
Repository: [https://github.com/eryks23/Python-OOP-Core-Architecture](https://github.com/eryks23/Python-OOP-Core-Architecture)

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
