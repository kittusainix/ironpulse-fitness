-- =====================================================================
-- IRONPULSE FITNESS & GYM MANAGEMENT SYSTEM
-- Oracle PL/SQL: Package Specification and Package Body
-- File: 04_pkg_gym_management.sql
-- =====================================================================

-- ---------------------------------------------------------------------
-- PACKAGE SPECIFICATION
-- ---------------------------------------------------------------------
CREATE OR REPLACE PACKAGE pkg_gym_management IS

    -- Custom Types
    TYPE t_user_rec IS RECORD (
        id             users.id%TYPE,
        full_name      users.full_name%TYPE,
        email          users.email%TYPE,
        phone          users.phone%TYPE,
        bmi_value      users.bmi_value%TYPE,
        bmi_category   users.bmi_category%TYPE,
        days_remaining NUMBER
    );
    TYPE t_user_cur IS REF CURSOR;

    -- Constants
    c_status_active   CONSTANT VARCHAR2(10) := 'ACTIVE';
    c_status_expired  CONSTANT VARCHAR2(10) := 'EXPIRED';

    -- Public Functions & Procedures
    FUNCTION get_days_remaining(p_user_id IN NUMBER) RETURN NUMBER;
    FUNCTION get_bmi_category(p_bmi IN NUMBER) RETURN VARCHAR2;
    FUNCTION format_time_left(p_end_date IN DATE) RETURN VARCHAR2;

    PROCEDURE register_member(
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
    );

    PROCEDURE enroll_subscription(
        p_user_id      IN  NUMBER,
        p_plan_id      IN  NUMBER,
        p_amount_paid  IN  NUMBER,
        p_notes        IN  VARCHAR2,
        o_sub_id       OUT NUMBER
    );

    PROCEDURE extend_subscription_days(
        p_user_id     IN NUMBER,
        p_extra_days  IN NUMBER,
        p_admin_name  IN VARCHAR2
    );

    PROCEDURE get_expiring_members(
        p_days_threshold IN NUMBER,
        o_cursor         OUT t_user_cur
    );

END pkg_gym_management;
/

-- ---------------------------------------------------------------------
-- PACKAGE BODY
-- ---------------------------------------------------------------------
CREATE OR REPLACE PACKAGE BODY pkg_gym_management IS

    FUNCTION get_days_remaining(p_user_id IN NUMBER) RETURN NUMBER IS
        v_end_date DATE;
    BEGIN
        SELECT end_date INTO v_end_date
        FROM (
            SELECT end_date
            FROM user_subscriptions
            WHERE user_id = p_user_id
              AND status IN ('ACTIVE', 'EXPIRING_SOON')
            ORDER BY end_date DESC
        )
        WHERE ROWNUM = 1;

        IF v_end_date > SYSDATE THEN
            RETURN CEIL(v_end_date - SYSDATE);
        ELSE
            RETURN 0;
        END IF;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RETURN 0;
    END get_days_remaining;

    FUNCTION get_bmi_category(p_bmi IN NUMBER) RETURN VARCHAR2 IS
    BEGIN
        IF p_bmi IS NULL OR p_bmi <= 0 THEN
            RETURN 'Not Available';
        ELSIF p_bmi < 18.5 THEN
            RETURN 'Underweight';
        ELSIF p_bmi <= 24.9 THEN
            RETURN 'Normal Weight';
        ELSIF p_bmi <= 29.9 THEN
            RETURN 'Overweight';
        ELSE
            RETURN 'Obese';
        END IF;
    END get_bmi_category;

    FUNCTION format_time_left(p_end_date IN DATE) RETURN VARCHAR2 IS
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

        v_days  := TRUNC(v_diff);
        v_hours := TRUNC((v_diff - v_days) * 24);
        v_mins  := TRUNC((((v_diff - v_days) * 24) - v_hours) * 60);

        RETURN TO_CHAR(v_days) || ' Days, ' || TO_CHAR(v_hours) || ' Hours, ' || TO_CHAR(v_mins) || ' Mins';
    END format_time_left;

    PROCEDURE register_member(
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
    ) IS
    BEGIN
        sp_register_user(
            p_full_name, p_email, p_password_hash, p_phone,
            p_age, p_gender, p_height_cm, p_weight_kg, p_photo_url, o_user_id
        );
    END register_member;

    PROCEDURE enroll_subscription(
        p_user_id      IN  NUMBER,
        p_plan_id      IN  NUMBER,
        p_amount_paid  IN  NUMBER,
        p_notes        IN  VARCHAR2,
        o_sub_id       OUT NUMBER
    ) IS
    BEGIN
        sp_subscribe_user(
            p_user_id, p_plan_id, p_amount_paid, p_notes, o_sub_id
        );
    END enroll_subscription;

    PROCEDURE extend_subscription_days(
        p_user_id     IN NUMBER,
        p_extra_days  IN NUMBER,
        p_admin_name  IN VARCHAR2
    ) IS
    BEGIN
        sp_admin_extend_subscription(p_user_id, p_extra_days, p_admin_name);
    END extend_subscription_days;

    PROCEDURE get_expiring_members(
        p_days_threshold IN NUMBER,
        o_cursor         OUT t_user_cur
    ) IS
    BEGIN
        OPEN o_cursor FOR
            SELECT u.id, u.full_name, u.email, u.phone, u.bmi_value, u.bmi_category,
                   CEIL(s.end_date - SYSDATE) AS days_remaining
            FROM users u
            JOIN user_subscriptions s ON u.id = s.user_id
            WHERE s.status = 'ACTIVE'
              AND (s.end_date - SYSDATE) <= p_days_threshold
              AND (s.end_date - SYSDATE) >= 0
            ORDER BY s.end_date ASC;
    END get_expiring_members;

END pkg_gym_management;
/

COMMIT;
