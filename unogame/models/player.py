class Player:
    # number : 플레이어 넘버 / type : 어떤 플레이어 종류인지 / hand : 플레이어의 패 / turn : 플레이어 객체의 턴
    def __init__(self, number, hand, turn):
        self.number = number
        self.hand = hand
        self.turn = turn
        self.uno = "unactive"  # unactive : 손패가 2장 이상, active : 손패가 1장이고, 우노버튼 누르면 영향, expired : 손패가 1장이고 우노버튼 눌러도 영향 없음