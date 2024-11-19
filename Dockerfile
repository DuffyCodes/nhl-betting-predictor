FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install mysql-connector-python pandas scikit-learn

CMD ["python", "analysis_service.py"]