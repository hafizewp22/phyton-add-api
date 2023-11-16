from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(50), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

class CustomerAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    address = db.Column(db.String(255), nullable=False)

class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('customer_address.id'), nullable=False)

@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()

    # Ambil data dari JSON request
    customer_name = data['customer_name']
    address = data['address']

    # Cari atau buat customer baru
    customer = Customer.query.filter_by(customer_name=customer_name).first()
    if not customer:
        customer = Customer(customer_name=customer_name)
        db.session.add(customer)
        db.session.commit()

    # Cari atau buat alamat customer baru
    customer_address = CustomerAddress.query.filter_by(address=address).first()
    if not customer_address:
        customer_address = CustomerAddress(customer_id=customer.id, address=address)
        db.session.add(customer_address)
        db.session.commit()

    # Buat transaksi baru
    transaction = Transaction(customer_id=customer.id, address_id=customer_address.id)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaksi berhasil dibuat!"})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
