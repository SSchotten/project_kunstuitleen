from src.models import Artwork, Loan, Reservation
from datetime import datetime

from src.common import (
    get_all_days_between_dates,
)


class ArtBrowserHandler:
    """
    Interface between user/view and data/models for gathering information about artworks and artists.
    """
    def __init__(self):
        self.artwork_information_checker = ArtworkInformationChecker()

    def style_filter(self):
        pass

    def dimension_filter(self):
        pass


class ReservationHandler:
    """
    Interface between user/view and data/models for making reservations.
    """
    def __init__(self):
        self.availability_checker = AvailabilityChecker()

    def is_available_during_time_interval(self, artwork_obj, loan_obj, reservation_obj, start_dtt=None, end_dtt=None) -> bool:
        time_interval = get_all_days_between_dates(start_date=start_dtt, end_date=end_dtt)
        return all(self.availability_checker.is_artwork_available_on_date(artwork_obj=artwork_obj,
                                                                          loan_obj=loan_obj,
                                                                          reservation_obj=reservation_obj,
                                                                          dt_of_interest=dtt) for dtt in time_interval)

    def create_reservation(self):
        is_available = self.is_available_during_time_interval(artwork_obj, loan_obj, reservation_obj, start_dtt=None, end_dtt=None)
        is_allowed_at_location = self.availability_checker.is_artwork_available_at_location(artwork_obj, location_of_interest)

        if is_available & is_allowed_at_location:
            pass  # if not reserved AND location is allowed, INSERT reservation if user wants to.

    def undo_reservation(self):
        pass  # user should be able to UPDATE/DELETE a previously made reservation

    def is_suitable_location_available_at_dtt_and_building(self):
        pass  # the selected artwork should be both available AND should fit at that location

    def close_reservation(self):
        pass  # a reservation should be UPDATED once the loan starts. This will reduce the number of reservations by 1

    def send_reminder(self):  # TODO: move to separate UserInteractor class
        pass  # a reminder should be sent to the user making the reservation x days before the reservation/loan starts


class LoanHandler:
    def __init__(self):
        pass

    def create_loan(self):
        pass  # INSERT of loan (including start_dtt+end_dtt) should follow directly after a reservation has been closed

    def close_loan(self):
        pass  # UPDATE loan transaction once artwork has been returned AND current_dtt >= end_dtt

    def artwork_has_been_returned(self):
        pass  # check that the user indeed returned the relevant artwork on (or before) the relevant end_dtt

    def send_reminder(self):  # TODO: move to separate UserInteractor class
        pass  # a reminder should be sent to the user making the reservation x days before the loan ends


class ArtworkInformationChecker:
    """
    Interface with Artwork and Artist classes.

    does_artwork_fit and is_artwork_desired_style methods could be used as filters on a user's preferences.
    """
    def __init__(self):
        pass

    @staticmethod
    def _get_dimensions(artwork_obj: Artwork):
        return artwork_obj.width_cm, artwork_obj.height_cm, artwork_obj.depth_cm

    @staticmethod
    def _is_painting(artwork_obj: Artwork):
        return artwork_obj.art_type == "painting"

    def does_artwork_fit(self, artwork_obj: Artwork, location_width_cm: int, location_height_cm: int, location_depth_cm: int = None):
        artwork_dimensions = self._get_dimensions(artwork_obj=artwork_obj)
        location_dimensions = (location_width_cm, location_height_cm, location_depth_cm)

        if self._is_painting(artwork_obj=artwork_obj):  # TODO: maybe just use 'not is location_depth' instead?
            location_dimensions = (location_width_cm, location_height_cm)

        return all(art_dim <= loc_dim for art_dim, loc_dim in zip(artwork_dimensions, location_dimensions))

    @staticmethod
    def is_artwork_desired_style(artwork_obj: Artwork, preferred_style: str):
        return artwork_obj.art_style == preferred_style


class AvailabilityChecker:
    """
    Interface with Loan and Reservation classes

    is_artwork_available and is_artwork_available_at_location could be used as filters on a user's preferences.
    """
    def __init__(self):
        pass

    @staticmethod
    def _get_current_location(artwork_obj: Artwork):
        return artwork_obj.building_id

    @staticmethod
    def _get_current_availability(artwork_obj: Artwork):
        return artwork_obj.is_lent_out

    @staticmethod
    def _get_category(artwork_obj: Artwork):
        return artwork_obj.category

    def is_artwork_available_on_date(self, artwork_obj: Artwork, loan_obj: Loan, reservation_obj: Reservation, dt_of_interest: str):
        if datetime.strptime(dt_of_interest) == datetime.today():
            return self._get_current_availability(artwork_obj=artwork_obj)
        else:
            return (dt_of_interest >= loan_obj.start_dt) & (dt_of_interest <= loan_obj.end_dt)
        # TODO: use reservation_obj to warn for future reservations?

    def is_artwork_available_at_location(self, artwork_obj: Artwork, location_of_interest: int):
        if self._get_category(artwork_obj=artwork_obj) == 1:
            return self._get_current_location(artwork_obj=artwork_obj) == location_of_interest
        return True


##############
some_book = Artwork(id=42, title="Zaphod Beeblebrox", creator_ids="Douglas Adams", width_cm=70, height_cm=100, depth_cm=5)
some_painting = Artwork(id=1, title="Nachtwacht", creator_ids="Rembrandt", art_type="painting", width_cm=600, height_cm=200)
artwork_info_checker = ArtworkInformationChecker()

print(artwork_info_checker.does_artwork_fit(some_book, location_width_cm=80, location_height_cm=200, location_depth_cm=10))
print(artwork_info_checker.does_artwork_fit(some_painting, location_width_cm=80, location_height_cm=200, location_depth_cm=10))


some_sculpture = Artwork(id=2, title="Le Penseur", creator_ids="Rodin", art_type="sculpture", width_cm=75, height_cm=185, depth_cm=100,
                         category=1, building_id="Stadhuis")
artwork_availability_checker = AvailabilityChecker()
print(artwork_availability_checker.is_artwork_available_at_location(artwork_obj=some_sculpture, location_of_interest="home"))
print(artwork_availability_checker.is_artwork_available_at_location(artwork_obj=some_sculpture, location_of_interest="Stadhuis"))
