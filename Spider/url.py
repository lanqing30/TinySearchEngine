
class URL(object):
    def __init__(self, url, id_, title,text, links_, time):
        self.url = url
        self.id = id_
        self.title = title
        self.text = text
        self.links = links_
        self.time = time
        self.links_id = []
        self.rank = 0.0
