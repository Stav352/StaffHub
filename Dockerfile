FROM python:alpine3.17
WORKDIR /app
RUN addgroup portfolio && adduser -D portfolio -G portfolio || true
USER portfolio
COPY .appenv main.py app.log requirements.txt id_validate.py ./
COPY ./templates ./templates
COPY ./static ./static
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT python3 main.py