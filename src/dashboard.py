import streamlit as st
import sqlite3
import pandas as pd
import time

st.set_page_config(page_title="智慧停車位戰情室", layout="centered")
st.title("🚗 AIoT 智慧停車即時監控面板")

# 讀取資料庫函數
def get_parking_data():
    conn = sqlite3.connect('parking.db')
    df = pd.read_sql_query("SELECT * FROM parking_spots", conn)
    conn.close()
    return df

# 渲染畫面
st.subheader("微觀邊緣感測狀態 (ESP32 即時回報)")

df = get_parking_data()

if not df.empty:
    for index, row in df.iterrows():
        # 判斷狀態與顏色
        if row['status'] == 1:
            color = "#dc3545" # 更漂亮柔和的紅色
            state_text = "已被佔用 (Occupied)"
        else:
            color = "#28a745" # 更漂亮柔和的綠色
            state_text = "目前空位 (Available)"
        
        # 畫出車格
        st.markdown(
            f"""
            <div style='background-color: {color}; padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 10px;'>
                <h2>車位 {row['spot_id']}</h2>
                <h4>{state_text}</h4>
                <p>最後更新時間: {row['last_update']}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
else:
    st.info("等待 ESP32 感測器傳送資料中...")

# 每 2 秒重新整理一次介面 (使用 Streamlit 原生的 rerun，避免 while True 導致卡頓)
time.sleep(2)
st.rerun()
