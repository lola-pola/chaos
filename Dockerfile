FROM python:3.10 



COPY app.py app.py
COPY requirements.txt requirements.txt


RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]