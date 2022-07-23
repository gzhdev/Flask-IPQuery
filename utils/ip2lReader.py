import IP2Location


class IP2LocationReader:

    def __init__(self, db_file="../resources/IP2LOCATION-DB25.BIN", SHARED_MEMORY=False):
        if SHARED_MEMORY:
            db = IP2Location.IP2Location(self.db, "SHARED_MEMORY")
        else:
            db = IP2Location.IP2Location(self.db)

    def get_info(self, ip):
        record = self.db.get_all(ip)
        return record



'''
    Cache the database into memory to accelerate lookup speed.
    WARNING: Please make sure your system have sufficient RAM to use this feature.
'''
if __name__ == '__main__':
    # # database = IP2Location.IP2Location(os.path.join("data", "IPV6-COUNTRY.BIN"), "SHARED_MEMORY")
    database = IP2Location.IP2Location("../resources/IP2LOCATION-DB25.BIN")
    rec = database.get_all("180.116.143.213")

    print("国家代码 ", rec.country_short)
    print("国家名称 ", rec.country_long)
    print("地区名称 ", rec.region)
    print("城市名称 ", rec.city)
    print("ISP名称 ", rec.isp)
    print("纬度 ", rec.latitude)
    print("经度 ", rec.longitude)
    print("域名 ", rec.domain)
    print("邮政编码 ", rec.zipcode)
    print("时区 ", rec.timezone)
    print("连接速度 ", rec.netspeed)
    print("IDD国家代码 ", rec.idd_code)
    print("区号 ", rec.area_code)
    print("气象站代码 ", rec.weather_code)
    print("气象站名称 ", rec.weather_name)
    print("移动国家代码 ", rec.mcc)
    print("移动网络代码 ", rec.mnc)
    print("手机运营商 ", rec.mobile_brand)
    print("海拔 ", rec.elevation)
    print("使用类型 ", rec.usage_type)
    print("地址类型 ", rec.address_type)
    print("类别 ", rec.category)


