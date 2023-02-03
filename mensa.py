import json
import csv
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

class Mensa():

    def __init__(self):
        self.nome = "Mensa Dipartimento"
        self.indirizzo = "Via del corso, numero"
        self.immagine = Image.open("src/logo-univaq.png").resize((100,100))
        self.prenotazioni = []
        self.menu_settimana = Menu()

    def export_prenotazioni(self):
        header = ['id', 'nome studente', 'cognome studente', 'matricola studente', 'giorno', 'pranzo', 'cena']
        if len(self.prenotazioni) == 0:
            messagebox.showwarning(message="Non sono presenti prenotazioni")
        else: 
            with open("prenotazioni.csv", "w") as w:
                writer = csv.writer(w)
                writer.writerow(header)
                writer.writerows(self.prenotazioni)
            
            messagebox.showinfo(message="Prenotazioni esportate con successo!")

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


class MensaApp:
    def __init__(self, main):
        self.main = main
        self.main.geometry("500x300")
        self.mensa = Mensa()
        self.start_page()
    

    def start_page(self):
        # Per la selezione dei giorni
        self.check_boxes_days = []
        self.selected_days = []

        self.check_boxes_launch = []
        self.check_boxes_dinner = []
        self.prenotazioni = []

        self.main.geometry("500x300")
        for i in self.main.winfo_children():
            i.destroy()
        self.frame1 = tk.Frame(self.main)
        self.frame1.pack(fill=tk.BOTH)

        img = ImageTk.PhotoImage(self.mensa.immagine)
        label = tk.Label(self.frame1, image = img)
        label.image = img
        label.place(x=10, y=20)
        label.pack()
        
        tk.Label(self.frame1, text=self.mensa.nome, anchor='w', font=("Arial", 25)).pack(padx=10, pady=(20, 5))
        tk.Label(self.frame1, text=self.mensa.indirizzo, anchor='w', font=("Arial", 15)).pack(padx=10, pady=(0, 20))
        
        tk.Button(self.frame1, text="Nuova\nprenotazione settimana", command=self.student_info, height = 3, width = 20).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.frame1, text="Esporta\nprenotazioni", command=self.mensa.export_prenotazioni, height = 3, width = 20).pack(side=tk.RIGHT, padx=10, pady=10)

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return("break")

    # Funzione per la validazione delle infomazioni inserite per lo studente
    def validation(self, nome, cognome, matricola):
        nome = nome.get(1.0, "end-1c").strip()
        cognome = cognome.get(1.0, "end-1c").strip()
        matricola = matricola.get(1.0, "end-1c").strip()

        mancanti = []
        if (len(nome) == 0) or (len(cognome) == 0) or (len(matricola) == 0) :
            msg = "Inserisci le infomazioni nei campi!\nCampi mancanti: "

            if (len(nome) == 0):
                mancanti.append('nome')
            if (len(cognome) == 0):
                mancanti.append('cognome')
            if (len(matricola) == 0):
                mancanti.append('matricola')
    
            messagebox.showinfo('message', msg + str(mancanti))
        
        else:
            self.current_student = Studente(nome, cognome, matricola)
            self.selection_days()

        

    # Inserimento dati studente
    def student_info(self):
        self.main.geometry("500x300")
        for i in self.main.winfo_children():
            i.destroy()

        self.frame = tk.Frame(self.main, width=400, height=400)
        self.frame.pack(fill=tk.BOTH)
        
        # Immagine uni
        img = ImageTk.PhotoImage(self.mensa.immagine.resize((50, 50)))
        img_uni = tk.Label(self.frame, image = img)
        img_uni.image = img
        img_uni.pack()


        tk.Label(self.frame, text='Inserisci i tuoi dati', anchor='w', font=("Arial", 25)).pack(padx=10, pady=(3, 5))

        # Nome studente
        tk.Label(self.frame, text='Inserisci il tuo nome:', anchor='w', font=("Arial", 15)).pack(fill=tk.BOTH, padx=10, pady=(10, 0))
        nome = tk.Text(self.frame, width= 5, height= 1, background="lightgrey",foreground="black",font= ('Sans Serif', 13, 'italic bold'))
        nome.bind("<Tab>", self.focus_next_widget)
        nome.bind("<Return>", self.focus_next_widget)
        nome.pack(expand= 1, fill= tk.BOTH, padx=10)

        # Cognome studente
        tk.Label(self.frame, text='Inserisci il tuo cognome:', anchor='w', font=("Arial", 15)).pack(fill=tk.BOTH, padx=10, pady=(10, 0))
        cognome = tk.Text(self.frame, width= 5, height= 1, background="lightgrey",foreground="black",font= ('Sans Serif', 13, 'italic bold'))
        cognome.bind("<Tab>", self.focus_next_widget)
        cognome.bind("<Return>", self.focus_next_widget)
        cognome.pack(expand= 1, fill= tk.BOTH, padx=10)

        # Matricola studente
        tk.Label(self.frame, text='Inserisci la tua matricola:', anchor='w', font=("Arial", 15)).pack(fill=tk.BOTH, padx=10, pady=(10, 0))
        matricola = tk.Text(self.frame, width= 5, height= 1, background="lightgrey",foreground="black",font= ('Sans Serif', 13, 'italic bold'))
        matricola.bind("<Tab>", self.focus_next_widget)
        matricola.bind("<Return>", self.focus_next_widget)
        matricola.pack(expand= 1, fill= tk.BOTH, padx=10)

        self.register_btn = tk.Button(self.frame, text="Inizia prenotazione", command=lambda:self.validation(nome, cognome, matricola))
        self.register_btn.pack()

    def confirm_days(self):
        for string_var in self.check_boxes_days:
            text = string_var.get()
            if text:
                self.selected_days.append(text)

        if len(self.selected_days) == 0:
            messagebox.showinfo('message', "Seleziona almeno un giorno della settimana")
        else:
            day = self.selected_days.pop(0)
            self.selection_food(day)
            
            
    # Selezione dei giorni nei quali mangerai a mensa
    def selection_days(self):
        self.main.geometry("500x300")
        for i in self.main.winfo_children():
            i.destroy()
        self.frame_header = tk.Frame(self.main)
        self.frame_header.pack(fill=tk.BOTH)

        self.frame = tk.Frame(self.main, width=400, height=400)
        self.frame.pack(fill=tk.BOTH)
        
        # Immagine uni 
        img = ImageTk.PhotoImage(self.mensa.immagine.resize((50, 50)))
        img_uni = tk.Label(self.frame_header, image = img)
        img_uni.image = img
        img_uni.pack(side=tk.LEFT, anchor='w', padx=10, pady=10)

        # Studente corrente
        tk.Label(self.frame_header, text='Studente corrente: \n' + self.current_student.nome + ' ' + self.current_student.cognome + ', ' + self.current_student.matricola,
                 anchor='e', font=("Arial", 12)).pack(side=tk.RIGHT, anchor='e', padx=10, pady=10)

        tk.Label(self.frame, text='Seleziona giorni in cui mangerai in mensa:', font=("Arial", 25)).pack(anchor='w', padx=10, pady=(2, 5))

        for item in self.mensa.menu_settimana.get_days_menu():
            string_var = tk.StringVar()
            self.check_boxes_days.append(string_var)

            cb = tk.Checkbutton(self.frame, text=item, font=("Arial", 15), anchor='w', variable=string_var, onvalue=item, offvalue='', width=50)
            cb.pack()

        b1 = tk.Button(self.frame, text="Conferma", command=lambda:self.confirm_days())
        b1.pack(side="bottom")

    def confirm_order(self, current_day):
        launch = []
        dinner = []

        for string_var in self.check_boxes_launch:
            text = string_var.get()
            if text:
                launch.append(text)

        for string_var in self.check_boxes_dinner:
            text = string_var.get()
            if text:
                dinner.append(text)

        if len(launch) == 0 and len(dinner) == 0:
            messagebox.showwarning(message="Non hai selezionato nulla")
        elif len(self.selected_days) > 0:
            self.prenotazioni.append(Prenotazione(self.current_student, current_day, launch, dinner))
            day = self.selected_days.pop(0)
            self.selection_food(day)
        else:
            self.prenotazioni.append(Prenotazione(self.current_student, current_day, launch, dinner))
            self.mensa.prenotazioni.extend(self.prenotazioni)
            messagebox.showinfo(message='Ordine registrato correttamente')
            self.start_page()

    # Selezione dei cibi da prenotare
    def selection_food(self, current_day):
        self.main.geometry("500x500")
        self.check_boxes_launch = []
        self.check_boxes_dinner = []

        for i in self.main.winfo_children():
            i.destroy()

        self.frame_header = tk.Frame(self.main)
        self.frame_header.pack(fill=tk.BOTH)

        # Immagine uni 
        img = ImageTk.PhotoImage(self.mensa.immagine.resize((50, 50)))
        img_uni = tk.Label(self.frame_header, image = img)
        img_uni.image = img
        img_uni.pack(side=tk.LEFT, anchor='w', padx=10, pady=10)

        # Studente corrente
        tk.Label(self.frame_header, text='Studente corrente: \n' + self.current_student.nome + ' ' + self.current_student.cognome + ', ' + self.current_student.matricola,
                 anchor='e', font=("Arial", 12)).pack(side=tk.RIGHT, anchor='e', padx=10, pady=10)

        self.frame_title = tk.Frame(self.main)
        self.frame_title.pack(fill=tk.BOTH)

        tk.Label(self.frame_title, text='Effettua l\'ordine per il seguente giorno: ' + current_day, font=("Arial", 20)).pack(anchor='w', padx=10, pady=(2, 5))

        self.frame_pranzo = tk.Frame(self.main, width=250)
        self.frame_pranzo.pack(fill=tk.BOTH, side=tk.LEFT, anchor='e')
        self.frame_pranzo.pack_propagate(False)

        self.frame_cena = tk.Frame(self.main, width=250)
        self.frame_cena.pack(fill=tk.BOTH, side=tk.RIGHT, anchor='w')
        self.frame_cena.pack_propagate(False)
        
        for frame in [self.frame_pranzo, self.frame_cena]:
            if frame == self.frame_pranzo:
                pranzo_cena = 'Pranzo'
            else:
                pranzo_cena = 'Cena'

            tk.Label(frame, font=("Arial", 18, 'bold'), text=pranzo_cena).pack(anchor='w', padx=5)

            menu = self.mensa.menu_settimana.get_menu_day(current_day)[pranzo_cena.lower()]

            for k in menu:
                tk.Label(frame, font=("Arial", 15, 'bold'), text=k).pack(anchor='w', padx=5, pady=(2, 0))
                for v in menu[k]:
                    string_var = tk.StringVar()
                    if pranzo_cena == 'Pranzo':
                        self.check_boxes_launch.append(string_var)
                    else:
                        self.check_boxes_dinner.append(string_var)

                    cb = tk.Checkbutton(frame, text=v, anchor='w', variable=string_var, onvalue=v, offvalue='', width=50)
                    cb.pack(anchor='w', padx=5)

        self.frame_footer = tk.Frame(self.main, width=500, height=50)
        self.frame_footer.pack(fill=tk.BOTH)
        self.frame_footer.place(y=450)
        self.frame_footer.pack_propagate(False)

        if len(self.selected_days) == 0:
            text_button = 'Conferma'
        else:
            text_button = 'Prossimo giorno'
        
        b1 = tk.Button(self.frame_footer, text=text_button, command=lambda: self.confirm_order(current_day))
        b1.pack()

root = tk.Tk()
root.title("Mensa Univaq")
MensaApp(root)
root.mainloop()