import datetime
from notes import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return self.name
    
class Sandwich(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    taille = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return self.name 
    
class Beverage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return self.name     

class Supplement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return self.name   

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    taille = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return self.name    
    
class Dessert(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return self.name

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    sandwich_id = db.Column(db.Integer, db.ForeignKey('sandwich.id'), nullable=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=True)
    beverage_id = db.Column(db.Integer, db.ForeignKey('beverage.id'), nullable=True)
    supplement_id = db.Column(db.Integer, db.ForeignKey('supplement.id'), nullable=True)
    dessert_id = db.Column(db.Integer, db.ForeignKey('dessert.id'), nullable=True)
    _price = db.Column('price', db.Float, nullable=False, server_default='0.0')

    sandwich = db.relationship('Sandwich', backref='menus', lazy=True)
    pizza = db.relationship('Pizza', backref='menus', lazy=True)
    beverage = db.relationship('Beverage', backref='menus', lazy=True)
    supplement = db.relationship('Supplement', backref='menus', lazy=True)
    dessert = db.relationship('Dessert', backref='menus', lazy=True)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    def calculate_total_price(self):
        total_price = 0.0
        if self.sandwich:
            total_price += self.sandwich.price
        if self.pizza:
            total_price += self.pizza.price
        if self.beverage:
            total_price += self.beverage.price
        if self.dessert:
            total_price += self.dessert.price
        self._price = total_price

 

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_category = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=True)

    customer = db.relationship('User', backref=db.backref('order_items', lazy=True))
    menu = db.relationship('Menu', backref=db.backref('order_items', lazy=True))

    @property
    def product(self):
        if self.food_category == 'Sandwich':
            return Sandwich.query.get(self.product_id)
        elif self.food_category == 'Pizza':
            return Pizza.query.get(self.product_id)
        elif self.food_category == 'Beverage':
            return Beverage.query.get(self.product_id)
        elif self.food_category == 'Supplement':
            return Supplement.query.get(self.product_id)
        elif self.food_category == 'Dessert':
            return Dessert.query.get(self.product_id)
        else:
            return None
    def menuName(self):
        menu = Menu.query.get(self.menu_id)
        return menu.name if menu else None
    def __repr__(self):
        return f"OrderItem(customer_id={self.customer_id}, food_category={self.food_category}, product_id={self.product_id}, quantity={self.quantity}, price={self.price})"

class UserBudget(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    budget = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref=db.backref('user_budget', uselist=False))


class Tables(db.Model):
    __tablename__ = 'tables'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    
    
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Modification ici
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    reservation_time = db.Column(db.DateTime, nullable=False)
    guests = db.Column(db.Integer, nullable=False)

    # Relations
    user = db.relationship('User', backref=db.backref('reservations', lazy=True))
    table = db.relationship('Tables', backref=db.backref('reservations', lazy=True))
    
    @property
    def calculate_end_time(self):
        return self.reservation_time + datetime.timedelta(hours=2)