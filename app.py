from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Customer, Room, Booking, Payment
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "secret-key"
db.init_app(app)
with app.app_context():
    pass

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rooms")
def rooms():
    rooms = Room.query.order_by(Room.room_number).all()
    return render_template("rooms.html", rooms=rooms)

@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "GET":
        rooms = Room.query.filter(Room.status != "Maintenance").all()
        return render_template("book.html", rooms=rooms)
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    room_id = request.form.get("room_id")
    check_in = request.form.get("check_in")
    check_out = request.form.get("check_out")
    try:
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
    except Exception:
        flash("Invalid date format", "danger")
        return redirect(url_for("book"))
    if check_out_date <= check_in_date:
        flash("Check-out must be after check-in", "danger")
        return redirect(url_for("book"))
    customer = Customer.query.filter_by(email=email).first()
    if not customer:
        customer = Customer(name=name, email=email, phone=phone)
        db.session.add(customer)
        db.session.flush()
    room = Room.query.get(room_id)
    total_nights = (check_out_date - check_in_date).days
    total_amount = float(room.price) * total_nights
    booking = Booking(customer_id=customer.customer_id, room_id=room.room_id, check_in=check_in_date, check_out=check_out_date, total_amount=total_amount)
    db.session.add(booking)
    try:
        db.session.commit()
        flash("Booking created successfully. Booking ID: {}".format(booking.booking_id), "success")
        return redirect(url_for("bookings"))
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(str(e.__dict__.get("orig")) , "danger")
        return redirect(url_for("book"))

@app.route("/bookings")
def bookings():
    bookings = Booking.query.order_by(Booking.check_in.desc()).all()
    return render_template("bookings.html", bookings=bookings)

@app.route("/payment/<int:booking_id>", methods=["GET", "POST"])
def payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if request.method == "GET":
        return render_template("payment.html", booking=booking)
    amount = request.form.get("amount")
    mode = request.form.get("mode")
    payment = Payment(booking_id=booking.booking_id, amount=amount, payment_date=datetime.now(), payment_mode=mode, payment_status="Completed")
    db.session.add(payment)
    db.session.commit()
    flash("Payment recorded", "success")
    return redirect(url_for("bookings"))
@app.route('/hybridaction/zybTrackerStatisticsAction')
def zyb_tracker():
    return jsonify({"status": "ok"}) 



if __name__ == "__main__":
    app.run(debug=True)
