# C:\Users\saksh\Desktop\New folder\greencart-simulation\backend\routes.py

from flask import Blueprint, request, jsonify,session
from models import db, Driver, Route, Order,Manager


from werkzeug.security import check_password_hash

routes_bp = Blueprint("routes", __name__)

# Manager Login API
@routes_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    manager = Manager.query.filter_by(username=username).first()
    if not manager or not manager.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    
    session['manager_id'] = manager.id
    session['username'] = manager.username

    return jsonify({'message': 'Login successful'})

@routes_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

@routes_bp.route('/protected', methods=['GET'])
def protected():
    if 'manager_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    return jsonify({'message': f"Hello {session['username']}, you are logged in."})

@routes_bp.route("/drivers", methods=["GET"])
def get_drivers():
    drivers = Driver.query.all()
    return jsonify([{
        "id": d.id,
        "name": d.name,
        "shift_hours": d.shift_hours,
        "past_week_hours": d.past_week_hours
    } for d in drivers])


@routes_bp.route("/routes", methods=["GET"])
def get_routes():
    routes = Route.query.all()
    return jsonify([{
        "id": r.id,
        "distance_km": r.distance_km,
        "traffic_level": r.traffic_level,
        "base_time_min": r.base_time_min
    } for r in routes])

@routes_bp.route("/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return jsonify([{
        "id": o.id,
        "value_rs": o.value_rs,
        "route_id": o.route_id,
        "delivery_time": o.delivery_time
    } for o in orders])



@routes_bp.route("/drivers", methods=["POST"])
def add_driver():
    data = request.json
    if not data.get("name") or not data.get("shift_hours") or not data.get("past_week_hours"):
        return jsonify({"error": "Missing fields"}), 400

    driver = Driver(
        name=data["name"],
        shift_hours=data["shift_hours"],
        past_week_hours=data["past_week_hours"]
    )
    db.session.add(driver)
    db.session.commit()
    return jsonify({"message": "Driver added", "id": driver.id}), 201

@routes_bp.route("/drivers/<int:driver_id>", methods=["PUT"])
def update_driver(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"error": "Driver not found"}), 404

    data = request.json
    driver.name = data.get("name", driver.name)
    driver.shift_hours = data.get("shift_hours", driver.shift_hours)
    driver.past_week_hours = data.get("past_week_hours", driver.past_week_hours)

    db.session.commit()
    return jsonify({"message": "Driver updated"})


@routes_bp.route("/simulation", methods=["POST"])
def run_simulation():
    data = request.json
    num_drivers = data.get("numDrivers")
    start_time = data.get("startTime")
    max_hours = data.get("maxHours")

    if not (num_drivers and start_time and max_hours):
        return jsonify({"error": "Missing parameters"}), 400

    drivers = Driver.query.limit(num_drivers).all()
    routes = Route.query.all()
    orders = Order.query.all()

    total_orders = len(orders)
    on_time_deliveries = 0
    late_deliveries = 0
    total_profit = 0

    def time_to_minutes(t):
        h, m = map(int, t.split(":"))
        return h * 60 + m

    start_time_mins = time_to_minutes(start_time)

    fatigue_factor = 1.0
    if max_hours > 8:
        fatigue_factor = 1.3  


    for idx, order in enumerate(orders):
        route = next((r for r in routes if r.id == order.route_id), None)
        if not route:
            continue

        base_route_time = route.base_time_min
        traffic_surcharge = 2 if route.traffic_level == "High" else 0

        expected_delivery_time = base_route_time * fatigue_factor + traffic_surcharge * 5

        actual_delivery_time = time_to_minutes(order.delivery_time)

        delay_due_to_driver_shortage = 0
        if idx >= num_drivers:
            delay_due_to_driver_shortage = 60 * (idx - num_drivers + 1)
            actual_delivery_time += delay_due_to_driver_shortage

        is_late = actual_delivery_time > expected_delivery_time + 10  
        penalty = 50 if is_late else 0

        if is_late:
            late_deliveries += 1
        else:
            on_time_deliveries += 1

        bonus = 0
        if order.value_rs > 1000 and not is_late:
            bonus = order.value_rs * 0.10

        fuel_cost = (5 + traffic_surcharge) * route.distance_km
        profit = order.value_rs + bonus - penalty - fuel_cost
        total_profit += profit

    efficiency_score = (on_time_deliveries / total_orders) * 100 if total_orders > 0 else 0

    result = {
        "total_profit": round(total_profit, 2),
        "efficiency_score": round(efficiency_score, 2),
        "on_time_deliveries": on_time_deliveries,
        "late_deliveries": late_deliveries,
        "total_orders": total_orders,
        "fatigue_factor": fatigue_factor,
        "driver_shortage_delay": delay_due_to_driver_shortage
    }

    return jsonify(result)



@routes_bp.route("/drivers/<int:driver_id>", methods=["DELETE"])
def delete_driver(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"error": "Driver not found"}), 404

    db.session.delete(driver)
    db.session.commit()
    return jsonify({"message": "Driver deleted"})

@routes_bp.route("/orders", methods=["POST"])
def add_order():
    data = request.json
    if not all(k in data for k in ("value_rs", "route_id", "delivery_time")):
        return jsonify({"error": "Missing fields"}), 400

    order = Order(
        value_rs=data["value_rs"],
        route_id=data["route_id"],
        delivery_time=data["delivery_time"]
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({"message": "Order added", "id": order.id}), 201

@routes_bp.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    data = request.json
    order.value_rs = data.get("value_rs", order.value_rs)
    order.route_id = data.get("route_id", order.route_id)
    order.delivery_time = data.get("delivery_time", order.delivery_time)

    db.session.commit()
    return jsonify({"message": "Order updated"})

@routes_bp.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"})

@routes_bp.route("/routes", methods=["POST"])
def add_route():
    data = request.json
    if not all(k in data for k in ("distance_km", "traffic_level", "base_time_min")):
        return jsonify({"error": "Missing fields"}), 400

    route = Route(
        distance_km=data["distance_km"],
        traffic_level=data["traffic_level"],
        base_time_min=data["base_time_min"]
    )
    db.session.add(route)
    db.session.commit()
    return jsonify({"message": "Route added", "id": route.id}), 201

@routes_bp.route("/routes/<int:route_id>", methods=["PUT"])
def update_route(route_id):
    route = Route.query.get(route_id)
    if not route:
        return jsonify({"error": "Route not found"}), 404

    data = request.json
    route.distance_km = data.get("distance_km", route.distance_km)
    route.traffic_level = data.get("traffic_level", route.traffic_level)
    route.base_time_min = data.get("base_time_min", route.base_time_min)

    db.session.commit()
    return jsonify({"message": "Route updated"})

@routes_bp.route("/routes/<int:route_id>", methods=["DELETE"])
def delete_route(route_id):
    route = Route.query.get(route_id)
    if not route:
        return jsonify({"error": "Route not found"}), 404

    db.session.delete(route)
    db.session.commit()
    return jsonify({"message": "Route deleted"})
