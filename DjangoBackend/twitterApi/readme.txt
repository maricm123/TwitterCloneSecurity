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
mihailomaric@gmail.com
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

- stao sam kod toga da moram promeniti lozinku za mihailo usera jer nije hashovana. - DONE (napravljane novi user, nisam uspeo drugacije)

- nastaviti sa lajkovanje tvitera
- ostao update da se uradi za usera (to sve uraditi i na frontu) - MyProfileView


02.05
- lajkovanje tvitera - DONE
- liked_by lista na tweet detail - DONE
- Tweet-ove treba sortirati opadajuće prema datumu i
vremenu objave. - DONE
- update da se uradi za usera (to sve uraditi i na frontu) - MyProfileView


03.05 
za uraditi
- Podešavanje privatnosti profila (običan i biznis korisnik) - DONE
- ostao update da se uradi za usera (to sve uraditi i na frontu) - MyProfileView - DONE

04.05
- button user profile na tweet detail ubaciti u funckiji (pozivamo sa beka getovanje samo ussera) - DONE
- zapracivanje profila - videti u specifikaciji 
        razlozeno na sitnije:
                -model napisati ( sta ubaciti u usera za followerse i koga follovuje) - DONE
                - napisati viewe (za request followa itd) - DONE

05.05 
- prelistati da li moze da se krene sa front delom za zapracivanje usera
- zapracivanje usera na frontu:

        
- izlistavanje home feeda na osnovu ljudi koji te prate itd itd (ovo mozda ostaviti za kasnije kad se bude moglo testirati na frontu)
- krenuti sa izradom front dela za zapracivanje usera
        - razlozeno na sitnije:

14.05
- odraditi zapracivanje usera na frontu ( follow User metoda ) - DONE
- odraditi dynamic za follow user button, znaci staviti requested ako se ceka odgovor
ili following ako smo ga zapratili, promeniti boje buttona) - DONE
Ovde sam stao, moram proveriti da li se user nalazi u listi usera koji ga vec prate ( mozda iz currentUsera videti da li vec prati
ovog usera kojeg zeli da zaprati ???????) - DONE
OVDE SAM STAO ! - DONE


+ stao sam da trebam da razradim casove u UserProfile, znaci pogledati da li je requeseted taj profil
(znaci u profilu usera koristim servis da izvadim follow request, i na osnovu toga vidim da li ima request za ovog usera iz currentUsera)
                - force atribut videti gde prosledjivati jer na osnovu njega cemo znati da li dolazi request accepted u follow metodu
                kod usera ili dolazi u tu metodu sa vec otkljucanim nalogom - DONE


+ u MyUserProfile namestiti da moze da se prihvati ili odbije zahtev za pracenje (saljem 1 ili 2, pogledati 
u serializeru) - znaci pored liste follow request staviti accept i reject
- DONE


19.05
- pogledati ostale casove i slucajeve i popraviit bugove
- urediti malo dizajn i podatke koji se trebaju dovesti



- Retweet (običan i biznis korisnik)
Korisnik može da retweet-uje svaki tweet kom može da pristupi. Kada to
odradi, retweet se tretira kao i svaki drugi tweet tog korisnika, ali sa naznakom
da je retweet. Mora se navesti ko je korisnik koji ga je originalno objavio.
Ukoliko je profil koji je originalno objavio tweet privatan i korisnik kom se
prikazuje retweet ne prati taj profil, potrebno je sakriti sadržaj retweet-a, ali ne
i ime osobe koja ga je objavila. - DONE
- home feed (tvitovi samo korisnika koje pratim) - DONE
- procitati specifikaciju bezbednosti i videti sta se treba uraditi da se unapredi


21.05
- odratiti retweet na frontu ( ubaciti dugme za retweet ) - DONE
- ubaciti da korisnik koji pristupa retweetu ne moze da vidi
 tweet ako ne prati korisnika koji je kreirao taj originalni tweet - DONE

- istraziti sta ide dalje za bezbednost
        pitati nekog
        pogledati videe
        
- sredjivati dizajn


- tek posle svega ovoga fokusirati se na izmenu lozinke itd, jer mozda i realno nije vezano za ove ostale
serailizere i viewe. 
https://medium.com/django-rest/django-rest-framework-change-password-and-update-profile-1db0c144c0a3?source=publication_recirc-----eb1b53ac6d35----3----------------------------




27.05:
- Potvrda naloga nakon registracije - uradio modele, radi se view - DONE

- Promena lozinke
        API:
           - view za kad se dobije mail da se posalje na taj mail token za reset lozinke - DONE
           - view da kad se dodje na stranicu za reset lozinke, ima dva polja koja kuca za reset lozinke - DONE
        Client:
           - view za forgot password gde kuca svoj email i na koji mu sse salje token - DONE
           - view sa dva polja gde kuca lozinku i to se salje na bek i resetuje lozinka - DONE




03.06 i 04.06:
+++Kontrolisanje pristupa endpoint-ima po RBAC modelu
        - Napraviti permissione za potrebe u projektu (Za biznisa i za ddefault usera) - DONE
        - Dodati ih u permission_classes u viewvima - DONE


- videti za lozinku (napraviti neki regex na beku ili frontu), zastiti lozinku itd - DONE


- pogledati sta treba uraditi za poslednji deo projekta

Zastita podataka:
