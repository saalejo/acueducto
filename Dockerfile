FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /acueducto
WORKDIR /acueducto
COPY . /acueducto/
COPY ./acueducto/settings-prod.py /acueducto/acueducto/settings.py
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 8080
CMD python manage.py runserver 0.0.0.0:8080