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
i na osnovu toga ce se prikazivati odredjene stranice