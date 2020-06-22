"""
Write following classes:

CarBase, which has following attributes: car_type, photo_file_name (".jpg",
".jpeg", ".png", ".gif"), brand, carrying. It also should have method
get_photo_file_ext which would get an extension of the file submitted as photo.

Truck should have attributes body_length, body_width, body_height. They should
be parsed from string body_whl (parameters are separated by x). They should be
rational numbers. If not valid string is submitted, all 3 parameters should be
set to 0. Truck should have method get_body_volume.

In class Car should be an attribute passenger_seats_count
In class SpecMachine should be an attribute extra
"""
import os
import csv


class CarBase:
    def __init__(self, car_type, brand, photo_file_name, carrying):
        self.car_type = car_type
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        # acceptable extensions
        ok_file_ext = [".jpg", ".jpeg", ".png", ".gif"]
        # split the path and get extension
        result = os.path.splitext(self.photo_file_name)[1]
        if result not in ok_file_ext:
            result = None
        return result


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__('Car', brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__('Truck', brand, photo_file_name, carrying)
        body_whl_split = str(body_whl).split('x', 3)
        for i, body_param in enumerate(body_whl_split):
            try:
                body_param = float(body_param)
                if i == 0:
                    self.body_length = body_param
                if i == 1:
                    self.body_width = body_param
                if i == 2:
                    self.body_height = body_param
            except ValueError:
                self.body_length = 0
                self.body_width = 0
                self.body_height = 0
                break

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__('SpecMachine', brand, photo_file_name, carrying)
        self.extra = str(extra)


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # skip header
        for row in reader:
            if row:
                if row[0] == 'car':
                    toAdd = Car(brand=row[1], passenger_seats_count=row[2],
                                photo_file_name=row[3], carrying=row[5])
                if row[0] == 'truck':
                    toAdd = Truck(brand=row[1], photo_file_name=row[3],
                                  body_whl=row[4], carrying=row[5])
                if row[0] == 'spec_machine':
                    # brand, photo_file_name, carrying, extra
                    toAdd = SpecMachine(brand=row[1], photo_file_name=row[3],
                                        carrying=row[5], extra=row[6])
                car_list.append(toAdd)
    return car_list


if __name__ == "__main__":
    pass
