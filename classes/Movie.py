class Movie():
    def __init__(self, title, star, price, pic):
        self.title = title
        self.star = star
        self.price = price
        self.pic = pic

    def int_star(self):
        return int(self.star)
