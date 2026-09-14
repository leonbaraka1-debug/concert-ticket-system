import json
import random
from models.event import get_event_by_id, update_event_seats

bookings = []
booking_count = 0


class Booking:
    def __init__(self, event, tickets, name="Guest"):
        global booking_count
        booking_count += 1
        self.booking_id = "B" + str(booking_count) + str(random.randint(100, 999))
        self.event = event
        self.tickets = tickets
        self.name = name
        self.status = "pending"
        self.total_price = 0
        bookings.append(self)

    def check_seats(self):
        return self.event.available_seats >= self.tickets

    def calculate_price(self):
        self.total_price = self.event.price * self.tickets
        return self.total_price

    def confirm_booking(self):
        if self.check_seats():
            ok, result = update_event_seats(self.event.event_id, -self.tickets)
            if not ok:
                self.status = "failed"
                print("Could not update seats:", result)
                return
            self.event = result  # refreshed event object with updated seat count
            self.calculate_price()
            self.status = "confirmed"
            print("Booking confirmed:", self.booking_id)
        else:
            self.status = "failed"
            print("Not enough seats for", self.event.name)

    def cancel_booking(self):
        if self.status == "confirmed":
            ok, result = update_event_seats(self.event.event_id, self.tickets)
            if not ok:
                print("Could not update seats:", result)
                return
            self.event = result  # refreshed event object with updated seat count
            self.status = "cancelled"
            print("Booking cancelled:", self.booking_id)
        else:
            print("Can't cancel this booking")

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "event": self.event.name,
            "name": self.name,
            "tickets": self.tickets,
            "total_price": self.total_price,
            "status": self.status
        }


def save_bookings(filename="booking.json"):
    data = []
    for b in bookings:
        data.append(b.to_dict())
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def load_bookings(filename="booking.json"):
    with open(filename, "r") as f:
        return json.load(f)


def create_booking(user_id, event_id, quantity, filename="booking.json"):
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