class Movie():
    def __init__(self, id, title, desc, star, price, pic,video,cast):
        self.id = id
        self.title = title
        self.desc = desc
        self.star = star
        self.price = price
        self.pic = pic
        self.video = video
        self.cast = cast


    def int_star(self):
        return int(self.star)
