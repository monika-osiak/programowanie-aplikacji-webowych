# Mendeley clone
## Repozytorium projektu z przedmiotu *Programowanie aplikacji mobilnych i webowych*
Monika Osiak, 291094

## P1
### Polecenie
Opracowanie formularza rejestracyjnego dla nowych użytkowników. Formularz musi pozwalać na walidowanie wszystkich pól na bieżąco. Kod JavaScript, HTML i CSS muszą być od siebie odesparowane. Komunikaty błędów muszą być tworzone dynamicznie przez kod JS. Polę login użytkownika będzie sprawdzane pod kątem dostępności asynchronicznie. Dane do rejestracji będą przesyłane do na zewnętrzny serwer. Kod HTML i CSS musi przechodzić walidację.
#### Deadline: 28.10.2019
#### Jak testować?
```
docker build -t flask:latest .
docker run -d -p 5000:5000 flask:latest
```

Następnie w dowolnej przeglądarce proszę wejść na stronę `http://0.0.0.0:5000/register` i wypełnić formularz.

W części backendowej zahardkodowane są dwa loginy, które są zajęte:
* osiakm
* admin

W tych dwóch przypadkach pojawi się komunikat o braku dostępności nazwy.
Pozostałe loginy mają działać.

## P2
### Polecenie
Opracowanie modułu służącego do bezpiecznego logowania i wylogowywania użytkownika. Moduł logowania otrzymuje od użytkownika hasło i login – w przypadku poprawnych danych generowany jest identyfikator sesji. Dane sesyjne przechowywane są w bazie danych Redis. Należy opracować formularz pozwalający na przechowywanie przez użytkownika plików PDF w systemie. Pliki PDF powinny być dostępne do pobrania i serwowane przez bezstanową aplikację. Należy wykorzystać JWT z krótką datą ważności.
#### Deadline: 25.11.2019
#### Jak testować?
Uruchomienie poleceń 
```
docker-compose build
docker-compose up
```
pozwoli postawić projekt. O ile dockery z moimi aplikacjami działają, pojawia się problem połączenia z Redisem - zabrakło mi czasu aby go rozwiązać.

Dlatego, jeśli to mozliwe, najlepiej jest sprawdzić działanie projektu uruchamiając ręcznie wszystkie trzy komponenty:
```
python3 auth/auth_app.py
python3 file/file_app.py
redis-server
```

Wstępna wersja aplikacji jest postawiona na [Heroku](https://mendeley.herokuapp.com). Działa tam logowanie i rejestracja uzytkowników, nie działa dodawanie plików - głównie ze względu na to, ze druga z aplikacji nie została jeszcze postawiona na Heroku.

## P3
### Polecenie
Opracowanie usługi sieciowej i klienta na urządzenie przenośne. Usługa sieciowa musi pozwalać na:
* dodawanie pozycji bibliograficznej,
* listowanie pozycji bibliograficznych,
* usuwaniu pozycji bibliograficznych,
* podpinaniu i odpinaniu plików przy pozycji bibliograficznej,
* dodawanie, pobieranie i usuwanie plików.

Usługa sieciowa powinna zwracać powiązane elementy (HATEOAS). Należy zwrócić uwagę na wykorzystanie odpowiednich metod HTTP oraz zwracanie poprawnych kodów statusu.

Aplikacja kliencka może być zrealizowana jako aplikacja dla Android czy iOS, jako aplikacja progresywna (PWA) albo jako aplikacja internetowa dostosowana do urządzeń mobilnych (wymagany responsywny interfejs użytkownika).
#### Deadline: 16.12.2019

## P4
### Polecenie
Umożliwienie autoryzacji użytkownika poprzez serwer `auth0.com` i OAuth 2.0. Należy też rozszerzyć aplikację o powiadomienia ze strony serwera o dodaniu nowych publikacji. Powiadomienia powinny pojawiać się we wszystkich aplikacjach, w których zalogowany jest użytkownik.
#### Deadline: 13.01.2020

## P5
### Polecenie
Opracowanie asynchronicznego modułu przetwarzającego pliki PDF. Po przesłaniu pliku PDF do aplikacji powinno powstać nowe zlecenie w kolejce zadań. Celem tego zlecenia jest odczytanie pliku PDF przez aplikację typu `pdftotext` w celu wyodrębnienia z niej danych o artykule (np. uniwersalnego numery identyfikacyjnego publikacji DOI) i automatyczne utworzenie pozycji bibliograficznej w systemie.
#### Deadline: 20.01.2020