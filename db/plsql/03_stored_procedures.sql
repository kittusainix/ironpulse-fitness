-- =====================================================================
-- IRONPULSE FITNESS & GYM MANAGEMENT SYSTEM
-- Oracle PL/SQL: Core Stored Procedures
-- File: 03_stored_procedures.sql
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. PROCEDURE: Register User with Complete Fitness Details
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE sp_register_user(
    p_full_name     IN  VARCHAR2,
    p_email         IN  VARCHAR2,
    p_password_hash IN  VARCHAR2,
    p_phone         IN  VARCHAR2,
    p_age           IN  NUMBER,
    p_gender        IN  VARCHAR2,
    p_height_cm     IN  NUMBER,
    p_weight_kg     IN  NUMBER,
    p_photo_url     IN  VARCHAR2,
    o_user_id       OUT NUMBER
)
IS
    v_existing NUMBER;
BEGIN
    -- Check if email already registered
    SELECT COUNT(*) INTO v_existing FROM users WHERE LOWER(email) = LOWER(p_email);
    IF v_existing > 0 THEN
        RAISE_APPLICATION_ERROR(-20002, 'Email address is already registered in IronPulse.');
    END IF;

    o_user_id := seq_users_id.NEXTVAL;

    INSERT INTO users (
        id, full_name, email, password_hash, phone, role,
        age, gender, height_cm, weight_kg, photo_url, created_at, updated_at
    ) VALUES (
        o_user_id, p_full_name, LOWER(p_email), p_password_hash, p_phone, 'member',
        p_age, p_gender, p_height_cm, p_weight_kg, 
        NVL(p_photo_url, '/static/images/default-avatar.png'), SYSDATE, SYSDATE
    );

    -- Log registration
    INSERT INTO audit_logs (id, action_type, performed_by, target_user_id, details)
    VALUES (seq_audit_id.NEXTVAL, 'USER_REGISTERED', 'SYSTEM', o_user_id, 
            'New member registered: ' || p_full_name || ' (' || p_email || ')');

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END sp_register_user;
/

-- ---------------------------------------------------------------------
-- 2. PROCEDURE: Subscribe User to Plan (Standard, Couple, Student, VIP)
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE sp_subscribe_user(
    p_user_id      IN  NUMBER,
    p_plan_id      IN  NUMBER,
    p_amount_paid  IN  NUMBER,
    p_notes        IN  VARCHAR2,
    o_sub_id       OUT NUMBER
)
IS
    v_duration_days NUMBER;
    v_current_end   DATE;
    v_new_start     DATE := SYSDATE;
    v_new_end       DATE;
BEGIN
    -- Fetch plan duration
    SELECT duration_days INTO v_duration_days
    FROM subscription_plans
    WHERE id = p_plan_id;

    -- Check if user currently has an active subscription
    BEGIN
        SELECT end_date INTO v_current_end
        FROM (
            SELECT end_date
            FROM user_subscriptions
            WHERE user_id = p_user_id
              AND status IN ('ACTIVE', 'EXPIRING_SOON')
              AND end_date > SYSDATE
            ORDER BY end_date DESC
        )
        WHERE ROWNUM = 1;

        -- If existing subscription is active, extend from current end date
        v_new_start := v_current_end;
        v_new_end   := v_current_end + v_duration_days;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            -- No active plan, start from today
            v_new_start := SYSDATE;
            v_new_end   := SYSDATE + v_duration_days;
    END;

    -- Mark prior subscriptions as SUPERSEDED / EXPIRED
    UPDATE user_subscriptions
    SET status = 'SUPERSEDED'
    WHERE user_id = p_user_id AND status = 'ACTIVE';

    o_sub_id := seq_subscriptions_id.NEXTVAL;

    INSERT INTO user_subscriptions (
        id, user_id, plan_id, start_date, end_date,
        amount_paid, payment_status, status, notes, created_at
    ) VALUES (
        o_sub_id, p_user_id, p_plan_id, v_new_start, v_new_end,
        p_amount_paid, 'PAID', 'ACTIVE', p_notes, SYSDATE
    );

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END sp_subscribe_user;
/

-- ---------------------------------------------------------------------
-- 3. PROCEDURE: Admin Extends User Subscription Duration
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE sp_admin_extend_subscription(
    p_user_id     IN NUMBER,
    p_extra_days  IN NUMBER,
    p_admin_name  IN VARCHAR2
)
IS
    v_sub_id     NUMBER;
    v_curr_end   DATE;
    v_new_end    DATE;
BEGIN
    -- Find latest subscription
    BEGIN
        SELECT id, end_date INTO v_sub_id, v_curr_end
        FROM (
            SELECT id, end_date
            FROM user_subscriptions
            WHERE user_id = p_user_id
            ORDER BY end_date DESC
        )
        WHERE ROWNUM = 1;

        IF v_curr_end < SYSDATE THEN
            v_new_end := SYSDATE + p_extra_days;
        ELSE
            v_new_end := v_curr_end + p_extra_days;
        END IF;

        UPDATE user_subscriptions
        SET end_date = v_new_end,
            status = 'ACTIVE'
        WHERE id = v_sub_id;

        INSERT INTO audit_logs (id, action_type, performed_by, target_user_id, details)
        VALUES (seq_audit_id.NEXTVAL, 'ADMIN_EXTEND_DAYS', p_admin_name, p_user_id,
                'Subscription extended by ' || p_extra_days || ' days. New expiry: ' || TO_CHAR(v_new_end, 'YYYY-MM-DD'));

        COMMIT;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20003, 'User has no prior subscription to extend.');
    END;
END sp_admin_extend_subscription;
/

-- ---------------------------------------------------------------------
-- 4. PROCEDURE: Update User Fitness Stats & Details
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE sp_update_user_stats(
    p_user_id   IN NUMBER,
    p_phone     IN VARCHAR2,
    p_weight_kg IN NUMBER,
    p_height_cm IN NUMBER,
    p_photo_url IN VARCHAR2
)
IS
BEGIN
    UPDATE users
    SET phone = NVL(p_phone, phone),
        weight_kg = NVL(p_weight_kg, weight_kg),
        height_cm = NVL(p_height_cm, height_cm),
        photo_url = NVL(p_photo_url, photo_url),
        updated_at = SYSDATE
    WHERE id = p_user_id;

    COMMIT;
END sp_update_user_stats;
/

-- ---------------------------------------------------------------------
-- 5. PROCEDURE: Place Order and Save Order Items
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE sp_place_order(
    p_user_id          IN  NUMBER,
    p_total_amount     IN  NUMBER,
    p_shipping_address IN  VARCHAR2,
    p_contact_phone    IN  VARCHAR2,
    p_payment_method   IN  VARCHAR2,
    o_order_id         OUT NUMBER
)
IS
BEGIN
    o_order_id := seq_orders_id.NEXTVAL;

    INSERT INTO orders (
        id, user_id, total_amount, shipping_address,
        contact_phone, payment_method, order_status, created_at
    ) VALUES (
        o_order_id, p_user_id, p_total_amount, p_shipping_address,
        p_contact_phone, NVL(p_payment_method, 'ONLINE'), 'CONFIRMED', SYSDATE
    );

    COMMIT;
END sp_place_order;
/

COMMIT;
