FROM python:alpine3.17
WORKDIR /app
RUN addgroup portfolio && adduser -D portfolio -G portfolio || true
RUN touch app.log && chmod 777 app.log
USER portfolio
COPY .appenv main.py requirements.txt id_validate.py ./
COPY ./templates ./templates
COPY ./static ./static
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT python3 main.py