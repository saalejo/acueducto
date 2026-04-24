FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir /acueducto
WORKDIR /acueducto
COPY . /acueducto/
COPY ./acueducto/settings-prod.py /acueducto/acueducto/settings.py
RUN pip install --trusted-host pypi.python.org --default-timeout=120 -r requirements.txt
EXPOSE 8080
CMD ["gunicorn", "acueducto.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "2", "--worker-class", "gthread", "--threads", "2"]