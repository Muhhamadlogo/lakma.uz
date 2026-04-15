from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from .extensions import db
from .models import Car, Order, User

main_bp = Blueprint("main", __name__)


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return User.query.get(uid)


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not current_user():
            flash("Сначала войдите в систему")
            return redirect(url_for("main.login"))
        return view(*args, **kwargs)

    return wrapper


def admin_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user or not user.is_admin:
            flash("Только администратор имеет доступ к этой странице")
            return redirect(url_for("main.index"))
        return view(*args, **kwargs)

    return wrapper


@main_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    brand = request.args.get("brand", "").strip()
    max_price = request.args.get("max_price", "").strip()

    cars = Car.query.filter_by(is_available=True)
    if q:
        cars = cars.filter((Car.brand.ilike(f"%{q}%")) | (Car.model.ilike(f"%{q}%")))
    if brand:
        cars = cars.filter(Car.brand.ilike(f"%{brand}%"))
    if max_price.isdigit():
        cars = cars.filter(Car.price <= int(max_price))

    cars = cars.order_by(Car.created_at.desc()).all()
    brands = sorted({c.brand for c in Car.query.all()})
    return render_template("index.html", cars=cars, brands=brands, user=current_user())


@main_bp.route("/car/<int:car_id>")
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template("car_detail.html", car=car, user=current_user())


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not full_name or not email or len(password) < 6:
            flash("Проверьте введенные данные. Пароль минимум 6 символов.")
            return redirect(url_for("main.register"))

        if User.query.filter_by(email=email).first():
            flash("Пользователь с таким email уже существует")
            return redirect(url_for("main.register"))

        user = User(full_name=full_name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Регистрация завершена. Войдите в систему.")
        return redirect(url_for("main.login"))

    return render_template("register.html", user=current_user())


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Неверный логин или пароль")
            return redirect(url_for("main.login"))

        session["user_id"] = user.id
        flash(f"Добро пожаловать, {user.full_name}!")
        return redirect(url_for("main.index"))

    return render_template("login.html", user=current_user())


@main_bp.route("/logout")
def logout():
    session.clear()
    flash("Вы вышли из системы")
    return redirect(url_for("main.index"))


@main_bp.route("/order/<int:car_id>", methods=["POST"])
@login_required
def order_car(car_id):
    car = Car.query.get_or_404(car_id)
    phone = request.form.get("phone", "").strip()
    comment = request.form.get("comment", "").strip()

    if len(phone) < 7:
        flash("Укажите корректный номер телефона")
        return redirect(url_for("main.car_detail", car_id=car_id))

    order = Order(user_id=current_user().id, car_id=car.id, phone=phone, comment=comment)
    db.session.add(order)
    db.session.commit()
    flash("Заявка отправлена. Менеджер свяжется с вами.")
    return redirect(url_for("main.my_orders"))


@main_bp.route("/my-orders")
@login_required
def my_orders():
    user = current_user()
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    return render_template("my_orders.html", orders=orders, user=user)


@main_bp.route("/admin", methods=["GET", "POST"])
@admin_required
def admin_panel():
    if request.method == "POST":
        car = Car(
            brand=request.form.get("brand", "").strip(),
            model=request.form.get("model", "").strip(),
            year=int(request.form.get("year", 2024)),
            price=int(request.form.get("price", 0)),
            mileage=int(request.form.get("mileage", 0)),
            fuel_type=request.form.get("fuel_type", "Бензин").strip(),
            transmission=request.form.get("transmission", "Автомат").strip(),
            description=request.form.get("description", "").strip(),
            photo_url=request.form.get("photo_url", "").strip() or None,
        )
        if not car.brand or not car.model or not car.description or car.price <= 0:
            flash("Заполните форму корректно")
            return redirect(url_for("main.admin_panel"))

        db.session.add(car)
        db.session.commit()
        flash("Автомобиль добавлен")
        return redirect(url_for("main.admin_panel"))

    cars = Car.query.order_by(Car.created_at.desc()).all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin.html", cars=cars, orders=orders, user=current_user())


@main_bp.route("/seed")
def seed_data():
    if Car.query.count() == 0:
        cars = [
            Car(brand="Chevrolet", model="Cobalt", year=2023, price=13500, mileage=15000, fuel_type="Бензин", transmission="Автомат", description="Экономичный седан для города."),
            Car(brand="Kia", model="Sportage", year=2024, price=31500, mileage=4000, fuel_type="Бензин", transmission="Автомат", description="Надежный кроссовер для семьи."),
            Car(brand="BYD", model="Song Plus", year=2024, price=34000, mileage=2000, fuel_type="Гибрид", transmission="Автомат", description="Современный гибрид с богатой комплектацией."),
        ]
        db.session.add_all(cars)

    if User.query.filter_by(email="admin@autosalon.uz").first() is None:
        admin = User(full_name="Администратор", email="admin@autosalon.uz", is_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)

    db.session.commit()
    return "База заполнена. Админ: admin@autosalon.uz / admin123"
