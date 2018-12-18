class Movie():
    def __init__(self, id, title, desc, star, price, director, cast, pic,video):
        self.id = id
        self.title = title
        self.desc = desc
        self.star = star
        self.price = price
        self.pic = pic
        self.video = video
        self.cast = cast
        self.director = director

    def int_star(self):
        return int(self.star)
