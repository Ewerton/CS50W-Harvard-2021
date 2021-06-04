

FROM python:3
COPY .  /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh
# ENtrypoint vai chamar um script bash que faz o que precisa fazer para iniciar a aplicação
ENTRYPOINT ["/docker-entrypoint.sh"]
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

