import requests
from lxml import etree, html
import re
def fetch_weather():
    url = "http://rss.weather.gov.hk/rss/CurrentWeather.xml"
    feed = requests.get(url)
    root = etree.fromstring(feed.content) 
    summary = root.xpath("//description")[1]
    html_root =  html.fromstring(summary.text)
    img = html_root.xpath("//img/@src")[0].strip()
    print "image url [%s]" % img
    lines = "\n".join([s.strip() for s in html_root.xpath("//p/text()")]).split("\n")
    lines = [l.strip() for l in lines]
    temperature, humidity = [int(re.match('[^\d]*(\d+).*', s).group(1)) for s in lines[3:5]]
    
    

    for line in lines:
        print line
    return [{'text': 'Air Temperature %d C.\nHumidity:%d%%' % (temperature, humidity)}, {'attachment': {'type':'image', 'payload':{'url': img}}}]
