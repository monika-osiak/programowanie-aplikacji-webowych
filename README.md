# Mendeley clone
## Repozytorium projektu z przedmiotu *Programowanie aplikacji mobilnych i webowych*
Monika Osiak, 291094

## P1
### Polecenie
Opracowanie formularza rejestracyjnego dla nowych użytkowników. Formularz musi pozwalać na walidowanie wszystkich pól na bieżąco. Kod JavaScript, HTML i CSS muszą być od siebie odesparowane. Komunikaty błędów muszą być tworzone dynamicznie przez kod JS. Polę login użytkownika będzie sprawdzane pod kątem dostępności asynchronicznie. Dane do rejestracji będą przesyłane do na zewnętrzny serwer. Kod HTML i CSS musi przechodzić walidację.
#### Deadline: 28.10.2019
#### Jak testować?
```
to do: dodać listing kodu na uruchomienia na Dockerze
also, wypadałoby sprawdzić, czy to w ogóle działa na Dockerze
```

W części backendowej zahardkodowane są dwa loginy, które są zajęte:
* osiakm
* admin

W tych dwóch przypadkach pojawi się komunikat o braku dostępności nazwy.
Pozostałe loginy mają działać.