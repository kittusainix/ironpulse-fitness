"""
IronPulse Gym Database Module
Provides database management, initialization, 40-product seed catalog,
and logic mirroring Oracle PL/SQL triggers and stored procedures.
"""

import sqlite3
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

# On Vercel (serverless), only /tmp is writable. Fall back to local path for dev.
_local_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ironpulse.db")
DB_PATH = os.environ.get("DB_PATH", _local_db)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def calculate_bmi(height_cm, weight_kg):
    """Calculates BMI and Category (Mirrors PL/SQL trigger trg_users_calc_bmi)"""
    if not height_cm or not weight_kg or height_cm <= 0 or weight_kg <= 0:
        return None, "Not Available"
    h_m = height_cm / 100.0
    bmi = round(weight_kg / (h_m * h_m), 2)
    if bmi < 18.5:
        category = "Underweight"
    elif bmi <= 24.9:
        category = "Normal Weight"
    elif bmi <= 29.9:
        category = "Overweight"
    else:
        category = "Obese"
    return bmi, category

def get_subscription_time_details(end_date_str, start_date_str=None):
    """
    Computes exact remaining time details ('kitna time bacha hai').
    Returns dict with days, hours, minutes, seconds, badge status, percent left, etc.
    """
    if not end_date_str:
        return {
            "has_subscription": False,
            "status": "NO_PLAN",
            "badge_color": "secondary",
            "time_str": "No Active Subscription",
            "days": 0,
            "hours": 0,
            "mins": 0,
            "percent_remaining": 0,
            "is_active": False
        }

    try:
        if "T" in end_date_str:
            end_dt = datetime.fromisoformat(end_date_str.replace("Z", ""))
        elif len(end_date_str) == 10:
            end_dt = datetime.strptime(end_date_str, "%Y-%m-%d")
        else:
            end_dt = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return {
            "has_subscription": False,
            "status": "ERROR",
            "badge_color": "secondary",
            "time_str": "Invalid Date",
            "days": 0, "hours": 0, "mins": 0, "percent_remaining": 0, "is_active": False
        }

    now = datetime.now()
    diff = end_dt - now

    if diff.total_seconds() <= 0:
        return {
            "has_subscription": True,
            "status": "EXPIRED",
            "badge_color": "danger",
            "time_str": "Plan Expired",
            "days": 0,
            "hours": 0,
            "mins": 0,
            "seconds": 0,
            "percent_remaining": 0,
            "is_active": False,
            "end_date_formatted": end_dt.strftime("%d %b %Y, %I:%M %p")
        }

    days = diff.days
    hours = diff.seconds // 3600
    mins = (diff.seconds % 3600) // 60
    secs = diff.seconds % 60

    # Calculate percentage remaining if start date is known
    percent = 100
    if start_date_str:
        try:
            if "T" in start_date_str:
                start_dt = datetime.fromisoformat(start_date_str.replace("Z", ""))
            elif len(start_date_str) == 10:
                start_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
            else:
                start_dt = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
            total_duration = (end_dt - start_dt).total_seconds()
            if total_duration > 0:
                percent = max(0, min(100, round((diff.total_seconds() / total_duration) * 100)))
        except Exception:
            percent = 80

    if days <= 7:
        badge_color = "warning"
        status = "EXPIRING_SOON"
    else:
        badge_color = "success"
        status = "ACTIVE"

    time_str = f"{days}d {hours}h {mins}m remaining"

    return {
        "has_subscription": True,
        "status": status,
        "badge_color": badge_color,
        "time_str": time_str,
        "days": days,
        "hours": hours,
        "mins": mins,
        "seconds": secs,
        "percent_remaining": percent,
        "is_active": True,
        "end_date_formatted": end_dt.strftime("%d %b %Y, %I:%M %p"),
        "end_date_iso": end_dt.strftime("%Y-%m-%dT%H:%M:%S")
    }

def init_db():
    """Initializes SQLite tables and seeds starter data if empty"""
    conn = get_db_connection()
    cur = conn.cursor()

    # Tables
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        phone TEXT NOT NULL,
        role TEXT DEFAULT 'member',
        age INTEGER,
        gender TEXT,
        height_cm REAL,
        weight_kg REAL,
        bmi_value REAL,
        bmi_category TEXT,
        photo_url TEXT DEFAULT '/static/images/default-avatar.png',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS subscription_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plan_code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        duration_days INTEGER NOT NULL,
        price REAL NOT NULL,
        original_price REAL,
        is_special_offer INTEGER DEFAULT 0,
        offer_tag TEXT,
        features TEXT,
        is_active INTEGER DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS user_subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        plan_id INTEGER NOT NULL,
        start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        end_date TIMESTAMP NOT NULL,
        amount_paid REAL NOT NULL,
        payment_status TEXT DEFAULT 'PAID',
        status TEXT DEFAULT 'ACTIVE',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (plan_id) REFERENCES subscription_plans (id)
    );

    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        description TEXT,
        icon_class TEXT
    );

    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        brand TEXT NOT NULL,
        price REAL NOT NULL,
        original_price REAL,
        rating REAL DEFAULT 4.8,
        reviews_count INTEGER DEFAULT 45,
        stock_quantity INTEGER DEFAULT 50,
        image_url TEXT NOT NULL,
        description TEXT NOT NULL,
        serving_specs TEXT,
        flavor_variant TEXT,
        is_featured INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    );

    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        total_amount REAL NOT NULL,
        shipping_address TEXT NOT NULL,
        contact_phone TEXT NOT NULL,
        payment_method TEXT DEFAULT 'ONLINE',
        order_status TEXT DEFAULT 'CONFIRMED',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        unit_price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products (id)
    );

    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_type TEXT NOT NULL,
        performed_by TEXT NOT NULL,
        target_user_id INTEGER,
        details TEXT,
        log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()

    # Seed data check
    cur.execute("SELECT COUNT(*) FROM subscription_plans")
    if cur.fetchone()[0] == 0:
        seed_database(conn)

    conn.close()

def seed_database(conn):
    """Seeds subscription plans, categories, demo users, and 40 products"""
    cur = conn.cursor()

    # 1. Admin & Demo Users
    admin_pw = generate_password_hash("admin123")
    user_pw = generate_password_hash("user123")

    cur.execute("""
    INSERT INTO users (full_name, email, password_hash, phone, role, age, gender, height_cm, weight_kg, bmi_value, bmi_category, photo_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ('IronPulse Master Admin', 'admin@ironpulse.gym', admin_pw, '+91 98765 00001', 'admin', 32, 'Male', 180, 82.5, 25.46, 'Overweight', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80'))

    cur.execute("""
    INSERT INTO users (full_name, email, password_hash, phone, role, age, gender, height_cm, weight_kg, bmi_value, bmi_category, photo_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ('Rahul Sharma (Student Member)', 'rahul@student.edu', user_pw, '+91 98111 22334', 'member', 20, 'Male', 175, 68.0, 22.20, 'Normal Weight', 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=400&q=80'))

    cur.execute("""
    INSERT INTO users (full_name, email, password_hash, phone, role, age, gender, height_cm, weight_kg, bmi_value, bmi_category, photo_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ('Aman & Priya (Couple Pass)', 'couple@titan.in', user_pw, '+91 98222 33445', 'member', 27, 'Male', 178, 76.0, 23.99, 'Normal Weight', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80'))

    cur.execute("""
    INSERT INTO users (full_name, email, password_hash, phone, role, age, gender, height_cm, weight_kg, bmi_value, bmi_category, photo_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ('Vikram Rajput (VIP Athlete)', 'vikram@fitness.com', user_pw, '+91 98333 44556', 'member', 29, 'Male', 185, 92.0, 26.88, 'Overweight', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80'))

    # 2. Subscription Plans
    plans = [
        ('STUDENT_OFFER', 'Student Discount Pass', 'Exclusive discounted gym access for university & high school students with valid ID.', 30, 799.00, 1499.00, 1, '45% OFF STUDENT SPECIAL', 'Unlimited Gym Floor Access, Locker Room & Showers, Free Fitness Assessment, Valid Student ID Verification'),
        ('COUPLE_OFFER', 'Couple Power Duo Pass', 'Work out together with your partner! Dual membership at massive savings with joint workout plans.', 30, 1999.00, 3200.00, 1, 'POPULAR COUPLE DEAL', '2 Memberships Included, Free Partner Workout Guide, All Group Aerobic & Zumba Classes, Locker Access'),
        ('MONTHLY_STARTER', 'Monthly Starter Plan', 'Flexible month-to-month membership with zero long-term commitments.', 30, 1299.00, 1699.00, 0, 'FLEXIBLE', 'Full Equipment & Free Weight Access, Locker & Showers, Cardio Deck, 1 Free Trainer Guidance Session'),
        ('QUARTERLY_BEAST', 'Quarterly Beast (3 Months)', '3-month power pack designed for visible body transformation and strength building.', 90, 3499.00, 4500.00, 0, 'TRANSFORMATION', 'Full Gym Access 7 Days a Week, 2 Personal Trainer Consultations, Customized Diet Chart, 10% Supplement Discount'),
        ('ANNUAL_TITAN', 'Annual Titan Pass (12 Months)', 'Our most popular annual membership. Unrestricted 365-day access with premium amenities.', 365, 11999.00, 18000.00, 0, 'BEST VALUE - SAVE 40%', 'Unlimited 365-Day Access, Steam & Sauna Facilities, 4 Guest Passes Every Month, 15% Flat Discount in Shop, Free Gym Duffle Bag'),
        ('VIP_PRO_ATHLETE', 'VIP Elite Pro Athlete Pass', 'The pinnacle fitness experience with dedicated personal coach and nutrition monitoring.', 365, 24999.00, 35000.00, 1, 'ALL-INCLUSIVE LUXURY', 'Dedicated 1-on-1 Personal Trainer, Weekly Body Composition Scans (InBody), Custom Macro Nutrition Coaching, VIP Locker & Reserved Parking, Monthly Free Supplement Pack')
    ]
    cur.executemany("""
    INSERT INTO subscription_plans (plan_code, name, description, duration_days, price, original_price, is_special_offer, offer_tag, features)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, plans)

    # 3. Demo Subscriptions
    now = datetime.now()
    # Rahul has Student plan (24 days left)
    cur.execute("""
    INSERT INTO user_subscriptions (user_id, plan_id, start_date, end_date, amount_paid, payment_status, status, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (2, 1, (now - timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S"), (now + timedelta(days=24)).strftime("%Y-%m-%d %H:%M:%S"), 799.00, 'PAID', 'ACTIVE', 'College ID: STU-2024-88912 (Delhi University)'))

    # Couple has Couple Offer (18 days left)
    cur.execute("""
    INSERT INTO user_subscriptions (user_id, plan_id, start_date, end_date, amount_paid, payment_status, status, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (3, 2, (now - timedelta(days=12)).strftime("%Y-%m-%d %H:%M:%S"), (now + timedelta(days=18)).strftime("%Y-%m-%d %H:%M:%S"), 1999.00, 'PAID', 'ACTIVE', 'Partner: Priya Verma (+91 98222 99887)'))

    # Vikram has VIP Athlete (310 days left)
    cur.execute("""
    INSERT INTO user_subscriptions (user_id, plan_id, start_date, end_date, amount_paid, payment_status, status, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (4, 6, (now - timedelta(days=55)).strftime("%Y-%m-%d %H:%M:%S"), (now + timedelta(days=310)).strftime("%Y-%m-%d %H:%M:%S"), 24999.00, 'PAID', 'ACTIVE', 'Assigned Master Coach: Arjun Dev'))

    # 4. Categories
    categories = [
        ('Proteins & Gainers', 'proteins-gainers', '100% Whey Isolate, Raw Whey, Mass Gainers & Plant Protein for maximum muscle hypertrophy.', 'fa-dumbbell'),
        ('Pre-Workout & Energy', 'pre-workout-energy', 'High-stimulant pre-workouts, pump enhancers, and clean sustained explosive energy.', 'fa-bolt'),
        ('Creatine & Recovery', 'creatine-recovery', 'Micronized Creatine, BCAAs, EAAs and Glutamine for rapid cellular ATP recovery.', 'fa-capsules'),
        ('Shakers & Bottles', 'shakers-bottles', 'Leak-proof stainless steel, electric vortex, and BPA-free high capacity gym shakers.', 'fa-wine-bottle'),
        ('Gym Gear & Accessories', 'gear-accessories', 'Powerlifting leather lever belts, wrist wraps, knee sleeves, lifting straps and chalk.', 'fa-shield-halved')
    ]
    cur.executemany("""
    INSERT INTO categories (name, slug, description, icon_class)
    VALUES (?, ?, ?, ?)
    """, categories)

    # 5. Exactly 40 High-Quality Gym Products (8 per category)
    products = [
        # CATEGORY 1: PROTEINS & GAINERS (1-8)
        (1, 'Gold Standard 100% Whey Protein (5 lbs)', 'Optimum Nutrition', 5999.00, 7299.00, 4.9, 842, 60,
         'https://images.unsplash.com/photo-1579722821273-0f6c7d44362f?auto=format&fit=crop&w=700&q=80',
         'The world’s best-selling whey protein powder. Delivers 24g of high quality whey protein primarily from Whey Protein Isolate to support muscle growth and repair.',
         '74 Servings • 24g Protein • 5.5g BCAAs', 'Double Rich Chocolate', 1),
        (1, 'ISO 100 Hydrolyzed 100% Whey Isolate (5 lbs)', 'Dymatize', 7499.00, 8999.00, 4.9, 615, 45,
         'https://images.unsplash.com/photo-1593095948071-474c5cc2989d?auto=format&fit=crop&w=700&q=80',
         'Fastest absorbing whey isolate designed for elite athletes and hard gainers. Ultra-filtered to remove excess lactose, fat, and sugar.',
         '71 Servings • 25g Hydrolyzed Isolate • <1g Sugar', 'Gourmet Vanilla', 1),
        (1, 'NitroTech Ripped Lean Protein & Fat Burner (4 lbs)', 'MuscleTech', 5299.00, 6499.00, 4.7, 390, 35,
         'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=700&q=80',
         'Advanced 7-in-1 musclebuilding whey isolate peptide formula enhanced with L-Carnitine, CLA, and Green Tea Extract for shredded lean muscle mass.',
         '42 Servings • 30g Protein • 500mg L-Carnitine', 'French Vanilla Creme', 0),
        (1, 'Impact Whey Protein Isolate (2.5 kg)', 'MyProtein', 6199.00, 7599.00, 4.8, 520, 50,
         'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=700&q=80',
         'Grade A premium whey isolate tested for extreme purity. Ideal for meeting daily macro targets with zero guilt and incredible mixability.',
         '100 Servings • 23g Protein • 0.1g Fat', 'Salted Caramel', 0),
        (1, 'Biozyme Performance Whey Protein (2 kg)', 'MuscleBlaze', 4499.00, 5499.00, 4.8, 710, 80,
         'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=700&q=80',
         'Clinically tested Enhanced Absorption Formula (EAF) ensuring 50% higher protein absorption and zero stomach bloating.',
         '60 Servings • 25g Protein • Labdoor Certified', 'Rich Chocolate Fudge', 1),
        (1, 'Serious Mass High Calorie Weight Gainer (6 lbs)', 'Optimum Nutrition', 3699.00, 4599.00, 4.6, 420, 30,
         'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=700&q=80',
         'Formulated with 1,250 calories per serving and 50g of protein to facilitate rapid healthy mass gains for ectomorphs and hardgainers.',
         '16 Huge Servings • 1250 Calories • 250g Carbs', 'Chocolate Peanut Butter', 0),
        (1, 'Classic Plus Organic Vegan Plant Protein (1 kg)', 'Sunwarrior', 4199.00, 4999.00, 4.7, 215, 25,
         'https://images.unsplash.com/photo-1532444458054-01a7dd3e9fca?auto=format&fit=crop&w=700&q=80',
         'Raw superfood organic plant protein packed with fermented pea, brown rice, quinoa, and chia seeds. 100% dairy and soy-free.',
         '40 Servings • 20g Clean Plant Protein • Non-GMO', 'Rich Mocha', 0),
        (1, 'Elite 100% Micellar Casein Slow Digestion (4 lbs)', 'Dymatize', 5899.00, 6999.00, 4.8, 180, 20,
         'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=700&q=80',
         'Sustained-release micellar casein protein providing continuous amino acid flow for 7-8 hours overnight muscle recovery.',
         '55 Servings • 25g Micellar Casein • Anti-Catabolic', 'Cookies & Cream', 0),

        # CATEGORY 2: PRE-WORKOUT & ENERGY (9-16)
        (2, 'C4 Original Explosive Pre-Workout (60 Servings)', 'Cellucor', 2899.00, 3699.00, 4.8, 920, 75,
         'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=700&q=80',
         'America’s #1 selling pre-workout powder with CarnoSyn Beta-Alanine, Creatine Nitrate, and 150mg caffeine for legendary pumps and endurance.',
         '60 Scoops • 150mg Caffeine • 1.6g Beta-Alanine', 'Fruit Punch', 1),
        (2, 'Hyde Nightmare High Stimulant Pre-Workout', 'ProSupps', 3199.00, 3999.00, 4.9, 430, 40,
         'https://images.unsplash.com/photo-1550345332-09e3ac987658?auto=format&fit=crop&w=700&q=80',
         'Hardcore pre-workout formulated for heavy lifters demanding intense vascularity, tunnel-vision focus, and unyielding energy.',
         '30 Servings • 300mg Caffeine Matrix • 2.5g Citrulline', 'Blue Razz Freeze', 0),
        (2, 'Ghost Legend V2 Premium Pre-Workout', 'Ghost Lifestyle', 3799.00, 4599.00, 4.9, 510, 35,
         'https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=700&q=80',
         'Full disclosure label with 4g L-Citrulline, 3.2g Beta-Alanine, and Senactiv for unmatched stamina, clarity, and skin-splitting pumps.',
         '30 Servings • 4000mg Pure Citrulline • Vegan Friendly', 'Sour Watermelon', 1),
        (2, 'Psychotic Insane High Energy Pre-Workout', 'Insane Labz', 2699.00, 3499.00, 4.7, 380, 50,
         'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=700&q=80',
         'Loaded with AMPiberry patent to extend the stimulant energy curve up to 3 hours with zero post-workout crash.',
         '35 Servings • Extreme Energy Matrix', 'Gummy Candy', 0),
        (2, 'Gorilla Mode Max Potency Pre-Workout', 'Gorilla Mind', 4599.00, 5499.00, 5.0, 780, 28,
         'https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?auto=format&fit=crop&w=700&q=80',
         'The most heavily dosed nitric oxide and intramuscular hydration formula on earth with 9000mg pure L-Citrulline.',
         '40 Scoops • 9g L-Citrulline • 5g Creatine', 'Tiger’s Blood', 1),
        (2, 'Total War Military Grade Pre-Workout', 'Redcon1', 2999.00, 3799.00, 4.7, 460, 45,
         'https://images.unsplash.com/photo-1549476464-37392f717541?auto=format&fit=crop&w=700&q=80',
         'Award-winning formula that combines rapid-acting caffeine with sustained Green Tea caffeine for non-stop battlefield aggression.',
         '30 Servings • 6g Citrulline Malate • 320mg Caffeine', 'Rainbow Candy', 0),
        (2, 'Outlift Clinically Dosed All-in-One Pre-Workout', 'Nutrex Research', 3499.00, 4299.00, 4.8, 290, 30,
         'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=700&q=80',
         'Complete 10 clinical-dose powerhouse ingredients including 8g Citrulline Malate, 3g Creapure, and 6g BCAAs.',
         '20 Heavy Scoops • 350mg Caffeine • Zero Filler', 'Miami Vice', 0),
        (2, 'N.O.-XPLODE Legendary Pre-Workout Igniter', 'BSN', 2799.00, 3599.00, 4.6, 520, 60,
         'https://images.unsplash.com/photo-1517963879433-6ad2b056d712?auto=format&fit=crop&w=700&q=80',
         'Engineered with advanced thermal energy matrices to elevate physical work capacity and muscle pump endurance.',
         '30 Servings • 275mg Caffeine • Beta-Alanine', 'Grape Slam', 0),

        # CATEGORY 3: CREATINE & RECOVERY (17-24)
        (3, 'Creapure 100% German Micronized Creatine (250g)', 'IronPulse Pure', 1299.00, 1699.00, 4.9, 1120, 120,
         'https://images.unsplash.com/photo-1594381898411-846e7d193883?auto=format&fit=crop&w=700&q=80',
         'The purest 99.99% HPLC tested Creapure monohydrate produced in Bavaria, Germany. Boosts muscular ATP and heavy lifting power.',
         '83 Servings • 3g Creapure Per Scoop • 0 Sugar', 'Unflavored (Neutral)', 1),
        (3, 'Micronized Creatine Powder 300g (100 Servings)', 'Optimum Nutrition', 1499.00, 1899.00, 4.9, 950, 90,
         'https://images.unsplash.com/photo-1579722821273-0f6c7d44362f?auto=format&fit=crop&w=700&q=80',
         'Micro-milled into ultra-fine particles for effortless mixing in water, shakes, or fruit juices without gritty sedimentation.',
         '100 Servings • 3g Pure Monohydrate', 'Unflavored', 1),
        (3, 'Xtend BCAA 7g Muscle Recovery Electrolytes (30 Serv)', 'Scivation', 2199.00, 2799.00, 4.8, 640, 70,
         'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=700&q=80',
         'The original gold standard intra-workout BCAA with 7g of 2:1:1 branched chain amino acids and replenishing electrolytes.',
         '30 Servings • 7g BCAA • 2.5g Glutamine', 'Blue Raspberry Ice', 0),
        (3, 'Creatine Monohydrate with Fast Absorb 250g', 'MuscleBlaze', 999.00, 1399.00, 4.7, 830, 110,
         'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=700&q=80',
         'Informed-choice certified pure creatine monohydrate to fuel strength progression and muscle cell volumization.',
         '83 Servings • 3g Creatine • Zero Preservatives', 'Unflavored', 0),
        (3, 'Fermented L-Glutamine Powder 500g', 'Kaged Muscle', 1899.00, 2399.00, 4.8, 310, 40,
         'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=700&q=80',
         '100% plant-fermented, non-animal sourced L-Glutamine to prevent post-workout immune suppression and muscle soreness.',
         '100 Servings • 5g L-Glutamine • Micro-Pure', 'Unflavored', 0),
        (3, 'Pure L-Citrulline Malate 2:1 Powder (300g)', 'Nutricost', 1799.00, 2299.00, 4.7, 240, 50,
         'https://images.unsplash.com/photo-1550345332-09e3ac987658?auto=format&fit=crop&w=700&q=80',
         'Pharmaceutical grade Citrulline Malate 2:1 for massive nitric oxide vasodilation, blood flow, and lactate clearance.',
         '100 Servings • 3000mg Citrulline Malate', 'Tart Lemon', 0),
        (3, 'Animal Pak The Complete Training Pack (44 Packs)', 'Universal Nutrition', 3899.00, 4699.00, 4.9, 580, 35,
         'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=700&q=80',
         'The legendary all-in-one vitamin, mineral, digestive enzyme, and antioxidant pack built specifically for heavy bodybuilders.',
         '44 Packs • 85+ Nutrients • Amino Complex', 'Convenient Daily Packs', 1),
        (3, 'EAA Max Full Spectrum Essential Amino Acids', 'Primeval Labs', 2599.00, 3299.00, 4.8, 290, 45,
         'https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=700&q=80',
         'All 9 Essential Amino Acids including BCAAs with Pink Himalayan Salt and coconut water powder for cellular rehydration.',
         '30 Servings • 9 Essential Aminos • Zero Calorie', 'Pink Lemonade', 0),

        # CATEGORY 4: SHAKERS, BOTTLES & HYDRATION (25-32)
        (4, 'Pro Series 28-Oz Leakproof Shaker with BlenderBall', 'BlenderBottle', 699.00, 999.00, 4.9, 1420, 150,
         'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=700&q=80',
         'Patented surgical-grade 316 stainless steel wire whisk ball blends thick protein powders into silk in 10 seconds. BPA-free Eastman Tritan.',
         '800ml Capacity • Leak-proof SpoutGuard • Dishwasher Safe', 'Matte Black Carbon', 1),
        (4, 'Revive Multi-Storage Smart Shaker Bottle', 'SmartShake', 849.00, 1199.00, 4.8, 620, 85,
         'https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=700&q=80',
         'Features 2 detachable compartments at the bottom for storing protein powder scoops, creatine, BCAAs, and daily gym vitamins.',
         '750ml • 2 Storage Pods • Soft Loop Handle', 'Stealth Gunmetal', 0),
        (4, 'Voltrx Premium Electric Vortex Protein Shaker', 'VOLTRX', 1899.00, 2499.00, 4.9, 540, 60,
         'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=700&q=80',
         'USB-C rechargeable high-torque electric motor generates a silent 5000 RPM vortex for 100% lump-free protein shakes on the go.',
         '700ml • USB-C Quick Charge • Glowing LED Base', 'Midnight Onyx', 1),
        (4, 'Stainless Steel Vacuum Insulated Gym Flask 32oz', 'Hydro Titan', 1499.00, 1999.00, 4.8, 380, 50,
         'https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=700&q=80',
         'Double-wall copper vacuum insulation keeps ice cold water chilled for 24 hours during grueling weight training sessions.',
         '950ml • 18/8 Pro Food Grade Steel • Chug Cap', 'Tactical Olive Green', 0),
        (4, 'Titan 2.2L Half Gallon Water Jug with Hourly Markers', 'IronPulse Gear', 799.00, 1099.00, 4.7, 720, 100,
         'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=700&q=80',
         'Huge 2.2-liter BPA-free indestructible jug with motivational hourly hydration tracking markers and heavy-duty paracord strap.',
         '2200ml • Time Markings • Leakproof Flip Top', 'Frosted Smoke Black', 0),
        (4, 'ShakeSphere Matte Capsule Tumbler (No Corners)', 'ShakeSphere', 1699.00, 2199.00, 4.8, 310, 40,
         'https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=700&q=80',
         'No whisk ball needed! Patented centrifugal rounded capsule design ensures no powder ever gets stuck in the corners.',
         '700ml • Capsule Shape • Slide Cap', 'Matte Jet Black', 0),
        (4, 'Strada Heavy Insulated Stainless Steel Shaker 24oz', 'BlenderBottle', 1999.00, 2699.00, 4.9, 410, 45,
         'https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=700&q=80',
         'Push-button flip cap with sliding safety lock and vacuum insulated steel keeping pre-workouts freezing cold.',
         '710ml • Push-Button Lock • Whisk Included', 'Brushed Titanium', 0),
        (4, 'Cyclone Cup Metallic High Shear Shaker 20oz', 'Cyclone', 949.00, 1299.00, 4.6, 280, 65,
         'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=700&q=80',
         'Stationary vortex turbine mixer blade that blasts through stubborn casein and whey clumps with absolute ease.',
         '600ml • Cyclone Mixing Blade • Pill Storage', 'Crimson Red / Black', 0),

        # CATEGORY 5: GYM GEAR, ACCESSORIES & EQUIPMENT (33-40)
        (5, 'Heavy Duty 10mm Leather Powerlifting Lever Belt', 'IronPulse Pro', 3299.00, 4499.00, 5.0, 890, 55,
         'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=700&q=80',
         'Competition legal genuine top-grain cowhide leather with alloy quick-release lever buckle for rock-solid intra-abdominal spine bracing during 200kg+ squats and deadlifts.',
         '10mm Thickness • Alloy Lever • S/M/L/XL Sizing', 'Matte Black / Red Suede Inner', 1),
        (5, 'Heavy Duty 18" Elastic Weightlifting Wrist Wraps', 'Titan Force', 599.00, 899.00, 4.8, 670, 130,
         'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=700&q=80',
         'Reinforced thumb loop and military grade Velcro provide maximum wrist joint stability for heavy bench press and overhead presses.',
         'Pair • 18-inch Length • Heavy Elastic Stitching', 'Black with Cyber Red Lines', 0),
        (5, '7mm Neoprene Compression Knee Sleeves (Pair)', 'IronPulse Pro', 1799.00, 2499.00, 4.9, 530, 70,
         'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=700&q=80',
         'Anatomically contoured 7mm SCR neoprene delivering optimal joint warmth, patellar tracking, and rebound spring during deep squats.',
         'Pair • 7mm Dense Neoprene • Anti-Slip Interior', 'Stealth Black', 1),
        (5, 'Heavy Duty Figure 8 Deadlift Lifting Straps', 'BeastGear', 499.00, 799.00, 4.9, 740, 140,
         'https://images.unsplash.com/photo-1517963879433-6ad2b056d712?auto=format&fit=crop&w=700&q=80',
         'Locked-in figure-8 webbing rated to withstand over 1,000 lbs. Eliminates grip fatigue so you can lift maximum poundage on barbell shrugs and deadlifts.',
         'Pair • Cotton Webbing Rated to 500kg', 'Tactical Black', 0),
        (5, 'Premium Fast-Drying Liquid Gym Chalk 250ml', 'GripMaster', 449.00, 699.00, 4.8, 610, 110,
         'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=700&q=80',
         'Dries in 5 seconds into a thin sweat-resistant magnesium carbonate coating. Zero chalk dust cloud, gym compliant.',
         '250ml Squeeze Bottle • 99% Pure Magnesium Carbonate', 'Citrus Scent', 0),
        (5, 'Heavy Duty Pull-Up Assistance Resistance Bands Set', 'IronPulse Pro', 1299.00, 1899.00, 4.8, 480, 80,
         'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=700&q=80',
         'Set of 5 100% natural layered Malaysian latex bands ranging from 10 lbs to 125 lbs resistance for mobility, stretching, and pull-up assist.',
         '5 Multi-Color Bands • Door Anchor • Carry Pouch', '5 Levels (10-125 lbs)', 0),
        (5, 'Tactical Gym Duffle Bag with Vented Shoe Compartment', 'IronPulse Gear', 2199.00, 2999.00, 4.9, 390, 65,
         'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=700&q=80',
         'Water-resistant 900D Oxford fabric with dedicated wet/sweaty clothes pocket, separate shoe chamber, and shaker bottle holsters.',
         '45L Capacity • Water Repellent 900D Fabric', 'Matte Shadow Camo', 1),
        (5, 'Pro Speed Jump Rope with 360° Double Ball Bearings', 'SpeedMaster', 549.00, 849.00, 4.7, 510, 95,
         'https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=700&q=80',
         'Self-locking length adjuster with dual smooth stainless steel ball bearings for lightning fast double-unders and high-intensity cardio HIIT.',
         '3-Meter Coated Steel Cable • Aluminum Handles', 'Cyber Crimson Red', 0)
    ]

    cur.executemany("""
    INSERT INTO products (category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, products)

    conn.commit()

# --- User & Auth Operations ---

def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email.strip(),)).fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None

def register_user(full_name, email, password, phone, age, gender, height_cm, weight_kg, photo_url=None):
    """Mirrors PL/SQL stored procedure sp_register_user"""
    conn = get_db_connection()
    cur = conn.cursor()

    existing = cur.execute("SELECT id FROM users WHERE LOWER(email) = LOWER(?)", (email.strip(),)).fetchone()
    if existing:
        conn.close()
        raise ValueError("An account with this email address already exists.")

    password_hash = generate_password_hash(password)
    bmi, category = calculate_bmi(height_cm, weight_kg)

    cur.execute("""
    INSERT INTO users (full_name, email, password_hash, phone, role, age, gender, height_cm, weight_kg, bmi_value, bmi_category, photo_url)
    VALUES (?, ?, ?, ?, 'member', ?, ?, ?, ?, ?, ?, ?)
    """, (
        full_name, email.strip().lower(), password_hash, phone,
        age, gender, height_cm, weight_kg, bmi, category,
        photo_url or "/static/images/default-avatar.png"
    ))
    user_id = cur.lastrowid

    cur.execute("""
    INSERT INTO audit_logs (action_type, performed_by, target_user_id, details)
    VALUES (?, ?, ?, ?)
    """, ('USER_REGISTERED', 'SYSTEM', user_id, f"Registered: {full_name} ({email})"))

    conn.commit()
    conn.close()
    return user_id

def update_user_profile(user_id, phone=None, weight_kg=None, height_cm=None, photo_url=None, full_name=None):
    """Mirrors PL/SQL stored procedure sp_update_user_stats and recalculates BMI"""
    conn = get_db_connection()
    cur = conn.cursor()

    user = cur.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        conn.close()
        return False

    new_height = height_cm if height_cm is not None else user["height_cm"]
    new_weight = weight_kg if weight_kg is not None else user["weight_kg"]
    new_phone = phone if phone is not None else user["phone"]
    new_name = full_name if full_name is not None else user["full_name"]
    new_photo = photo_url if photo_url is not None else user["photo_url"]

    bmi, category = calculate_bmi(new_height, new_weight)

    cur.execute("""
    UPDATE users
    SET full_name = ?, phone = ?, height_cm = ?, weight_kg = ?, bmi_value = ?, bmi_category = ?, photo_url = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    """, (new_name, new_phone, new_height, new_weight, bmi, category, new_photo, user_id))

    conn.commit()
    conn.close()
    return True

# --- Subscription Operations ---

def get_all_plans():
    conn = get_db_connection()
    plans = conn.execute("SELECT * FROM subscription_plans WHERE is_active = 1 ORDER BY price ASC").fetchall()
    conn.close()
    return [dict(p) for p in plans]

def get_plan_by_id(plan_id):
    conn = get_db_connection()
    plan = conn.execute("SELECT * FROM subscription_plans WHERE id = ?", (plan_id,)).fetchone()
    conn.close()
    return dict(plan) if plan else None

def get_user_active_subscription(user_id):
    """Fetches user active subscription and full countdown details"""
    conn = get_db_connection()
    sub = conn.execute("""
    SELECT s.*, p.name as plan_name, p.plan_code, p.features, p.offer_tag
    FROM user_subscriptions s
    JOIN subscription_plans p ON s.plan_id = p.id
    WHERE s.user_id = ?
    ORDER BY s.end_date DESC
    LIMIT 1
    """, (user_id,)).fetchone()
    conn.close()

    if not sub:
        return get_subscription_time_details(None)

    sub_dict = dict(sub)
    time_info = get_subscription_time_details(sub_dict["end_date"], sub_dict["start_date"])
    sub_dict.update(time_info)
    return sub_dict

def enroll_user_subscription(user_id, plan_id, notes=""):
    """Mirrors PL/SQL stored procedure sp_subscribe_user"""
    conn = get_db_connection()
    cur = conn.cursor()

    plan = cur.execute("SELECT * FROM subscription_plans WHERE id = ?", (plan_id,)).fetchone()
    if not plan:
        conn.close()
        raise ValueError("Selected subscription plan does not exist.")

    now = datetime.now()
    duration = plan["duration_days"]

    # Check existing active subscription
    current_sub = cur.execute("""
    SELECT end_date FROM user_subscriptions 
    WHERE user_id = ? AND end_date > CURRENT_TIMESTAMP
    ORDER BY end_date DESC LIMIT 1
    """, (user_id,)).fetchone()

    if current_sub and current_sub["end_date"]:
        try:
            curr_end = datetime.strptime(current_sub["end_date"], "%Y-%m-%d %H:%M:%S")
            if curr_end > now:
                start_dt = curr_end
                end_dt = curr_end + timedelta(days=duration)
            else:
                start_dt = now
                end_dt = now + timedelta(days=duration)
        except Exception:
            start_dt = now
            end_dt = now + timedelta(days=duration)
    else:
        start_dt = now
        end_dt = now + timedelta(days=duration)

    # Archive older subs
    cur.execute("UPDATE user_subscriptions SET status = 'SUPERSEDED' WHERE user_id = ? AND status = 'ACTIVE'", (user_id,))

    cur.execute("""
    INSERT INTO user_subscriptions (user_id, plan_id, start_date, end_date, amount_paid, payment_status, status, notes)
    VALUES (?, ?, ?, ?, ?, 'PAID', 'ACTIVE', ?)
    """, (
        user_id, plan_id,
        start_dt.strftime("%Y-%m-%d %H:%M:%S"),
        end_dt.strftime("%Y-%m-%d %H:%M:%S"),
        plan["price"], notes
    ))
    sub_id = cur.lastrowid

    cur.execute("""
    INSERT INTO audit_logs (action_type, performed_by, target_user_id, details)
    VALUES (?, ?, ?, ?)
    """, ('SUBSCRIPTION_PURCHASED', 'MEMBER', user_id, f"Plan: {plan['name']} for {plan['price']} INR. Expiry: {end_dt.strftime('%Y-%m-%d')}"))

    conn.commit()
    conn.close()
    return sub_id

# --- Admin Operations ("Admin sab control kr sake and sab bata sake") ---

def admin_get_dashboard_metrics():
    conn = get_db_connection()
    cur = conn.cursor()

    total_users = cur.execute("SELECT COUNT(*) FROM users WHERE role = 'member'").fetchone()[0]
    total_products = cur.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    low_stock = cur.execute("SELECT COUNT(*) FROM products WHERE stock_quantity <= 10").fetchone()[0]

    # Active subscriptions
    active_subs = cur.execute("SELECT COUNT(*) FROM user_subscriptions WHERE end_date > CURRENT_TIMESTAMP AND status = 'ACTIVE'").fetchone()[0]

    # Expiring in <= 7 days
    expiring_soon = cur.execute("""
    SELECT COUNT(*) FROM user_subscriptions 
    WHERE end_date > CURRENT_TIMESTAMP 
      AND end_date <= datetime('now', '+7 days')
      AND status = 'ACTIVE'
    """).fetchone()[0]

    # Total revenue (subs + shop orders)
    sub_rev = cur.execute("SELECT COALESCE(SUM(amount_paid), 0) FROM user_subscriptions WHERE payment_status = 'PAID'").fetchone()[0]
    order_rev = cur.execute("SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE order_status != 'CANCELLED'").fetchone()[0]
    total_revenue = sub_rev + order_rev

    total_orders = cur.execute("SELECT COUNT(*) FROM orders").fetchone()[0]

    conn.close()
    return {
        "total_users": total_users,
        "active_subs": active_subs,
        "expiring_soon": expiring_soon,
        "total_revenue": total_revenue,
        "total_products": total_products,
        "low_stock": low_stock,
        "total_orders": total_orders
    }

def admin_get_all_users():
    """Fetches all users with their subscription details and exact time left"""
    conn = get_db_connection()
    users = conn.execute("""
    SELECT u.*, 
           s.id as sub_id, s.start_date, s.end_date, s.status as sub_status, s.notes as sub_notes,
           p.name as plan_name, p.plan_code
    FROM users u
    LEFT JOIN user_subscriptions s ON s.id = (
        SELECT id FROM user_subscriptions WHERE user_id = u.id ORDER BY end_date DESC LIMIT 1
    )
    LEFT JOIN subscription_plans p ON s.plan_id = p.id
    ORDER BY u.id DESC
    """).fetchall()
    conn.close()

    result = []
    for u in users:
        u_dict = dict(u)
        time_details = get_subscription_time_details(u_dict.get("end_date"), u_dict.get("start_date"))
        u_dict["sub_time"] = time_details
        result.append(u_dict)
    return result

def admin_extend_subscription(user_id, extra_days, admin_name="Master Admin"):
    """Mirrors PL/SQL stored procedure sp_admin_extend_subscription"""
    conn = get_db_connection()
    cur = conn.cursor()

    sub = cur.execute("""
    SELECT id, end_date, plan_id FROM user_subscriptions
    WHERE user_id = ? ORDER BY end_date DESC LIMIT 1
    """, (user_id,)).fetchone()

    now = datetime.now()
    if sub and sub["end_date"]:
        try:
            curr_end = datetime.strptime(sub["end_date"], "%Y-%m-%d %H:%M:%S")
            if curr_end > now:
                new_end = curr_end + timedelta(days=extra_days)
            else:
                new_end = now + timedelta(days=extra_days)
        except Exception:
            new_end = now + timedelta(days=extra_days)

        cur.execute("""
        UPDATE user_subscriptions
        SET end_date = ?, status = 'ACTIVE'
        WHERE id = ?
        """, (new_end.strftime("%Y-%m-%d %H:%M:%S"), sub["id"]))
    else:
        # User had no plan, assign default Starter plan
        starter_plan = cur.execute("SELECT id FROM subscription_plans ORDER BY id ASC LIMIT 1").fetchone()
        plan_id = starter_plan["id"] if starter_plan else 1
        new_end = now + timedelta(days=extra_days)
        cur.execute("""
        INSERT INTO user_subscriptions (user_id, plan_id, start_date, end_date, amount_paid, payment_status, status, notes)
        VALUES (?, ?, ?, ?, 0.0, 'PAID', 'ACTIVE', 'Admin Complimentary Pass')
        """, (user_id, plan_id, now.strftime("%Y-%m-%d %H:%M:%S"), new_end.strftime("%Y-%m-%d %H:%M:%S")))

    cur.execute("""
    INSERT INTO audit_logs (action_type, performed_by, target_user_id, details)
    VALUES (?, ?, ?, ?)
    """, ('ADMIN_EXTEND_SUBSCRIPTION', admin_name, user_id, f"Extended membership by {extra_days} days to {new_end.strftime('%Y-%m-%d')}"))

    conn.commit()
    conn.close()
    return True, new_end.strftime("%d %b %Y, %I:%M %p")

def admin_assign_plan(user_id, plan_id, admin_name="Master Admin"):
    """Assigns or changes a user's subscription directly from admin panel"""
    conn = get_db_connection()
    cur = conn.cursor()

    plan = cur.execute("SELECT * FROM subscription_plans WHERE id = ?", (plan_id,)).fetchone()
    if not plan:
        conn.close()
        return False, "Plan not found."

    now = datetime.now()
    end_dt = now + timedelta(days=plan["duration_days"])

    cur.execute("UPDATE user_subscriptions SET status = 'SUPERSEDED' WHERE user_id = ?", (user_id,))
    cur.execute("""
    INSERT INTO user_subscriptions (user_id, plan_id, start_date, end_date, amount_paid, payment_status, status, notes)
    VALUES (?, ?, ?, ?, ?, 'PAID', 'ACTIVE', 'Assigned directly by Admin')
    """, (user_id, plan_id, now.strftime("%Y-%m-%d %H:%M:%S"), end_dt.strftime("%Y-%m-%d %H:%M:%S"), plan["price"]))

    cur.execute("""
    INSERT INTO audit_logs (action_type, performed_by, target_user_id, details)
    VALUES (?, ?, ?, ?)
    """, ('ADMIN_ASSIGN_PLAN', admin_name, user_id, f"Admin assigned plan: {plan['name']}"))

    conn.commit()
    conn.close()
    return True, f"Assigned {plan['name']} successfully."

def admin_delete_user(user_id, admin_name="Master Admin"):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ? AND role != 'admin'", (user_id,))
    cur.execute("""
    INSERT INTO audit_logs (action_type, performed_by, target_user_id, details)
    VALUES (?, ?, ?, ?)
    """, ('ADMIN_DELETE_USER', admin_name, user_id, f"Admin deleted user ID: {user_id}"))
    conn.commit()
    conn.close()
    return True

# --- Shop & Product Operations ---

def get_categories():
    conn = get_db_connection()
    cats = conn.execute("SELECT * FROM categories ORDER BY id ASC").fetchall()
    conn.close()
    return [dict(c) for c in cats]

def get_products(category_id=None, search=None, sort=None, featured_only=False):
    conn = get_db_connection()
    query = """
    SELECT p.*, c.name as category_name, c.slug as category_slug
    FROM products p
    JOIN categories c ON p.category_id = c.id
    WHERE 1=1
    """
    params = []

    if category_id:
        query += " AND p.category_id = ?"
        params.append(category_id)

    if featured_only:
        query += " AND p.is_featured = 1"

    if search:
        query += " AND (p.name LIKE ? OR p.brand LIKE ? OR p.description LIKE ?)"
        s_term = f"%{search}%"
        params.extend([s_term, s_term, s_term])

    if sort == "price_asc":
        query += " ORDER BY p.price ASC"
    elif sort == "price_desc":
        query += " ORDER BY p.price DESC"
    elif sort == "rating":
        query += " ORDER BY p.rating DESC"
    elif sort == "popular":
        query += " ORDER BY p.reviews_count DESC"
    else:
        query += " ORDER BY p.id ASC"

    prods = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(p) for p in prods]

def get_product_by_id(product_id):
    conn = get_db_connection()
    prod = conn.execute("""
    SELECT p.*, c.name as category_name 
    FROM products p
    JOIN categories c ON p.category_id = c.id
    WHERE p.id = ?
    """, (product_id,)).fetchone()
    conn.close()
    return dict(prod) if prod else None

def admin_save_product(data, product_id=None):
    """Add or edit product in catalog"""
    conn = get_db_connection()
    cur = conn.cursor()

    if product_id:
        cur.execute("""
        UPDATE products
        SET category_id = ?, name = ?, brand = ?, price = ?, original_price = ?,
            stock_quantity = ?, image_url = ?, description = ?, serving_specs = ?,
            flavor_variant = ?, is_featured = ?
        WHERE id = ?
        """, (
            data.get("category_id"), data.get("name"), data.get("brand"),
            data.get("price"), data.get("original_price"), data.get("stock_quantity"),
            data.get("image_url"), data.get("description"), data.get("serving_specs"),
            data.get("flavor_variant"), 1 if data.get("is_featured") else 0,
            product_id
        ))
    else:
        cur.execute("""
        INSERT INTO products (category_id, name, brand, price, original_price, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("category_id"), data.get("name"), data.get("brand"),
            data.get("price"), data.get("original_price"), data.get("stock_quantity", 50),
            data.get("image_url"), data.get("description"), data.get("serving_specs"),
            data.get("flavor_variant"), 1 if data.get("is_featured") else 0
        ))
        product_id = cur.lastrowid

    conn.commit()
    conn.close()
    return product_id

def admin_delete_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return True

# --- Order Operations ---

def create_order(user_id, total_amount, shipping_address, phone, payment_method, cart_items):
    """Creates order and reduces product stock (mirrors trigger trg_order_items_reduce_stock)"""
    conn = get_db_connection()
    cur = conn.cursor()

    # Verify inventory first
    for item in cart_items:
        prod = cur.execute("SELECT stock_quantity, name FROM products WHERE id = ?", (item["product_id"],)).fetchone()
        if not prod or prod["stock_quantity"] < item["quantity"]:
            conn.close()
            raise ValueError(f"Insufficient stock for {prod['name'] if prod else 'Item'}.")

    cur.execute("""
    INSERT INTO orders (user_id, total_amount, shipping_address, contact_phone, payment_method, order_status)
    VALUES (?, ?, ?, ?, ?, 'CONFIRMED')
    """, (user_id, total_amount, shipping_address, phone, payment_method))
    order_id = cur.lastrowid

    for item in cart_items:
        subtotal = item["unit_price"] * item["quantity"]
        cur.execute("""
        INSERT INTO order_items (order_id, product_id, product_name, unit_price, quantity, subtotal)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (order_id, item["product_id"], item["name"], item["unit_price"], item["quantity"], subtotal))

        # Decrement stock (mirrors trigger trg_order_items_reduce_stock)
        cur.execute("""
        UPDATE products SET stock_quantity = stock_quantity - ? WHERE id = ?
        """, (item["quantity"], item["product_id"]))

    conn.commit()
    conn.close()
    return order_id

def get_user_orders(user_id):
    conn = get_db_connection()
    orders = conn.execute("""
    SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC
    """, (user_id,)).fetchall()

    result = []
    for o in orders:
        o_dict = dict(o)
        items = conn.execute("""
        SELECT oi.*, p.image_url FROM order_items oi
        LEFT JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?
        """, (o["id"],)).fetchall()
        o_dict["items"] = [dict(i) for i in items]
        result.append(o_dict)

    conn.close()
    return result

def admin_get_all_orders():
    conn = get_db_connection()
    orders = conn.execute("""
    SELECT o.*, u.full_name as customer_name, u.email as customer_email
    FROM orders o
    JOIN users u ON o.user_id = u.id
    ORDER BY o.id DESC
    """).fetchall()

    result = []
    for o in orders:
        o_dict = dict(o)
        items = conn.execute("SELECT * FROM order_items WHERE order_id = ?", (o["id"],)).fetchall()
        o_dict["items"] = [dict(i) for i in items]
        result.append(o_dict)

    conn.close()
    return result

def admin_update_order_status(order_id, new_status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET order_status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    conn.close()
    return True
