import geoip2.database


class geoip2Reader:
    def __init__(self,
                 lan,
                 cityFile="../resources/GeoLite2-City.mmdb",
                 asnFile="../resources/GeoLite2-ASN.mmdb"
                 ):
        self.cityReader = geoip2.database.Reader(cityFile)
        self.asnReader = geoip2.database.Reader(asnFile)
        self.lan = lan
        # self.asnFile = asnFile

    def load(self, ip):
        cityResponse = self.cityReader.city(ip)
        asnResponse = self.asnReader.asn(ip)
        return cityResponse, asnResponse

    def getAll(self, ip):
        city, asn = self.load(ip)
        ll = [self.cityReader, self.asnReader, city, asn]
        self.close(ll)

    def close(self, linkList):
        for l in linkList:
            l.close()


if __name__ == "__main__":
    g2r = geoip2Reader("zh-CN")
    g2r.getAll("1.1.1.1")
