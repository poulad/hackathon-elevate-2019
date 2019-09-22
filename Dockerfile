FROM debian

RUN set -x                                                      \
    && apt-get update -y                                        \
    && apt-get install -y python-pip python-dev build-essential \
    && rm -rfv /var/lib/apt/lists/*

WORKDIR /app
COPY src .

RUN pip install -r requirements.txt

ENV PORT 80
EXPOSE 80

ENTRYPOINT ["python"]
CMD ["/app/app.py"]
