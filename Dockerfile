FROM python:3.9.16-bullseye

COPY requirements.txt /app/

WORKDIR /app

RUN pip install --force-reinstall --no-cache-dir --upgrade -r /app/requirements.txt

COPY /freebooksapi .

CMD ["uvicorn", "main:FREEBOOKSAPI", "--host", "0.0.0.0", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]