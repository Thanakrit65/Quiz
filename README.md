# โปรแกรมสำหรับQuizเพื่อสมัครฝึกงาน
ไฟล์ Quiz1.py สำหรับข้อที่ 1

ไฟล์ Quiz2.py สำหรับข้อที่ 2

---
ไฟล์ Quiz3.py สำหรับข้อที่ 3

## การติดตั้งสำหรับใช้งานQuiz3.py

### ความต้องการเบื้องต้น
- ngrok
- Python 3.7 หรือสูงกว่า
- บัญชี LINE Developers ที่มีการสร้างช่อง Messaging API
- ติดตั้งไลบรารี Python ที่จำเป็นตามที่ระบุใน requirements.txt

### ขั้นตอนการติดตั้ง

1. โคลนหรือดาวน์โหลด repository
2. ติดตั้งไลบรารี Python ที่จำเป็น:

    ```bash
    pip install -r requirements.txt
    ```

3. พิมพ์ `CHANNEL_ACCESS_TOKEN` และ `CHANNEL_SECRET` จากLINE Developers Console ลงใน `"your line access token"` และ `"your line channel secret"`

### การเรียกใช้แอปพลิเคชัน

1. เรียกใช้แอปพลิเคชัน เรียกใช้ในcode editor หรือเรียกใช้ผ่านcommand line:

    ```bash
    python Quiz3.py
    ```

2. แอปพลิเคชันจะเริ่มทำงานที่ http://127.0.0.1:5000/ คุณสามารถเปิดให้เข้าถึงจากอินเทอร์เน็ตได้โดยใช้บริการทันเนลลิ่งเช่น ngrok เพื่อจัดการเหตุการณ์ webhook จาก LINE

3. สร้างทันเนลลิ่ง(tunneling)ด้วย ngrok
    ```bash
    ngrok http 5000
    ```

### Webhook Setup

- ตั้งค่าเส้นทาง `/callback` เป็น URL webhook ใน LINE Developers Console (เช่น `https://<your-ngrok-url>/callback`)
- ตรวจสอบให้แน่ใจว่าแอปพลิเคชันของคุณสามารถเข้าถึงได้จากภายนอกเพื่อให้ LINE สามารถส่งเหตุการณ์ไปยัง webhook ของคุณ

## ตัวอย่างการใช้งาน

เมื่อบอทเชื่อมต่อกับช่อง LINE ของคุณแล้ว จะตอบกลับต่อการป้อนข้อมูลของผู้ใช้ดังนี้:

- "1": ตอบกลับด้วย "good"
- "2": ตอบกลับด้วย "nice"
- "3": แสดงตัวเลือกการตอบกลับด่วน
- "4": แสดงเทมเพลตปุ่มกด
- "5": แสดงเทมเพลตการ์ด

