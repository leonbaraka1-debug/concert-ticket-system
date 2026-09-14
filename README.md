# 🎟️ Concert Ticket System

A Python-based command-line application for managing concert events, users, bookings, and tickets.

The system allows users to register and log in, view and search for events, book tickets, view their tickets, and cancel tickets. Administrators can also create new events.

---

## 📁 Project Structure

```text
concert-ticket-system/
│
├── data/
│   ├── booking.json
│   ├── event.json
│   ├── ticket.json
│   └── users.json
│
├── models/
│   ├── booking.py
│   ├── event.py
│   ├── ticket.py
│   └── user.py
│
├── tests/
│   ├── test_booking.py
│   ├── test_decorators.py
│   ├── test_event.py
│   ├── test_ticket.py
│   └── test_user.py
│
├── utils/
│   ├── decorators.py
│   └── validators.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## 🚀 How the System Works

The application starts from `main.py`.

When the program runs, the user is presented with the following menu:

```text
================================
      EVENT TICKET SYSTEM
================================
1. Register
2. Login
3. View Events
4. Search Events
5. Book Ticket
6. My Tickets
7. Cancel Ticket
8. Exit
9. Add Event
```

The user selects an option, and the program calls the appropriate function from the model files.

---

# 📄 File Descriptions

## `main.py`

This is the main entry point of the application.

It controls the command-line interface and connects the different parts of the system.

### What it does

- Displays the main menu
- Registers users
- Logs users in
- Displays events
- Searches for events
- Books tickets
- Displays a user's tickets
- Cancels tickets
- Allows administrators to create events
- Controls which features require login or administrator access

`main.py` imports functionality from:

- `models/event.py`
- `models/ticket.py`
- `models/booking.py`
- `models/user.py`
- `utils/decorators.py`

---

## 👤 `models/user.py`

This file manages users and authentication.

### Main responsibilities

- Create users
- Hash passwords
- Save users to JSON
- Load users from JSON
- Register new users
- Authenticate users during login

### `register_user()`

Creates a new user and saves the user's information to:

```text
data/users.json
```

### `login_user()`

Checks the username and password and returns the logged-in user if the credentials are correct.

### `load_users()`

Reads users from the JSON file.

### `save_users()`

Writes user information to the JSON file.

### Password Security

Passwords are not stored as plain text.

The system uses SHA-256 hashing:

```text
Password
   ↓
SHA-256
   ↓
Password Hash
   ↓
users.json
```

---

## 🎤 `models/event.py`

This file manages concert and event information.

An event contains:

- Event ID
- Event name
- Date
- Venue
- Available seats
- Ticket price

### `create_event()`

Creates a new event and saves it to:

```text
data/event.json
```

### `list_events()`

Loads and returns all available events.

### `search_events()`

Allows users to search for events using:

- Event name
- Venue
- Date

### `get_event_by_id()`

Finds a specific event using its event ID.

### `update_event_seats()`

Updates the number of available seats after tickets are booked or cancelled.

---

## 🎟️ `models/ticket.py`

This file manages individual tickets.

It is responsible for:

- Creating tickets
- Loading tickets
- Finding tickets belonging to a user
- Cancelling tickets
- Saving ticket information

Ticket information is stored in:

```text
data/ticket.json
```

When a user successfully books a ticket, a ticket is created and associated with the user's username and event.

---

## 📑 `models/booking.py`

This file handles the booking process.

A booking connects:

```text
User
  ↓
Event
  ↓
Number of Tickets
  ↓
Total Price
```

### Main responsibilities

- Check if enough seats are available
- Confirm bookings
- Calculate the total price
- Update available event seats
- Cancel confirmed bookings
- Save booking information

Bookings are stored in:

```text
data/booking.json
```

### Example

If an event has:

```text
Price = 1000
Tickets = 2
```

The system calculates:

```text
1000 × 2 = 2000
```

The event's available seats are also reduced by the number of tickets booked.

---

## 🛡️ `utils/decorators.py`

This file contains decorators used to control access to certain features.

### `login_required`

Some actions can only be performed by logged-in users.

For example:

- Book Ticket
- My Tickets
- Cancel Ticket

If a user is not logged in, the system displays:

```text
Please login first.
```

### `admin_required`

Some actions require administrator privileges.

For example:

- Add Event

If the user is not logged in:

```text
Please login first.
```

If the user is logged in but is not an administrator:

```text
Admin access required.
```

---

## 🔍 `utils/validators.py`

This file contains validation functions used to check user input.

For example, it can check whether required values are empty.

The validation functions are used by other parts of the application before data is saved.

---

# 💾 Data Files

The application uses JSON files for data storage instead of a database.

## `data/users.json`

Stores registered users.

Example:

```json
{
    "Leo": {
        "username": "Leo",
        "password_hash": "...",
        "role": "Admin"
    }
}
```

## `data/event.json`

Stores concert and event information.

Example:

```json
[
    {
        "event_id": "E001",
        "name": "Most Wanted",
        "date": "9/10/2026",
        "venue": "Uhuru Gardens",
        "available_seats": 200,
        "price": 1000
    }
]
```

## `data/booking.json`

Stores booking information.

A booking contains:

- Booking ID
- Event
- User
- Number of tickets
- Total price
- Booking status

## `data/ticket.json`

Stores individual ticket information.

Tickets contain:

- Ticket ID
- User
- Event
- Ticket status

---

# 🧪 Testing

The project uses **pytest** to test the different parts of the system.

Tests are located in:

```text
tests/
```

The test files include:

- `test_booking.py`
- `test_decorators.py`
- `test_event.py`
- `test_ticket.py`
- `test_user.py`

### Run all tests

```bash
python3 -m pytest -v
```

### Run an individual test file

For example:

```bash
python3 -m pytest tests/test_user.py -v
```

Or:

```bash
python3 -m pytest tests/test_decorators.py -v
```

The decorator tests verify that:

- Logged-in users can access protected features
- Logged-out users are blocked
- Administrators can access administrator features
- Normal users cannot access administrator features

---

## ⚠️ Test Data Safety

The user tests use temporary files so that running the tests does not delete or modify the real:

```text
data/users.json
```

This keeps the application's actual user data safe during testing.

---

# ▶️ Running the Application

First, make sure you are inside the project directory:

```bash
cd ~/concert-ticket-system
```

Then run:

```bash
python3 main.py
```

The main menu will appear.

---

# 🔐 User Roles

The system has two main roles.

## User

Regular users can:

- Register
- Login
- View events
- Search events
- Book tickets
- View their tickets
- Cancel tickets

## Admin

Administrators can perform the regular user functions and can also:

- Add new events

The administrator role is checked by the `admin_required` decorator.

---

# 🔄 Booking Process

When a user books tickets, the process is:

```text
User logs in
      ↓
Selects "Book Ticket"
      ↓
Enters Event ID
      ↓
Enters number of tickets
      ↓
System checks the event
      ↓
System checks available seats
      ↓
Booking is confirmed
      ↓
Available seats are reduced
      ↓
Ticket is created
      ↓
Booking and ticket are saved
```

---

# ❌ Ticket Cancellation

When a logged-in user cancels a ticket:

```text
User selects "Cancel Ticket"
        ↓
Enters Ticket ID
        ↓
System finds the ticket
        ↓
Ticket status is changed
        ↓
Ticket is cancelled
```

For confirmed bookings, the booking system can also return the seats to the event.

---

# 🛠️ Technologies Used

- Python
- JSON
- Pytest
- Object-Oriented Programming
- Decorators
- File Handling
- SHA-256 Password Hashing

---

# 🎯 Project Goal

The goal of this project is to demonstrate how a Python application can manage a complete concert ticketing process using:

- Classes and objects
- Functions
- JSON file storage
- Authentication
- User roles
- Decorators
- Input validation
- Automated testing
- CRUD-style operations

The application provides a simple command-line interface while keeping the code organized into separate models, utilities, data files, and tests.

# Authors

### Leon Baraka
### Erick Waweru
### Lerionka Olentiki
### Wanjiru Muthike