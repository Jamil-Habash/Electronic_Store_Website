from website import create_app
from flask import session,g

app = create_app()

@app.before_request
def cart_count():
    cart = session.get('cart', {})
    g.cart_count = len(cart) if cart else 0

if __name__ == '__main__':
    app.run(debug=True)