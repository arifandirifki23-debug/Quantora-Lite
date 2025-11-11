# minimal Flask entry (production-editable)
import os
from flask import Flask, jsonify, send_from_directory
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__, static_folder='../frontend/build', template_folder='../frontend/build')
@app.route('/api/ping')
def ping():
    return jsonify({"ok": True, "version": "4.1.5"})
@app.route('/')
def index():
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception:
        return "<h1>Quantora v4.1.5</h1><p>Frontend not built.</p>"
if __name__=='__main__':
    app.run(host=os.getenv('FLASK_HOST','0.0.0.0'), port=int(os.getenv('FLASK_PORT','8080')))
