# How to Run RegAI Backend Locally

## 1. Setup Environment
Open your terminal in `d:\RegAi\cdsco\regai_backend`.

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## 2. Run the Server
```bash
# Run with uvicorn (auto-reload enabled)
uvicorn main:app --reload
```

## 3. Test the API
Open your browser to: `http://127.0.0.1:8000/docs` to use the interactive Swagger UI.

### Sample CURL Request
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/classify' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "device_name": "Infusion Pump",
  "intended_use": "Used for controlled intravenous infusion of fluids"
}'
```

## Data Management
- The MVP uses `data/device_data.json` as the source of truth.
- Update this file to add more devices.
