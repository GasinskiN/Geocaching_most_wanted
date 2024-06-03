# Użyj obrazu bazowego Pythona
FROM python:3.9

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki aplikacji do kontenera
COPY . .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Otwórz port 5000, na którym będzie działać aplikacja Flask
EXPOSE 5000

# Uruchom aplikację Flask
CMD ["flask", "run", "--host=0.0.0.0"]
