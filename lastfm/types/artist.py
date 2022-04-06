class Artist:
    def __init__(self, url: str, name: str, mbid: str) -> None:
        self.url = url
        self.name = name
        self.mbid = mbid

    def as_dict(self) -> dict:
        return {
            "url": self.url,
            "name": self.name,
            "mbid": self.mbid
        }
