# Backend
FROM python:3.11-slim
WORKDIR /app
COPY backend/ .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD [ "python","manage.py", "runserver", "0.0.0.0:8000" ]

# Fronted   
FROM python:3.11-slim
WORKDIR /app
COPY frontend/ .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8501"]