# AppointmentAI
This repo is a AI agent to book an appointment with Doctors.

#### This command installs Python packages listed in a file called requirements.txt, with some specific options: 
```
pip install -r requirements.txt --no-deps --upgrade
```

#### RUN streamlit UI
```
streamlit run streamlit_ui.py
```
#### RUN streamlit API
```
uvicorn main:app --reload --port 8002
```
