# Medoc OPD Token Allocation Engine

A FastAPI + SQLite based backend system to manage OPD token booking and queue handling for doctors.
It supports doctor creation, time slot scheduling, token booking, queue viewing, and appointment serving/cancellation.

---

## 🚀 Features

- Create and list doctors
- Create and list doctor time slots
- Book OPD token (ONLINE / WALK_IN)
- Auto token allocation per slot (incremental)
- Queue display (only active BOOKED tokens)
- Serve an appointment
- Cancel an appointment

---

## 🛠 Tech Stack

- Python 3
- FastAPI
- SQLAlchemy ORM
- SQLite
- Pydantic

---

## 📦 Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Sanjayarjun/medoc-opd-token-engine.git
cd medoc-opd-token-engine
2️⃣ Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Run the server
uvicorn app.main:app --reload
Server runs at:

http://127.0.0.1:8000
Swagger Docs:

http://127.0.0.1:8000/docs
📌 API Endpoints
✅ Doctors
Method	Endpoint	Description
GET	/api/v1/doctors	List all doctors
POST	/api/v1/doctors	Create a doctor
Example create doctor:

{
  "name": "Dr Raj",
  "specialization": "Cardiology",
  "doctor_code": "DOC001"
}
✅ Slots
Method	Endpoint	Description
GET	/api/v1/doctors/{doctor_id}/slots	Get doctor slots
POST	/api/v1/doctors/{doctor_id}/slots	Create slot
Example create slot:

{
  "start_time": "2026-01-29T10:00:00",
  "end_time": "2026-01-29T12:00:00",
  "capacity": 10
}
✅ Booking (Token Allocation)
Method	Endpoint	Description
POST	/api/v1/book	Book token for doctor
Example book token:

{
  "doctor_id": 1,
  "patient_name": "Sanjay",
  "patient_phone": "9876543210",
  "source": "ONLINE"
}
Response:

{
  "appointment_id": 1,
  "token_number": 1,
  "slot_id": 1,
  "estimated_time": "2026-01-29T10:00:00"
}
✅ Queue
Method	Endpoint	Description
GET	/api/v1/doctors/{doctor_id}/queue	View queue for doctor
Queue shows only active BOOKED tokens.

✅ Appointments
Method	Endpoint	Description
PATCH	/api/v1/appointments/{appointment_id}/serve	Mark appointment as SERVED
PATCH	/api/v1/appointments/{appointment_id}/cancel	Cancel appointment
✅ Notes
Token allocation is handled per slot.

Token numbers are generated using:
max(existing_token_number) + 1

Queue only includes appointments with status BOOKED.

👤 Author
Sanjay Arjun
GitHub: https://github.com/Sanjayarjun


---

## Next (Important)
After pasting README:
1) Save file
2) Commit and push

```bash
git add README.md
git commit -m "Add project README"
git push