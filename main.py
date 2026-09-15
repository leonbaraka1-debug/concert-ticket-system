import json
import os
import getpass

from models.event import create_event, list_events, search_events
from models.ticket import create_ticket, cancel_ticket, get_tickets_by_user
from models.booking import create_booking
from models.user import register_user as create_user, login_user as authenticate_user
from utils.decorators import login_required, admin_required

EVENTS_FILE = "data/event.json"
TICKETS_FILE = "data/ticket.json"
BOOKINGS_FILE = "data/booking.json"


class EventTicketApp:
    def __init__(self):
        self.current_user = None

    def print_menu(self):
        print("=========================================")
        print("       EVENT TICKET SYSTEM")
        print("=========================================")

        if not self.current_user:
            print("1. Register")
            print("2. Login")
            print("3. Exit")
        else:
            print(f"(Logged in as {self.current_user.username} / {self.current_user.role})")
            print("1. View Events")
            print("2. Search Events")
            print("3. Book Ticket")
            print("4. My Tickets")
            print("5. Cancel Ticket")
            print("6. Add Event")
            print("7. Logout")
            print("8. Exit")

    def register_user(self):
        username = input("Choose a username: ").strip()
        password = getpass.getpass("Choose a password: ").strip()
        role = input("Role (User/Admin) [User]: ").strip() or "User"
        success, message = create_user(username, password, role)
        print(message)

    def login_user(self):
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()
        success, result = authenticate_user(username, password)
        if success:
            self.current_user = result
            print("Login successful. Welcome,", username)
        else:
            print(result)

    def view_events(self):
        events = list_events(EVENTS_FILE)
        if not events:
            print("No events found.")
            return

        for event in events:
            print(f"{event.event_id} | {event.name} | {event.date} | {event.venue} | seats={event.available_seats}")

    def search_events_cli(self):
        keyword = input("Search by event name, venue or date: ").strip()
        events = search_events(keyword, EVENTS_FILE)
        if not events:
            print("No matching events found.")
            return

        for event in events:
            print(f"{event.event_id} | {event.name} | {event.date} | {event.venue} | seats={event.available_seats}")

    @login_required
    def book_ticket(self):
        event_id = input("Event ID: ").strip()
        user_id = self.current_user.username

        try:
            quantity = int(input("Number of tickets: ").strip())
        except ValueError:
            print("Number of tickets must be a whole number.")
            return

        ok, booking = create_booking(user_id, event_id, quantity, BOOKINGS_FILE)
        if ok:
            ok_ticket, ticket = create_ticket(user_id, event_id, TICKETS_FILE)
            if ok_ticket:
                print(f"Booked. Booking: {booking.booking_id}. Ticket: {ticket.ticket_id}")
            else:
                print(ticket)
        else:
            print(booking)

    @login_required
    def my_tickets(self):
        user_id = self.current_user.username
        tickets = get_tickets_by_user(user_id, TICKETS_FILE)
        if not tickets:
            print("No tickets found for that user.")
            return

        for ticket in tickets:
            print(f"{ticket.ticket_id} | {ticket.event_id} | {ticket.status}")

    @login_required
    def cancel_ticket_cli(self):
        ticket_id = input("Ticket ID: ").strip()
        ok, result = cancel_ticket(ticket_id, TICKETS_FILE)
        if ok:
            print(f"Ticket {ticket_id} cancelled.")
        else:
            print(result)

    @admin_required
    def add_event_cli(self):
        name = input("Event name: ").strip()
        date = input("Event date: ").strip()
        venue = input("Venue: ").strip()
        seats = input("Available seats: ").strip()
        price = input("Price per ticket: ").strip()

        ok, result = create_event(name, date, venue, seats, price=price, filepath=EVENTS_FILE)
        if ok:
            print(f"Event created: {result.event_id}")
        else:
            print(result)

    def run(self):
        while True:
            self.print_menu()
            choice = input("Pick your hangover spot: ").strip()

            if not self.current_user:
                if choice == "1":
                    self.register_user()
                elif choice == "2":
                    self.login_user()
                elif choice == "3":
                    print("(Touch more grass next time you lazy couch grape)!")
                    break
                else:
                    print("Choose a valid number from the menu.")
            else:
                if choice == "1":
                    self.view_events()
                elif choice == "2":
                    self.search_events_cli()
                elif choice == "3":
                    self.book_ticket()
                elif choice == "4":
                    self.my_tickets()
                elif choice == "5":
                    self.cancel_ticket_cli()
                elif choice == "6":
                    self.add_event_cli()
                elif choice == "7":
                    self.current_user = None
                    print("Logged out.")
                elif choice == "8":
                    print("(Touch more grass next time you lazy couch grape)!")
                    break
                else:
                    print("Choose a valid number from the menu.")

if __name__ == "__main__":
    app = EventTicketApp()
    app.run()