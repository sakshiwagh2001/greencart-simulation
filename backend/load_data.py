# # C:\Users\saksh\Desktop\New folder\greencart-simulation\backend\load_data.py

import csv
import os
from models import db, Driver, Route, Order
import csv
import os
from models import db, Driver, Route, Order
def load_csv_data(app):
    with app.app_context():
        if not Driver.query.first():
            print("📥 Loading Drivers data...")
            with open(os.path.join("data", "drivers.csv"), encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    db.session.add(
                        Driver(
                            name=row["name"].strip(),
                            shift_hours=int(row["shift_hours"]),
                            past_week_hours=row["past_week_hours"].strip()
                        )
                    )
            db.session.commit()
            print("✅ Drivers data loaded!")
        else:
            print("✅ Drivers data already loaded, skipping...")

        if not Route.query.first():
            print("📥 Loading Routes data...")
            with open(os.path.join("data", "routes.csv"), encoding="utf-8-sig", newline='') as f:
                first_line = f.readline()
                print("Raw first line of routes.csv:", repr(first_line))
                f.seek(0)
                reader = csv.DictReader(f)
                print("Routes CSV fieldnames:", reader.fieldnames)

                for row in reader:
                    print("Route row keys:", list(row.keys()))
                    print("Route row content:", row)

                    db.session.add(
                        Route(
                            id=int(row["route_id"]),
                            distance_km=float(row["distance_km"]),
                            traffic_level=row["traffic_level"].strip(),
                            base_time_min=int(row["base_time_min"])
                        )
                    )
            db.session.commit()
            print("✅ Routes data loaded!")
        else:
            print("✅ Routes data already loaded, skipping...")

        if not Order.query.first():
            print("📥 Loading Orders data...")
            with open(os.path.join("data", "orders.csv"), encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                print("Orders CSV fieldnames:", reader.fieldnames)

                for row in reader:
                    print("Order row keys:", list(row.keys()))
                    print("Order row content:", row)

                    db.session.add(
                        Order(
                            id=int(row["order_id"]),
                            value_rs=float(row["value_rs"]),
                            route_id=int(row["route_id"]),
                            delivery_time=row["delivery_time"].strip()
                        )
                    )
            db.session.commit()
            print("✅ Orders data loaded!")
        else:
            print("✅ Orders data already loaded, skipping...")

        print("\n=== DB Content Summary ===")
        print("Drivers:")
        for d in Driver.query.all():
            print(d.id, d.name, d.shift_hours, d.past_week_hours)
        print("\nRoutes:")
        for r in Route.query.all():
            print(r.id, r.distance_km, r.traffic_level, r.base_time_min)
        print("\nOrders:")
        for o in Order.query.all():
            print(o.id, o.value_rs, o.route_id, o.delivery_time)

