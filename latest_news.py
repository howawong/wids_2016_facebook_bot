import requests
from lxml import etree, html
import json
import re
def fetch_news(provider):
    print provider
    if provider.lower() == "bbc":
        url = "http://feeds.bbci.co.uk/news/rss.xml"
    else:
        url = "http://news.mingpao.com/rss/pns/s00001.xml"
    root = etree.fromstring(requests.get(url).content)
    items = root.xpath("//item")
    if len(items) > 5:
        items = items[0:5]
    message_bodies = []
    for item in items:
        title = item.xpath(".//title/text()")[0]
        description = item.xpath(".//description/text()")[0]
        link  = item.xpath(".//link/text()")[0]
        text = item.xpath(".//title/text()")[0] + "\n" + item.xpath(".//link/text()")[0] + "\n" + item.xpath(".//description/text()")[0]
        attachment = {"type": "template", "payload": {"template_type": "generic", "elements":[{"title": title, "subtitle": description, "buttons":[{"type":"web_url","url": link, "title": "Read more."}]}]}}
        message_bodies.append({'attachment': attachment})
    return message_bodies
print json.dumps(fetch_news(""))
