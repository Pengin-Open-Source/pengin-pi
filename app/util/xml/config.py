import os
from dotenv import load_dotenv
load_dotenv()
import xml.etree.ElementTree as ET
import re
from datetime import datetime

path = os.path.join(os.getcwd(), '../app/static/sitemap.xml')
tree = ET.parse('sitemap.xml')
root = tree.getroot()
domain = os.getenv('URL')

with open('robots.txt','r') as file:
    def parse(line):
        out = re.search(':', line)
        
        if out:
            return {line[:out.start()]: line[out.start()+1:]}
    
    robots = [parse(line) for line in file.readlines() if parse(line) is not None]
    file.close()

def load_defaults(url=domain, protocol='https'):
    url = ET.Element('url')
    home = ET.Element('loc')
    home.text = f"{protocol}://{url}/"
    home_lastmod = ET.Element('lastmod')
    home_lastmod.text = datetime.utcnow().strftime("%Y-%m-%d")  # update the lastmod to current date
    home_changefreq = ET.Element('changefreq')
    home_changefreq.text = "weekly"
    home_priority = ET.Element('priority')
    home_priority.text = '1.0'
    about = ET.Element('loc')
    about.text = f"{protocol}://{url}/about"
    about_lastmod = ET.Element('lastmod')
    about_lastmod.text = datetime.utcnow().strftime("%Y-%m-%d")  # update the lastmod to current date
    about_changefreq = ET.Element('changefreq')
    about_changefreq.text = "weekly"
    about_priority = ET.Element('priority')
    about_priority.text = '0.8'
    forum = ET.Element('loc')
    forum.text = f"{protocol}://{url}/forums"
    forum_lastmod = ET.Element('lastmod')
    forum_lastmod.text = datetime.utcnow().strftime("%Y-%m-%d")  # update the lastmod to current date
    forum_changefreq = ET.Element('changefreq')
    forum_changefreq.text = "daily"
    forum_priority = ET.Element('priority')
    forum_priority.text = '0.5'
    url.append(home)
    url.append(home_lastmod)
    url.append(home_changefreq)
    url.append(home_priority)
    url.append(home_lastmod)
    url.append(home_changefreq)
    url.append(home_priority)
    url.append(forum)
    url.append(forum_lastmod)
    url.append(forum_changefreq)
    url.append(forum_priority)
    url.append(forum_lastmod)
    url.append(forum_changefreq)
    url.append(forum_priority)
    url.append(about)
    url.append(about_lastmod)
    url.append(about_changefreq)
    url.append(about_priority)
    url.append(about_lastmod)
    url.append(about_changefreq)
    url.append(about_priority)
    root.append(url)


def load_blogs(blogs, url=domain, protocol='https'):
    for blog in blogs:
        url = ET.Element('url')
        loc = ET.Element('loc')
        loc.text = f"{protocol}://{url}/products/{blog.name}"
        lastmod = ET.Element('lastmod')
        lastmod.text = datetime.utcnow().strftime("%Y-%m-%d")  # update the lastmod to current date
        changefreq = ET.Element('changefreq')
        changefreq.text = "weekly"
        priority = ET.Element('priority')
        priority.text = '0.7'
        url.append(loc)
        url.append(lastmod)
        url.append(changefreq)
        url.append(priority)
        root.append(url)


def load_products(products, url=domain, protocol='https'):
    for product in products:
        url = ET.Element('url')
        loc = ET.Element('loc')
        loc.text = f"{protocol}://{url}/products/{product.name}"
        lastmod = ET.Element('lastmod')
        lastmod.text = datetime.utcnow().strftime("%Y-%m-%d")  # update the lastmod to current date
        changefreq = ET.Element('changefreq')
        changefreq.text = "monthly"
        priority = ET.Element('priority')
        priority.text = '0.9'
        url.append(loc)
        url.append(lastmod)
        url.append(changefreq)
        url.append(priority)
        root.append(url)

def update(name, PATH, new=None, url=domain, protocol='https'):
    n_tree = ET.parse(path)
    n_root = n_tree.getroot()
    if new:
        for URL in n_root.iter('url'):
            if name in URL.find('loc').text:
                URL.find('loc').text = f"{protocol}://{url}/{PATH}/{new}"
                URL.find('loc').text = datetime.utcnow().strftime("%Y-%m-%d")
    else:
        for URL in n_root.iter('url'):
            if name in URL.find('loc').text:
                URL.find('loc').text = f"{protocol}://{url}/{PATH}/{name}"
                URL.find('loc').text = datetime.utcnow().strftime("%Y-%m-%d")
    n_tree.write(path)
        

def save():
    tree.write(path)

if __name__ == "__main__":
    """Used for running a manual config option"""
    pass