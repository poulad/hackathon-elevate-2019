FROM debian
RUN set -x                                                      \
    && apt-get update -y                                        \
    && apt-get install -y python-pip python-dev build-essential \
WORKDIR /app
COPY src .
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["/app/app.py"]