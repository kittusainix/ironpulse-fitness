# IronPulse Fitness - Oracle PL/SQL Database Documentation

This directory contains the complete, production-grade **Oracle Database (PL/SQL)** schema, triggers, stored procedures, package specifications, and seed data for the **IronPulse Gym Management & E-Commerce Web System**.

---

## 📁 PL/SQL File Manifest

| Execution Order | File Name | Description |
| :---: | :--- | :--- |
| **01** | `01_schema_tables_sequences.sql` | Sequences, Tables (`USERS`, `SUBSCRIPTION_PLANS`, `USER_SUBSCRIPTIONS`, `CATEGORIES`, `PRODUCTS`, `ORDERS`, `ORDER_ITEMS`, `AUDIT_LOGS`), Foreign Keys, Check Constraints & Indexes. |
| **02** | `02_functions_and_triggers.sql` | Triggers: Auto BMI calculation (`trg_users_calc_bmi`), stock decrement (`trg_order_items_reduce_stock`), audit logs (`trg_sub_audit`). Functions: `fn_calculate_days_remaining`, `fn_format_time_left`, `fn_get_bmi_category`. |
| **03** | `03_stored_procedures.sql` | Procedures: `sp_register_user`, `sp_subscribe_user`, `sp_admin_extend_subscription`, `sp_update_user_stats`, `sp_place_order`. |
| **04** | `04_pkg_gym_management.sql` | Complete Enterprise Oracle PL/SQL Package (`pkg_gym_management` Specification + Body) encapsulating cursor management, subscription enrollment, member lookup, and remaining time calculation. |
| **05** | `05_seed_products_and_plans.sql` | Seed data: Master Admin, 3 Demo Members (Student, Couple, VIP), 6 Subscription Plans, 5 Categories, and **40 Detailed Gym Products** (Whey, Pre-Workout, Creatine, Shakers, Gear). |

---

## 🚀 Execution Guide (How to Run in Oracle)

### Option A: Using Oracle SQL Developer
1. Connect to your Oracle database instance (e.g. `XE`, `FREE`, `ORCL`, or Oracle Cloud ATP).
2. Open each SQL script in sequence:
   - Run `01_schema_tables_sequences.sql` (press F5 or click **Run Script**)
   - Run `02_functions_and_triggers.sql`
   - Run `03_stored_procedures.sql`
   - Run `04_pkg_gym_management.sql`
   - Run `05_seed_products_and_plans.sql`
3. Check the **Script Output** console to ensure all objects compiled with `0 errors`.

### Option B: Using SQL*Plus / Command Line
```sql
sqlplus username/password@localhost:1521/XEPDB1

@01_schema_tables_sequences.sql
@02_functions_and_triggers.sql
@03_stored_procedures.sql
@04_pkg_gym_management.sql
@05_seed_products_and_plans.sql
EXIT;
```

### Option C: Using Oracle Live SQL (Browser)
Copy and paste each script into [Oracle Live SQL](https://livesql.oracle.com/) and execute sequentially.

---

## ⚡ Key PL/SQL Features Implemented

### 1. Automated BMI Computation Trigger
```sql
CREATE OR REPLACE TRIGGER trg_users_calc_bmi
BEFORE INSERT OR UPDATE OF height_cm, weight_kg ON users
FOR EACH ROW
...
```
- Every time a member registers or updates their height/weight, this trigger fires before row insertion and computes:
  $$\text{BMI} = \frac{\text{weight\_kg}}{(\text{height\_cm} / 100)^2}$$
- Automatically sets `bmi_category` to `'Underweight'`, `'Normal Weight'`, `'Overweight'`, or `'Obese'`.

### 2. Real-Time Subscription Remaining Time ("Kitna time bacha hai")
- Function: `fn_calculate_days_remaining(p_user_id)` returns integer days.
- Function: `fn_format_time_left(p_end_date)` returns string: `"24 Days, 6 Hours, 30 Mins"`.

### 3. Inventory Stock Protection Trigger
- `trg_order_items_reduce_stock` triggers when a supplement or shaker is ordered. It verifies that stock is available and decrements `products.stock_quantity`. If out of stock, it aborts the transaction with `RAISE_APPLICATION_ERROR(-20001)`.

### 4. Admin Extension Procedure
- `sp_admin_extend_subscription(p_user_id, p_extra_days, p_admin_name)` allows an administrator to grant additional membership days directly to any user.

---

## 🔌 Connecting Python to Oracle
The Python backend contains `oracle_connector.py` configured with `python-oracledb`. To point Flask to your Oracle database, set your credentials in `config.py`:

```python
USE_ORACLE = True  # Switch from SQLite to Oracle Database
ORACLE_USER = "system"
ORACLE_PASSWORD = "your_oracle_password"
ORACLE_DSN = "localhost:1521/XEPDB1"
```
