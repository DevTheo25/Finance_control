from typing import Any, List, Optional, Union
from flet import *
import flet as ft
from datetime import datetime
import sqlite3
from math import pi
from time import sleep
import threading
import pyperclip

# Classe Database para Contas
class Database:

    def ConnectToDatabase():
        try:
            db = sqlite3.connect("finanças.db")

            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE if not exists tasks (
                    id INTEGER PRIMARY KEY,
                    Task VARCHAR(255) NOT NULL,
                    Date VARCHAR(255) NOT NULL,
                    Gasto VARCHAR(255),
                    Pago INTEGER DEFAULT 0 CHECK (Pago IN (0, 1)),
                    Mes VARCHAR(255) NOT NULL,
                    Data_vencimento VARCHAR(255)
                )
            ''')

            return db

        except Exception as e:
            print(e)


    def ReadDatabase(db):

        cursor = db.cursor()

        cursor.execute("SELECT Task, Date, Gasto, Pago, Mes FROM tasks")
        results = cursor.fetchall()
        return results

    def InsertDatabase(db, values):
        cursor = db.cursor()
        cursor.execute("INSERT INTO tasks (Task, Date, Gasto, Mes) VALUES (?,?,?,?)", values)
        db.commit()

    def DeleteDatabase(db, Task, Mes):

        cursor = db.cursor()
        cursor.execute("DELETE FROM tasks WHERE Task=? AND Mes=?", (Task, Mes))
        db.commit()



    def UpdateDatabase(db, new_name, new_price, old_name):
        cursor = db.cursor()
        cursor.execute("UPDATE tasks SET Task=?, Gasto=? WHERE Task=?", (new_name, new_price, old_name))
        db.commit()

# Classe Database para cartões
class Database_card:



    def ConnetToDatabase_card():
        db = sqlite3.connect("card_data.db")
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE if not exists cards (
                CardName VARCHAR(255) NOT NULL,
                CardNumber VARCHAR(255) NOT NULL,
                CVCNumber VARCHAR(255),
                DataValid VARCHAR(255)
            )
        ''')
        return db




    def ReadDatabase(db):

        cursor = db.cursor()

        cursor.execute("SELECT CardName, CardNumber, CVCNumber, DataValid FROM cards")
        results = cursor.fetchall() 
        return results


    def InsertDatabase(db, values):
        cursor = db.cursor()
        cursor.execute("INSERT INTO cards (CardName, CardNumber, CVCNumber, DataValid) VALUES (?,?,?,?)", values)
        db.commit()


    def DeleteDatabase(db, CardNumber, CVCNumber):

        cursor = db.cursor()
        cursor.execute("DELETE FROM cards WHERE CardNumber=? AND CVCNumber=?", (CardNumber, CVCNumber))
        db.commit()


# Classe para adicionar novas contas
class FormContainer(UserControl):
    def __init__(self, func):
        self.func = func

        super().__init__()
    


    def build(self):
        return Container(
            width=480,
            height=0,
            bgcolor=colors.BLUE_GREY,
            opacity=0,
            border_radius=40,
            margin=margin.only(left=-18, right=-18),
            animate=animation.Animation(400, 'decelerate'),
            animate_opacity=800,
            padding=padding.only(top=45, bottom=45),
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[

                    TextField(
                        height=30,
                        width=250,
                        filled=True,
                        border_radius=20,
                        color="white",
                        border_color="transparent",
                        hint_text="Nome da Nova Conta:",
                        hint_style=TextStyle(size=11, color="white"),
                        bgcolor=colors.BLACK38,
                    
     
                    ),

                    TextField(
                        height=30,
                        width=250,
                        filled=True,
                        border_radius=20,
                        color="white",
                        border_color="transparent",
                        hint_text="Valor da Conta:",
                        hint_style=TextStyle(size=11, color="white"),
                        bgcolor=colors.BLACK38,
                        
                        
                    ),

                    ElevatedButton(
                        content=Text("Adicionar", color="white"),
                            width=130, 
                            height=40,
                            on_click=None,
                            style=ButtonStyle(
                                bgcolor={"": colors.BLACK38},
                                shape={"": RoundedRectangleBorder(radius=20)},

                            ),
                    
                    ),

                    
                ],
            )
        )
    
# Classe para adicionar novos cartões
class AddCard(UserControl):
    def __init__(self, bank_name: str, card_number:str, card_cvc:str, data_valid: str):

        self.card_number = card_number
        self.card_cvc = card_cvc
        self.bank_name = bank_name
        self.data_valid = data_valid

        super().__init__()

    
    

    def GetValue(self, e):
        valor =  e.control.data

        pyperclip.copy(valor)
        self.snack.open = True
        self.update()


    def build(self):

        

        self.img = Image()

        if self.card_number[0] == "4":
            self.img = Image(
                src="https://img.icons8.com/external-tal-revivo-bold-tal-revivo/384/000000/external-visa-an-american-multinational-financial-services-corporation-logo-bold-tal-revivo.png",
                width=80,
                height=80,
                fit="contain",
            )
        elif self.card_number[0] == "5":
            self.img = Image(
                src="https://img.icons8.com/color/1200/000000/mastercard-logo.png",
                width=80,
                height=80
            )
        else:
            self.img = Image(
                src="https://www.vectorlogo.zone/logos/cartaoelocombr/cartaoelocombr-ar21.svg",
                width=80,
                height=60
            )



        if self.bank_name == "Nubank":
            
            ColorList = {
                "start": ["#9100b3"],
                "end" : ["#3a0147"],
            }
        
        if self.bank_name == "Santander":

            ColorList = {
                "start": ["#eb3434"],
                "end" : ["#330101"],
            }


        if self.bank_name == "Itaú":

            ColorList = {
                "start": ["#e87602"],
                "end" : ["#c26602"],
            }

        if self.bank_name == "Caixa":

            ColorList = {
                "start": ["#003a9e"],
                "end" : ["#3a0147"],
            }

        if self.bank_name == "Bradesco":

            ColorList = {
                "start": ["#eb3434"],
                "end" : ["#003a9e"],
            }


        self.snack = SnackBar(Text(f"Numero do Cartão {self.bank_name} Copiado!"))
        
        return Container(
            border_radius=border_radius.all(20),
            width=280,
            height=180,
            padding=padding.all(10),
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=[
                    ColorList["start"][0],
                    ColorList["end"][0],
                ],
            ),
            
            content=Column(
                spacing=-5,
                controls=[
                    self.snack,
                    Container(
                        content=(
                            Text(
                                self.bank_name,
                                size=25,
                                weight="w700"
                            )
                        ),
                        alignment=alignment.top_left,
                    ),
                    Container(
                        padding=padding.only(top=10,bottom=10)

                    ),

                    Row(
                        alignment="spaceBetween",
                        controls=[
                            Column(
                                spacing=1,
                                controls=[
                                    Container(
                                        alignment=alignment.top_right,
                                        content=Text(
                                            f"Data de Validade: {self.data_valid}",
                                            color="gray",
                                            size=10,
                                            weight="w700",
                                        )
                                    ),
                                    Container(
                                        padding=padding.only(top=10,bottom=5)

                                    ),
                                    Container(
                                        alignment=alignment.bottom_left,
                                        content=Text(
                                            "Numero do Cartão",
                                            color="gray",
                                            size=9,
                                            weight="w500",
                                        )
                                    ),
                                    Container(
                                        alignment=alignment.top_left,
                                        content=Text(
                                            f"**** **** **** {self.card_number[-4:]}",
                                            color="e2e8f0",
                                            size=15,
                                            weight="w700",
                                        ),
                                        data=self.card_number,
                                        on_click=lambda e: self.GetValue(e)
                                    ),
                                    Container(
                                        bgcolor="pink",
                                        padding=padding.only(bottom=5)
                                    ),
                                    Container(
                                        alignment=alignment.bottom_left,
                                        content=Text(
                                            "CVV",
                                            color="gray",
                                            size=10,
                                            weight="w500"
                                        )
                                    ),
                                    Container(
                                        alignment=alignment.top_left,
                                        content=Text(
                                            f"**{self.card_cvc[-1:]}",
                                            color="#e2e8f0",
                                            size=13,
                                            weight="w700",
                                        ),
                                        data=self.card_cvc,
                                        on_click=lambda e: self.GetValue(e)
                                    ),
                                ]
                            ),
                            Column(
                                horizontal_alignment="end",
                                controls=[self.img],
                            ),


                        ]
                    ),
                ],
            ),
        )

# Classe para abrir o form Input Card
class FormCard(UserControl):
    def __init__(self, func):
            self.func = func

            super().__init__()
        


    def build(self):
        
        return Container(
            width=320,
            height=0,
            bgcolor=colors.BLUE_GREY,
            opacity=0,
            border_radius=20,
            animate=animation.Animation(400, 'decelerate'),
            animate_opacity=800,
            
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                
                controls=[

                    Divider(height=20, color="transparent"),
                    
                    Text("Insira os Dados do Novo Cartão", color="white", size=18, weight="bold"),

                    Divider(height=10, color="transparent"),

                    Dropdown(
                        height=50,
                        width=200,
                        filled=True,
                        border_radius=10,
                        color="white",
                        border_color="transparent",
                        hint_text="Instituição Ficanceira",
                        hint_style=TextStyle(size=15, color="white"),
                        bgcolor=colors.BLACK38,
                        options=[
                            dropdown.Option("Nubank"),
                            dropdown.Option("Santander"),
                            dropdown.Option("Itaú"),
                            dropdown.Option("Caixa"),
                            dropdown.Option("Bradesco"),

                        ]
                    
    
                    ),

                    TextField(
                        height=50,
                        width=200,
                        filled=True,
                        border_radius=10,
                        color="white",
                        border_color="transparent",
                        hint_text="Numero do Cartão:",
                        hint_style=TextStyle(size=14, color="white"),
                        bgcolor=colors.BLACK38,
                        
                        
                    ),
                    TextField(
                        height=50,
                        width=200,
                        filled=True,
                        border_radius=10,
                        color="white",
                        border_color="transparent",
                        hint_text="CVC do Cartão:",
                        hint_style=TextStyle(size=14, color="white"),
                        bgcolor=colors.BLACK38,
                        
                        
                    ),
                    TextField(
                        height=50,
                        width=200,
                        filled=True,
                        border_radius=10,
                        color="white",
                        border_color="transparent",
                        hint_text="Data de Validade:",
                        hint_style=TextStyle(size=14, color="white"),
                        bgcolor=colors.BLACK38,
                    ),

                    ElevatedButton(
                        content=Text("Adicionar", color="white"),
                            width=130, 
                            height=40,
                            on_click=(self.func),
                            style=ButtonStyle(
                                bgcolor={"": colors.BLACK38},
                                shape={"": RoundedRectangleBorder(radius=20)},

                            ),
                    
                    ),

                    
                ],
            )
        )


# Classe para gerar as contas quando o usuario adicionar
class Createtask(UserControl):
    def __init__(self, task:str, date:str, color:str, func1, func2, func3):

        self.task = task
        self.date = date
        self.color = color
        self.func1 = func1
        self.func2 = func2
        self.func3 = func3
        super().__init__()

    def TaskDeleteEdit(self, name, color, func):
        return IconButton(
            icon=name,
            width=30,
            icon_size=18,
            icon_color=color,
            opacity=0,
            animate_opacity=200,
            on_click= lambda e: func(self.GetContainerInstance())
        )


    def GetContainerInstance(self):
        return self



    def ShowIcons(self, e):

        name = e.control.content.controls[0].controls[0].value
        
        if " - PAGO" in name:
            e.control.content.controls[1].controls[2].opacity = 1
            e.control.content.controls[1].controls[0].opacity = 0
            e.control.content.controls[1].controls[1].opacity = 0
            e.control.content.update()

        else:
            
            if e.data == "true":
                
                (
                    e.control.content.controls[1].controls[0].opacity,
                    e.control.content.controls[1].controls[1].opacity,
                    e.control.content.controls[1].controls[2].opacity,
                ) = (1,1,1)
                e.control.content.update()
            else:
                (
                    e.control.content.controls[1].controls[0].opacity,
                    e.control.content.controls[1].controls[1].opacity,
                    e.control.content.controls[1].controls[2].opacity,
                ) = (0,0,0)
                e.control.content.update()


    def build(self):
        return Container(
            width=350,
            height=60,
            border=border.all(0.85, "white54"),
            border_radius=20,
            on_hover=lambda e:self.ShowIcons(e),
            clip_behavior=ClipBehavior.HARD_EDGE,
            padding=10,
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(
                        spacing=1,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Text(value=self.task, size=12, color=self.color),
                            Text(value=self.date, size=11, color='white54'),
                        ],
                    ),

                    Row(
                        spacing=10,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.TaskDeleteEdit(icons.DELETE_ROUNDED, "red500", self.func1,),
                            self.TaskDeleteEdit(icons.EDIT_ROUNDED, "white70", self.func2),
                            self.TaskDeleteEdit(icons.DONE_ALL_ROUNDED, "green",self.func3),
                        ]
                    )



                ],
            ),
        )



class AnimatedBox(UserControl):

    def __init__(self, border_color, bg_color, rotate_angle):

        self.border_color = border_color
        self.bg_color = bg_color
        self.rotate_angle = rotate_angle

        super().__init__()



    def build(self):

        return  Container(
            width=78,
            height=78,
            border=border.all(2.5, self.border_color),
            bgcolor=self.bg_color,
            border_radius=2,
            rotate=transform.Rotate(self.rotate_angle, alignment.center),
            animate_rotation=animation.Animation(700, "easeInOut"),
        )




def main(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.window_width = 400
    page.window_height = 760
    page.window_resizable = False
    page.theme_mode = "dark"
    

    
    def animate_boxes():

        clock_wise_rotate = pi /4

        counter_clock_wise_rotate = -pi * 2

        red_box = contender.content.controls[0].content.controls[2].controls[0].controls[0].controls[0]
        blue_box = contender.content.controls[0].content.controls[2].controls[0].controls[1].controls[0]

        counter = 0

        while True:

            if counter >= 0 and counter <= 4:
                red_box.rotate = transform.Rotate(
                    counter_clock_wise_rotate, alignment.center

                )
                
                blue_box.rotate = transform.Rotate(
                    clock_wise_rotate, alignment.center

                )


                red_box.update()
                blue_box.update()


                clock_wise_rotate += pi / 2
                counter_clock_wise_rotate -= pi / 2
                
                counter += 1
                sleep(0.7)


            if counter >=5 and counter <= 10:
                
                clock_wise_rotate -= pi / 2
                counter_clock_wise_rotate += pi / 2

                red_box.rotate = transform.Rotate(
                    counter_clock_wise_rotate, alignment.center

                )
                
                blue_box.rotate = transform.Rotate(
                    clock_wise_rotate, alignment.center

                )

                red_box.update()
                blue_box.update()

                counter += 1
                sleep(0.7)

            if counter > 10:
                counter = 0


    def calculate_value():
        value_dropdown = dropdown_mês.value



        db = Database.ConnectToDatabase()

        cursor = db.cursor()

        if value_dropdown is not None and value_dropdown != "Todos Meses":
            cursor.execute("SELECT SUM(CAST(REPLACE(Gasto, ',', '.') AS DECIMAL(10, 2))) FROM tasks WHERE Pago = 0 AND Mes = ?", (value_dropdown,))
        else:
            cursor.execute("SELECT SUM(CAST(REPLACE(Gasto, ',', '.') AS DECIMAL(10, 2))) FROM tasks WHERE Pago = 0")


        valor = cursor.fetchone()[0]  

        if not valor:
            valor = 0

        valor_não_pago = Text(f"Não Pago R$ {valor:.2f}", size=10, color="red")


        page.update()

        return valor_não_pago


    def calculate_value_paied():

        value_dropdown = dropdown_mês.value


        db = Database.ConnectToDatabase()

        cursor = db.cursor()

        if value_dropdown is not None and value_dropdown != "Todos Meses":
            cursor.execute("SELECT SUM(CAST(REPLACE(Gasto, ',', '.') AS DECIMAL(10, 2))) FROM tasks WHERE Pago = 1 AND Mes = ?", (value_dropdown,))

        else:
            cursor.execute("SELECT SUM(CAST(REPLACE(Gasto, ',', '.') AS DECIMAL(10, 2))) FROM tasks WHERE Pago = 1")


        valor = cursor.fetchone()[0]  

        if not valor:
            valor = 0

        valor_pago = Text(f"Pago R$ {valor:.2f}", size=10, color="green")


        page.update()

        return valor_pago


    def DeleteFunction(e):
        
        mes = dropdown_mês.value

        if mes == "Todos Meses":
            data = e.controls[0].content.controls[0].controls[1].value

            mes = data.split()[2]

        
        valor = e.controls[0].content.controls[0].controls[0].value
        name = valor.split(' R$ ')[0]
        
        db = Database.ConnectToDatabase()

        Database.DeleteDatabase(db, name, mes)
        
        db.close()

        

        _main_column_.controls.remove(e)
        _main_column_.controls[0].update()


        _main_column_.controls[1].controls[0] = calculate_value_paied()

        _main_column_.controls[2].controls[0] = calculate_value()

        _main_column_.update()


    def UpdateFunction(e):

        form_add.height, form_add.opacity = 230, 1

        name = e.controls[0].content.controls[0].controls[0].value.split(' R$ ')[0]
        price = e.controls[0].content.controls[0].controls[0].value.split(' R$ ')[1]
        if " - PAGO" in price:
            price = price.replace(" - PAGO", "")


        (
            form_add.content.controls[0].value,
            form_add.content.controls[1].value,
            form_add.content.controls[2].content.value,
            form_add.content.controls[2].on_click,
        ) = (
            name, price, "Atualizar", lambda _: FinalizeUpdate(e))
        
       
        form_add.update()


    def FinalizeUpdate(e):
        if form_add.content.controls[0].value and form_add.content.controls[1].value:
            new_name = form_add.content.controls[0].value
            new_price = form_add.content.controls[1].value
            old_name = e.controls[0].content.controls[0].controls[0].value.split(' R$ ')[0]

            db = Database.ConnectToDatabase()
            Database.UpdateDatabase(db, new_name, new_price, old_name
            )

            
            e.controls[0].content.controls[0].controls[0].value = f"{new_name} R$ {new_price}"
            e.controls[0].content.update()


            _main_column_.controls[1].controls[0] = calculate_value_paied()
            _main_column_.controls[2].controls[0] = calculate_value()
            _main_column_.update()
            
            CreateToDoTask(e)


    def FinalFuncition(e):
        valor = e.controls[0].content.controls[0].controls[0].value
        name = e.controls[0].content.controls[0].controls[0].value.split(' R$ ')[0]
        valor_pago = f"{valor} - PAGO"

        if " - PAGO" in valor:
            # Remove " - PAGO" se estiver presente no valor
            e.controls[0].content.controls[0].controls[0].value = valor.replace(" - PAGO", "")
            e.controls[0].content.controls[0].controls[0].color = "white"


            db = Database.ConnectToDatabase()

            cursor = db.cursor()
            cursor.execute("UPDATE tasks SET Pago=? WHERE Task=?", (0, name))
            db.commit()

            cursor.close()
        else:
            # Adiciona " - PAGO" se não estiver presente no valor
            e.controls[0].content.controls[0].controls[0].value = valor_pago
            e.controls[0].content.controls[0].controls[0].color = "green"
            db = Database.ConnectToDatabase()

            cursor = db.cursor()
            cursor.execute("UPDATE tasks SET Pago=? WHERE Task=?", (1, name))
            db.commit()

            cursor.close()

        _main_column_.controls[1].controls[0] = calculate_value_paied()
        _main_column_.controls[2].controls[0] = calculate_value()
        _main_column_.update()
        e.controls[0].content.update()


    def AddTaskToScreen(e):
        
        import locale

        # Defina a localização para português do Brasil (pt_BR)
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

        # Obtenha a data e hora atual
        now = datetime.now()

        # Formate a data e hora com o nome completo do mês em português
        dateTime = now.strftime("%d de %B de %Y %H:%M").capitalize()

        dateTime = dateTime[:6] + dateTime[6:].capitalize()

        

        if dropdown_mês.value is not None and dropdown_mês.value != "Todos Meses":
            mes_corrente = dropdown_mês.value
            # Converta a string dateTime em um objeto datetime
            dateTime = dateTime.replace(dateTime.split()[2], dropdown_mês.value)
            


        else:
            mes_corrente = mes_atual()


        if form_add.content.controls[0].value and form_add.content.controls[1].value:

            db = Database.ConnectToDatabase()

            Database.InsertDatabase(db, (form_add.content.controls[0].value, dateTime, form_add.content.controls[1].value, mes_corrente))

            db.close()

        else:
            pass



        completename = f"{form_add.content.controls[0].value} R$ {form_add.content.controls[1].value}"
        color = "white"
        if form_add.content.controls[0].value and form_add.content.controls[1].value:
            _main_column_.controls.append(
                Createtask(
                    completename,
                    dateTime,
                    color,
                    DeleteFunction,
                    UpdateFunction,
                    FinalFuncition,

                )
            )

            _main_column_.controls[1].controls[0] = calculate_value_paied()
            _main_column_.controls[2].controls[0] = calculate_value()
            _main_column_.update()

            CreateToDoTask(e)


    def AddCardToSCreen(e):
        

        bank_name = form_card.content.controls[3].value
        card_number = form_card.content.controls[4].value
        card_cvc = form_card.content.controls[5].value 
        data = form_card.content.controls[6].value 

        if bank_name and card_number and card_cvc:

            db = Database_card.ConnetToDatabase_card()
            Database_card.InsertDatabase(db,(bank_name, card_number, card_cvc, data))

            db.close()


        if bank_name and card_number and card_cvc:

            if form_card.height == 400:                
                form_card.height, form_card.opacity = 0, 0
                form_card.update()
            pagina_3.controls[0].content.controls.append(
                Column(
                    controls=[
                        Row(
                            alignment="center",
                            controls=[
                                    AddCard(
                                    bank_name,
                                    card_number,
                                    card_cvc,
                                    data
                                )
                            ]
                        )
                    ]
                )

            )
            


            pagina_3.update()
            page.update()


    def CreateCardTask(e):

        form_card.content.controls[7].on_click = lambda e: AddCardToSCreen(e)


        if form_card.height != 400:
            form_card.height, form_card.opacity = 400, 1
            form_card.update()

        else:
            form_card.height, form_card.opacity = 0, 0
            form_card.content.controls[3].value = None
            form_card.content.controls[4].value = None
            form_card.content.controls[5].value = None
            form_card.content.controls[6].value = None
            form_card.content.controls[7].content.value = "Adicionar"
            form_card.content.controls[7].on_click = lambda e: AddCardToSCreen(e)
            form_card.update()


    def CreateToDoTask(e):
        form_add.content.controls[2].on_click = lambda e: AddTaskToScreen(e)

        if form_add.height != 230:
            form_add.height, form_add.opacity = 230, 1
            form_add.update()
        else:
            form_add.height, form_add.opacity = 0, 0

            form_add.content.controls[0].value = None
            form_add.content.controls[1].value = None
            form_add.content.controls[2].content.value = "Adicionar"
            form_add.content.controls[2].on_click = lambda e: AddTaskToScreen(e)
            form_add.update()

    
    def shrink(e):
        pagina_2.controls[0].width = 80
        pagina_2.controls[0].scale = transform.Scale(0.9, alignment=alignment.center_right)
        pagina_2.controls[0].border_radius=border_radius.only(
            top_left=35,
            top_right=0,
            bottom_left=35,
            bottom_right=0
        )
        page.update()


    def restore(e):
        pagina_2.controls[0].width = 350
        pagina_2.controls[0].scale = transform.Scale(1, alignment=alignment.center_right)
        page.update()



    def get_dropdown_value(e):
        value_dropdown = dropdown_mês.value

        # Crie uma lista temporária para armazenar os controles de Createtask a serem removidos
        controls_to_remove = []

        # Loop pelas instâncias de Createtask dentro de _main_column_
        for controle in _main_column_.controls:
            if isinstance(controle, Createtask):
                controls_to_remove.append(controle)

        # Remova os controles de Createtask da _main_column_
        for controle in controls_to_remove:
            _main_column_.controls.remove(controle)

        db = Database.ConnectToDatabase()

        if value_dropdown == "Todos Meses":

            for task in Database.ReadDatabase(db)[::-1]:
                
                price_str = task[2]
                pago = task[3]

                # Concatene o nome e o preço
                task_combined = f"{task[0]} R$ {price_str}"

                if pago == 1:
                    task_combined += " - PAGO"

                color = "green" if pago == 1 else "white"

                _main_column_.controls.append(
                    Createtask(
                        task_combined,
                        task[1],
                        color,
                        DeleteFunction,
                        UpdateFunction,
                        FinalFuncition,
                    )
                )
        
        else:
            for task in Database.ReadDatabase(db)[::-1]:
                if task[4] == value_dropdown:
                    price_str = task[2]
                    pago = task[3]

                    # Concatene o nome e o preço
                    task_combined = f"{task[0]} R$ {price_str}"

                    if pago == 1:
                        task_combined += " - PAGO"

                    color = "green" if pago == 1 else "white"

                    _main_column_.controls.append(
                        Createtask(
                            task_combined,
                            task[1],
                            color,
                            DeleteFunction,
                            UpdateFunction,
                            FinalFuncition,
                        )
                    )


        _main_column_.controls[1].controls[0] = calculate_value_paied()

        _main_column_.controls[2].controls[0] = calculate_value()

        if value_dropdown != "Todos Meses":
            _main_column_.controls[0].controls[0].value = f"Contas de {value_dropdown}"
        else:
            _main_column_.controls[0].controls[0].value = "Todas Contas"
        
        _main_column_.update()
        restore(e)
        

    def mes_atual():
        import locale
        import datetime
        # Defina a localização para português do Brasil (pt_BR)
        locale.setlocale(locale.LC_TIME, 'pt_BR')

        # Obtenha a data atual
        data_atual = datetime.datetime.now()

        # Obtenha o nome do mês atual no formato em português
        mes_corrente = data_atual.strftime('%B').capitalize()


        return mes_corrente


    def restore_home(e):
            pagina_2.controls[0].height = 700
            pagina_3.controls[0].height = 0

            page.update()



    dropdown_mês = Dropdown(
                    label="Escolha o Mês",
                    label_style=TextStyle(color="white"),
                    height=50,
                    width=200,
                    filled=True,
                    border_radius=10,
                    color="white",
                    text_size=15,
                    border_color="white",
                    bgcolor=colors.BLACK54,
                    value=mes_atual(),
                    on_change= get_dropdown_value,
                    options=[
                        dropdown.Option("Todos Meses"),
                        dropdown.Option("Janeiro"),
                        dropdown.Option("Fevereiro"),
                        dropdown.Option("Março"),
                        dropdown.Option("Abril"),
                        dropdown.Option("Maio"),
                        dropdown.Option("Junho"),
                        dropdown.Option("Julho"),
                        dropdown.Option("Agosto"),
                        dropdown.Option("Setembro"),
                        dropdown.Option("Outubro"),
                        dropdown.Option("Novembro"),
                        dropdown.Option("Dezembro"),

                    ],
                    
                        
                    )
          
     

    _main_column_ = Column(
        expand=True,
        alignment=MainAxisAlignment.START,
        scroll=ScrollMode.HIDDEN,
        controls=[
            Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text(
                        f"Contas de {mes_atual()}", size=22, weight="bold", color="white"),
                    IconButton(
                        icons.ADD_CIRCLE_ROUNDED,
                        icon_size=22,
                        on_click=lambda e: CreateToDoTask(e)
                        
                        ),
                    IconButton(
                        icons.MENU_ROUNDED,
                        icon_size=24,
                        on_click=lambda e: shrink(e)
                    ),
                    
                ],
            ),
            Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    calculate_value_paied()
                    ]
            ),
            Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    calculate_value()
                    ]
            ),

            Divider(height=8, color="white24")
        ]
        )


    pagina_1 = Container( 
        width=350,
        height=700,
        border_radius=40,
        border=border.all(1, "white"),
        bgcolor=colors.BLACK26,
        padding=padding.only(left=30,top=30,right=100),
        
        

        content=Column(
            
            controls=[
                Row(
                alignment="end",
                controls= [
                    IconButton(icons.ARROW_BACK, icon_color= "white",on_click=lambda e: restore(e)),

                    ],
                ),

                Divider(height=20,color="transparent"),

                Row(
                    alignment="Center",
                    controls=[
                        Stack(
                            controls=[
                                AnimatedBox("#e9665a", None, 0),
                                AnimatedBox("#7df6dd", "#23262a", pi / 4)

                            ]

                        ),

                    ]
                ),


                Divider(height=20,color="transparent"),


                Row(
                    alignment="Center",
                    controls= [
                        Text("Olá, Théo", size=34,weight="bold",color="white"),
                    ],
                    
                ),


                Divider(height=20,color="transparent"),

                Row(
                    alignment="Center",
                    controls=[
                        dropdown_mês
                    ]

                ),
                Divider(height=10,color="transparent"),

                Row(
                    alignment="center",
                    controls=[
                        
                        TextButton(text="Wallet", icon=icons.WALLET_OUTLINED, on_click=lambda e: open_pg_3(e)),
                        
                    ]

                ),
                Divider(height=10,color="transparent"),
                Row(
                    alignment="center",
                    controls=[
                        TextButton(text="Analytics", icon=icons.ANALYTICS_OUTLINED,)
                    ]

                ),
                Divider(height=10,color="transparent"),
                
                Row(
                    alignment="center",
                    controls=[
                        TextButton(text="Logout", icon=icons.LOGIN_OUTLINED,)
                    ]

                )
                    
            ]
        )
    )
                          
    

    pagina_2 = Row(
                alignment="end",
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        width=350,
                        height=700,
                        bgcolor="black",
                        border_radius=40,
                        padding=padding.only(top=50, left=20, right=20, bottom=5),
                        animate=animation.Animation(600, AnimationCurve.DECELERATE),
                        animate_scale= animation.Animation(400, AnimationCurve.DECELERATE),
                        clip_behavior=ClipBehavior.HARD_EDGE,

                        content=Column(
                            
                            alignment=MainAxisAlignment.CENTER,
                            expand=True,
                            controls=[
                                _main_column_,
                                FormContainer(lambda e: AddTaskToScreen(e)),
                                

                            ]

                        ),

                    ),
                ],
            )


    pagina_3 = Row(
                
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        width=350,
                        height=0,
                        bgcolor="black",
                        border_radius=40,
                        padding=padding.only(top=50, left=20, right=20, bottom=5),
                        animate=animation.Animation(600, AnimationCurve.DECELERATE),
                        animate_scale= animation.Animation(400, AnimationCurve.DECELERATE),
                        clip_behavior=ClipBehavior.HARD_EDGE,

                        content=
                        
                        Column(
                            expand=True,
                            scroll="hidden",
                            controls=[
                                    Row(
                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    controls= [
                                        IconButton(icons.ARROW_BACK, icon_color= "white",on_click=lambda e: restore_home(e)),
                                        Text("Wallet", color="white", size=32, weight="bold"),
                                        IconButton(icon=icons.ADD_CARD_OUTLINED,icon_color="white",on_click=lambda e: CreateCardTask(e))
                                        ],
                                    ),
                                    Divider(height=20, color="white24"),
                                    FormCard(lambda e: CreateCardTask(e))
                            ]

                        ),
                    
                    ),
                ],
            )



    contender = Container(
        width=350,
        height= 700,
        border_radius=40,
        content= Stack(
            controls=[
                pagina_1,
                pagina_2,
                pagina_3
            ]
        )
        
        )


    def open_pg_3(e):

        if pagina_2.controls[0].height == 700:
            pagina_2.controls[0].height = 0
            pagina_3.controls[0].height = 700

            pagina_2.update()
            pagina_3.update()


    page.add(contender

    )


    page.update()
    


    form_add = pagina_2.controls[0].content.controls[1].controls[0]

    form_card = pagina_3.controls[0].content.controls[2].controls[0]

    

    # Inserido contas salvas no DB ao inciar a aplicação
    db = Database.ConnectToDatabase()
    for task in Database.ReadDatabase(db)[::-1]:

        if task[4] == mes_atual():
            price_str = task[2]
            pago = task[3]

            # Concatene o nome e o preço
            task_combined = f"{task[0]} R$ {price_str}"

            if pago == 1:
                task_combined += " - PAGO"
            

            color = "green" if pago == 1 else "white"

            _main_column_.controls.append(
                Createtask(
                    task_combined,
                    task[1],
                    color,
                    DeleteFunction,
                    UpdateFunction,
                    FinalFuncition,
                )
            )

    
    #Inserido Cartões ao salvos no DB ao iniciar a aplicação
    db_card = Database_card.ConnetToDatabase_card()
    for card in Database_card.ReadDatabase(db_card):

        CardName = card[0]
        CardNumber = card[1]
        CVCNumber = card[2]
        data = card[3]


        pagina_3.controls[0].content.controls.append(
                Column(
                    controls=[
                        Row(
                            alignment="center",
                            controls=[
                                    AddCard(
                                    CardName,
                                    CardNumber,
                                    CVCNumber,
                                    data
                                )
                            ]
                        )
                    ]
                )

            )
        
        pagina_3.update()
        page.update()





    _main_column_.update()

        # Crie uma instância da thread
    animation_thread = threading.Thread(target=animate_boxes)

    # Inicie a thread
    animation_thread.start()
    mes_atual()
    
    
app(target=main)