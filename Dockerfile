FROM python:3
WORKDIR /usr/src/app
COPY . .
ENV TOKEN = "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"
ENV TIME = "03:00"
ENV CHANNEL_ID = "938461049617809438"
RUN pip install -r requirements.txt
CMD ["main.py"]
ENTRYPOINT ["python3"]
