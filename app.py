from flask import Flask, render_template, request, redirect, url_for, make_response
from utils.qqwryReader import CzIp
from flask import jsonify
import IP2Location

app = Flask(__name__)
cz = CzIp("resources/qqwry.dat")
app.config['JSON_AS_ASCII'] = False
database = IP2Location.IP2Location("resources/IP2LOCATION-LITE-DB11.BIN", "SHARED_MEMORY")


@app.route('/myip', methods=['GET', 'POST'])
def myip():
    ip = request.remote_addr
    rec = database.get_all(ip)
    czInfo = {
        "ip": ip,
        "database_version": cz.get_version(),
        "ip_range": cz.get_ip_range(ip),
        "addresses": cz.get_addr_by_ip(ip)
    }
    i2lInfo = {
        "IP": ip,
        "国家名称（短）": rec.country_short,
        "国家名称（长）": rec.country_long,
        "地区名称 ": rec.region,
        "城市名称 ": rec.city,
        "纬度 ": rec.latitude,
        "经度 ": rec.longitude,
        "邮政编码 ": rec.zipcode,
        "时区": rec.timezone
    }
    # msg = jsonify(ipInfo)
    return render_template("myip.html", cz=czInfo, i2l=rec)


@app.route('/api/<askIp>', methods=['GET', 'POST'])
def api(askIp):
    if askIp == "myip":
        ip = request.remote_addr
    else:
        ip = askIp
    rec = database.get_all(ip)
    czInfo = {
        "ip": ip,
        "database_version": cz.get_version(),
        "ip_range": cz.get_ip_range(ip),
        "addresses": cz.get_addr_by_ip(ip)
    }
    i2lInfo = {
        "IP": ip,
        "国家名称（短）": rec.country_short,
        "国家名称（长）": rec.country_long,
        "地区名称 ": rec.region,
        "城市名称 ": rec.city,
        "纬度 ": rec.latitude,
        "经度 ": rec.longitude,
        "邮政编码 ": rec.zipcode,
        "时区": rec.timezone
    }
    ipInfo = {
        "纯真数据库": czInfo,
        "IP2Location数据库": i2lInfo
    }
    msg = jsonify(ipInfo)
    return msg


if __name__ == '__main__':
    app.run(debug=True)
