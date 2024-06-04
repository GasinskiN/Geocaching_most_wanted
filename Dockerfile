# Użyj oficjalnego obrazu Python jako bazowego
FROM python:3.9-slim

# Ustaw zmienną środowiskową, aby `python` i `pip` nie używały bufora
ENV PYTHONUNBUFFERED=1

# Utwórz katalog dla aplikacji
RUN mkdir /app
WORKDIR /app

# Skopiuj plik requirements.txt do katalogu roboczego
COPY requirements.txt /app/

# Zainstaluj zależności
RUN pip install -r requirements.txt

# Skopiuj zawartość katalogu lokalnego do obrazu
COPY . /app/

# Otwarcie portu 5000 dla aplikacji Flask
EXPOSE 5000

# Polecenie do uruchomienia aplikacji za pomocą Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
