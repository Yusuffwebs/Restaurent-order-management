from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

ORDERS_FILE = "orders.json"
kitchen_password = "2003"


def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r") as file:
            return json.load(file)
    return []


def save_orders(orders):
    with open(ORDERS_FILE, "w") as file:
        json.dump(orders, file)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/place_order", methods=["POST"])
def place_order():
    table_number = request.form.get("table_number")
    order_details = request.form.get("order_details")
    orders = load_orders()
    orders.append({"table_number": table_number, "order_details": order_details})
    save_orders(orders)
    return redirect(url_for("order_placed"))

@app.route("/order_placed")
def order_placed():
    return render_template("order_placed.html")

@app.route("/kitchen", methods=["GET", "POST"])
def kitchen():
    if request.method == "POST":
        password = request.form.get("password")
        if password == kitchen_password:
            orders = load_orders()
            return render_template("kitchen.html", orders=orders)
        else:
            return render_template("kitchen_login.html", error="Incorrect password")
    return render_template("kitchen_login.html")

@app.route("/delete_order/<int:index>", methods=["POST"])
def delete_order(index):
    orders = load_orders()
    if 0 <= index < len(orders):
        orders.pop(index)
        save_orders(orders)
    return redirect(url_for("kitchen"))

if __name__ == "__main__":
    app.run(debug=True)