import requests
from lxml import etree, html
import re
import random
def fetch_restro(place):
    url = "http://www.openrice.com/en/hongkong/restaurants?where=" + place
    headers = {'User-agent': 'Mozilla/5.0'}
    req = requests.get(url, headers = headers)
    root = html.fromstring(req.content) 
    link_nodes = root.xpath("//div[@class=\"content-wrapper\"]/div/h2/a")
    links  = []
    titles = []
    images = []
    addresses = []    

    for link_node in link_nodes:
        titles.append(link_node.xpath("text()")[0])
        links.append(link_node.xpath("@href")[0])
    detail_wrapper_nodes = root.xpath("//div[@class=\"details-wrapper\"]")
    for detail_wrapper_node in detail_wrapper_nodes:
        divs = detail_wrapper_node.xpath("div")
        image_style = divs[0].xpath("a/div/@style")[0]
        img_url = re.match("background-image: url\('([^']*)'\)", image_style).group(1)
        images.append(img_url)
        address =  " ".join([s.strip() for s in divs[1].xpath("div/div/span//text()")])
        addresses.append(address)

    indices = range(0, len(titles))
    random.shuffle(indices)
    indices = indices[0:5]
    message_bodies = []
    for i in indices:
        link = links[i]
        address = addresses[i]
        title = titles[i]
        image = images[i]
        buttons = [{"type": "web_url", "url": "http://www.openrice.com/" + link, "title": "Read more."}]
        elements = [{"title": title, "subtitle": address, "buttons": buttons, "image_url": image}]
        attachment = {"type":"template", "payload": {"template_type":"generic", "elements": elements}}
        message_bodies.append({'attachment': attachment})
    return message_bodies
print fetch_restro("Mongkok")
