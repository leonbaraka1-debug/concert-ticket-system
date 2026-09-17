import json
import os
import random

from models.event import get_event_by_id, update_event_seats
from models.ticket import create_ticket, cancel_ticket

BOOKINGS_FILE = "booking.json"

bookings = []
booking_count = 0


class Booking:
    def __init__(self, event, tickets, name="Guest", booking_id=None, status="pending",
                 total_price=0, ticket_ids=None):
        global booking_count

        if booking_id is None:
            booking_count += 1
            booking_id = "B" + str(booking_count) + str(random.randint(100, 999))

        self.booking_id = booking_id
        self.event = event
        self.tickets = tickets
        self.name = name
        self.status = status
        self.total_price = total_price
        self.ticket_ids = ticket_ids or []

        bookings.append(self)

    def check_seats(self):
        return self.event.available_seats >= self.tickets

    def calculate_price(self):
        self.total_price = self.event.price * self.tickets
        return self.total_price

    def confirm_booking(self):
        if not self.check_seats():
            self.status = "failed"
            print("Not enough seats for", self.event.name)
            return

        ok, result = update_event_seats(self.event.event_id, -self.tickets)
        if not ok:
            self.status = "failed"
            print("Could not update seats:", result)
            return

        self.event = result  # refreshed event object with updated seat count

        # create one Ticket record per ticket in this booking
        self.ticket_ids = []
        for _ in range(self.tickets):
            ok, ticket = create_ticket(self.name, self.event.event_id)
            if not ok:
                # roll back: restore the seats we just took and abort
                update_event_seats(self.event.event_id, self.tickets)
                self.status = "failed"
                print("Could not create ticket:", ticket)
                return
            self.ticket_ids.append(ticket.ticket_id)

        self.calculate_price()
        self.status = "confirmed"
        print("Booking confirmed:", self.booking_id)

    def cancel_booking(self):
        if self.status != "confirmed":
            print("Can't cancel this booking")
            return

        ok, result = update_event_seats(self.event.event_id, self.tickets)
        if not ok:
            print("Could not update seats:", result)
            return

        self.event = result  # refreshed event object with updated seat count

        # cancel each underlying ticket too, so ticket.json stays consistent
        for ticket_id in self.ticket_ids:
            cancel_ticket(ticket_id, self.name)

        self.status = "cancelled"
        print("Booking cancelled:", self.booking_id)

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "event_id": self.event.event_id,
            "event": self.event.name,
            "name": self.name,
            "tickets": self.tickets,
            "total_price": self.total_price,
            "status": self.status,
            "ticket_ids": self.ticket_ids
        }

    @staticmethod
    def from_dict(data):
        event = get_event_by_id(data["event_id"])
        return Booking(
            event=event,
            tickets=data["tickets"],
            name=data.get("name", "Guest"),
            booking_id=data["booking_id"],
            status=data.get("status", "pending"),
            total_price=data.get("total_price", 0),
            ticket_ids=data.get("ticket_ids", [])
        )


def save_bookings(filename=BOOKINGS_FILE):
    data = [b.to_dict() for b in bookings]
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def load_bookings(filename=BOOKINGS_FILE):
    """
    Rebuilds Booking objects from disk into the global `bookings` list.
    Call this once at CLI startup so in-memory state matches what's on disk.
    """
    global bookings, booking_count

    bookings = []

    if not os.path.exists(filename):
        return bookings

    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return bookings

    if not isinstance(data, list):
        return bookings

    max_num = 0
    for item in data:
        event = get_event_by_id(item.get("event_id"))
        if event is None:
            # the event this booking referenced no longer exists — skip it
            # rather than crash the whole reload
            continue
        Booking.from_dict(item)  # appends itself to `bookings` via __init__

        # keep booking_count ahead of any id already on disk, so new ids
        # generated this session can't collide with old ones
        digits = "".join(ch for ch in item.get("booking_id", "") if ch.isdigit())
        if digits:
            max_num = max(max_num, int(digits[0]) if len(digits) else 0)

    booking_count = max(booking_count, max_num)
    return bookings


def create_booking(user_id, event_id, quantity, filename=BOOKINGS_FILE):
    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        print("Ticket quantity must be a whole number")
        return False, None

    if quantity <= 0:
        print("Ticket quantity must be greater than zero")
        return False, None

    event = get_event_by_id(event_id)
    if not event:
        print("Event not found:", event_id)
        return False, None

    booking = Booking(event=event, tickets=quantity, name=user_id)
    booking.confirm_booking()

    if booking.status != "confirmed":
        return False, booking

    save_bookings(filename)
    return True, booking