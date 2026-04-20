#include <WiFi.h>
#include <HTTPClient.h>

// Wi-Fi 設定
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
// Flask 伺服器的 IP 位置 (請改成你電腦的區域網路 IP)
const char* serverName = "http://192.168.1.X:5000/update_parking";

// 超音波腳位設定
const int trigPin = 5;
const int echoPin = 18;

void setup() {
  Serial.begin(115200);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // 連接 Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected!");
}

void loop() {
  // 測量距離
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH);
  int distance = duration * 0.034 / 2;

  // 判斷車位狀態 (距離小於 10cm 代表有車)
  int status = (distance < 10) ? 1 : 0;

  // 發送 HTTP POST 請求
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // 組合 JSON 封包
    String jsonPayload = "{\"spot_id\":\"A1\", \"status\":" + String(status) + "}";
    int httpResponseCode = http.POST(jsonPayload);
    
    Serial.println("Distance: " + String(distance) + " cm, Status: " + String(status));
    http.end();
  }
  
  delay(2000); // 每兩秒偵測一次
}
