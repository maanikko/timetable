#### ***Lukujärjestys - äppi***

##### Työn aihe ja kuvaus

Tämä on komentorivipohjainen ohjelma, joka mallintaa lukujärjestystä. Ohjelmassa on myös mahdollista lisätä muistutuksia, joko jatkuvia tai tietylle päivälle tulevia muistutuksia. Lukujärjestys – ominaisuuden tarvitsema data (aikataulut) pitää käyttäjän itse tallentaa tekstitiedostoihin. Muistutuksien tallentaminen ja muut siihen liittyvät toiminnot taas hoituvat automaattisesti itse ohjelmassa.

##### Työn ratkaisuperiaate

Aloitin projektin suunnittelemalla ohjelman tärkeimmät funktiot. Tarkoitukseni oli, että ohjelma olisi jaettu mahdollisimman moneen aliohjelmaan. Tämä siksi, että koodi pysyisi mahdollisimman yksinkertaisena sekä samaa toiminnallisuutta voidaan käyttää monessa eri paikassa kutsumalla vain tiettyä funktiota.

##### Ohjelman rakenne
###### main.py
*Ulkoiset kirjastot*
```python
import json #Pystytään tallentamaan JSON dataa suoraan teksitiedostoon
import os 
import datetime import datetime #Mahdollistaa päivämäärien käsittelyn datetime olioina
```

*Funktiot*
```python
def print_red(text):
def print_green(text):
```
Näiden funktioiden avulla voidaan tulosteiden väriä muuttaa.

```python
def serialize_value(obj):
```
Serialisoi datan eli muuntaa objektin (tässä tapauksessa sanakirjan) eri muotoon, jotta se olisi helpompi tallentaa tiedostoon.

```python
def read_schedule_from_file(file_path):
```
Lukee kurssin aikataulut teksitiedostosta ja palauttaa listan sanakirjoja(dict). Jokainen sanakirja vastaa yhtä kurssin "tuntia".

```python
def find_classes_for_date(folder_path,target_date):
```
Etsii kaikista tekstitiedostoista tietyssä hakemistossa tietoja "tunneista" kohdepäivänä. Kutsuu funktiota **read_schedule_from_file**. Palauttaa listan kohdepäivänä olevista tunneista


```python
def print_target_date_classes(target_date):
```
Tulostaa kohdepäivän tunnit(jos on). Kutsuu funktiota **find_classes_for_date**.

```python
def write_notes():
```
Kirjoittaa muistutuksia tiedostoon ”notes.txt”.

```python
def read_notes_for_date(target_date):
```

Lukee muistutukset tekstitiedosta ja palauttaa listan sanakirjoja(dict). Jokainen sanakirja vastaa yhtä kurssin muistutusta.
```python
def find_notes_for_date(target_date):
```
Etsii kaikista tekstitiedostoista tietyssä hakemistossa tietoja "tunneista" kohdepäivänä. Kutsuu funktiota **read_notes_from_file.** Palauttaa listan kohdepäivänä olevista tunneista.

```python
def print_target_date_note(target_date):
```
Tulostaa kohdepäivän muistutukset (jos on). Kutsuu funktiota **find_notes_for_date**.

```python
def main():
```
Pääohjelma. Vastaa komentokehote pohjaisesta käyttöliittymästä.
######  notes.txt
Toimii muistutuksien tietokantana
###### lukujarjestys.bat
```batch
@echo off
python3 'main.py'
```
Batch tiedosto, joka ajaa ohjelman main.py. Suorittaa ohjelman pääohjelman käyttäjän klikkatessa kyseistä tiedostoa. Voi tehdä batch tiedostosta pikakuvakkeen esimerkiksi työpöydälle.

##### Ohjeet ohjelman käyttäjälle
###### Kurssien aikataulujen lisääminen
1. Mene opinto-oppaaseen kurssin sivulle
2. Kopio opinto-oppaasta kurssin aikataulut
3. Tee tekstitiedosto kurssin nimellä (esim. 'Ohjelmoinnin_perusteet_LUENNOT.txt')
4. Lisää kyseiseen tekstiedostoon kurssin aikataulut (Huom. muoto)

Huomioi, että kurssin, että kurssin aikataulut täytyy olla seuraavassa muodossa: 
```txt
[viikonpäivä] [päivämäärä] [alkuaika-loppuaika] [muut tiedot]

ESIMERKKI
ti 05.12.2023 10:15-12:00 Etäopetus, https://utu.zoom.us/j/64614152809
ti 12.12.2023 12:15-14:00 Etäopetus, https://utu.zoom.us/j/64614152809
...
```
Jos kurssin aikataulut kopioi Turun yliopiston opinto-oppaasta (opas.peppi.utu.fi), on aikataulut valmiiksi oikeassa muodossa. Jos omassa oppilaitoksessa aikataulut erilaisessa muodossa, täytyy joko ohjelman funktiota `read_schedule_from_file()` muuttaa(todennäköisesti helpoin tapa) tai vaihtoehtoisesti muokata aikataulujen muoto ennen tekstitiedostoon lisäämistä vastaamaa yllä kuvattua muotoa.
###### Ohjelman suorittaminen
*Windows*
Ohjelma voidaan suorittaa käyttäen hyväksi batch tiedostoa 'lukujarjestys.bat'. Tiedostoa klikatessa ohjelma avaa komentokehotteen ja suorittaa ohjelman. Batch tiedostosta voi myös tehdä pikakuvakkeen ja lisätä se esimerkiksi työpöydälle.

Vaihtoehtoisesti ohjelma voidaan suorittaa komentorivillä käyttäen komentoa :
```batch
python3 'path\to\main.py' 
```

Huom. python täytyy olla asennettuna tietokoneelle

*Linux*
Voit suorittaa ohjelman suoraan komentoriviltä käyttäen oman distribuution komentoja. Yleisimmissä distribuutiossa komento näyttää seuraavalta:
```batch
python3 'path/to/main.py' 
```

*MacOS*
Voit suorittaa ohjelman suoraan komentoriviltä käyttäen komentoa:
```batch
python3 'path/to/main.py' 
```

###### Muistutuksien lisääminen

![[Pasted image 20231220175651.png]]

Jatkuva muistutus tulee näkyviin aina kun näytetään muistutuksia kun taas tietyn päivän muistutukset tulevat näkyviin jos tarkastellaan saman päivän muistutuksia.

##### Kehitysideoita
Muistutukset pitää tällä hetkellä poista manuaalisesti tiedostosta 'notes.txt'. Tämän voisi totetuttaa sekä automaattisena muistutuksien poistamisena että komentorivikehotteen kautta poistamisena.

Ohjelmaan voisi myös kehittää siten, että se automaattisesti hakisi opinto-oppaasta tietyn kurssin tiedot linkin perusteella.

Ohjelmaan voisi myös lisätä graafisen käyttöliittymän.


