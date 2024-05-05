# Vehicle manager #

Vehicle manager is a repository that implements a Python package containing the VehicleManager class as per the task.

Required Python version:
* python3.6+

Installation of dependencies:

`pip install -r requirements.txt`

Example of usage:
```python
from vehicle_manager import Vehicle, VehicleManager

# Creating an instance of the VehicleManager class
manager = VehicleManager(url="https://test.tspb.su/test-task")

# Retrieving a list of all vehicles
vehicles = manager.get_vehicles()

# Retrieving a list of vehicles where the 'name' field is equal to 'Toyota'
toyotas = manager.filter_vehicles(params={"name": "Toyota"})

# Retrieving a vehicle with id=1
vehicle_1 = manager.get_vehicle(vehicle_id=1)

# Adding a new vehicle to the database
new_vehicle = Vehicle(
    name='Toyota',
    model='Camry',
    year=2021,
    color='red',
    price=21000,
    latitude=55.753215,
    longitude=37.620393
)
manager.add_vehicle(vehicle=new_vehicle)

# Updating vehicle information with id=1
updated_vehicle = Vehicle(
    id=1,
    name='Toyota',
    model='Camry',
    year=2021,
    color='red',
    price=21000,
    latitude=55.753215,
    longitude=37.620393
)
manager.update_vehicle(vehicle=updated_vehicle)

# Deleting a vehicle with id=1
manager.delete_vehicle(id=1)

# Calculating the distance between vehicles with id=1 and id=2
distance = manager.get_distance(id1=1, id2=2)

# Finding the nearest vehicle to the vehicle with id=1
nearest_vehicle = manager.get_nearest_vehicle(id=1)

```