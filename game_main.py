import random


class Game:
    """Словарь с колодой и номиналом карт"""
    @classmethod
    def get_playing_cards(cls):
        playing_cards = {
            "6 пика": 6, "6 чирва": 6, "6 бубна": 6, "6 крести": 6,
            "7 пика": 7, "7 чирва": 7, "7 бубна": 7, "7 крести": 7,
            "8 пика": 8, "8 чирва": 8, "8 бубна": 8, "8 крести": 8,
            "9 пика": 9, "9 чирва": 9, "9 бубна": 9, "9 крести": 9,
            "10 пика": 10, "10 чирва": 10, "10 бубна": 10, "10 крести": 10,
            "Валет пика": 2, "Валет чирва": 2, "Валет бубна": 2, "Валет крести": 2,
            "Дама пика": 3, "Дама чирва": 3, "Дама бубна": 3, "Дама крести": 3,
            "Король пика": 4, "Король чирва": 4, "Король бубна": 4, "Король крести": 4,
            "Туз пика": 11, "Туз чирва": 11, "Туз бубна": 11, "Туз крести": 11
        }
        return playing_cards

    def __init__(self, name):
        self.name = name
        self._money = 100
        print(f"\n"'*******************'
              f"Добрейший вечерочек, {self.name}"
              f"*******************\n")

    def info(self):
        return self._money

    @staticmethod
    def separator(instanse):
        if isinstance(instanse, Dealer):
            print(f"\n*************** Ход {instanse.name} ****************")
        else:
            print(f"\n---------------- Ход {instanse.name} ----------------")

    def get_card(self, playing_cards):
        """Метод, который рандомно выдаёт карты и показывает их номинал"""

        player_card = random.choice(list(playing_cards.keys()))
        value = playing_cards.get(player_card)
        playing_cards.pop(player_card)
        print(f'"{self.name}, ваша карта: {player_card}, Номинал: {value}')
        return value

    def bets(self):
        """Реализация ставки"""
        print(f'Баланс вашего счета: {self.money}')
        while self.money > 0:
            bet = Player.top_down_balance(
                self, abs(int(input(f'{self.name} укажите сумму ставки: ')))
            )
            if bet:
                print(f"Ваша ставка: {bet}")
                return bet

    def top_down_balance(self, bet):
        """Метод, который снимает деньги с кошелька"""
        if self._money - bet < 0:
            print('Недостаточно средств')
            return False
        self._money = self._money - bet
        return bet

    def top_up_balance(self, howmany):
        """Метод, который пополняет кошелёк"""
        self._money = self._money + howmany
        return howmany

    @property
    def money(self):
        return self._money


class Player(Game):
    def get_result(self, value, bet, playing_cards):
        """Метод, который считает сумму очков"""
        card_sum = 1
        value_sum = value
        while card_sum != 5:
            player_input = input(f'Нужно дабавить карту {self.name} y/n?: ')
            if player_input == 'y':
                card_sum += 1
                value_sum += Player.get_card(self, playing_cards)
                if value_sum > 21:
                    perebor = f"Перебор {value_sum}"
                    print(perebor)
                    return perebor
                print(f'Сумма очков: {value_sum}\n')
            if player_input == 'n':
                break
        print(f'Итоговая сумма очков: {value_sum}\n')
        return value_sum


class Dealer(Player):

    def bets(self):
        bet = self._money  # можно обратиться через имя класса
        print(f'Банк: {bet}')
        return bet

    def get_result(self, value, bet, playing_cards):
        card_sum = 1
        value_sum = value
        while card_sum != 5:
            card_sum += 1
            value_sum += Dealer.get_card(self, playing_cards)
            if value_sum > 21:
                perebor = f"Перебор {value_sum}"
                print(perebor)
                return perebor
            elif value_sum == 21:
                break
            elif value_sum >= 17:
                break
            print(f'Сумма очков: {value_sum}\n')
        print(f'Итоговая сумма очков: {value_sum}\n')
        return value_sum


class BaseMixin:
    def new_game(self, player_name, dealer_name="Dealer"):
        player = Player(name=player_name)
        dealer = Dealer(name=dealer_name)

        # цикл пока не кончатся деньги в банке

        while player.money > 0:
            playing_cards = Game.get_playing_cards()
            Game.separator(player)
            a = player.get_result(player.get_card(playing_cards), player.bets(), playing_cards)
            Game.separator(dealer)
            b = dealer.get_result(dealer.get_card(playing_cards), dealer.bets(), playing_cards)
            if a > b:
                print("Игрок победил")




# class TestLoginProduction(BaseMixin):
#     def test_login_ok(self, name):
#         self.new_game(player_name=name)


player1 = BaseMixin()
player1.new_game("Михаил")

# прописать чтобы выдавало ответ кто победил и сколько денег заработал и сколько в банке денег

# # база данных с статистикой игрока
# player = Player(name=player_name)
# player.get_result(player.get_card(), player.bets())
# dealer = Dealer(name=dealer_name)
# dealer.get_result(dealer.get_card(), dealer.bets())
# player = Player("Mike")
# player.get_result(player.get_card(), player.bets())
# player_1 = Player("Kyzbass")
# player_1.get_result(player_1.get_card(), player_1.bets())
# player_3 = Player("Stason_Seltison")
# player_3.get_result(player_3.get_card(), player_3.bets())
# dealer = Dealer('Dealer_Bob')
# dealer.get_result(dealer.get_card(), dealer.bets())


# Банкир в свою очередь не может остановится на 15(петля)и обязан остановиться на 17(казна)

# Минимальная ставка 5$
# раздаётся по одной карте каждому игроку. Нужно набрать 21 очко, но не больше, либо больше, чем у твоего противника
# два туза - золотое очко. (при переборе туз идёт за одно очко по договорённости)
# банкир ставит максимальную ставку, всё, что у него есть
# раздаётся по одной карте банкиру и игроку, потом игрок делает ставку. Ставка не должна превышать суммы банка,
# потом просит карту, если количество очков достаточное (либо игрок набрал 21), то карты вскрываются, если игрок набрал 21,
# то автоматически выигрывает(в этом случае карты банкира не играют)
# Если у игрока достаточное количество очков и он вскрывается, то банкир вскрывает свою карту и набирает карты, до достаточного по его мнению
# количества. Если у банкира 16 очков, или менее, он обязан взять еще одну карту, если у банкира 17 очков, он не имеет права больше набирать карты
# При выигрыше игрок забирает свою ставку + сумму равную ставке из банка
# При проигрыше, ставка игрока идёт в банк
# При переборе игра останавливается
# Игра может продолжаться до того момента, пока не закончится банк, либо до того момента, пока не наступит
# "Стук" - это тот случай, когда в банке будет денег в три раза больше, чем было изначально
# https://www.youtube.com/watch?v=YxYx0eVeBK0 ссылка на правила игры
# максимальное количество карт, которые можно набрать =5
# Если у игрока выпало 21 и он взял ещё одну карту, то игрок проигрывает и платит штраф 10$
# Банкир при первой раздаче по одной карте, свою карту не показывает, когда игрок сказал хватит,
# то банкир открывает свою карту и набирает карты в открытую
# Игра вслепую с шестёркой реализовать
# Реализовать регистрацию и рейтинг игроков
# Суммарная ставка всех игроков за столом не может превышать сумму банка.


# Слово else, примененное в цикле for или while, проверяет, был ли произведен выход из цикла инструкцией break,
# или же "естественным" образом. Блок инструкций внутри else выполнится только в том случае,
# если выход из цикла произошел без помощи break.
#
# >>>
# >>> for i in 'hello world':
# ...     if i == 'a':
# ...         break
# ... else:
# ...     print('Буквы a в строке нет')
# ...
# Буквы a в строке нет
