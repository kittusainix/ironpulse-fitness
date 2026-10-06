"""
Oracle Database Connector using python-oracledb.
Allows running against Oracle Database 19c/21c/23ai XE or Oracle Cloud ATP,
invoking the PL/SQL stored procedures and triggers directly.
"""

import os
import oracledb

# Configuration from environment or defaults
ORACLE_USER = os.getenv("ORACLE_USER", "system")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "oracle")
ORACLE_DSN = os.getenv("ORACLE_DSN", "localhost:1521/XEPDB1")
ORACLE_CONFIG_DIR = os.getenv("TNS_ADMIN", "")

def get_oracle_connection():
    """Establish connection to Oracle Database in Thin mode (no Oracle Client required)"""
    try:
        connection = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN
        )
        return connection
    except Exception as e:
        print(f"[Oracle DB] Connection failed: {e}")
        return None

def test_oracle_connection():
    conn = get_oracle_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT banner FROM v$version WHERE ROWNUM = 1")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        return True, version[0] if version else "Oracle Connected"
    return False, "Could not establish Oracle Database connection"

def call_sp_register_user(full_name, email, password_hash, phone, age, gender, height_cm, weight_kg, photo_url):
    """Executes Oracle PL/SQL stored procedure sp_register_user"""
    conn = get_oracle_connection()
    if not conn:
        raise ConnectionError("Oracle DB is not accessible.")
    try:
        cursor = conn.cursor()
        out_user_id = cursor.var(oracledb.NUMBER)
        cursor.callproc("sp_register_user", [
            full_name, email, password_hash, phone, age, gender,
            height_cm, weight_kg, photo_url, out_user_id
        ])
        user_id = out_user_id.getvalue()
        conn.commit()
        cursor.close()
        conn.close()
        return int(user_id)
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        raise e

def call_sp_subscribe_user(user_id, plan_id, amount_paid, notes=""):
    """Executes Oracle PL/SQL stored procedure sp_subscribe_user"""
    conn = get_oracle_connection()
    if not conn:
        raise ConnectionError("Oracle DB is not accessible.")
    try:
        cursor = conn.cursor()
        out_sub_id = cursor.var(oracledb.NUMBER)
        cursor.callproc("sp_subscribe_user", [
            user_id, plan_id, amount_paid, notes, out_sub_id
        ])
        sub_id = out_sub_id.getvalue()
        conn.commit()
        cursor.close()
        conn.close()
        return int(sub_id)
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        raise e

def call_sp_admin_extend_subscription(user_id, extra_days, admin_name="Master Admin"):
    """Executes Oracle PL/SQL stored procedure sp_admin_extend_subscription"""
    conn = get_oracle_connection()
    if not conn:
        raise ConnectionError("Oracle DB is not accessible.")
    try:
        cursor = conn.cursor()
        cursor.callproc("sp_admin_extend_subscription", [
            user_id, extra_days, admin_name
        ])
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        raise e
