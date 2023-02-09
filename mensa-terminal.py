import json
import csv

class Mensa():

    def __init__(self):
        self.nome = "Mensa Dipartimento"
        self.indirizzo = "Via del corso, numero"
        self.prenotazioni = []
        self.menu_settimana = Menu()
        self.header = ['id', 'nome studente', 'cognome studente', 'matricola studente', 'giorno', 'pranzo', 'cena']

    def print_prenotazioni(self):

        if len(self.prenotazioni) == 0:
            print("\n------ Non sono presenti prenotazioni! ------")
        else:
            print("\n{:<3} | {:<15} | {:<20} | {:<18} | {:<10} | {:<30} | {:<30}".format(*self.header))
            print("--------------------------------------------------------------------------------------------------------------------------------------------------")
            for p in self.prenotazioni:
                print("{:<3} | {:<15} | {:<20} | {:<18} | {:<10} | {:<30} | {:<30}".format(p.id, p.nome_studente, p.cognome_studente, p.matricola_studente, p.giorno, str(p.pranzo), str(p.cena)))

    def export_prenotazioni(self):

        if len(self.prenotazioni) == 0:
            print("\n------ Non sono presenti prenotazioni! ------")
        else: 
            with open("prenotazioni.csv", "w") as w:
                writer = csv.writer(w)
                writer.writerow(self.header)
                writer.writerows(self.prenotazioni)
            
            print("\n------ Prenotazioni esportate con successo! ------")


class Prenotazione():
    
    id_prenotazione = 0

    def __init__(self, studente, giorno, pranzo, cena):
        self.id = self.id_prenotazione
        self.nome_studente = studente.nome
        self.cognome_studente = studente.cognome
        self.matricola_studente = studente.matricola
        self.giorno = giorno
        self.pranzo = pranzo
        self.cena = cena
        Prenotazione.id_prenotazione += 1

    def __iter__(self):
        return iter([self.id, self.nome_studente, self.cognome_studente, self.matricola_studente, self.giorno, self.pranzo, self.cena])

class Menu():

    def __init__(self):
        self.menu_settimana = self.read_menu()
    
    def get_menu_day(self, day):
        return self.menu_settimana[day]     

    def get_days_menu(self):
        days = []
        for day in self.menu_settimana:
            days.append(day)
        return days

    def read_menu(self):
        with open('src/menu.json', 'r') as f:
            data = json.load(f)
        return data

class Studente():

    def __init__(self, nome, cognome, matricola):
        self.nome = nome
        self.cognome = cognome
        self.matricola = matricola

    def print_current_student(self):
        print('\nStudente corrente: ' + self.nome + ' ' +  self.cognome + ', ' + self.matricola)



class MensaApp:
    def __init__(self):
        self.mensa = Mensa()
        self.welcome_page()

    def welcome_page(self):

        self.current_student = None
        self.days = {}
        self.selected_days = []
        self.current_reservations = []

        print('\n|------------------------------|')
        print('|            Mensa             |')
        print('|------------------------------|')
        print(self.mensa.nome)
        print(self.mensa.indirizzo + '\n')
        print('Effettua una scelta: ')
        print('1 - Effettua prenotazione settimana')
        print('2 - Visualizza prenotazioni')
        print('3 - Esporta prenotazioni')
        print('0 - Chiudi')

        scelta = input('>> ')

        try: 
            scelta = int(scelta)
        except:
            print('Inserisci un numero!')

        while scelta != 0 and scelta != 1 and scelta != 2 and scelta != 3:
            print('Scelta non valida!')
            scelta = input('>> ')
            try: 
                scelta = int(scelta)
            except:
                print('Inserisci un numero!')

        if scelta == 0:
            print('\nChiusura....')
            exit()
        elif scelta == 1:
            print('\nInizio prenotazione...')
            self.student_info()
            
        elif scelta == 2:
            self.mensa.print_prenotazioni()
            self.welcome_page()

        elif scelta == 3:
            self.mensa.export_prenotazioni()
            self.welcome_page()


    def student_info(self):

        print('Inserisci i tuoi dati')

        nome_studente = input('Nome: ')
        while len(nome_studente.strip()) == 0 or nome_studente.isnumeric():
            print('Inserisci un nome valido!\n')
            nome_studente = input('Nome: ')

        cognome_studente = input('Cognome: ')
        while len(cognome_studente.strip()) == 0 or cognome_studente.isnumeric() :
            print('Inserisci un cognome valido!\n')
            cognome_studente = input('Cognome: ')

        matricola_studente = input('Matricola: ')
        while not matricola_studente.isnumeric():
            matricola_studente = input('Matricola: ')
            if not matricola_studente.isnumeric():
                print('Inserisci un numero di matricola valido!\n')

        self.current_student = Studente(nome_studente.strip(), cognome_studente.strip(), matricola_studente.strip())
        self.selection_days()


    
    def selection_days(self):
        self.current_student.print_current_student()

        print('Seleziona i giorni in cui mangerai in mensa:')
        print('Per scegliere il giorno inserisci un numero e premi invio (enter).')
        print('f - Per terminare la scelta dei giorni')
        print('0 - Per annullare la prenotazione e tornare al menu iniziale\n') 
        
        i = 1
        for day in self.mensa.menu_settimana.get_days_menu():
            print(str(i) + ' - ' + day)
            self.days[i] = day
            i += 1

        input_day = None
        
        while input_day != 0 and input_day != 'f':
            
            if len(self.selected_days) > 0:
                print('Giorni selezionati: ' + str([self.days[j] for j in sorted(self.selected_days)]) + '\n')

            input_day = input('>> ')

            try:
                input_day = int(input_day) 
                if input_day not in self.days and input_day != 0:
                    print('Numero non valido!')
                elif input_day != 0:
                    if input_day in self.selected_days:
                        print(self.days[input_day] + ' è stato già selezionato!')
                    else:
                        self.selected_days.append(input_day)
            except:
                try:
                    input_day = str(input_day).strip()
                    if input_day != 'f':
                        print('Inserisci un numero valido o f per terminare la scelta!\n')    
                except:
                    print('Inserisci un numero valido o f per terminare la scelta!\n')

        if input_day == 0:
            print('Torno al menu iniziale...')
            self.welcome_page()
        elif input_day == 'f':
            if len(self.selected_days) > 0:
                self.selected_days = sorted(self.selected_days)
                self.make_reservation(self.selected_days.pop(0))
            else:
                print('\n------- Seleziona almeno un giorno! -------')
                self.selection_days()

    
    
    def make_reservation(self, current_day):
        self.current_student.print_current_student()
        menu_numbers = {}     
        reservation = {}
        print('Effettua la prenotazione per il seguente giorno: ' + self.days[current_day])
        print('Per fare una scelta inserisci un numero e premi invio (enter).')
        print('f - Per terminare la scelta')
        print('0 - Per annullare la prenotazione e tornare al menu iniziale\n') 

        for pranzo_cena in ['Pranzo', 'Cena']:
            reservation[pranzo_cena] = []
            menu_numbers[pranzo_cena] = {}  
            print('\n-------------------------------------')
            print(self.days[current_day] + ' - ' + pranzo_cena)
            print('-------------------------------------')
            i = 1
            menu = self.mensa.menu_settimana.get_menu_day(self.days[current_day])[pranzo_cena.lower()]
            
            for k in menu:
                print('\n' + str(k).capitalize())
                for v in menu[k]:
                    print(str(i) + ' - ' + v)
                    menu_numbers[pranzo_cena][i] = v
                    i += 1
            print('-------------------------------------')

            input_n = None

            while input_n != 0 and input_n != 'f':
                if len(reservation[pranzo_cena]) > 0:
                    print('Scelte effettuate: ' + str([menu_numbers[pranzo_cena][j] for j in reservation[pranzo_cena]]) + '\n')
                input_n = input('>> ')
                try:
                    input_n = int(input_n)
                    if input_n not in menu_numbers[pranzo_cena] and input_n != 0:
                        print('Numero non valido!\n')
                    else:
                        if input_n in reservation[pranzo_cena]:
                            print(menu_numbers[pranzo_cena][input_n] + ' è stato già selezionato!')
                        else:
                            reservation[pranzo_cena].append(input_n)
                except:
                    try:
                        input_n = str(input_n).strip()
                        if input_n != 'f':
                            print('Inserisci un numero valido o f per terminare la prenotazione\n')    
                    except:
                        print('Inserisci un numero valido o f per terminare la prenotazione\n')

            if input_n == 0:
                print('Torno al menu iniziale...')
                self.welcome_page()
            else:
                print('\nScelte effettuate per ' + self.days[current_day] + ' - ' + pranzo_cena + ': ' + str([menu_numbers[pranzo_cena][j] for j in reservation[pranzo_cena]]))
        
        
        if len(reservation['Pranzo']) == 0 and len(reservation['Cena']) == 0:
            print('---- Non hai selezionato nulla per pranzo e cena di ' + self.days[current_day] + ' ----')
            self.make_reservation(current_day)

        elif len(self.selected_days) > 0:
            launch = [menu_numbers['Pranzo'][j] for j in reservation['Pranzo']]
            dinner = [menu_numbers['Cena'][j] for j in reservation['Cena']]
            self.current_reservations.append(Prenotazione(self.current_student, self.days[current_day], launch, dinner))
            day = self.selected_days.pop(0)
            self.make_reservation(day)
        
        else:
            launch = [menu_numbers['Pranzo'][j] for j in reservation['Pranzo']]
            dinner = [menu_numbers['Cena'][j] for j in reservation['Cena']]
            self.current_reservations.append(Prenotazione(self.current_student, self.days[current_day], launch, dinner))
            self.mensa.prenotazioni.extend(self.current_reservations)
            print('\n------------ Ordine registrato correttamente ------------')
            self.welcome_page()



MensaApp()