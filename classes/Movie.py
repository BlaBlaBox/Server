class Movie():
    def __init__(self, movie_id, title, release_year, added_at, duration, star, desc, pic, video, rent_price, purc_price, cast):
        self.id = movie_id
        self.title = title
        self.release_year = release_year
        self.added_at = added_at
        self.duration = duration
        self.star = star
        self.desc = desc
        self.pic = pic
        self.video = video
        self.rent_price = rent_price
        self.purc_price = purc_price
        self.cast = cast


    def int_star(self):
        return int(self.star)
