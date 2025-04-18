# Backend
FROM python:3.11-slim
WORKDIR /app
COPY backend/ .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD [ "python","manage.py", "runserver", "0.0.0.0:8000" ]

# Fronted   
FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "frontend/streamlit_app.py", "--server.port=8501", "--server.enableCORS=false"]