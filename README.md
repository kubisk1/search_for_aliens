# search_for_aliens

## Wstęp - cel i zakres systemu:

Celem projektu jest opracowanie i wdrożenie nowoczesnego systemu komunikacji z sondami kosmicznymi.

System ten będzie odpowiadał za:
- Utrzymywanie łącznościz sondami kosmicznymi, które poruszają się w przestrzeni kosmicznej i mają ograniczone okna komunikacyjne ze stacją naziemną.
- Odbieranie danych z sond kosmicznych.
- Przechowywanie danych w bazie.
- Wykrywanie zepsutych sond.

System będzie składał się z następujących komponentów:
- Interfejs służący do nawiązywania łączności z sondami, odbierania, przetwarzania i zapisywania danych w bazie, oraz wykrywania zepsutych sond.
- Baza danych w której zapisywane będą dane odebrane z sond kosmicznych.

## Opis ogólny systemu:
 
System będzie utrzymywał łączność z sondami kosmicznymi, które poruszają się w przestrzeni kosmicznej i mają ograniczone okna komunikacyjne ze stacją naziemną. Stacja Odbiorcza będzie odbierać sygnały z sond w czasie trwania okna komunikacyjnego. System będzie odbierać pakiety danych z wielu sond jednocześnie. Po odebraniu całego pakietu danych, będą one zapisywane i przechowywane w bazie. System będzie miał zdolność do wykrywania zepsutych sond i zerwaniu z nimi komunikacji po stwierdzeniu awari

## Przypadki użycia - use case diagrams:
  [![Zrzut-ekranu-2024-03-25-o-23-07-06.png](https://i.postimg.cc/Jn9jH5Gw/Zrzut-ekranu-2024-03-25-o-23-07-06.png)](https://postimg.cc/dkjhzd2n)

  [![Zrzut-ekranu-2024-03-25-o-23-08-03.png](https://i.postimg.cc/x1C7R960/Zrzut-ekranu-2024-03-25-o-23-08-03.png)](https://postimg.cc/tYK2RG0f)

  [![Zrzut-ekranu-2024-03-25-o-23-08-59.png](https://i.postimg.cc/HWF4KdWY/Zrzut-ekranu-2024-03-25-o-23-08-59.png)](https://postimg.cc/yWXZ3qSt)

## Scenariusz użycia:
[![Zrzut-ekranu-2024-03-25-o-23-10-09.png](https://i.postimg.cc/Prcc2B9Y/Zrzut-ekranu-2024-03-25-o-23-10-09.png)](https://postimg.cc/jLHZjksS)

  

  
