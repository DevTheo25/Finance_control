import flet
from flet import *



class App(UserControl):

    global ColorPick
    ColorPick = 0

    ColorList = {
        "start": ["#13547a", "#f43b47", "#30cfd0", "#243949"],
        "end" : ["#80d0c7", "#453a94", "#330867", "#517fa4"],
    }


    def build(self):
        self.InsertButton = Container(
            content=IconButton(
                on_click= lambda e: self.OpenEntryForm(),
                icon="add",
                icon_size=15,
            ),
            alignment=alignment.center_right,
            padding=padding.only(0,0,10,0),
        )

        self.Title = Text(value="Wallet", size=22)


        self.CardWallet = Column(
            scroll="hidden"
        )


        self.CardName = TextField(
            label="Nome do Cartão",
            border="underline",
            text_size=12,
        )

        self.CardNumber = TextField(
            label="Numero do Cartão",
            border="underline",
            text_size=12, 
        )


        self.EntryForm = AlertDialog(
            title=Text(
                "Insira os dados do Cartão",
                text_align="center",
                size=12,

            ), 

            content=Column(
                [
                    self.CardName,
                    self.CardNumber,
                ],
                spacing=20,
                height=180,
            ),
            actions=[
                TextButton("Insert", on_click=lambda e: self.CheckEntryForm()),
                TextButton("Cancel", on_click=lambda e: self.CancelEntryForm()),
            ],
            actions_alignment="center",
            on_dismiss=lambda e: self.CancelEntryForm(),
        )

        return Column(
            controls=[
                Row(
                    controls=[
                        self.EntryForm,
                        Container(
                            width=160,
                            content=(self.Title),
                            padding=padding.all(10),
                        ),
                        Container(
                            width=160,
                            content=(self.InsertButton),
                            alignment=alignment.center_right,
                            padding=padding.all(10),
                        )

                    ],
                    alignment="spaceAround"
                ),
                Row(

                    wrap=False,
                    scroll='hidden',
                    controls=[
                        self.CardWallet,
                    ],
                ),
            ],
        )

    def CardMaker(self):

        global ColorPick

        self.img = Image()

        if self.CardNumber.value[0] == "4":
            self.img = Image(
                src="https://img.icons8.com/external-tal-revivo-bold-tal-revivo/384/000000/external-visa-an-american-multinational-financial-services-corporation-logo-bold-tal-revivo.png",
                width=80,
                height=80,
                fit="contain",
            )
        elif self.CardNumber.value[0] == "5":
            self.img = Image(
                src="https://img.icons8.com/color/1200/000000/mastercard-logo.png",
                width=80,
                height=80
            )
        elif self.CardNumber.value[0] == "3":
            pass

        else:
            pass

#4234 5678 9123 1234
#5234 5678 9123 1234

        self.card = Container(
            content=Column(
                controls=[
                    Container(
                        content=(
                            Text(
                                self.CardName.value,
                                size=20,
                                #bgcolor=colors.AMBER_200,
                            )
                        ),
                        alignment=alignment.top_left,
                    ),
                    Row(
                        controls=[
                            TextButton(
                                content=Container(
                                    alignment=alignment.bottom_left,
                                    #bgcolor=colors.PURPLE_200,
                                    content=Column(
                                        [
                                            Text(
                                                value=f"**** **** ****{self.CardNumber.value[-4:]}",
                                                size=14,
                                                color=colors.WHITE,
                                                height=20,
                                            )
                                        ]
                                    )
                                ),
                                on_click=None,
                            ),
                            Container(
                                #bgcolor=colors.AMBER_200,
                                content=(self.img),
                                alignment=alignment.bottom_right
                            )
                        ],
                        alignment="spaceBetween"
                    ),
                ],
                alignment="spaceBetween"
            ),
            
            border_radius=border_radius.all(20),
            width=280,
            height=180,
            padding=padding.all(10),
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=[
                    App.ColorList["start"][ColorPick],
                    App.ColorList["end"][ColorPick],
                ],
            ),
        )

        ColorPick += 1
        self.CardWallet.controls.append(self.card)
        self.CancelEntryForm()
        self.update()



    def CheckEntryForm(self):
        if len(self.CardNumber.value) == 0:
            self.CardNumber.error_text = "Por favor insira o numero do cartão!"
            self.update()
        else:
            self.CardNumber.error_text = None
            self.update()

        if len(self.CardName.value) == 0:
            self.CardName.error_text = "Por favor insira seu CVV"
            self.update()
        else:
            self.CardName.error_text = None
            self.update()

        if len(self.CardNumber.value) & len(self.CardName.value) != 0:
            self.CardMaker()





    def OpenEntryForm(self):
        self.dialog = self.EntryForm
        self.EntryForm.open = True
        self.update()


    def CancelEntryForm(self):
        self.CardName.value, self.CardNumber.value = None, None
        self.CardNumber.error_text, self.CardName.error_text = None, None
        self.EntryForm.open = False
        self.update()









def start(page: Page):

    page.title = "Wallite"
    page.vertical_alignment = "start"
    page.window_width = 320
    page.window_height = 600
    page.scroll = "hidden"
    page.theme_mode = 'dark'
    page.update()

    app = App()
    page.add(app)

if __name__ == "__main__":
    flet.app(target=start)