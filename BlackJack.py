#Подключение библиотек
from random import randint
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
from time import sleep

#Я использую camelCase

#Создание словарей с картами (все карты и текущие), хранящие достоинство карты и её номер для нахождения изображения
allCards = {"26": 11, "13": 11, "52": 11, "39": 11, "14": 2, "1": 2,
            "40": 2, "27": 2, "15": 3, "2": 3, "41": 3, "28": 3,
            "16": 4, "3": 4, "42": 4, "29": 4, "17": 5, "4": 5,
            "43": 5, "30": 5, "18": 6, "5": 6, "44": 6, "31": 6,
            "19": 7, "6": 7, "45": 7, "32": 7, "20": 8, "7": 8,
            "46": 8, "33": 8, "21": 9, "8": 9, "47": 9, "34": 9,
            "22": 10, "9": 10, "48": 10, "35": 10, "23": 10, "10": 10,
            "49": 10, "36": 10, "24": 10, "11": 10, "50": 10, "37": 10,
            "25": 10, "12": 10, "51": 10, "38": 10}

currentCards = {}

window = CTk()

class Main:
    def __init__(self):
        #Инициализация главного класса игры, объявление переменных игрока и дилера
        self.igrok = Player(5000, True)
        self.dealer = Player(10000, False)

        #Настройка окна customtkinter
        window.title('BlackJack')
        set_appearance_mode('dark')
        window.wm_attributes('-alpha', 0.975)
        window.geometry('1024x768')
        window.resizable(width=False, height=False)
        window.wm_iconbitmap()
        iconImg = ImageTk.PhotoImage(file="images/blackjack.png")
        window.iconphoto(False, iconImg)
	
        #Загрузка изображений
        self.bgImage = CTkImage(Image.open("images/table.jpg"), size=(1024, 768))
        self.bgImageLabelsFrame = CTkImage(Image.open("images/cards/player.png"), size=(250, 320))
        self.chipsImage = CTkImage(Image.open("images/chips.png"), size=(100, 100))
        self.backImage = CTkImage(Image.open("images/cards/back.png"), size=(120, 200))
        self.questionImage = CTkImage(Image.open("images/question.png"), size=(50, 50))

        self.setWidgets()

    def setWidgets(self):
        global main
        #Функция расстановки объектов на окне
        #Инициализация фона
        self.background = CTkLabel(window, image=self.bgImage, text="")
        self.background.place(x=0, y=0, relwidth=1, relheight=1)
        
        #Создание и расположение всех UI элементов
        #Кнопки
        self.stakeButton = CTkButton(
            window,
            text="Сделать ставку",
            font=("Arial", 28),
            width = 120,
            height = 70,
            fg_color = "#00BB00",
            hover_color = "#007700",
            corner_radius = 8,
            command=self.setStake
        )
        self.stakeButton.place(anchor="center", relx=0.55, rely=0.935)

        self.questionButton = CTkButton(
            window,
            text="",
            #fg_color = "#222",
            #hover_color = "#222",
            height=70,
            corner_radius = 8,
            image = self.questionImage,
            command=self.questionCommand
        )
        self.questionButton.place(anchor="center", relx=0.9, rely=0.935)

        self.doubleButton = CTkButton(
            window,
            text="Удвоить",
            font=("Arial", 28),
            width = 120,
            height = 70,
            fg_color='#222222',
            hover_color='#222222',
            corner_radius = 8,
            command=lambda: None
        )
        self.doubleButton.place(anchor="center", relx=0.75, rely=0.935)
        
        self.moreButton = CTkButton(
            window,
            text="Ещё",
            font=("Arial", 28),
            width = 120,
            height = 70,
            fg_color='#222222',
            hover_color='#222222',
            corner_radius = 8,
            command=lambda: None
        )
        self.moreButton.place(anchor="center", relx=0.35, rely=0.935)

        self.stopButton = CTkButton(
            window,
            text="Хватит",
            font=("Arial", 28),
            width = 120,
            height = 70,
            fg_color='#222222',
            hover_color='#222222',
            corner_radius = 8,
            command=lambda: None
        )
        self.stopButton.place(anchor="center", relx=0.2, rely=0.935)

        #Изображения и фрейм, связанные со слайдером и ставками
        self.stakeImage = CTkLabel(
            window,
            fg_color = '#064d23',
            image=None,
            text=""
        )
        self.stakeImage.place(anchor="center", relx=0.35, rely=0.8)

        self.sliderFrame = CTkFrame(
            window,
            width=200,
            height=70,
            fg_color="#222"
        )
        self.sliderFrame.place(anchor="center", relx=0.55, rely=0.8)
        
        #Слайдер
        self.stakeSlider = CTkSlider(
            window,
            from_=0,
            to=self.igrok.getBank(),
            fg_color="#222",
            command=self.sliderConfigure
        )
        self.stakeSlider.place(anchor="center", relx=0.55, rely=0.85)

        #Фрейм для текста и сам текст
        self.sliderLabel = CTkLabel(
            window,
            text = str(int(self.stakeSlider.get())),
            text_color = '#0000FF',
            fg_color = "#222",
            font=("Arial", 28),
        )
        self.sliderLabel.place(anchor="center", relx=0.55, rely=0.8)
        
        self.labelsFrame = CTkFrame(
            window,
            width=250,
            height=320
        )
        self.labelsFrame.place(anchor="center", relx=0.125, rely=0.675)
        
        self.backgroundLabelsFrame = CTkLabel(self.labelsFrame, image=self.bgImageLabelsFrame, text="")
        self.backgroundLabelsFrame.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.bankLabel = CTkLabel(
            window,
            text = "Ваш банк: \n" + str(int(self.igrok.getBank())),
            text_color = '#00FF00',
            fg_color = '#FFFFFF',
            font=("Arial", 28),
        )
        self.bankLabel.place(anchor="center", relx=0.1275, rely=0.8)

        self.stakeLabel = CTkLabel(
            window,
            text = "Ваша ставка: \n" + str(int(self.igrok.getStake())),
            text_color = '#0000FF',
            fg_color = '#FFFFFF',
            font=("Arial", 24),
        )
        self.stakeLabel.place(anchor="center", relx=0.1275, rely=0.7)

        self.scorePlayerLabel = CTkLabel(
            window,
            text = "Ваши очки: " + str(int(self.igrok.getScore())),
            text_color = '#FF0000',
            fg_color = '#FFFFFF',
            font=("Arial", 24),
        )
        self.scorePlayerLabel.place(anchor="center", relx=0.1275, rely=0.62)

        self.scoreDealerLabel = CTkLabel(
            window,
            text = "Очки дилера: ??",
            text_color = '#FF0000',
            fg_color = '#FFFFFF',
            font=("Arial", 24),
        )
        self.scoreDealerLabel.place(anchor="center", relx=0.1275, rely=0.55)

        #Объявление начальных мест для карт
        self.playerCardImage1 = CTkLabel(
            window,
            fg_color = '#064d23',
            image=None,
            text=None
        )
        self.playerCardImage1.place(anchor="center", relx=0.325, rely=0.55)

        self.dealerCardImage1 = CTkLabel(
            window,
            fg_color = '#064d23',
            image=None,
            text=None
        )
        self.dealerCardImage1.place(anchor="center", relx=0.325, rely=0.15)

        if self.igrok.getStake() <= 0 and self.igrok.getBank() <= 0:
            self.msg = CTkMessagebox(title="Проигрыш", message="Вы всё проиграли! \nПерезапускаем игру...", option_1="Ok")
            if self.msg.get() == "Ok":
                self.destroyWidgets()
                main = Main()

    def disableButton(self, button):
        #Выключение кнопки
        button.configure(fg_color='#222222', hover_color='#222222',command=lambda: None)

    def questionCommand(self):
        self.guide = CTkMessagebox(title="Справка", width=500, message="""“Blackjack” – это всемирно известная карточная игра “двадцать одно” или “очко”. \n
Те или иные карты в “Blackjack” приносят определённое количество очков, а главная задача – набрать 21 очко или максимально приблизиться к этой сумме, но не набрать больше. \n
Картам от двойки до десятки присваиваются очки соответственно от 2 до 10.
Все картинки (валет, дама и король), за исключением тузов, имеют ценность в 10 очков. 
Тузы же могут быть расценены как 11 или как 1 в случае перебора. \n
Удвоение - одна из возможностей игрока, при которой он удваивает свою ставку и дилер выдает ему еще одну карту, но возможности взять еще одну или удвоить ставку второй раз не дается.""")

    def doubleStake(self):
        #Удвоение ставки, как в блэк джеке
        self.igrok.setBank(self.igrok.getBank() - self.igrok.getStake())
        self.igrok.setStake(self.igrok.getStake() * 2)
        #Обновление текста
        self.stakeLabel.configure(text="Ваша ставка: \n" + str(int(self.igrok.getStake())))
        self.bankLabel.configure(text="Ваш банк: \n" + str(int(self.igrok.getBank())))
        #Выключение кнопок
        self.disableButton(self.doubleButton)
        self.disableButton(self.moreButton)
        self.igrok.takeCard(False)

    def moreCommand(self):
        self.disableButton(self.doubleButton)
        self.igrok.takeCard(False)

    def stopCommand(self):
        #Набор кард для дилера, пока его очки не превысят 16
        while self.dealer.getScore() <= 16:
            self.dealer.takeCard(False)
        #Выяснение результатов и отображение очков дилера
        if self.dealer.getScore() > self.igrok.getScore():
            self.stopGame(False, 1)
        elif self.dealer.getScore() == self.igrok.getScore():
            self.stopGame(False, 2)
        else:
            self.stopGame(True, 1)

    def sliderConfigure(self, value):
        #Изменение текста из-за слайдера
        if self.igrok.getBank() != 0:
            self.sliderLabel.configure(text = str(int(value)))

    def setCard(self, player):
        #Проверка на игрока или дилера
        if player == True:
            #Выставление карты со смещением
            exec(f"playerCardImage{len(self.igrok.cards)} = CTkLabel(window,fg_color = '#064d23',image=CTkImage(Image.open('images/cards/' + str(list(self.igrok.cards.keys())[-1]) + '.jpg'), size=(120, 200)),text='')")
            #Проверка не пересечение границы и при этом выставление нового ряда карт снизу
            if (0.325+((len(self.igrok.cards)-1)*0.125)) < 1:
                exec(f"playerCardImage{len(self.igrok.cards)}.place(anchor='center', relx=0.325+((len(self.igrok.cards)-1)*0.125), rely=0.55)")
            else:
                exec(f"playerCardImage{len(self.igrok.cards)}.place(anchor='center', relx=0.35+((len(self.igrok.cards)-7)*0.125), rely=0.6)")
        else:
            exec(f"dealerCardImage{len(self.dealer.cards)} = CTkLabel(window,fg_color = '#064d23',image=CTkImage(Image.open('images/cards/' + str(list(self.dealer.cards.keys())[-1]) + '.jpg'), size=(120, 200)),text='')")
            if (0.325+((len(self.igrok.cards)-1)*0.125)) < 1:
                exec(f"dealerCardImage{len(self.dealer.cards)}.place(anchor='center', relx=0.325+((len(self.dealer.cards)-1)*0.125), rely=0.15)")
            else:
                exec(f"dealerCardImage{len(self.dealer.cards)}.place(anchor='center', relx=0.35+((len(self.dealer.cards)-7)*0.125), rely=0.2)")

    def setStake(self):
        #Выставление стандартных значений, ставок
        global main
        global currentCards
        currentCards = allCards.copy()
        self.igrok.setScore()
        self.dealer.setScore()
        self.igrok.setStake(self.stakeSlider.get())
        
        #Проверка на наличие денег и не нулевой ставки
        if self.igrok.getStake() <= 0:
            self.msg = CTkMessagebox(title="Ставка", message="Ставка должна быть больше 0!")
            return

        #Выставление ставки, обновление текста
        self.stakeLabel.configure(text="Ваша ставка: \n" + str(int(self.igrok.getStake())))
        self.igrok.setBank(self.igrok.getBank() - self.igrok.getStake()) 
        self.bankLabel.configure(text="Ваш банк: \n" + str(int(self.igrok.getBank())))
        self.disableButton(self.stakeButton)
        self.stakeImage.configure(image=self.chipsImage)

        #Включение возможных кнопок, проверка на возможность удваивания ставки
        if self.igrok.getStake() <= self.igrok.getBank():
            self.doubleButton.configure(fg_color = "#CCCC00", hover_color = "#888800", command=self.doubleStake)
        self.moreButton.configure(fg_color = "#BB0000", hover_color = "#770000", command=self.moreCommand)
        self.stopButton.configure(fg_color = "#0000BB", hover_color = "#000077", command=self.stopCommand)

        #Выдача карт по очереди, с изменением словаря текущих карт для избежания повторений
        self.igrok.takeCard(False)

        self.dealer.takeCard(True)

        self.igrok.takeCard(False)

        self.dealer.takeCard(False)

        self.scorePlayerLabel.configure(text="Ваши очки: " + str(int(self.igrok.getScore())))   

    def stopGame(self, player, result):
        #Остановка игры, проверка полученных результатов
        self.scoreDealerLabel.configure(text="Очки дилера: " + str(int(self.dealer.getScore())))
        self.dealer.setScore()
        self.dealerCardImage1.configure(image=CTkImage(Image.open("images/cards/" + str(list(self.dealer.cards.keys())[0]) + ".jpg"), size=(120, 200)))
        #Обновление окна, и задержка на 2.5 секунды, для того чтобы посмотреть карты дилера
        #Так как sleep вешает весь интерфейс tkinter, поэтому я использую update() для обновления окна до задержки (.after() выдает такой же эффект, а использовать async io не разрешено)
        self.dealerCardImage1.update()
        sleep(2.5)
        self.destroyWidgets()

        #Начисление выигрыша при победе или возвращение ставки при ничьей
        if result == 0:
            if player == False:
                self.igrok.setBank(self.igrok.getBank() + self.igrok.getStake() * 2) 
        elif result == 1:
            if player == True:
                if self.igrok.getScore() == 21 and len(self.igrok.cards) == 2:
                    self.igrok.setBank(self.igrok.getBank() + self.igrok.getStake() * 1.5)
                else:
                    self.igrok.setBank(self.igrok.getBank() + self.igrok.getStake() * 2)
        else:
            self.igrok.setBank(self.igrok.getBank() + self.igrok.getStake())

        #Обнуление переменных и обновление окна и текста ставки
        self.igrok.setStake()
        self.igrok.setScore()
        self.igrok.cards = {}
        self.dealer.cards = {}
        self.setWidgets()
        
    def destroyWidgets(self):
        #Уничтожение всех объектов tkinter (виджетов)
        for widget in window.winfo_children():
            widget.destroy()

class Player:
    #Инициализация необходимых переменных
    __bank = 5000
    __stake = 0
    __score = 0
    cards = {}
    #Переменная player для выявления игрока
    player = False
    
    def __init__(self, bank=5000, player=False):
        #Инициализация Player
        self.__bank = bank
        self.__score = 0
        self.cards = {}
        self.player = player

    #Геттеры
    def getScore(self):
        return self.__score

    def getStake(self):
        return self.__stake

    def getBank(self):
        return self.__bank

    #Сеттеры
    def setScore(self, score=0):
        self.__score = score

    def setStake(self, stake=0):
        self.__stake = stake

    def setBank(self, bank=0):
        self.__bank = bank

    def takeCard(self, back):
        #Подбор карты
        global currentCards
        r = list(currentCards.keys())[randint(0, len(currentCards)-1)]
        score = currentCards[r]
        self.cards[r] = score
        self.__score += score
        currentCards.pop(r, None)

        #Выдача скрытой карты, либо для дилера, либо для игрока (Прописал для игрока для возможного имплементирования в дальнейшую игру)
        if back == True and self.player == False:
            main.dealerCardImage1.configure(image=main.backImage)
        elif back == True and self.player == True:
            main.playerCardImage1.configure(image=main.backImage)
        else:
            main.setCard(self.player)

        #Проверка на возможность преобразовать туз в 1 очко для избежания перебора
        while self.__score > 21 and 11 in list(self.cards.values()):
            self.cards[str(list(self.cards.keys())[list(self.cards.values()).index(11)])] = 1
            self.__score -= 10
            
        #Показ только очков игрока
        if self.player == True:
            main.scorePlayerLabel.configure(text="Ваши очки: " + str(int(self.__score)))
            
        #Проверка на перебор 
        if self.__score > 21:
            main.stopGame(self.player, 0)

if __name__ == '__main__':
    main = Main()
    window.mainloop()
