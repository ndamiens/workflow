[example uml output](https://kroki.io/plantuml/svg/eNp1UEESgyAMvPuKTE_l4BP0Kw6j0TK10AGsfX4hGSG104O4SXaTTTyOUdtlRbgsGId5dZu_gA5QosZ_U4JeY2Hk4EzYdcTagyJJ2bVhfQay8DBvyqe_TD-3OBg7uBdaKou4uVrECcimgq7rheuCoG17ICJ7Uawi61VEixyAJdlfmrR4nAzaGA4hdylKXrAgMY4mNL99SErb5-ffsFpLBzn5OGeoY75b-lgzOndPDFUz0tJRJZ08qMCsmo014YaT-gD6C77P)


<div hidden>
```
@startuml firstDiagram

rectangle "get_flour" as get_flour
rectangle "get_salt" as get_salt
rectangle "get_water" as get_water
rectangle "wait" as wait
rectangle "mix" as mix
rectangle "put_in_oven" as put_in_oven
(need flour) ==> get_flour
get_flour --> (need_water)
(need_salt) ==> get_salt
get_salt --> (wait_ingredients)
(need_water) ==> get_water
get_water --> (need_salt)
(wait_ingredients) ==> wait
wait --> (wait_ingredients)
wait --> (mix_ingredients)
(mix_ingredients) ==> mix
mix --> (cooking)
mix --> (need_salt)
(cooking) ==> put_in_oven
put_in_oven --> (finished)

@enduml
```
</div>

![](firstDiagram.svg)