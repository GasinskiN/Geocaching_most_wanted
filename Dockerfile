FROM python:3.9-slim

# Ustawienie zmiennej środowiskowowej, aby `python` i `pip` nie używały bufora
ENV PYTHONUNBUFFERED=1

# Utwórzenie katalogu dla aplikacji
RUN mkdir /app
WORKDIR /app

# Kopiowanie pliku requirements.txt do katalogu /app/
COPY requirements.txt /app/

# Instalacja zależności
RUN pip install -r requirements.txt

# Kopiowanie zawartości katalogu lokalnego do obrazu
COPY . /app/

# Otwarcie portu 5000 dla aplikacji Flask
EXPOSE 5000

# Polecenie do uruchomienia aplikacji za pomocą Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
