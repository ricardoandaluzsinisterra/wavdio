FROM python:3.9
WORKDIR /app
COPY . .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY home-app.py .
EXPOSE 443

CMD ["python", "home-app.py"]