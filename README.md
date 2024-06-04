## Uruchomienie aplikacji:
- Przejdź do katalogu głównego aplikacji: `GEOCACHING_MOST_WANTED`
- Wykonaj polecenie `docker compose build`
- Uruchom aplikację za pomocą polecenia `docker-compose up`
- Serwer działa na: `https://localhost`

## Dokumentacja API:
- Dokumentacja jest zaimplementowana narzędziem "swagger"
- Dokumentację można otworzyć pod adresem: `https://localhost/apidocs`

## Uwagi:
- Uruchomienie aplikacji poleceniem `flask run` nie spowoduje obsługi protokołu HTTPS.
- Brak obsługi protokołu HTTPS uniemożliwi dostęp do geolokalizacji na urządzeniu mobilnym, co skutkuje brakiem funkcjonalności rozgrywki.