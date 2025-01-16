FROM python:3.12.0

WORKDIR /root
RUN pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 443

CMD ["python","app/upload-app.py"]