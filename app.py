from flask import Flask, render_template, request, redirect, url_for, make_response
from utils.qqwryReader import CzIp
from flask import jsonify
import IP2Location
import geoip2.database
import IPy

app = Flask(__name__)
cz = CzIp("resources/qqwry.dat")
app.config['JSON_AS_ASCII'] = False
database = IP2Location.IP2Location("resources/IP2LOCATION-LITE-DB11.BIN", "SHARED_MEMORY")


def getIP(askIp):
    if askIp == "myip":
        ip = request.remote_addr
        # ips = request.headers.get("X-Forwarded-For")
        # ip = ips.split(', ')[0]
    else:
        ip = askIp
    return ip


def czReader(ip):
    czInfo = {
        "ip": ip,
        "database_version": cz.get_version(),
        "ip_range": cz.get_ip_range(ip),
        "addresses": cz.get_addr_by_ip(ip)
    }
    return czInfo


def i2lReader(ip):
    rec = database.get_all(ip)
    i2lInfo = {
        "IP": ip,
        "country_s ": rec.country_short,
        "country_l ": rec.country_long,
        "region ": rec.region,
        "city ": rec.city,
        "latitude ": rec.latitude,
        "longitude ": rec.longitude,
        "zipcode ": rec.zipcode,
        "timezone ": rec.timezone
    }
    return i2lInfo


def geoip2Reader(ip):
    geo2Info = {}
    with geoip2.database.Reader('resources/GeoLite2-City.mmdb') as cityReader:
        try:
            cityResponse = cityReader.city(ip)
            geo2Info['ip'] = ip
            geo2Info['continent_code'] = cityResponse.continent.code
            geo2Info['continent'] = cityResponse.continent.names['zh-CN']
            geo2Info['country_code'] = cityResponse.country.iso_code
            geo2Info['country'] = cityResponse.country.names['zh-CN']
            geo2Info['state'] = cityResponse.subdivisions.most_specific.name
            geo2Info['state_code'] = cityResponse.subdivisions.most_specific.iso_code
            geo2Info['city'] = cityResponse.city.name
            geo2Info['latitude'] = str(cityResponse.location.latitude)
            geo2Info['longitude'] = str(cityResponse.location.longitude)
            geo2Info['metro_code'] = str(cityResponse.location.metro_code)
            geo2Info['time_zone'] = cityResponse.location.time_zone
            geo2Info['zip_code'] = cityResponse.postal.code
            geo2Info['network'] = str(cityResponse.traits.network)
        except geoip2.errors.AddressNotFoundError:
            print("IP do not found in city database!")
            geo2Info['continent_code'] = "IP do not found in city database!"
            geo2Info['continent'] = "IP do not found in city database!"
            geo2Info['country_code'] = "IP do not found in city database!"
            geo2Info['country'] = "IP do not found in city database!"
            geo2Info['state'] = "IP do not found in city database!"
            geo2Info['state_code'] = "IP do not found in city database!"
            geo2Info['city'] = "IP do not found in city database!"
            geo2Info['latitude'] = "IP do not found in city database!"
            geo2Info['longitude'] = "IP do not found in city database!"
            geo2Info['metro_code'] = "IP do not found in city database!"
            geo2Info['time_zone'] = "IP do not found in city database!"
            geo2Info['zip_code'] = "IP do not found in city database!"
            geo2Info['network'] = "IP do not found in city database!"

    with geoip2.database.Reader('resources/GeoLite2-ASN.mmdb') as asnReader:
        try:
            asnResponse = asnReader.asn(ip)
            geo2Info['ASN'] = str(asnResponse.autonomous_system_number)
            geo2Info['ASN_Organization'] = asnResponse.autonomous_system_organization
        except geoip2.errors.AddressNotFoundError:
            print("IP do not found in ASN database!")
            geo2Info['ASN'] = "IP do not found in ASN database!"
            geo2Info['ASN_Organization'] = "IP do not found in ASN database!"
    return geo2Info


@app.route('/<askIp>', methods=['GET', 'POST'])
def myip(askIp):
    ip = getIP(askIp)
    # if askIp == "myip":
    #     # ip = request.remote_addr
    #     ip = request.headers.get("X-Forwarded-For")
    # else:
    #     ip = askIp
    # ip = request.remote_addr
    try:
        version = IPy.IP(ip).version()
        if version == 4:
            czInfo = czReader(ip)
            rec = database.get_all(ip)
            geo2Info = geoip2Reader(ip)
            return render_template("myip.html", cz=czInfo, i2l=rec, geo2=geo2Info)
        elif version == 6:
            czInfo = {
                "ip": "IPv6 is not supported",
                "database_version": "IPv6 is not supported",
                "ip_range": "IPv6 is not supported",
                "addresses": "IPv6 is not supported"
            }
            rec = database.get_all(ip)
            geo2Info = geoip2Reader(ip)
            return render_template("myip.html", cz=czInfo, i2l=rec, geo2=geo2Info)
        else:
            return "IP格式非法"
    except Exception as e:
        return "IP格式非法"

    # rec = database.get_all(ip)
    # czInfo = czReader(ip)
    # geo2Info = geoip2Reader(ip)

    # return render_template("myip.html", cz=czInfo, i2l=rec, geo2=geo2Info)
    # return ip


@app.route('/api/<askIp>', methods=['GET', 'POST'])
def api(askIp):
    ip = getIP(askIp)
    # if askIp == "myip":
    #     # ip = request.remote_addr
    #     ips = request.headers.get("X-Forwarded-For")
    #     ip = ips.split(', ')[0]
    # else:
    #     ip = askIp
    support_lan = ["de", "en", "es", "fr", "ja", "pt-BR", "ru", "zh-CN"]
    # if language not in support_lan:
    #     language = "zh-CN"
    # rec = database.get_all(ip)
    # czInfo = czReader(ip)
    # i2lInfo = i2lReader(ip)
    # geo2Info = geoip2Reader(ip)
    try:
        version = IPy.IP(ip).version()
        if version == 4:
            czInfo = czReader(ip)
            i2lInfo = i2lReader(ip)
            geo2Info = geoip2Reader(ip)
            # return render_template("myip.html", cz=czInfo, i2l=rec, geo2=geo2Info)
        elif version == 6:
            czInfo = {
                "ip": "IPv6 is not supported",
                "database_version": "IPv6 is not supported",
                "ip_range": "IPv6 is not supported",
                "addresses": "IPv6 is not supported"
            }
            i2lInfo = i2lReader(ip)
            geo2Info = geoip2Reader(ip)
            # return render_template("myip.html", cz=czInfo, i2l=rec, geo2=geo2Info)
        else:
            return jsonify({"error": "IP格式非法"})
    except Exception as e:
        return jsonify({"error": "IP格式非法"})

    ipInfo = {
        "cz88 Database": czInfo,
        "IP2Location Database": i2lInfo,
        "Geoip2Lite Database": geo2Info
    }
    msg = jsonify(ipInfo)
    return msg


# cityReader.close()
# asnReader.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
