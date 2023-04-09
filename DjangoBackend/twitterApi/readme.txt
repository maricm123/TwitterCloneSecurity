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


- tek posle svega ovoga fokusirati se na izmenu lozinke itd, jer mozda i realno nije vezano za ove ostale
serailizere i viewe. 
https://medium.com/django-rest/django-rest-framework-change-password-and-update-profile-1db0c144c0a3?source=publication_recirc-----eb1b53ac6d35----3----------------------------





*** KAKO FUNKCIONISE LOGOUT OVDE ***
SIMPLE_JWT = {
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True
}|------------|-----------------------------------------------------|
| ACTION     | DESCRIPTION                                         |
|------------|-----------------------------------------------------|
|  LOGIN     | - Refresh token is added automaticaly to            |
|            | outstanding tokens                                  |
|------------|-----------------------------------------------------|
|  LOGOUT    | - You should add refresh token to the blacklisted   |
|            | tokens manually.                                    |
|------------|-----------------------------------------------------|
|  REFRESH   | - Old refresh token is added automaticaly to        |
|            | blacklisted tokens.                                 |
|            | - You should add new refresh token to the           |
|            | outstanding tokens                                  |
|------------|-----------------------------------------------------|

REFRESH_TOKEN_LIFETIME: This sets the amount of time that a refresh token is valid for. In this case, refresh tokens will be valid for 15 days.

ROTATE_REFRESH_TOKENS: When this is set to True, each time a refresh token is used to obtain a new access token, the refresh token will be rotated
(i.e. a new refresh token will be issued). This is a security measure to prevent long-term use of the same refresh token.

BLACKLIST_AFTER_ROTATION: When this is set to True, after a refresh token has been rotated,
the previous refresh token (which is no longer valid) will be added to a blacklist.
This ensures that even if a previous refresh token is somehow obtained by an attacker, it cannot be used to obtain a new access token.


***Outstanding tokens*** refer to valid and authorized tokens that have been issued to users and have not yet expired or been revoked. 
These tokens allow users to access certain resources or perform certain actions based on their privileges.

On the other hand, ***blacklisted tokens*** are tokens that have been revoked or invalidated,
either because they have been compromised, or because the associated user's access rights have been changed or terminated.
***Blacklisted tokens*** are no longer valid and cannot be used to access any resources or perform any actions.

In summary, ***outstanding tokens*** are valid and authorized tokens that allow users to access resources,
while ***blacklisted tokens*** are invalid and unauthorized tokens that have been revoked or invalidated.














{
"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MjM0MjkwOSwiaWF0IjoxNjgxMDQ2OTA5LCJqdGkiOiJkNGJjZjM0OWIyNjg0NWI2YTc0ZTI5NTFlZGJhMTIzNiIsInVzZXJfaWQiOjI1fQ.UWAP6g6oUMD5RaB8xHhq1g9sAQmVw3EhToTPYqw_zus"
}

(XSS ATTACKS)
Additionally, storing tokens in localStorage also exposes them to Cross-Site Scripting (XSS) attacks.
An attacker could exploit a vulnerability in your application to execute malicious code in a user's browser,
which could then access and steal the tokens from localStorage.

To mitigate these risks,
it is recommended to store tokens in an HTTP-only cookie with the secure flag set.
This ensures that the tokens are only accessible via HTTP requests,
and cannot be accessed by JavaScript running on the page.
https://www.procoding.org/jwt-token-as-httponly-cookie-in-django/


























Yes, you can set tokens to HTTP cookies in your Vue.js app. This is a common approach to handling authentication and authorization in web applications.

To set tokens to HTTP cookies in Vue.js, you can use the vue-cookies package. This package provides an easy-to-use API for setting and retrieving cookies in Vue.js.


// Set the token cookie
this.$cookies.set('token', 'your_token_value', { expires: '1d' })
In the example above, we import the vue-cookies package and then use the Vue.use() method to install it. We then set the token cookie using the $cookies.set() method. The expires option is used to specify the cookie's expiration time.

To retrieve the token cookie, you can use the $cookies.get() method:

kotlin
Copy code
// Get the token cookie
const token = this.$cookies.get('token')
In the example above, we use the $cookies.get() method to retrieve the token cookie.

Note that setting tokens to HTTP cookies alone is not enough to fully secure your application. You should also implement other security measures, such as using HTTPS and validating user input, to protect your application from attacks.