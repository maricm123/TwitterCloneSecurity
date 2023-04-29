Skontati koji od security sistema za prijavu i login koristiti


Potrebne stvari za security za projekat:
https://docs.djangoproject.com/en/4.1/topics/security/


ToDo lista:
1. Prvo odraditi Registraciju obe vrste profila sa JWT auth (biznis i obican profil) pa onda videti sta se pokrilo od ovih pod 1.1
Mora da prati sve ovo :
    1.1 Validaciju podataka
        ● Sprečiti relevantne Injection napade;
        ● Sprečiti XSS napade;
        ● Izvršiti validaciju podatka, koristeći kriterijume validacije definisane po najboljim
        praksama za pisanje bezbednog koda.

2. Onda odraditi prijavu (login) isto sa jwt auth (simple jwt) pa videti sta se pokrilo sve pod ovim za 1.1

- Onda kada se ovo dvoje zavrsi videti da li se jos nesto pokrilo i sta jos moze da se doradi da bi se pokrilo iz IB




3. Postavljanje twita
 - Napraviti model (Tweet) - Moze sadrzati tekst, sliku ili oba 
 - Podaci - Tekst, slika, datum postavljanja, ko je postavio (Moze i biznis i obican korisnik)


SUPER USER
mihailomaric001@gmail.com
mihailo



26.03 - nastaviti i usavrsiti login kod obe role.
Stao si kod BussinesUserLoginView


02.04 - napraviti jedan login i tu da se prepoznaje koji je type od usera i to ce se na frontu setovati u vuex
i na osnovu toga ce se prikazivati odredjene stranice - uradjeno


08.04 - napraviti na frontu da radi sve sto se tice logina i sign up-a 
- Login radi za obe role
- Sign up radi za obe role

- dalje istraziti sta da se radi za: 
      Omogućiti mehanizme za potvrdu naloga, oporavak lozinke i promenu lozinke


09.04
- Odraditi na frontu sto se tice rola, prikazivanje odredjenih stvari na osnovu role - DONE - (izvuce se rola iz localStorage i na osnovu toga se prikazuje)
- Odraditi mail da bude unique(imam gresku kada radim sign-up sa istim emailom, hendlati to na neki nacin) - DONE - (UNIQUE VALIDATOR)
- odraditi logout na beku i frontu (zapisati kako funkcionise logout i sta se desava sa tokenima u mom primeru) - DONE -
- krenuti na beku odradjivati prikaz profila oba korisnika i izmena profila
- probati namestati i skontati kako ide slanje tokena uz zahtev i na beku namestati permision_class DONE (na primeru logouta, back i front)



17.04
Postavljanje tweet-a (običan i biznis korisnik)
Tweet može da sadrži:
A. Tekstualni sadržaj
B. Sliku
C. Kombinaciju prethodna dva tipa sadržaja


19.04
Treba nasttaviti raditi na dashboardu
- prikazati sve tweetove za ulogovanog korisnika (datum namestiti da bude normalan)
date and time format from serialier looks like this 2023-04-23T11:49:02.751420Z
How i can get normal format like 2023-04-23
Django serializer


- dugme za dodavanje tweeta u user-profile i u dashobbard komponentama - DONE
- stranica za dodavanje tweeta - DONE



23.04
- next todos
- odraditi detalje tweeta (razmisliti da li praviti posebno detalje kad user otvara svoj tweet pa da moze da edituje
ili raditi direktno u ovome TweetDetail)
        - u viewu raspoznajem da li ima permisiju ili ne na beku
        - onda na frontu gadjam current user api i uporedjujem ga sa tweet userom i onda mu ili dajem buttone za edit i delete ili ne
DONE




29.04

- odraditi lajkovanje tweeta
- videti views_profile MyProfileView objasnjenje sta treba uraditi (ostao update da se uradi i da se prikaze to na frontu)




30.04







- tek posle svega ovoga fokusirati se na izmenu lozinke itd, jer mozda i realno nije vezano za ove ostale
serailizere i viewe. 
https://medium.com/django-rest/django-rest-framework-change-password-and-update-profile-1db0c144c0a3?source=publication_recirc-----eb1b53ac6d35----3----------------------------