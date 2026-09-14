from models.booking import Booking


def test_confirm_booking():
    concert = {"name": "Sauti Sol Live", "price": 2500, "seats": 5}
    b = Booking(concert, 3, "Acey")
    b.confirm_booking()
    assert b.status == "confirmed"
    assert concert["seats"] == 2
    assert b.total_price == 7500


def test_not_enough_seats():
    concert = {"name": "Nyege Nyege", "price": 4000, "seats": 2}
    b = Booking(concert, 5, "John")
    b.confirm_booking()
    assert b.status == "failed"
    assert concert["seats"] == 2


def test_cancel_booking():
    concert = {"name": "Sauti Sol Live", "price": 2500, "seats": 5}
    b = Booking(concert, 3, "Acey")
    b.confirm_booking()
    b.cancel_booking()
    assert b.status == "cancelled"
    assert concert["seats"] == 5


test_confirm_booking()
test_not_enough_seats()
test_cancel_booking()
print("All booking tests passed")
 


