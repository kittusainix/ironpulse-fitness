"""
IRONPULSE FITNESS & GYM MANAGEMENT SYSTEM
Flask Application with Authentication, User Profile, Live Countdown Timer,
Shop with 40 Products, Cart & Orders, and Full Admin Command Center.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from functools import wraps

# Setup module search paths for 3-tier architecture
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "backend"))
sys.path.insert(0, str(BASE_DIR / "db"))

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

import config
import db

app = Flask(
    __name__,
    template_folder=config.TEMPLATE_FOLDER,
    static_folder=config.STATIC_FOLDER
)
app.config.from_object(config)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Ensure DB initialized
db.init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session or session.get("role") != "admin":
            flash("Access denied. Administrator privileges required.", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_global_data():
    """Injects user session details into all templates"""
    user = None
    active_sub = None
    if "user_id" in session:
        user = db.get_user_by_id(session["user_id"])
        if user and user["role"] == "member":
            active_sub = db.get_user_active_subscription(user["id"])
    return {
        "current_user": user,
        "current_sub": active_sub,
        "now_year": datetime.now().year
    }

# --- Public Routes ---

@app.route("/")
def index():
    plans = db.get_all_plans()
    featured_products = db.get_products(featured_only=True)
    if len(featured_products) < 8:
        featured_products = db.get_products()[:8]
    categories = db.get_categories()
    return render_template("index.html", plans=plans, featured_products=featured_products, categories=categories)

@app.route("/plans")
def plans():
    all_plans = db.get_all_plans()
    return render_template("plans.html", plans=all_plans)

@app.route("/shop")
def shop():
    category_id = request.args.get("category", type=int)
    search = request.args.get("search", type=str)
    sort = request.args.get("sort", type=str)
    
    products = db.get_products(category_id=category_id, search=search, sort=sort)
    categories = db.get_categories()
    
    return render_template("shop.html", 
                           products=products, 
                           categories=categories, 
                           selected_category=category_id,
                           search_query=search or "",
                           selected_sort=sort or "default",
                           total_count=len(products))

@app.route("/api/products")
def api_products():
    category_id = request.args.get("category", type=int)
    search = request.args.get("search", type=str)
    sort = request.args.get("sort", type=str)
    products = db.get_products(category_id=category_id, search=search, sort=sort)
    return jsonify({"success": True, "count": len(products), "products": products})

# --- Authentication Routes ---

@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("profile"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        phone = request.form.get("phone", "").strip()
        age = request.form.get("age", type=int)
        gender = request.form.get("gender", "")
        height_cm = request.form.get("height_cm", type=float)
        weight_kg = request.form.get("weight_kg", type=float)

        if not full_name or not email or not password or not phone or not height_cm or not weight_kg:
            flash("Please fill in all required fields.", "danger")
            return render_template("register.html", form_data=request.form)

        photo_url = "/static/images/default-avatar.png"
        if "photo" in request.files:
            file = request.files["photo"]
            if file and file.filename != "" and allowed_file(file.filename):
                fname = secure_filename(f"user_{int(datetime.now().timestamp())}_{file.filename}")
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], fname)
                file.save(file_path)
                photo_url = f"/static/uploads/{fname}"

        try:
            user_id = db.register_user(
                full_name=full_name,
                email=email,
                password=password,
                phone=phone,
                age=age,
                gender=gender,
                height_cm=height_cm,
                weight_kg=weight_kg,
                photo_url=photo_url
            )
            flash("Welcome to IronPulse! Your account has been registered successfully. Please log in.", "success")
            return redirect(url_for("login"))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("register.html", form_data=request.form)
        except Exception as e:
            flash("An unexpected error occurred during registration. Please try again.", "danger")
            print(f"Registration error: {e}")
            return render_template("register.html", form_data=request.form)

    return render_template("register.html", form_data={})

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        if session.get("role") == "admin":
            return redirect(url_for("admin_dashboard"))
        return redirect(url_for("profile"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = db.get_user_by_email(email)
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["full_name"]
            session["role"] = user["role"]
            session["email"] = user["email"]

            flash(f"Welcome back, {user['full_name']}!", "success")
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            next_url = request.args.get("next")
            return redirect(next_url or url_for("profile"))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("index"))

# --- User Profile & Subscription ---

@app.route("/profile")
@login_required
def profile():
    user = db.get_user_by_id(session["user_id"])
    if not user:
        session.clear()
        return redirect(url_for("login"))

    sub = db.get_user_active_subscription(user["id"])
    orders = db.get_user_orders(user["id"])
    plans = db.get_all_plans()

    # Calculate additional fitness recommendations
    bmi = user["bmi_value"] or 22.0
    height_m = (user["height_cm"] or 175) / 100.0
    ideal_min_wt = round(18.5 * (height_m ** 2), 1)
    ideal_max_wt = round(24.9 * (height_m ** 2), 1)
    water_liters = round((user["weight_kg"] or 70) * 0.035, 1)
    calorie_est = int((user["weight_kg"] or 70) * 32)

    return render_template("profile.html", 
                           user=user, 
                           sub=sub, 
                           orders=orders, 
                           plans=plans,
                           ideal_min_wt=ideal_min_wt,
                           ideal_max_wt=ideal_max_wt,
                           water_liters=water_liters,
                           calorie_est=calorie_est)

@app.route("/profile/update", methods=["POST"])
@login_required
def update_profile():
    user_id = session["user_id"]
    phone = request.form.get("phone", "").strip()
    full_name = request.form.get("full_name", "").strip()
    weight_kg = request.form.get("weight_kg", type=float)
    height_cm = request.form.get("height_cm", type=float)

    photo_url = None
    if "photo" in request.files:
        file = request.files["photo"]
        if file and file.filename != "" and allowed_file(file.filename):
            fname = secure_filename(f"user_{user_id}_{int(datetime.now().timestamp())}_{file.filename}")
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], fname)
            file.save(file_path)
            photo_url = f"/static/uploads/{fname}"

    db.update_user_profile(user_id=user_id, phone=phone, weight_kg=weight_kg, height_cm=height_cm, photo_url=photo_url, full_name=full_name)
    flash("Your fitness profile has been updated! New BMI calculated.", "success")
    return redirect(url_for("profile"))

@app.route("/subscribe", methods=["POST"])
@login_required
def subscribe():
    plan_id = request.form.get("plan_id", type=int)
    notes = request.form.get("notes", "").strip()

    if not plan_id:
        flash("Invalid subscription selection.", "danger")
        return redirect(url_for("plans"))

    try:
        sub_id = db.enroll_user_subscription(session["user_id"], plan_id, notes=notes)
        flash("🎉 Subscription activated successfully! Your membership timer has started.", "success")
        return redirect(url_for("profile"))
    except Exception as e:
        flash(f"Subscription failed: {str(e)}", "danger")
        return redirect(url_for("plans"))

# --- Checkout & Orders ---

@app.route("/checkout", methods=["POST"])
@login_required
def checkout():
    import json
    user_id = session["user_id"]
    shipping_address = request.form.get("address", "").strip()
    phone = request.form.get("phone", "").strip()
    payment_method = request.form.get("payment_method", "ONLINE")
    cart_json = request.form.get("cart_data", "[]")

    try:
        cart_items = json.loads(cart_json)
        if not cart_items:
            flash("Your cart is empty!", "warning")
            return redirect(url_for("shop"))

        total_amount = sum(item["unit_price"] * item["quantity"] for item in cart_items)
        order_id = db.create_order(user_id, total_amount, shipping_address, phone, payment_method, cart_items)
        flash(f"Order #{order_id} placed successfully! Thank you for ordering with IronPulse.", "success")
        return redirect(url_for("profile"))
    except ValueError as ve:
        flash(str(ve), "danger")
        return redirect(url_for("shop"))
    except Exception as e:
        flash(f"Order failed: {str(e)}", "danger")
        return redirect(url_for("shop"))

# --- Admin Command Center ---

@app.route("/admin")
@admin_required
def admin_dashboard():
    metrics = db.admin_get_dashboard_metrics()
    users = db.admin_get_all_users()
    products = db.get_products()
    categories = db.get_categories()
    orders = db.admin_get_all_orders()
    plans = db.get_all_plans()
    
    return render_template("admin.html",
                           metrics=metrics,
                           users=users,
                           products=products,
                           categories=categories,
                           orders=orders,
                           plans=plans)

@app.route("/admin/extend-sub", methods=["POST"])
@admin_required
def admin_extend_sub():
    user_id = request.form.get("user_id", type=int)
    extra_days = request.form.get("extra_days", type=int)
    if not user_id or not extra_days or extra_days <= 0:
        return jsonify({"success": False, "message": "Invalid user or duration"}), 400

    admin_name = session.get("user_name", "Master Admin")
    success, new_expiry = db.admin_extend_subscription(user_id, extra_days, admin_name)
    if success:
        return jsonify({"success": True, "message": f"Added {extra_days} days! New Expiry: {new_expiry}"})
    return jsonify({"success": False, "message": "Could not extend subscription"}), 400

@app.route("/admin/assign-plan", methods=["POST"])
@admin_required
def admin_assign_plan_route():
    user_id = request.form.get("user_id", type=int)
    plan_id = request.form.get("plan_id", type=int)
    admin_name = session.get("user_name", "Master Admin")
    success, msg = db.admin_assign_plan(user_id, plan_id, admin_name)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/user/delete/<int:user_id>", methods=["POST"])
@admin_required
def admin_delete_user_route(user_id):
    db.admin_delete_user(user_id, session.get("user_name", "Master Admin"))
    flash(f"User ID #{user_id} removed successfully.", "info")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/product/save", methods=["POST"])
@admin_required
def admin_save_product_route():
    product_id = request.form.get("product_id", type=int)
    data = {
        "name": request.form.get("name"),
        "brand": request.form.get("brand"),
        "category_id": request.form.get("category_id", type=int),
        "price": request.form.get("price", type=float),
        "original_price": request.form.get("original_price", type=float),
        "stock_quantity": request.form.get("stock_quantity", type=int),
        "image_url": request.form.get("image_url"),
        "description": request.form.get("description"),
        "serving_specs": request.form.get("serving_specs"),
        "flavor_variant": request.form.get("flavor_variant"),
        "is_featured": 1 if request.form.get("is_featured") else 0
    }
    db.admin_save_product(data, product_id=product_id)
    flash("Product catalog updated successfully!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/product/delete/<int:product_id>", methods=["POST"])
@admin_required
def admin_delete_product_route(product_id):
    db.admin_delete_product(product_id)
    flash("Product removed from shop catalog.", "info")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/order/status", methods=["POST"])
@admin_required
def admin_order_status_route():
    order_id = request.form.get("order_id", type=int)
    status = request.form.get("status")
    db.admin_update_order_status(order_id, status)
    flash(f"Order #{order_id} status updated to {status}.", "success")
    return redirect(url_for("admin_dashboard"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
