from models.booking import Booking
from models.event import Event
from unittest.mock import patch


def test_confirm_booking():

    concert = Event(
        "E001",
        "Sauti Sol Live",
        "2026-09-13",
        "Hall A",
        5,
        2500
    )

    b = Booking(concert, 3, "Acey")

    with patch("models.booking.update_event_seats") as mock_update:
        updated_concert = Event(
            "E001",
            "Sauti Sol Live",
            "2026-09-13",
            "Hall A",
            2,
            2500
        )

        mock_update.return_value = (True, updated_concert)

        b.confirm_booking()

    assert b.status == "confirmed"
    assert b.event.available_seats == 2
    assert b.total_price == 7500


def test_not_enough_seats():

    concert = Event(
        "E002",
        "Nyege Nyege",
        "2026-09-13",
        "Hall B",
        2,
        4000
    )

    b = Booking(concert, 5, "John")

    b.confirm_booking()

    assert b.status == "failed"
    assert concert.available_seats == 2


def test_cancel_booking():

    concert = Event(
        "E003",
        "Sauti Sol Live",
        "2026-09-13",
        "Hall A",
        5,
        2500
    )

    b = Booking(concert, 3, "Acey")

    with patch("models.booking.update_event_seats") as mock_update:
        updated_concert = Event(
            "E003",
            "Sauti Sol Live",
            "2026-09-13",
            "Hall A",
            2,
            2500
        )

        mock_update.return_value = (True, updated_concert)

        b.confirm_booking()

        cancelled_concert = Event(
            "E003",
            "Sauti Sol Live",
            "2026-09-13",
            "Hall A",
            5,
            2500
        )

        mock_update.return_value = (True, cancelled_concert)

        b.cancel_booking()

    assert b.status == "cancelled"
    assert b.event.available_seats == 5


if __name__ == "__main__":
    test_confirm_booking()
    test_not_enough_seats()
    test_cancel_booking()
    print("All booking tests passed")
