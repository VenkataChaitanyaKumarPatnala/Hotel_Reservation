from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(15))

class Room(db.Model):
    __tablename__ = "room"
    room_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_number = db.Column(db.String(10), unique=True)
    room_type = db.Column(db.String(50))
    price = db.Column(db.Numeric(10,2))
    status = db.Column(db.String(20), default="Available")

class Booking(db.Model):
    __tablename__ = "booking"
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"))
    room_id = db.Column(db.Integer, db.ForeignKey("room.room_id"))
    check_in = db.Column(db.Date)
    check_out = db.Column(db.Date)
    total_amount = db.Column(db.Numeric(10,2))
    booking_status = db.Column(db.String(20), default="Confirmed")
    customer = db.relationship("Customer", backref="bookings")
    room = db.relationship("Room", backref="bookings")

class Payment(db.Model):
    __tablename__ = "payment"
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # ADD CASCADE HERE
    booking_id = db.Column(
        db.Integer,
        db.ForeignKey("booking.booking_id", ondelete="CASCADE")
    )
    
    amount = db.Column(db.Numeric(10,2))
    payment_date = db.Column(db.DateTime)
    payment_mode = db.Column(db.String(20))
    payment_status = db.Column(db.String(20))
