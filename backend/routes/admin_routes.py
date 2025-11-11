import os, time, json, sqlite3
from flask import Blueprint, request, jsonify
from helpers.auth_jwt import create_token, admin_required
bp = Blueprint("admin_routes", __name__)
DB_PATH = os.getenv("DB_PATH", "quantora_data.db")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "nexolve123")
def get_db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
@bp.route("/admin/login", methods=["POST"])
def admin_login():
    if not request.is_json:
        return jsonify({"ok": False, "msg": "json required"}), 400
    body = request.get_json()
    if body.get("username")==ADMIN_USERNAME and body.get("password")==ADMIN_PASSWORD:
        token = create_token({"username": ADMIN_USERNAME, "is_admin": True})
        return jsonify({"ok": True, "token": token})
    return jsonify({"ok": False, "msg": "invalid credentials"}), 403
@bp.route("/admin/users", methods=["GET"])
@admin_required
def admin_users():
    conn = get_db_conn(); cur = conn.cursor()
    cur.execute("SELECT user_id, device_token, is_premium, premium_until FROM users")
    rows = cur.fetchall(); conn.close()
    out = [{"user_id": r["user_id"], "device_token": r["device_token"], "is_premium": bool(r["is_premium"]), "premium_until": r["premium_until"]} for r in rows]
    return jsonify({"ok": True, "users": out})
@bp.route("/admin/grant", methods=["POST"])
@admin_required
def admin_grant():
    if not request.is_json:
        return jsonify({"ok": False, "msg": "json required"}), 400
    body = request.get_json()
    user_id = body.get("user_id"); days = int(body.get("days",30))
    if not user_id: return jsonify({"ok": False, "msg": "user_id required"}), 400
    expiry = int(time.time()) + days*24*3600
    conn = get_db_conn(); cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO users (user_id, device_token, is_premium, premium_until) VALUES (?,?,?,?)", (user_id, None, 1, expiry))
    cur.execute("INSERT INTO subscriptions (user_id, provider, product_id, purchase_token, order_id, status, expiry_ts, raw, created_at) VALUES (?,?,?,?,?,?,?,?,?)",(user_id,"admin",f"grant_{days}d","",f"admin_grant_{int(time.time())}","active",expiry,"{}",int(time.time())))
    conn.commit(); conn.close()
    return jsonify({"ok": True, "user_id": user_id, "expiry": expiry})
@bp.route("/admin/revoke", methods=["POST"])
@admin_required
def admin_revoke():
    if not request.is_json:
        return jsonify({"ok": False, "msg": "json required"}), 400
    body = request.get_json(); user_id = body.get("user_id")
    if not user_id: return jsonify({"ok": False, "msg": "user_id required"}), 400
    conn = get_db_conn(); cur = conn.cursor()
    cur.execute("UPDATE users SET is_premium=0, premium_until=0 WHERE user_id=?", (user_id,))
    conn.commit(); conn.close()
    return jsonify({"ok": True, "user_id": user_id})
@bp.route("/admin/logs", methods=["GET"])
@admin_required
def admin_logs():
    conn = get_db_conn(); cur = conn.cursor()
    cur.execute("SELECT id, ts, payload FROM top5_cache ORDER BY ts DESC LIMIT 50")
    rows = cur.fetchall(); conn.close()
    out = [{"id": r["id"], "ts": r["ts"], "payload": json.loads(r["payload"])} for r in rows]
    return jsonify({"ok": True, "logs": out})
