class Elevator():
    amount = 5
    current = 3

    def __init__(self, amount, current):

        self.amount = amount
        self.current = current

    def up(self):

        if self.current >= self.amount:
            print("Лифт не может подняться выше")
        else:
            self.current += 1
            print(f"Лифт поднимается на {self.current} этаж")

    def down(self):
        if self.current > 1:
            self.current -= 1
            print(f"Лифт опускается на {self.current} этаж")
        else:
            self.current = 1
            print("Лифт не может опуститься ниже")
