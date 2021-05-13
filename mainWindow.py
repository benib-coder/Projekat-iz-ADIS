from tkinter import *
from tkcalendar import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
import sys,os
from tkinter import messagebox
import sqlite3
from datetime import datetime
from datetime import date
import base64
import io 
import schedule
import time
from fpdf import *


## txt file u pdf se konvertuje
def txt_to_pdf(file):
    datum_stampe=datetime.now()
    stampa=datum_stampe.strftime("%m/%d/%y %H:%M:%S")
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial",size=18)
##Otvara se file kreiran u upisuju se podaci    
    with open(file,'r') as f:
        pdf.cell(200,10,'Spisak dana',ln=1,align='C')
        pdf.cell(200,10,'Datum: '+str(stampa),ln=1,align='c')
        for x in f:
            pdf.cell(200, 10, txt = x, ln=1,align = 'C')
        pdf.output("spisak_dana_Ben.pdf")




def main_window():
   #kreiranje framea
    main_window=Tk()
    main_window.title("Frizer Ben")
    main_window.state("zoomed")
    main_window["bg"]='#B4B8BE'

    
 

    
    #menubar
    menubar=Menu(main_window)
    main_window.config(menu=menubar)
    helpMenu= Menu(menubar, tearoff=0)  
    helpMenu.add_command(label="About")  
    menubar.add_cascade(label="Help", menu=helpMenu)  

    #separator
    separator=ttk.Separator(main_window,orient="vertical")
    separator.place(relx=0.5, rely=0, relwidth=0, relheight=1)

    #kalendar widget
    Label(main_window,text="Izaberite datum termina:",bg=('#B4B8BE'),font='30').grid(row=0,column=0)
    kalendar=Calendar(main_window,selectmode="day")
    kalendar.grid(row=2,column=0)
   
    
    #ime opcionalno 
    Label(main_window,text="Ime klijenta:",bg=('#B4B8BE'),font='20').place(x=260,y=95)
    ime=StringVar()
    ime_input=Entry(main_window,width=40,textvariable=ime).place(x=380,y=100)
    
    
    #time display
    clock_label = Label(
    main_window, bg="black", fg="white", font=("Times", 30, "bold"), relief="flat")
    clock_label.place(x=420, y=35)
    def update_label():
    
            current_time = strftime("%H: %M: %S")
            clock_label.configure(text=current_time)
            clock_label.after(80, update_label)

    update_label()
    #vrijeme biranje
    Label(main_window,text="Izaberite vrijeme:",bg=('#B4B8BE'),font='25').place(x=260,y=135)
    lista_vremena=[
            '10:00','10:30','11:00','11:30','12:00','12:30',
            '13:00','13:30','15:00','15:30','16:00','16:30',
            '17:00','17:30','18:00','18:30'
        ]    
    clicked=StringVar()
    clicked.set(lista_vremena[0])
    dropbox = OptionMenu(main_window,clicked,*lista_vremena).place(x=430,y=140)
    
    #Biranje usluge
    uslugaLabel=Label(main_window,text="Izaberite uslugu:",bg=('#B4B8BE'),font='25').place(x=265,y=170)
    lista_usluga=['Sisanje','Brijanje','Oboje']
    clicked2=StringVar()
    clicked2.set(lista_usluga[0])
    dropboxUsluga=OptionMenu(main_window,clicked2,*lista_usluga).place(x=430,y=168)
##==============================================================================================================
   
    
    
    ##Image Frizer ben
    def kreiraj_sliku():
        db=sqlite3.connect("projekatBen.db")
        cur=db.cursor()
        sql="SELECT * from slika "
        cur.execute(sql)
        data=cur.fetchall()
        
        for row in data:
            row[1]
        with open('benLogo.jpg','wb') as f:
            f.write(row[1])
        
       
       
        db.close()
    
    kreiraj_sliku()
    canvas = Canvas(main_window, width = 500, height = 500)  
    canvas.place(x=100,y=310)  
    image=PhotoImage(file="C:\\Users\\Korisnik\\Desktop\\Python Files\\benLogo.jpg")
    canvas.create_image(30,80,anchor=NW,image=image)

    ##display termine from db
    terminiLabel=Label(main_window,text="Termini",bg=('#B4B8BE'),font='50').place(x=1120,y=30)
    frame=Frame(main_window,height=700,width=500)
    frame.place(x=800,y=70)
    
    def connect():
            con1 = sqlite3.connect("projekatBen.db")
            cur1 = con1.cursor()
            cur1.execute("CREATE TABLE IF NOT EXISTS termini(id_Termin INTEGER PRIMARY KEY, ime TEXT, datum_vrijeme TEXT ,usluga TEXT)")
            con1.commit()
            con1.close()
    def View():
            con1 = sqlite3.connect("projekatBen.db")
            cur1 = con1.cursor()
            cur1.execute("SELECT * FROM termini")
            rows = cur1.fetchall()    
            for row in rows:
                print(row) 
                tree.insert("", END, values=row)        
            
            con1.close()
    
    connect() 
    tree = ttk.Treeview(frame, column=("c1", "c2","c3","c4"), show='headings')
    tree.column("#1", anchor=CENTER,width=160)
    tree.heading("#1", text="ID")
    tree.column("#2", anchor=CENTER,width=160)
    tree.heading("#2", text="Ime")
    tree.column("#3", anchor=CENTER,width=180)
    tree.heading("#3", text="Datum i vrijeme")
    tree.column("#4", anchor=CENTER,width=180)
    tree.heading("#4", text="Usluga")
    tree.configure(height=20)
    tree.pack()
       
    View()
    
    
##==============================================================================================================
 #Button save
     ##Funkcija koja uzima podatke iz entry-a 
    def salji_podatke():
        i=ime.get()
        kl=kalendar.get_date()
        vrijeme=clicked.get()
        datum_vrijeme=kl+" "+vrijeme
        usluga=clicked2.get()


        ##Konekcija ka bazi i vršenje upita
        db=sqlite3.connect("projekatBen.db")
        cur=db.cursor()
        sql="INSERT INTO termini (ime,datum_vrijeme,usluga) VALUES (?,?,?)"
        cur.execute(sql,(i,datum_vrijeme,usluga))
        
        sql2="SELECT * FROM termini ORDER BY id_Termin DESC LIMIT 1"
        cur.execute(sql2)
        termini=cur.fetchall()
        ##U TreeView se selektovani podaci iz baze stavljaju
        for termin in termini:
            tree.insert("",END,values=termin)

            
        db.commit()
        db.close()
        messagebox.showinfo("Info","Podaci su uspjesno sacuvani!")
    dugme_save=Button(main_window,text='Sacuvaj',command=salji_podatke,fg='green',height = 2, width = 40).place(x=300,y=250)   
        
    ##dugme exit
    exitButton=Button(main_window,text="EXIT",fg="red",height=2,width=30,command=exit).place(x=1280,y=700)
    
  



    ## dugme print
    def print_data():
        db=sqlite3.connect("projekatBen.db")
        cur=db.cursor()
        sql="SELECT * from termini"
        ##otvaranje txt file spisak dana i upisivanje sql podataka u sam te isti fajl
        spisak=open("spisak_dana.txt","w")
        table=cur.execute(sql)
        for row in table:
            spisak.write(str(row)) 
            spisak.write("\n")
        spisak.close()
        db.close()
        ##pozivanje funckcije za prebacivanje u pdf file 
        txt_to_pdf("spisak_dana.txt")
    
    
    
    printPdf=Button(main_window,text="Print",fg='orange',height=2,width=30,command=print_data).place(x=850,y=700)




    ## dugme brisi podatke iz db i treeja 
    def brisi_sve():
        msg=messagebox.askyesno("Obrisi","Da li ste sigurni da sve zelite obrisati?")
        if msg==True:
            db=sqlite3.connect('projekatBen.db')
            cur=db.cursor()
            cur.execute("DELETE  from termini")
            termini=cur.fetchall()
            print(termini)
            ##brise u treeju podatke
            x=tree.get_children()
            for item in x:
                tree.delete(item)

            db.commit()
        else:
            pass

    brisiButton=Button(main_window,text="Brisi sve",fg='red',height=2,width=25,command=brisi_sve).place(x=1200,y=500)
    
        
    ##dugme brisi selektovano 
    def brisi_selektovano():
        selektovano=tree.selection()[0]
        uid=tree.item(selektovano)['values'][0]
        ##brise iz db ii brise selektovano u trreeeeVIew
        db=sqlite3.connect('projekatBen.db')
        cur=db.cursor()
        sql="DELETE FROM termini WHERE id_Termin = ? "
        data=(uid,)
        cur.execute(sql,data)
        db.commit()
        tree.delete(selektovano)

    
    selButton=Button(main_window,text="Obrisi",fg='orange',height=2,width=25,command=brisi_selektovano).place(x=950,y=500)

   
    #Checkbox obavijesti me
    def obavjesti_me():
        def msgbox_reminder():
         messagebox.showinfo("Imate zakazan termin!")
      
      
        if ticked.get()==1:
            print('HI')
            ##vrijeme koje je sad
            now_time = datetime.now()
            now_date = date.today()

            
            
            vrijeme_sad = now_time.strftime("%H:%M")
            datum_sad = now_date.strftime("%m/%d/%y")
            vreme=datum_sad+' '+vrijeme_sad
            print(vreme)
            def sql_vrijeme():
                db=sqlite3.connect("projekatBen.db")
                cur=db.cursor()
                sql="SELECT datum_vrijeme from termini"
                cur.execute(sql)
                data=cur.fetchall()
                for x in data:
                     print(x)
                     for ex in x:
                         if ex==vreme:
                             msgbox_reminder()
                         else:
                              pass
                     
            sql_vrijeme()
        




        





    ticked=IntVar()


    chbox = Checkbutton(main_window, text='Obavijesti me o terminu',variable=ticked,onvalue=1,offvalue=0,command=obavjesti_me,bg=('#B4B8BE'),font=30)
    chbox.place(x=380,y=200)
    
    
    
    

    main_window.mainloop()



main_window()