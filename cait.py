from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Для работы сессий

# Конфигурация
app.config['SITE_NAME'] = "Курица от Зули"
app.config['SITE_SLOGAN'] = "Сочная курица гриль с дымком в Оренбурге"
app.config['PRIMARY_COLOR'] = "#FF6B00"  # Оранжевый
app.config['SECONDARY_COLOR'] = "#8B4513"  # Коричневый
app.config['BACKGROUND_COLOR'] = "#FFF9F2"  # Светло-бежевый

# Меню с товарами
menu_items = [
    {"id": 1, "name": "Целая курица гриль", "price": 450, 
     "description": "Свежая курица весом ~1.2 кг с хрустящей корочкой", 
     "image": "chicken-whole.jpg"},
    {"id": 2, "name": "Половина курицы", "price": 250, 
     "description": "Сочная половина курицы гриль с ароматными специями", 
     "image": "chicken-half.jpg"},
    {"id": 3, "name": "Набор бедер (4 шт)", "price": 280, 
     "description": "Ароматные куриные бедра с золотистой корочкой", 
     "image": "chicken-thighs.jpg"},
    {"id": 4, "name": "Картофель фри", "price": 120, 
     "description": "Хрустящий картофель с фирменным соусом", 
     "image": "fries.jpg"},
    {"id": 5, "name": "Салат Цезарь", "price": 150, 
     "description": "Свежий салат с курицей, крутонами и соусом", 
     "image": "caesar.jpg"},
    {"id": 6, "name": "Комбо Оренбург", "price": 550, 
     "description": "Целая курица + картофель + 2 соуса + напиток", 
     "image": "combo.jpg"}
]

@app.route('/')
def home():
    # Инициализируем корзину в сессии, если ее нет
    if 'cart' not in session:
        session['cart'] = []
    
    return render_template('index.html', 
                         site_name=app.config['SITE_NAME'],
                         slogan=app.config['SITE_SLOGAN'],
                         primary_color=app.config['PRIMARY_COLOR'],
                         secondary_color=app.config['SECONDARY_COLOR'],
                         bg_color=app.config['BACKGROUND_COLOR'],
                         menu=menu_items,
                         cart=session['cart'])

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = int(request.form.get('item_id'))
    quantity = int(request.form.get('quantity', 1))
    
    item = next((item for item in menu_items if item['id'] == item_id), None)
    if item:
        # Получаем текущую корзину из сессии
        cart = session.get('cart', [])
        
        # Проверяем, есть ли уже такой товар в корзине
        found = False
        for cart_item in cart:
            if cart_item['id'] == item_id:
                cart_item['quantity'] += quantity
                found = True
                break
        
        if not found:
            cart.append({
                "id": item['id'],
                "name": item['name'],
                "price": item['price'],
                "quantity": quantity,
                "image": item['image']
            })
        
        # Сохраняем обновленную корзину в сессии
        session['cart'] = cart
    
    return redirect(url_for('home'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', 
                         site_name=app.config['SITE_NAME'],
                         primary_color=app.config['PRIMARY_COLOR'],
                         secondary_color=app.config['SECONDARY_COLOR'],
                         bg_color=app.config['BACKGROUND_COLOR'],
                         cart=cart, 
                         total=total)

@app.route('/checkout', methods=['POST'])
def checkout():
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    comments = request.form.get('comments')
    
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    
    # Логирование заказа
    print(f"\n=== НОВЫЙ ЗАКАЗ ===")
    print(f"Клиент: {name}")
    print(f"Телефон: {phone}")
    print(f"Адрес: {address}")
    print(f"Комментарии: {comments}")
    print("Состав заказа:")
    for item in cart:
        print(f"- {item['name']} x{item['quantity']} - {item['price'] * item['quantity']} руб.")
    print(f"ИТОГО: {total} руб.")
    print("==================\n")
    
    # Очищаем корзину после оформления
    session.pop('cart', None)
    
    return render_template('order_success.html', 
                         site_name=app.config['SITE_NAME'],
                         primary_color=app.config['PRIMARY_COLOR'],
                         name=name)

if __name__ == '__main__':
    # Для локального запуска используйте:
    # app.run(debug=True)
    
    # Для Render.com используйте:
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)