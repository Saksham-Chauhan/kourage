FROM python:3
WORKDIR /usr/src/app
COPY . .
ENV TOKEN = ""
ENV TIME = ""
ENV CHANNEL_ID = ""
RUN pip install -r requirements.txt
CMD ["main.py"]
ENTRYPOINT ["python3"]
