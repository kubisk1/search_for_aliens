Use case diagram

@startuml

left to right direction
actor Operator as "Operator Centrum Kontroli"
actor System as "System Stacji Odbiorczej"
rectangle "System Komunikacji z Sondami Kosmicznymi" {
  System -- (Wysyłanie Danych przez Sondę)
  System -- (Odbieranie Danych przez Stację Odbiorczą)
  (Odbieranie Danych przez Stację Odbiorczą) .> (Przetwarzanie Danych) : includes
  Operator -- (Monitorowanie Stanu Sond)
  Operator -- (Przeglądanie Danych)
  (Przetwarzanie Danych) .> (Przeglądanie Danych) : extends
}

@enduml