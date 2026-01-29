# 🏥 Medoc OPD Token Allocation Engine

A FastAPI-based backend system to manage **OPD token booking**, **doctor slot scheduling**, and **queue tracking** with token allocation.

---

## ✅ Features

- 👨‍⚕️ Create / List Doctors
- 🕒 Create / View Doctor Time Slots
- 🎟️ Book OPD Token (ONLINE / WALK_IN)
- 📌 Auto Token Allocation (slot-wise)
- ⏳ Estimated consultation time calculation
- 📋 Live Queue Display (only BOOKED tokens)
- ✅ Serve / ❌ Cancel appointments

---

## 🧰 Tech Stack

| Component | Used |
|----------|------|
| Backend  | FastAPI |
| Database | SQLite |
| ORM      | SQLAlchemy |
| Docs UI  | Swagger (OpenAPI) |
| Server   | Uvicorn |

---

## 📂 Project Structure

medoc-opd-token-engine/
│── app/
│ ├── api/
│ │ ├── v1/
│ │ │ ├── routes.py
│ │ │ ├── booking.py
│ ├── core/
│ │ ├── database.py
│ ├── models/
│ │ ├── entities.py
│ ├── schemas/
│ │ ├── booking.py
│ │ ├── queue.py
│ ├── main.py
│── requirements.txt
│── README.md


---

## ⚙️ Setup & Installation

### ✅ 1. Clone Repo
```bash
git clone https://github.com/Sanjayarjun/medoc-opd-token-engine.git
cd medoc-opd-token-engine
✅ 2. Create Virtual Environment
python -m venv venv
✅ 3. Activate Environment
Windows:

venv\Scripts\activate
Mac/Linux:

source venv/bin/activate
✅ 4. Install Requirements
pip install -r requirements.txt
▶️ Run Project
uvicorn app.main:app --reload
Server runs at:

API Base: http://127.0.0.1:8000

Swagger Docs: http://127.0.0.1:8000/docs

✅ API Endpoints (Quick View)
👨‍⚕️ Doctors
Method	Endpoint	Description
GET	/api/v1/doctors	List Doctors
POST	/api/v1/doctors	Create Doctor
🕒 Slots
Method	Endpoint	Description
GET	/api/v1/doctors/{doctor_id}/slots	Get all slots
POST	/api/v1/doctors/{doctor_id}/slots	Create new slot
🎟️ Booking
Method	Endpoint	Description
POST	/api/v1/book	Book token
📋 Queue
Method	Endpoint	Description
GET	/api/v1/doctors/{doctor_id}/queue	Get live queue
✅ Appointment Actions
Method	Endpoint	Description
PATCH	/api/v1/appointments/{id}/serve	Serve appointment
PATCH	/api/v1/appointments/{id}/cancel	Cancel appointment
🧪 Sample API Testing Flow (Swagger)
✅ Step 1: Create Doctor
POST /api/v1/doctors

{
  "name": "Dr Raj",
  "specialization": "Cardiology",
  "doctor_code": "DOC001"
}
✅ Step 2: Create Slot
POST /api/v1/doctors/{doctor_id}/slots

{
  "start_time": "2026-01-29T10:00:00",
  "end_time": "2026-01-29T12:00:00",
  "capacity": 10
}
✅ Step 3: Book Token
POST /api/v1/book

{
  "doctor_id": 1,
  "patient_name": "Sanjay",
  "patient_phone": "9876543210",
  "source": "ONLINE"
}
✅ Step 4: View Queue
GET /api/v1/doctors/1/queue

✅ Step 5: Serve / Cancel Appointment
Use real appointment_id from booking response.

Serve:
PATCH /api/v1/appointments/{id}/serve

Cancel:
PATCH /api/v1/appointments/{id}/cancel

📌 Notes
Token number is allocated slot-wise using:

max(token_number) + 1

Queue shows only BOOKED tokens

Served or Cancelled tokens won't appear in queue

👤 Author
Sanjay Arjun
GitHub: https://github.com/Sanjayarjun


---

## ✅ Now push this README into GitHub

Run these commands in your project folder:

```bash
git init
git add .
git commit -m "Added README and final submission"
git branch -M main
git remote add origin https://github.com/Sanjayarjun/medoc-opd-token-engine.git
git push -u origin main
