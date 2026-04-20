from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# 初始化資料庫
def init_db():
    conn = sqlite3.connect('parking.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS parking_spots
                 (spot_id TEXT PRIMARY KEY, status INTEGER, last_update TEXT)''')
    conn.commit()
    conn.close()

@app.route('/update_parking', methods=['POST'])
def update_parking():
    data = request.get_json()
    
    # 簡單防護：確保收到的 JSON 有包含必填欄位，避免伺服器報錯崩潰
    if not data or 'spot_id' not in data or 'status' not in data:
        return jsonify({"error": "Invalid payload format"}), 400
        
    spot_id = data.get('spot_id')
    status = data.get('status')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('parking.db')
    c = conn.cursor()
    # 寫入或更新車位狀態
    c.execute("REPLACE INTO parking_spots (spot_id, status, last_update) VALUES (?, ?, ?)", 
              (spot_id, status, current_time))
    conn.commit()
    conn.close()

    return jsonify({"message": "Status updated successfully"}), 200

if __name__ == '__main__':
    init_db()
    # 啟動伺服器，允許區域網路連線
    app.run(host='0.0.0.0', port=5000, debug=True)
