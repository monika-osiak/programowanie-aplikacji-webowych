FROM python:3.7

COPY . /auth

WORKDIR /auth

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["auth_app.py"]