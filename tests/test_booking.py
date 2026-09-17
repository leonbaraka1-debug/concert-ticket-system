from unittest.mock import patch

from models.booking import Booking
from models.event import Event
from models.ticket import Ticket


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

    with patch("models.booking.update_event_seats") as mock_update, \
         patch("models.booking.create_ticket") as mock_create_ticket:

        updated_concert = Event(
            "E001",
            "Sauti Sol Live",
            "2026-09-13",
            "Hall A",
            2,
            2500
        )

        mock_update.return_value = (True, updated_concert)
        # create_ticket is called once per unit of quantity — return a
        # fresh fake Ticket each time so ticket_ids ends up with 3 entries
        mock_create_ticket.side_effect = [
            (True, Ticket("T001", "Acey", "E001")),
            (True, Ticket("T002", "Acey", "E001")),
            (True, Ticket("T003", "Acey", "E001")),
        ]

        b.confirm_booking()

    assert b.status == "confirmed"
    assert b.event.available_seats == 2
    assert b.total_price == 7500
    # bug-1 regression check: 3 tickets requested -> 3 tickets actually created
    assert mock_create_ticket.call_count == 3
    assert b.ticket_ids == ["T001", "T002", "T003"]


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
    assert b.ticket_ids == []


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

    with patch("models.booking.update_event_seats") as mock_update, \
         patch("models.booking.create_ticket") as mock_create_ticket, \
         patch("models.booking.cancel_ticket") as mock_cancel_ticket:

        updated_concert = Event(
            "E003",
            "Sauti Sol Live",
            "2026-09-13",
            "Hall A",
            2,
            2500
        )
        mock_update.return_value = (True, updated_concert)
        mock_create_ticket.side_effect = [
            (True, Ticket("T010", "Acey", "E003")),
            (True, Ticket("T011", "Acey", "E003")),
            (True, Ticket("T012", "Acey", "E003")),
        ]

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
    # bug-2 regression check: cancelling a booking cancels its underlying tickets
    assert mock_cancel_ticket.call_count == 3
    mock_cancel_ticket.assert_any_call("T010", "Acey")


def test_zero_or_negative_quantity_rejected():
    """
    Regression test for bug 5: create_booking() must reject a quantity
    of zero or less before ever touching seats or tickets.
    """
    from models.booking import create_booking

    with patch("models.booking.get_event_by_id") as mock_get_event, \
         patch("models.booking.update_event_seats") as mock_update, \
         patch("models.booking.create_ticket") as mock_create_ticket:

        ok, result = create_booking("Acey", "E001", 0)
        assert ok is False

        ok, result = create_booking("Acey", "E001", -3)
        assert ok is False

        # neither invalid call should have touched the event or created tickets
        mock_get_event.assert_not_called()
        mock_update.assert_not_called()
        mock_create_ticket.assert_not_called()


if __name__ == "__main__":
    test_confirm_booking()
    test_not_enough_seats()
    test_cancel_booking()
    test_zero_or_negative_quantity_rejected()
    print("All booking tests passed")