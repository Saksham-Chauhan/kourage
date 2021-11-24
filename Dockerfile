# TODO => Set volumes for passing data -> Resume, Career, Kommunity Data
FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
CMD ["main.py"]
ENTRYPOINT ["python3"]
