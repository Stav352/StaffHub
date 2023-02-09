FROM python:alpine3.17
WORKDIR /app
RUN addgroup portfolio && adduser -D portfolio -G portfolio || true
USER portfolio
COPY main.py requirements.txt id_validate.py ./
COPY ./templates ./templates
COPY ./static ./static
RUN pip install -r requirements.txt
ENV MONGO="mongodb://root:nVEck3VTUWvVPSNYv83E@portfolio-mongodb-headless:27017/"
EXPOSE 5000
ENTRYPOINT python3 main.py