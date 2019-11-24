FROM python:3.7

COPY . /file

WORKDIR /file

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["file_app.py"]