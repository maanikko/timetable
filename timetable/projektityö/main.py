import json
import os
from datetime import datetime
def print_red(text):
    #Tulostaa kurssin nimen punaisella powershellissä
    #Kommentoi pois jos eri komentokehote kuin powershell Huom. Tarvitsee muutoksia myös pääohjelmassa
    os.system(f'powershell Write-Host "{text}" -ForegroundColor Red')

def print_green(text):
    #Tulostaa kurssin nimen punaisella powershellissä
    #Kommentoi pois jos eri komentokehote kuin powershell Huom. Tarvitsee muutoksia myös pääohjelmassa
    os.system(f'powershell Write-Host "{text}" -ForegroundColor Green')

#Jotta voidaan kirjoittaa dictionaryt tiedostoon
def serialize_value(obj):
    """
    Serialisoi datan.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, bool):
        return str(obj)
    else:
        raise TypeError("Unsupported type for serialization")

def read_schedule_from_file(file_path):
    """
    Lukee kurssin aikataulut teksitiedostosta ja palauttaa listan sanakirjoja(dict). Jokainen sanakirja vastaa yhtä kurssin "tuntia".
    """
    # Tyhjä lista tallentamaan kurssin aikatauluja
    schedules = []
    
    # Avataan tiedosto lukutilassa
    with open(file_path, 'r') as file:
        for line in file:
            #Splitataan rivi neljään eri muuttujaan
            parts = line.strip().split(' ', 3)
            day, date, timings, other_info = parts
            start_time, end_time = timings.split('-')
            formatted_date = datetime.strptime(f"{date} {start_time}", '%d.%m.%Y %H:%M')
            
            # Luodaan sanakirja jokaista kurssin "tuntia" varten
            schedule_entry = {
                'date': formatted_date,
                'start_time': start_time,
                'end_time': end_time,
                'other_info': other_info.strip()
            }
            
            
            schedules.append(schedule_entry)

    return schedules

def find_classes_for_date(folder_path, target_date):
    """
    Etsii kaikista tekstitiedostoista tietyssä hakemistossa tietoja "tunneista" kohdepäivänä. Palauttaa listan kohdepäivänä olevista tunneista
    """
    
    # TYhjä lista tallentamaan kohdepäivän kurssien nimet ja niiden aikataulut
    matching_courses = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            # Ottaa kurssin nimen talteen tiedoston nimestä ja rakentaa absoluuttisen polun tiedostoon
            course_name = os.path.splitext(filename)[0]
            file_path = os.path.join(folder_path, filename)
            # Lukee aikataulut tiedostosta
            schedules = read_schedule_from_file(file_path)
            # Tarkistaa jos jokin kurssin aikatauluista on kohdepäivällä
            for schedule in schedules:
                if schedule['date'].date() == target_date.date():
                    matching_courses.append((course_name, schedule))
    return matching_courses


def print_target_date_classes(target_date):
    """
    Tulostaa kohdepäivän tunnit (jos on).
    """
    # Tiedostopolku hakemistoon jossa kaikki kurssien aikataulu tiedostot
    folder_path = "cources"

    # Etsii kohdepäivällä olevat kurssien "tunnit"
    matching_courses = find_classes_for_date(folder_path, target_date)

    # Tulostaa kohdepäivällä olevat "tunnit"
    if not matching_courses:
        print_red(f"{target_date} ei ole tunteja.")
    else:
        print_green(f"{target_date} olevat tunnit:")
        for course_name, schedule in matching_courses:
            print()
            print_red(f'Kurssi: {course_name}')
            print(f'{schedule["start_time"]}-{schedule["end_time"]}: ', end='')
            print(f'{schedule["other_info"]}')
            print()


def write_notes():
    """
    Kirjoittaa muistutuksen tiedostoon "notes.txt"
    """

    # Tyhjä lista tallentamaan muistuksia sanakirjoina
    notes = []

    while True:
        print_green("Valitse toiminto:")
        print("1. Lisää jatkuva muistutus")
        print("2. Lisää muistutus tietylle päivälle")
        print("0. Mene takaisin")
        try:
            choice3 = int(input("Valintasi: "))
        except ValueError:
            print_red(f"Valinnan tulee olla kokonaisluku")
            continue
        
        if choice3 == 0:
            break
        try:
            note = str(input("Muistutus: "))
        except ValueError:
            print_red(f"Muistutuksen tulee olla merkkijono")
            continue
        
        if choice3 == 1:
            notes_entry= {
                'date': False,
                'note': note
            }
            
        elif choice3 == 2:
            while True:
                try:
                    date_note_input = input("Anna muistutuksen päivämäärä(PP.KK.VVVV):")
                    date_note = datetime.strptime(date_note_input, '%d.%m.%Y')
                except ValueError:
                    print_red("Päivmäärä väärässä muodosssa")
                    continue
                notes_entry= {
                    'date': date_note,
                    'note': note
                }
                break
    
        notes.append(notes_entry)

    # Kirjoittaa tiedostoon notes.txt muistutukset
    with open("notes.txt","a") as f2:
        for dict_note in notes:
            serialisable_data = json.dumps(dict_note, default=serialize_value)
            f2.write(json.dumps(serialisable_data)+"\n")
        

def read_notes_from_file():
    """
    Lukee muistutukset teksitiedostosta ja palauttaa listan sanakirjoja(dict). Jokainen sanakirja vastaa yhtä kurssin muistutusta.
    """
    dict_list_notes = []
    with open("notes.txt") as f3:
        for line in f3:
            line = line.strip()
            try:
                dictionary = json.loads(line.strip())
                dict_list_notes.append(json.loads(dictionary))
            except json.JSONDecodeError:
                print_red(f"Varoitus: Väärä JSON muoto rivillä: {line}. Muistutuksen lukemisessa ongelmia. Tarkista tiedosto 'notes.txt'.")
    # Muunta stringin datetime olioksi
    for i in dict_list_notes:
        if i['date'] != False:
            date = i['date']
            i['date'] = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    return dict_list_notes

def find_notes_for_date(target_date):
    """
    Etsii kaikista tekstitiedostoista tietyssä hakemistossa tietoja "tunneista" kohdepäivänä. Palauttaa listan kohdepäivänä olevista tunneista
    """
    
    # Tyhjä lista tallentamaan kohdepäivön muistutukset
    matching_notes = []
    
    
    notes = read_notes_from_file()
    # Tarkistaa jos jokin muistutuksista on kohdepäivälle tai jatkuvia muistutuksia
    for notes_dict in notes:
        if (notes_dict['date'] == False) or (notes_dict['date'].date() == target_date.date()):
            matching_notes.append(notes_dict)
    return matching_notes

def print_target_date_notes(target_date):
    """
    Tulostaa kohdepäivän muistutukset (jos on).
    """
    c = 0
    # Etsii kohdepäivällä olevat muistutukset
    matching_notes = find_notes_for_date(target_date)

    # Tulostaa kohdepäivällä olevat "tunnit"
    if not matching_notes:
        print_green(f"Ei muistutuksia päivälle {target_date}.")
    else:
        print_green(f"Muistutukset päivälle {target_date}:")
        for notes in matching_notes:
            c += 1
            print()
            print(f"{c}. {notes['note']}")
            print()
    


def main():
    while True:
        print_red("YLIOPISTOKALENTERI")
        print_green("Valitse toiminto:")
        print("1. Näytä tämän päivän kurssit ja muistutukset")
        print("2. Näytä kohdepäivän kurssit ja muistutukset")
        print("3. Muistutukset")
        print("0. Poistu")
        
        try:
            choice = int(input("Valintasi: "))
        except ValueError:
            print_red(f"Valinnan tulee olla kokonaisluku")
            continue
        
        if choice == 1:
            target_date = datetime.now()
            print_target_date_classes(target_date)
            print_target_date_notes(target_date)
            input("Paina mitä tahansa näppäintä jatkaaksesi eteenpäin...")
        
        elif choice == 2:
            while True:
                try:
                    target_date_input=input("Anna kohdepäivä (PP.KK.VVVV): ")
                    if (target_date_input == "tänään"):
                        target_date = datetime.now()
                    else:
                        target_date = datetime.strptime(target_date_input, '%d.%m.%Y')
                except ValueError:
                    print_red("Päivmäärä väärässä muodosssa!")
                    continue
                break
            print_target_date_classes(target_date)
            print_target_date_notes(target_date)
            input("Paina mitä tahansa näppäintä jatkaaksesi eteenpäin...")
        
        elif choice == 3:
            while True:
                print_green("Valitse toiminto:")
                print("1. Näytä tietyn päivän muistutukset")
                print("2. Lisää muistutus:")
                print("0. Mene takaisin")
                try:
                    choice2 = int(input("Valintasi: "))
                except ValueError:
                    print_red(f"Valinnan tulee olla kokonaisluku")
                    continue
                if choice2 == 1:
                    while True:
                        try:
                            target_date_input=input("Anna kohdepäivä (PP.KK.VVVV): ")
                            if (target_date_input == "tänään"):
                                target_date = datetime.now()
                            else:
                                target_date = datetime.strptime(target_date_input, '%d.%m.%Y')
                        except ValueError:
                            print_red("Päivmäärä väärässä muodosssa!")
                            continue
                        break
                    print_target_date_notes(target_date)
                    input("Paina mitä tahansa näppäintä jatkaaksesi eteenpäin...")
                elif choice2 == 2:
                    write_notes()
                elif choice2 == 0:
                    break

                

        elif choice == 0:
            break

if __name__ == "__main__":
    main()

