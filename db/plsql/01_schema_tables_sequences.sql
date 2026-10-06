-- =====================================================================
-- IRONPULSE FITNESS & GYM MANAGEMENT SYSTEM
-- Oracle PL/SQL DDL Schema: Tables, Sequences, Constraints
-- File: 01_schema_tables_sequences.sql
-- =====================================================================

-- Drop existing tables (in reverse foreign-key order) if re-running
BEGIN
    FOR t IN (SELECT table_name FROM user_tables WHERE table_name IN (
        'AUDIT_LOGS', 'ORDER_ITEMS', 'ORDERS', 'PRODUCTS', 
        'CATEGORIES', 'USER_SUBSCRIPTIONS', 'SUBSCRIPTION_PLANS', 'USERS'
    )) LOOP
        EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS PURGE';
    END LOOP;
END;
/

-- Drop existing sequences if re-running
BEGIN
    FOR s IN (SELECT sequence_name FROM user_sequences WHERE sequence_name IN (
        'SEQ_USERS_ID', 'SEQ_PLANS_ID', 'SEQ_SUBSCRIPTIONS_ID',
        'SEQ_CATEGORIES_ID', 'SEQ_PRODUCTS_ID', 'SEQ_ORDERS_ID',
        'SEQ_ORDER_ITEMS_ID', 'SEQ_AUDIT_ID'
    )) LOOP
        EXECUTE IMMEDIATE 'DROP SEQUENCE ' || s.sequence_name;
    END LOOP;
END;
/

-- ---------------------------------------------------------------------
-- 1. Sequences for Auto-Increment Primary Keys
-- ---------------------------------------------------------------------
CREATE SEQUENCE seq_users_id START WITH 100 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_plans_id START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_subscriptions_id START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_categories_id START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_products_id START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_orders_id START WITH 1000 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_order_items_id START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_audit_id START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

-- ---------------------------------------------------------------------
-- 2. USERS Table (Members & Admins with Fitness/BMI Profile)
-- ---------------------------------------------------------------------
CREATE TABLE users (
    id             NUMBER PRIMARY KEY,
    full_name      VARCHAR2(100) NOT NULL,
    email          VARCHAR2(120) UNIQUE NOT NULL,
    password_hash  VARCHAR2(256) NOT NULL,
    phone          VARCHAR2(20) NOT NULL,
    role           VARCHAR2(20) DEFAULT 'member' CHECK (role IN ('member', 'admin')),
    age            NUMBER(3) CHECK (age >= 10 AND age <= 100),
    gender         VARCHAR2(20) CHECK (gender IN ('Male', 'Female', 'Other')),
    height_cm      NUMBER(5, 2) CHECK (height_cm > 50 AND height_cm < 260),
    weight_kg      NUMBER(5, 2) CHECK (weight_kg > 20 AND weight_kg < 350),
    bmi_value      NUMBER(5, 2),
    bmi_category   VARCHAR2(30),
    photo_url      VARCHAR2(500) DEFAULT '/static/images/default-avatar.png',
    created_at     DATE DEFAULT SYSDATE NOT NULL,
    updated_at     DATE DEFAULT SYSDATE NOT NULL
);

-- ---------------------------------------------------------------------
-- 3. SUBSCRIPTION_PLANS Table (Standard, Couple, Student, VIP)
-- ---------------------------------------------------------------------
CREATE TABLE subscription_plans (
    id                NUMBER PRIMARY KEY,
    plan_code         VARCHAR2(50) UNIQUE NOT NULL,
    name              VARCHAR2(100) NOT NULL,
    description       VARCHAR2(500) NOT NULL,
    duration_days     NUMBER(4) NOT NULL,
    price             NUMBER(10, 2) NOT NULL,
    original_price    NUMBER(10, 2),
    is_special_offer  NUMBER(1) DEFAULT 0 CHECK (is_special_offer IN (0, 1)),
    offer_tag         VARCHAR2(50),
    features          VARCHAR2(1000), -- Comma separated feature list
    is_active         NUMBER(1) DEFAULT 1 CHECK (is_active IN (0, 1))
);

-- ---------------------------------------------------------------------
-- 4. USER_SUBSCRIPTIONS Table (Active/Past Memberships & Expiry)
-- ---------------------------------------------------------------------
CREATE TABLE user_subscriptions (
    id              NUMBER PRIMARY KEY,
    user_id         NUMBER NOT NULL,
    plan_id         NUMBER NOT NULL,
    start_date      DATE DEFAULT SYSDATE NOT NULL,
    end_date        DATE NOT NULL,
    amount_paid     NUMBER(10, 2) NOT NULL,
    payment_status  VARCHAR2(30) DEFAULT 'PAID' CHECK (payment_status IN ('PAID', 'PENDING', 'FAILED', 'REFUNDED')),
    status          VARCHAR2(30) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'EXPIRING_SOON', 'EXPIRED', 'CANCELLED')),
    notes           VARCHAR2(400), -- e.g. Couple Partner Name, Student ID number
    created_at      DATE DEFAULT SYSDATE NOT NULL,
    CONSTRAINT fk_sub_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_sub_plan FOREIGN KEY (plan_id) REFERENCES subscription_plans(id)
);

-- ---------------------------------------------------------------------
-- 5. CATEGORIES Table (Shop categories)
-- ---------------------------------------------------------------------
CREATE TABLE categories (
    id           NUMBER PRIMARY KEY,
    name         VARCHAR2(80) UNIQUE NOT NULL,
    slug         VARCHAR2(80) UNIQUE NOT NULL,
    description  VARCHAR2(300),
    icon_class   VARCHAR2(50)
);

-- ---------------------------------------------------------------------
-- 6. PRODUCTS Table (Supplements, Shakers, Apparel, Gear)
-- ---------------------------------------------------------------------
CREATE TABLE products (
    id              NUMBER PRIMARY KEY,
    category_id     NUMBER NOT NULL,
    name            VARCHAR2(200) NOT NULL,
    brand           VARCHAR2(100) NOT NULL,
    price           NUMBER(10, 2) NOT NULL,
    original_price  NUMBER(10, 2),
    rating          NUMBER(3, 1) DEFAULT 4.8,
    reviews_count   NUMBER(6) DEFAULT 42,
    stock_quantity  NUMBER(6) DEFAULT 50 CHECK (stock_quantity >= 0),
    image_url       VARCHAR2(500) NOT NULL,
    description     VARCHAR2(1000) NOT NULL,
    serving_specs   VARCHAR2(200),
    flavor_variant  VARCHAR2(100),
    is_featured     NUMBER(1) DEFAULT 0 CHECK (is_featured IN (0, 1)),
    created_at      DATE DEFAULT SYSDATE NOT NULL,
    CONSTRAINT fk_prod_cat FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- ---------------------------------------------------------------------
-- 7. ORDERS Table (Store purchases)
-- ---------------------------------------------------------------------
CREATE TABLE orders (
    id                NUMBER PRIMARY KEY,
    user_id           NUMBER NOT NULL,
    total_amount      NUMBER(10, 2) NOT NULL,
    shipping_address  VARCHAR2(400) NOT NULL,
    contact_phone     VARCHAR2(20) NOT NULL,
    payment_method    VARCHAR2(50) DEFAULT 'ONLINE' NOT NULL,
    order_status      VARCHAR2(30) DEFAULT 'PROCESSING' CHECK (order_status IN ('PROCESSING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED')),
    created_at        DATE DEFAULT SYSDATE NOT NULL,
    CONSTRAINT fk_order_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------------
-- 8. ORDER_ITEMS Table (Line items per order)
-- ---------------------------------------------------------------------
CREATE TABLE order_items (
    id            NUMBER PRIMARY KEY,
    order_id      NUMBER NOT NULL,
    product_id    NUMBER NOT NULL,
    product_name  VARCHAR2(200) NOT NULL,
    unit_price    NUMBER(10, 2) NOT NULL,
    quantity      NUMBER(4) CHECK (quantity > 0),
    subtotal      NUMBER(10, 2) NOT NULL,
    CONSTRAINT fk_item_order FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    CONSTRAINT fk_item_prod FOREIGN KEY (product_id) REFERENCES products(id)
);

-- ---------------------------------------------------------------------
-- 9. AUDIT_LOGS Table (Admin actions & system events)
-- ---------------------------------------------------------------------
CREATE TABLE audit_logs (
    id             NUMBER PRIMARY KEY,
    action_type    VARCHAR2(60) NOT NULL,
    performed_by   VARCHAR2(100) NOT NULL,
    target_user_id NUMBER,
    details        VARCHAR2(1000),
    log_timestamp  DATE DEFAULT SYSDATE NOT NULL
);

-- Create helpful performance indexes
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_sub_user_id ON user_subscriptions(user_id);
CREATE INDEX idx_sub_status ON user_subscriptions(status);
CREATE INDEX idx_prod_cat ON products(category_id);
CREATE INDEX idx_orders_user ON orders(user_id);

COMMIT;
