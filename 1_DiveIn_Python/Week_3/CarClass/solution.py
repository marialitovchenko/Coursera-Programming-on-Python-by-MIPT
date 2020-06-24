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
    car_type = ''

    def __init__(self, brand, photo_file_name, carrying):
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

    def __repr__(self):
        return "<class 'solution.%s'>" % self.car_type.capitalize()


class Car(CarBase):
    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.body_length = float(0)
        self.body_width = float(0)
        self.body_height = float(0)

        body_whl_split = str(body_whl).split('x')
        if len(body_whl_split) == 3:
            for i, body_param in enumerate(body_whl_split):
                try:
                    body_param = float(body_param)
                except ValueError:
                    body_param = float(0)
                    break

                if i == 0:
                    self.body_length = body_param
                if i == 1:
                    self.body_width = body_param
                if i == 2:
                    self.body_height = body_param

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = str(extra)


def check_validity(one_row):
    """ Check validity of the string in the file with cars description"""
    if len(one_row) > 4:
        # first element shouldn't be empty, it's car type
        car_type_ok = one_row[0] in ['car', 'truck', 'spec_machine']
        # brand shouldn't be empty either
        brand_ok = (one_row[1] != '')
        # passenger seats count should be either empty or int
        passenger_seats_count = False
        if one_row[2] == '':
            passenger_seats_count = True
        else:
            try:
                passenger_seats_count = int(one_row[2])
            except ValueError:
                pass
        # photo_file_name shouldn't be empty
        photo_ok = (one_row[3] != '')
        # down't check body_whl, will do it inside the object
        # carrying should be float
        carrying_ok = False
        try:
            carrying_ok = float(one_row[5])
            carrying_ok = True
        except ValueError:
            pass
        all_ok = car_type_ok and brand_ok and passenger_seats_count and photo_ok
        all_ok = all_ok and carrying_ok
    else:
        all_ok = False

    if all_ok:
        all_ok = False

        if one_row[0] == 'car':
            # passenger seats counts should be int
            try:
                passenger_seats_count = int(one_row[2])
                all_ok = True
            except ValueError:
                all_ok = False

            all_ok = all_ok and one_row[6] == ''

        if one_row[0] == 'truck':
            # passenger seats counts should be empty
            all_ok = (one_row[2] == '')
            # extra should be empty
            all_ok = all_ok and one_row[6] == ''

        if one_row[0] == 'spec_machine':
            # passenger seats counts should be empty
            all_ok = (one_row[6] != '')

    return all_ok


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # skip header
        for row in reader:
            if check_validity(row):
                if row[0] == 'car':
                    try:
                        pass_seat_count = int(row[2])
                        to_add = Car(brand=row[1], passenger_seats_count=row[2],
                                     photo_file_name=row[3], carrying=row[5])
                        if to_add.get_photo_file_ext():
                            car_list.append(to_add)
                    except ValueError:
                        pass
                if row[0] == 'truck':
                    to_add = Truck(brand=row[1], photo_file_name=row[3],
                                   body_whl=row[4], carrying=row[5])
                    if to_add.get_photo_file_ext():
                        car_list.append(to_add)
                if row[0] == 'spec_machine':
                    # brand, photo_file_name, carrying, extra
                    to_add = SpecMachine(brand=row[1], photo_file_name=row[3],
                                         carrying=row[5], extra=row[6])
                    if to_add.get_photo_file_ext():
                        car_list.append(to_add)
    return car_list


if __name__ == "__main__":
    pass
