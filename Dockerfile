FROM python:3.7-alpine

pip install --no-cache-dir -r requirements.txt

COPY app.py app.py

CMD ["python", "app.py"]