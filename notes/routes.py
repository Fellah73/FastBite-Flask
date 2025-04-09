import datetime
from operator import and_
from notes import app,db,login_manager
from flask import render_template, request,url_for,redirect,flash
from notes.forms import RegisterForm,LoginForm,PurchaseItemForm,CancelItemForm,ReservationForm,AddPromoCodeForm
from notes.models import User,Pizza,Dessert,Beverage,Sandwich,Supplement,Menu,OrderItem,UserBudget,Reservation,Tables
from flask_login import current_user, login_user,login_required,logout_user
from datetime import datetime, timedelta

@app.route('/home')
@app.route('/')
def home_page():
    
    return render_template('home.html')

@app.route('/register',methods=['GET','POST'])
def register_page():
   login_form=RegisterForm()
   
   if login_form.validate_on_submit():
      new_user=User(name=login_form.username.data,
                    email=login_form.email.data,
                    password=login_form.password1.data)
      #add user to database
      print(new_user.name,new_user.email,new_user.password)
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user)
      flash(f'Thanks for registering {new_user.name}',category='success')
      user_id=new_user.id
      existed_user=UserBudget.query.filter_by(user_id=user_id).first()
      if not existed_user:
        user_budget=UserBudget(user_id=user_id, budget=1000)
        db.session.add(user_budget)
        db.session.commit()
      
      return redirect(url_for('home_page'))
   if login_form.errors != {}:
        for err_msg in login_form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}',category='success')
      
   return render_template('register.html',login_form=login_form)

@app.route('/login',methods=['GET','POST'])
def login_page():
   login_form=LoginForm()
   if login_form.validate_on_submit():
      user=User.query.filter_by(email=login_form.email.data).first()
      if user and user.password == login_form.password.data:
         login_user(user)
         flash(f'Welcome {user.name}',category='success')
         user_id=user.id
         existed_user=UserBudget.query.filter_by(user_id=user_id).first()
         if not existed_user:
            user_budget=UserBudget(user_id=user_id, budget=1000)
            db.session.add(user_budget)
            db.session.commit()
         
         return redirect(url_for('command_page'))
      else:
         flash('Wrong username or password',category='danger')
         
         
   return render_template('login.html',login_form=login_form)


@app.route('/logout')
def logout_page():
   logout_user()
   flash(f'You have been logged out ',category='info')
   return redirect(url_for('home_page'))

@app.route('/command', methods=['GET', 'POST'])
def command_page():
    purchase_form = PurchaseItemForm()

    if request.method == 'POST':
        # Pizza purchase
        pizza_id = request.form.get('purchased_pizza')
        if pizza_id:
            pizza = Pizza.query.filter_by(id=pizza_id).first()
            pizza_qte = request.form.get('purchased_pizza_qte')
            print(pizza_qte)
            if pizza:
                flash(f'You purchased {pizza_qte} of {pizza.name} for {int(pizza_qte) * pizza.price} DZ', category='success')
                order= OrderItem(customer_id=current_user.id, food_category='Pizza', product_id=pizza.id, quantity=int(pizza_qte), price=pizza.price * int(pizza_qte))
                db.session.add(order)
                
        # Sandwich purchase
        sandwich_id=request.form.get('purchased_sandwich')
        if sandwich_id:
            sandwich = Sandwich.query.filter_by(id=sandwich_id).first()
            
            sandwich_qte=request.form.get('purchased_sandwich_qte')
            if sandwich and sandwich_qte: 
                print(sandwich_qte)
                flash(f'You purchased {sandwich_qte} of  {sandwich.name} for {int(sandwich_qte) * sandwich.price} DZ', category='success')
                order= OrderItem(customer_id=current_user.id, food_category='Sandwich', product_id=sandwich.id, quantity=int(sandwich_qte), price=sandwich.price * int(sandwich_qte))
                db.session.add(order)
                
        beverage_id=request.form.get('purchased_beverage')
        if beverage_id:
            beverage = Beverage.query.filter_by(id=beverage_id).first()
            beverage_qte=request.form.get('purchased_beverage_qte')
            if beverage:
                flash(f'You purchased {beverage_qte} of {beverage.name} for {beverage.price * int(beverage_qte)} DZ', category='success')
                order= OrderItem(customer_id=current_user.id, food_category='Beverage', product_id=beverage.id, quantity=int(beverage_qte), price=beverage.price * int(beverage_qte))
                db.session.add(order)
        supplement_id=request.form.get('purchased_supplement')
        if supplement_id:
            supplement = Supplement.query.filter_by(id=supplement_id).first()
            supplement_qte=request.form.get('purchased_supplement_qte')
            if supplement:
                flash(f'You purchased {supplement_qte} of  {supplement.name} for {supplement.price*int(supplement_qte)} DZ', category='success')
                order= OrderItem(customer_id=current_user.id, food_category='Supplement', product_id=supplement.id, quantity=int(supplement_qte), price=supplement.price * int(supplement_qte))
                db.session.add(order)
        gateau_id=request.form.get('purchased_gateau')
        if gateau_id:
            gateau=Dessert.query.filter_by(category="Gâteaux").filter_by(id=gateau_id).first()
            gateau_qte=request.form.get('purchased_gateau_qte')

            if gateau:
                flash(f'You purchased {gateau_qte} of  {gateau.name} for {gateau.price * int(gateau_qte)} DZ', category='success')
                order= OrderItem(customer_id=current_user.id, food_category='Dessert', product_id=gateau.id, quantity=int(gateau_qte), price=gateau.price * int(gateau_qte))
                db.session.add(order)
        tarte_id=request.form.get('purchased_tarte')
        if tarte_id:
            tarte=Dessert.query.filter_by(category="Tartes").filter_by(id=tarte_id).first()
            tarte_qte=request.form.get('purchased_tarte_qte')
            if tarte:
                flash(f'You purchased {tarte_qte} of {tarte.name} for {tarte.price * int(tarte_qte)} DZ', category='success')
                order= OrderItem(customer_id=current_user.id, food_category='Dessert', product_id=tarte.id, quantity=int(tarte_qte), price=tarte.price * int(tarte_qte))
                db.session.add(order)
                
        creme_id=request.form.get('purchased_creme')
        if creme_id:
            creme=Dessert.query.filter_by(category="Crèmes").filter_by(id=creme_id).first()
            creme_qte=request.form.get('purchased_creme_qte')
            if creme:
                flash(f'You purchased {creme_qte} of {creme.name} for {creme.price * int(creme_qte)} DZ', category='success')
                order= OrderItem(customer_id=current_user.id, food_category='Dessert', product_id=creme.id, quantity=int(creme_qte), price=creme.price * int(creme_qte))
                db.session.add(order)
        db.session.commit()    
        return redirect(url_for('command_page'))

    if request.method == 'GET':
        current_user_budget=UserBudget.query.filter_by(user_id=current_user.id).first()
        budget=current_user_budget.budget
        return render_template('command.html', budget=budget,Pizza=Pizza, Sandwich=Sandwich, Beverage=Beverage, Dessert=Dessert, Supplement=Supplement, purchase_form=purchase_form)




@app.route('/promotion',methods=['GET','POST'])
def promotion_page():
   for menu in Menu.query.all(): 
      menu.calculate_total_price()
   purchase_form=PurchaseItemForm()
   if request.method == 'POST':
     menu_id=request.form.get('purchased_menu')
     menu_qte=request.form.get('purchased_menu_qte')
     if menu_id:
        menu = Menu.query.filter_by(id=menu_id).first()
        
        if menu:         
            flash(f'You purchased {menu_qte} of {menu.name} for {menu._price * int(menu_qte)} DZ', category='success')
            order= OrderItem(customer_id=current_user.id, food_category='Menu', menu_id=menu.id, quantity=int(menu_qte), price=menu._price * int(menu_qte),product_id=1)
            db.session.add(order)
            db.session.commit()
     return redirect(url_for('promotion_page'))
 
   if request.method == 'GET': 
    current_user_budget=UserBudget.query.filter_by(user_id=current_user.id).first()
    budget=current_user_budget.budget
    return render_template('promotion.html',budget=budget,Menu=Menu,purchase_form=purchase_form)

@app.route('/panier',methods=['GET','POST'])
def panier_page():
   code_promo=["SUMMER20","WINTER15","SPRING10","FALL25","HOLIDAY30","NEWYEAR20","BLACKFRIDAY50"]
   cancel_form=CancelItemForm()
   form=AddPromoCodeForm()
   if request.method == 'POST':
    
    if form.validate_on_submit():
        promo_code=form.promo_code.data
        print(promo_code)
        if promo_code in code_promo:
            flash(f'Promo code {promo_code} added to your budget', category='success')
            user=UserBudget.query.filter_by(user_id=current_user.id).first()
            user.budget=user.budget*1.25
            db.session.commit()
        else:
            flash(f'Promo code {promo_code} not valid', category='danger')
            
    
    delete_command=request.form.get('canceled_command')
    print(delete_command)
    if delete_command:
        order=OrderItem.query.filter_by(id=delete_command).first()
        db.session.delete(order)
        db.session.commit()
        flash(f'Command deleted', category='success')
        
    return redirect(url_for('panier_page'))
    
    
   if request.method == 'GET':
    current_user_budget=UserBudget.query.filter_by(user_id=current_user.id).first()
    budget=current_user_budget.budget   
       
    categories = db.session.query(OrderItem.food_category).distinct().all()
    categories = [category[0] for category in categories]
    #effacer Menu de categories
    if 'Menu' in categories:
     categories.remove('Menu')
    
   
   
   return render_template('panier.html',budget=budget,OrderItem=OrderItem,categories=categories,cancel_form=cancel_form,form=form)

@app.route('/reservation',methods=['GET','POST'])
def reservation_page():
  cancel_form=CancelItemForm()
  if request.method == 'POST':
    
    canceled_reservation=request.form.get('canceled_reservation')
    
    if cancel_form:
        reservation=Reservation.query.filter_by(id=canceled_reservation).first()
        db.session.delete(reservation)
        db.session.commit()
        flash(f'Reservation deleted', category='success')
        
    return redirect(url_for('reservation_page'))
  if request.method == 'GET':
    current_user_budget=UserBudget.query.filter_by(user_id=current_user.id).first()
    budget=current_user_budget.budget
    return render_template('reservation.html',budget=budget,Reservation=Reservation,cancel_form=cancel_form)

@app.route('/reservation/new',methods=['GET','POST'])
def new_reservation_page():
   
    reserve_form = ReservationForm()
    if reserve_form.validate_on_submit():
        try:
            reservation_time = datetime(
                reserve_form.reservation_annee.data,
                reserve_form.reservation_mois.data,
                reserve_form.reservation_day.data,
                reserve_form.reservation_horaire_hour.data,
                reserve_form.reservation_horaire_minute.data
            )
            print(reservation_time)

            # Filtrer les tables par capacité
            dispo_table = Tables.query.filter(Tables.capacity >= reserve_form.guests.data + 1).all()
            dispo_table_ids = [table.id for table in dispo_table]

            # Filtrer les réservations existantes pour le créneau horaire donné
            end_time = reservation_time + timedelta(hours=2)
            reservations = Reservation.query.filter(
                Reservation.table_id.in_(dispo_table_ids),
                Reservation.reservation_time <= end_time,
                reservation_time <= (Reservation.reservation_time + timedelta(hours=2))
            ).all()

            # Obtenir les IDs des tables déjà réservées
            reserved_table_ids = {reservation.table_id for reservation in reservations}

            # Obtenir les tables disponibles
            available_table_ids = [table_id for table_id in dispo_table_ids if table_id not in reserved_table_ids]

            if not available_table_ids:
                flash('No table available for the given time slot', category='danger')
            else:
                # Réserver la première table disponible
                table_id_to_reserve = available_table_ids[0]
                new_reservation = Reservation(
                    user_id=current_user.id,
                    table_id=table_id_to_reserve,
                    reservation_time=reservation_time,
                    guests=reserve_form.guests.data
                )
                db.session.add(new_reservation)
                db.session.commit()
                flash(f'{current_user.name}, your reservation for {reservation_time} has been created!', category='success')
                return redirect(url_for('reservation_page'))  # Redirigez vers la page souhaitée après la réservation

        except ValueError:
            flash('Invalid date', category='danger')
            return redirect(url_for('new_reservation_page'))

    if reserve_form.errors:
        for err_msg in reserve_form.errors.values():
            flash(f'There was an error with creating a reservation: {err_msg}', category='danger')

    return render_template('new_reservation.html', reserve_form=reserve_form)


@app.route('/about')
def about_page():
    return render_template('about.html')