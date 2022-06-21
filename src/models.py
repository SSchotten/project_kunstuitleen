from typing import List, Union


class Artwork:
    def __init__(self, id: int, title: str, creator_ids: Union[int, List], building_id: int = 1, width_cm: int = None, height_cm: int = None,
                 depth_cm: int = None, year_of_creation: int = None, art_type: str = None, art_style: str = None, is_lent_out: bool = False,
                 category: int = None):
        self.id = id
        self.title = title
        self.creator_ids = creator_ids  # many-to-many
        self.building_id = building_id  # many-to-one  (many artworks per location)
        self.width_cm = width_cm
        self.height_cm = height_cm
        self.depth_cm = depth_cm
        self.year_of_creation = year_of_creation
        self.art_type = art_type
        self.art_style = art_style
        self.is_lent_out = is_lent_out  # not exactly a property of an artwork, but important for app
        self.category = category


class Artist:
    def __init__(self, id: int, first_name: str, last_name: str, url: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.url = url

    # def get_full_name(self):
    #     return f"{self.first_name} {self.last_name}"


class MunicipalBuilding:
    def __init__(self, id: int, name: str, address: str):
        self.id = id
        self.name = name  # e.g. "Depot" for id==1
        self.address = address


class DisplayRoomsPerBuilding:
    def __init__(self, id: int, building_id: int, room_in_building: str):
        self.id = id
        self.building_id = building_id  # many-to-one  (many rooms per location)
        self.room_in_building = room_in_building


class Loan:
    def __init__(self, id: int, artwork_id: int, reservation_id: int, borrower_id: int, building_id: int, room_id: int, start_dt: str, end_dt: str):
        self.id = id
        self.artwork_id = artwork_id
        self.building_id = building_id  # many-to-one  (many loans per location)
        self.room_id = room_id  # one-to-one (one loan per room)
        self.start_dt = start_dt
        self.end_dt = end_dt


class Reservation:
    def __init__(self, id: int, artwork_id: int, user_id: int, building_id: int, room_id: int, reservation_issuance_dt: str, start_dt: str, end_dt: str):
        self.id = id
        self.artwork_id = artwork_id
        self.user_id = user_id  # many-to-one (many reservations per user)
        self.building_id = building_id  # many-to-one  (many loans per location)
        self.room_id = room_id  # one-to-one (one loan per room)
        self.reservation_issuance_dt = reservation_issuance_dt
        self.start_dt = start_dt
        self.end_dt = end_dt


class AppUser:
    def __init__(self, id: int, first_name: str, last_name: str, locations: Union[str, List]):
        self.id = id
        pass
