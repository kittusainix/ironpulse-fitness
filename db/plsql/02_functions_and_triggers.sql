-- =====================================================================
-- IRONPULSE FITNESS & GYM MANAGEMENT SYSTEM
-- Oracle PL/SQL: Database Triggers and Business Functions
-- File: 02_functions_and_triggers.sql
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. FUNCTION: Determine BMI Category (WHO Standards)
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_get_bmi_category(p_bmi IN NUMBER)
RETURN VARCHAR2
IS
BEGIN
    IF p_bmi IS NULL OR p_bmi <= 0 THEN
        RETURN 'Not Available';
    ELSIF p_bmi < 18.5 THEN
        RETURN 'Underweight';
    ELSIF p_bmi >= 18.5 AND p_bmi <= 24.9 THEN
        RETURN 'Normal Weight';
    ELSIF p_bmi >= 25.0 AND p_bmi <= 29.9 THEN
        RETURN 'Overweight';
    ELSE
        RETURN 'Obese';
    END IF;
END fn_get_bmi_category;
/

-- ---------------------------------------------------------------------
-- 2. TRIGGER: Auto-calculate BMI & Category on Insert/Update of User
--    BMI Formula = Weight (kg) / (Height (m) ^ 2)
-- ---------------------------------------------------------------------
CREATE OR REPLACE TRIGGER trg_users_calc_bmi
BEFORE INSERT OR UPDATE OF height_cm, weight_kg ON users
FOR EACH ROW
DECLARE
    v_height_m NUMBER;
BEGIN
    IF :NEW.height_cm IS NOT NULL AND :NEW.height_cm > 0 AND
       :NEW.weight_kg IS NOT NULL AND :NEW.weight_kg > 0 THEN
        
        -- Convert height from cm to meters
        v_height_m := :NEW.height_cm / 100.0;
        
        -- Compute BMI rounded to 2 decimal places
        :NEW.bmi_value := ROUND(:NEW.weight_kg / POWER(v_height_m, 2), 2);
        
        -- Set BMI Category automatically
        :NEW.bmi_category := fn_get_bmi_category(:NEW.bmi_value);
    END IF;
    
    :NEW.updated_at := SYSDATE;
END trg_users_calc_bmi;
/

-- ---------------------------------------------------------------------
-- 3. FUNCTION: Calculate Exact Remaining Subscription Days for User
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_calculate_days_remaining(p_user_id IN NUMBER)
RETURN NUMBER
IS
    v_end_date DATE;
    v_days_left NUMBER := 0;
BEGIN
    -- Get latest active subscription end date
    BEGIN
        SELECT end_date
        INTO v_end_date
        FROM (
            SELECT end_date
            FROM user_subscriptions
            WHERE user_id = p_user_id
              AND status IN ('ACTIVE', 'EXPIRING_SOON')
            ORDER BY end_date DESC
        )
        WHERE ROWNUM = 1;
        
        IF v_end_date IS NOT NULL THEN
            IF v_end_date > SYSDATE THEN
                v_days_left := CEIL(v_end_date - SYSDATE);
            ELSE
                v_days_left := 0;
            END IF;
        END IF;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            v_days_left := 0;
    END;

    RETURN v_days_left;
END fn_calculate_days_remaining;
/

-- ---------------------------------------------------------------------
-- 4. FUNCTION: Format Subscription Time Left as String ("X Days, Y Hours")
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_format_time_left(p_end_date IN DATE)
RETURN VARCHAR2
IS
    v_diff NUMBER;
    v_days NUMBER;
    v_hours NUMBER;
    v_mins NUMBER;
BEGIN
    IF p_end_date IS NULL THEN
        RETURN 'No Active Plan';
    END IF;

    v_diff := p_end_date - SYSDATE;

    IF v_diff <= 0 THEN
        RETURN 'Expired';
    END IF;

    v_days := TRUNC(v_diff);
    v_hours := TRUNC((v_diff - v_days) * 24);
    v_mins := TRUNC((((v_diff - v_days) * 24) - v_hours) * 60);

    RETURN TO_CHAR(v_days) || ' Days, ' || TO_CHAR(v_hours) || ' Hours, ' || TO_CHAR(v_mins) || ' Mins';
END fn_format_time_left;
/

-- ---------------------------------------------------------------------
-- 5. TRIGGER: Decrement Product Stock on Order Placement
--    Prevents overselling when order item is created
-- ---------------------------------------------------------------------
CREATE OR REPLACE TRIGGER trg_order_items_reduce_stock
AFTER INSERT ON order_items
FOR EACH ROW
DECLARE
    v_current_stock NUMBER;
BEGIN
    -- Check current stock
    SELECT stock_quantity INTO v_current_stock
    FROM products
    WHERE id = :NEW.product_id
    FOR UPDATE;

    IF v_current_stock < :NEW.quantity THEN
        RAISE_APPLICATION_ERROR(-20001, 'Insufficient stock for product ID: ' || :NEW.product_id || '. Available: ' || v_current_stock);
    END IF;

    -- Deduct stock
    UPDATE products
    SET stock_quantity = stock_quantity - :NEW.quantity
    WHERE id = :NEW.product_id;
END trg_order_items_reduce_stock;
/

-- ---------------------------------------------------------------------
-- 6. TRIGGER: Audit Subscription Events
-- ---------------------------------------------------------------------
CREATE OR REPLACE TRIGGER trg_sub_audit
AFTER INSERT OR UPDATE ON user_subscriptions
FOR EACH ROW
DECLARE
    v_action VARCHAR2(60);
    v_desc VARCHAR2(1000);
BEGIN
    IF INSERTING THEN
        v_action := 'SUBSCRIPTION_CREATED';
        v_desc := 'New subscription assigned. Plan ID: ' || :NEW.plan_id || ', End Date: ' || TO_CHAR(:NEW.end_date, 'YYYY-MM-DD');
    ELSIF UPDATING THEN
        v_action := 'SUBSCRIPTION_UPDATED';
        v_desc := 'Subscription ID ' || :NEW.id || ' status changed to ' || :NEW.status || '. New End Date: ' || TO_CHAR(:NEW.end_date, 'YYYY-MM-DD');
    END IF;

    INSERT INTO audit_logs (id, action_type, performed_by, target_user_id, details, log_timestamp)
    VALUES (seq_audit_id.NEXTVAL, v_action, 'SYSTEM', :NEW.user_id, v_desc, SYSDATE);
END trg_sub_audit;
/

COMMIT;
