# 🏋️ IronPulse Fitness & Gym Management System

A full-stack, enterprise-grade Gym Management & E-Commerce Web Application built with **HTML5, CSS3, JavaScript, Python (Flask)** and an **Oracle PL/SQL database architecture**.

---

## 🌟 Highlights & Features Implemented

1. **Member Authentication & Onboarding**:
   - Detailed registration form collecting **Weight (kg), Height (cm), Age, Gender, Phone, and Profile Picture**.
   - **Automated BMI Trigger**: Instantly evaluates BMI score, WHO category (Underweight, Normal, Overweight, Obese), ideal weight range, daily hydration target, and calorie estimation.

2. **Subscription Models ("Kitna Time Bacha Hai" Countdown)**:
   - 🎓 **Student Discount Pass (₹799/mo)** with Student ID verification.
   - 💑 **Couple Power Duo Pass (₹1,999/mo)** covering dual memberships with partner details.
   - ⚡ **Monthly Starter (₹1,299/mo)**
   - 🔥 **Quarterly Beast (₹3,499/3 mo)**
   - 🏆 **Annual Titan Pass (₹11,999/yr)** (Save 40%)
   - 👑 **VIP Elite Pro Athlete Pass (₹24,999/yr)** with dedicated personal coach.
   - **Live Countdown Timer**: Real-time ticking clock on user profile calculating days, hours, minutes, and seconds remaining with a visual progress bar.

3. **Official Pro Shop (Exactly 40 Gym Products)**:
   - Categorized into 5 distinct lines (8 products each):
     1. *Proteins & Gainers* (Gold Standard Whey, ISO 100, NitroTech, Serious Mass, Vegan Plant...)
     2. *Pre-Workout & Energy* (C4 Original, Hyde Nightmare, Ghost Legend, Gorilla Mode...)
     3. *Creatine & Recovery* (German Creapure, ON Micronized, Xtend BCAA, Animal Pak...)
     4. *Shakers, Bottles & Hydration* (BlenderBottle Pro, SmartShake, Voltrx Electric Vortex...)
     5. *Gym Gear & Equipment* (10mm Leather Lever Belts, Knee Sleeves, Wrist Wraps, Chalk...)
   - Search bar, category filters, sorting by price/rating/popularity, slide-out cart drawer, and instant checkout.

4. **Member Fitness Profile**:
   - Photo & contact details.
   - **Membership Clock**: Real-time remaining time countdown.
   - **BMI Health Hub**: BMI gauge, weight tracking, water goal, and customized macro suggestions.
   - **Shop Order History**: Line-item tracking of supplements and shaker purchases.
   - **Edit Profile Modal**: Dynamically update weight (triggers instant BMI recalculation), phone, and photo.

5. **Admin Command Center ("Admin Sab Control Kr Sake & Sab Bata Sake")**:
   - Master KPI metrics: Registered Members, Active Subscriptions, Expiring Soon (≤ 7 Days alert), Total Revenue, Catalog Count, Low Stock items.
   - **User Data Oversight**:
     - View all member profiles, photos, body metrics, and BMI categories.
     - **Time Remaining Monitor**: Displays exact remaining time badge (Green for active, Yellow for ≤ 7 days, Red for expired).
   - **Admin Controls**:
     - **Quick Extend Subscriptions**: Add +7, +30, or +90 days with 1-click AJAX.
     - **Assign / Change Plan**: Manually allocate any subscription plan.
     - **Delete Member**: Remove user accounts.
   - **Product Inventory Management**: Add new products, update stock/prices/descriptions, delete products.
   - **Store Orders Monitor**: Track customer orders and update status (CONFIRMED, SHIPPED, DELIVERED, CANCELLED).

6. **Oracle PL/SQL Database (`database/plsql/`)**:
   - `01_schema_tables_sequences.sql`: Sequences, Tables, Constraints & Indexes.
   - `02_functions_and_triggers.sql`: Triggers for BMI calculation (`trg_users_calc_bmi`), stock deduction (`trg_order_items_reduce_stock`), and audit tracking.
   - `03_stored_procedures.sql`: `sp_register_user`, `sp_subscribe_user`, `sp_admin_extend_subscription`, etc.
   - `04_pkg_gym_management.sql`: Complete Oracle PL/SQL package specification and body.
   - `05_seed_products_and_plans.sql`: Complete seed data with 40 products and demo accounts.
   - `oracle_connector.py`: Python connector with `python-oracledb`.

---

## 🔑 Demo Login Accounts

| Role | Email | Password | Details |
| :--- | :--- | :--- | :--- |
| **Master Admin** | `admin@ironpulse.gym` | `admin123` | Full access to Admin Command Center, users, time tracking, products, orders |
| **Student Member** | `rahul@student.edu` | `user123` | Active Student Offer membership (countdown running) |
| **Couple Pass** | `couple@titan.in` | `user123` | Active Couple Duo membership with partner details |
| **VIP Athlete** | `vikram@fitness.com` | `user123` | Active VIP Annual Athlete pass (300+ days remaining) |

*(You can also register a brand new member with your own photo, height, and weight via the Register form!)*

---

## 🚀 How to Run the Project

### 1. Open Terminal or PowerShell
Navigate to this project folder:
```powershell
cd C:\Users\user\Desktop\project
```

### 2. Start the Flask Server
```powershell
python app.py
```

### 3. Open in Browser
Visit:
```
http://127.0.0.1:5000
```

---

## 📂 Project Directory Structure

```
project/
├── app.py                      # Main Flask application and REST routes
├── config.py                   # Configuration and Oracle toggle
├── db.py                       # SQLite database engine mirroring PL/SQL logic
├── ironpulse.db                # Initialized database with 40 products & seed data
├── oracle_connector.py         # Oracle DB connector using python-oracledb
├── requirements.txt            # Python requirements
├── database/
│   └── plsql/
│       ├── 01_schema_tables_sequences.sql     # Oracle DDL schema
│       ├── 02_functions_and_triggers.sql      # PL/SQL triggers (BMI, stock decrement)
│       ├── 03_stored_procedures.sql           # PL/SQL stored procedures
│       ├── 04_pkg_gym_management.sql          # PL/SQL Package specification & body
│       ├── 05_seed_products_and_plans.sql     # Seed data for Oracle DB
│       └── README_ORACLE_PLSQL.md             # Execution instructions for Oracle XE/APEX
├── static/
│   ├── css/
│   │   ├── main.css            # Dark luxury athletic styling & glassmorphism
│   │   ├── animations.css      # Pulse glow, countdown tickers & keyframe effects
│   │   └── dashboard.css       # Member & admin dashboard tables and widgets
│   ├── js/
│   │   ├── main.js             # Sticky navbar, toast notifications, modals
│   │   ├── bmi.js              # Interactive real-time BMI calculator engine
│   │   ├── timer.js            # Live countdown timer ("Kitna time bacha hai")
│   │   ├── shop.js             # Cart management, drawer, 40-product filters
│   │   └── admin.js            # Admin user management & AJAX subscription extender
│   ├── images/
│   │   └── default-avatar.png  # Fallback athletic avatar
│   └── uploads/                # Member uploaded profile pictures
└── templates/
    ├── base.html               # Master layout, navbar, cart drawer & modals
    ├── index.html              # Hero with loop video, BMI calculator, featured shop
    ├── plans.html              # Student, Couple, and VIP membership models
    ├── shop.html               # 40 Gym Products catalog with search and filters
    ├── login.html              # Member & Admin dual login with 1-click test credentials
    ├── register.html           # Member registration with live BMI preview & photo upload
    ├── profile.html            # User dashboard with countdown timer, BMI stats & orders
    └── admin.html              # Admin Command Center with full user control & metrics
```
