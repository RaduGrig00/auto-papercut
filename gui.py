import tkinter as tk
from tkinter import messagebox
from certificato import Certificato


class GuiApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x800")

        self.root.resizable(True, True)
        self.root.configure(background="white")
        self.root.title("Auto configurazione Papercut")


        frame_classes = [IpConfFrame, CertificatoFrame]#, NtpFrame

        self.frames = {}

        for FrameClass in frame_classes:
            frame = FrameClass(self.root, controller=self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.mostra_ip()
        
    def mostra_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
    
    def mostra_ip(self):
        self.mostra_frame(IpConfFrame)

    #def mostra_ntp(self):
        #self.mostra_frame(NtpFrame)

    def mostra_certificato(self):
        self.mostra_frame(CertificatoFrame)


class IpConfFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        tk.Label(self, text="Inserire indirizzo IP della macchina", font=("Helvetica", 16)).pack()
        self.indirizzo_entry = tk.Entry(self)
        self.indirizzo_entry.pack()
        tk.Button(self, text="Conferma", command= lambda: (self.salva_indirizzo(), self.controller.mostra_certificato())).pack()
    
    def salva_indirizzo(self):
        self.controller.indirizzo_ip = self.indirizzo_entry.get()
        print("Indirizzo salvato:", self.controller.indirizzo_ip)

"""class NtpFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        tk.Label(self, text="Si desidera impostare il regolamento automatico dell'ora?", font=("Helvetica", 16)).pack()
        tk.Button(self, text="Sì", command= lambda: (self.salva_ntp(True), self.controller.mostra_certificato())).pack()
        tk.Button(self, text="No", command= lambda: (self.salva_ntp(False), self.controller.mostra_certificato())).pack()
    
    def salva_ntp(self, valore):
        self.config.set_ntp(valore)"""


class CertificatoFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        tk.Label(self, text="Inserire informazioni del certificato", font=("Helvetica", 16)).pack()
        tk.Label(self, text="Inserisci reparto:").pack()
        self.reparto_entry = tk.Entry(self)
        self.reparto_entry.pack()
        tk.Label(self, text="Inserisci nome:").pack()
        self.nome_entry = tk.Entry(self)
        self.nome_entry.pack()
        tk.Label(self, text="Inserisci localita:").pack()
        self.localita_entry = tk.Entry(self)
        self.localita_entry.pack()
        tk.Label(self, text="Inserisci provincia:").pack()
        self.provincia_entry = tk.Entry(self)
        self.provincia_entry.pack()
        tk.Label(self, text="Inserisci paese:").pack()
        self.paese_entry = tk.Entry(self)
        self.paese_entry.pack()
        tk.Label(self, text="Inserisci email:").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        

        tk.Button(self, text="Conferma", command=self.salva_certificato).pack()
    
    def salva_certificato(self):
        try:
            self.controller.certificato = Certificato(
                self.reparto_entry.get(),
                self.nome_entry.get(), 
                self.localita_entry.get(), 
                self.provincia_entry.get(), 
                self.paese_entry.get(), 
                self.email_entry.get()
                )
            
            self.controller.root.destroy()
            
        except ValueError as e:
            messagebox.showerror("Errore nei dati", str(e))
        
    
