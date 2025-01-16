FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY catalog-app.py .
EXPOSE 443

CMD ["python", "catalog-app.py"]