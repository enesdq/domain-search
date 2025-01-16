#!/usr/bin/env python3
import argparse
import re
import requests
import urllib3

from bs4 import BeautifulSoup
from Color_Console import ctext

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser()
parser.add_argument('-u')
parser.add_argument('-f')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-o', nargs="?")
group.add_argument('-v', action="store_true")
args = parser.parse_args()

SUBDOMAINS_ENUMERATED = []
SITES_VISITED = []
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}

def find_scripts(url):
    if url in SITES_VISITED:
        return False
    SITES_VISITED.append(url)
    r = is_live(url)
    if not r:
        return False
    soup = BeautifulSoup(r.text, 'lxml')
    script_tags = soup.find_all('script')

    for script_tag in script_tags:
        if is_src(script_tag.attrs):
            script_src = script_tag.attrs['src']
            if script_src[0] == "/" and script_src[1] != "/":
                parsed_url = url + script_src
            elif script_src[0] == "/" and script_src[1] == "/":
                parsed_url = script_src[2:]
            elif "http" not in script_src:
                parsed_url = url + "/" + script_src
            else:
                parsed_url = re.search("[a-zA-Z0-9-_.]+\.[a-zA-Z]{2,}", script_src).group()
            try:
                find_subdomains(requests.get('http://' + parsed_url, verify=False, headers=HEADERS).text, url)
                src_url = re.search("[a-zA-Z0-9-_.]+\.[a-zA-Z]{2,}", script_src).group()
                if src_url not in SUBDOMAINS_ENUMERATED:
                    SUBDOMAINS_ENUMERATED.append(src_url)
            except:
                pass
        else:
            find_subdomains(script_tag, url)

def is_src(tag):
    return isinstance(tag, dict) and 'src' in tag

def is_live(url):
    try:
        r = requests.get('http://' + str(url), verify=False, headers=HEADERS)
        return r
    except:
        return False

def find_subdomains(script, url):
    subdomain_regex = re.findall(r"[%\\]?[a-zA-Z0-9][a-zA-Z0-9-_.]*\." + url, str(script))
    for subdomain in subdomain_regex:
        if "%" in subdomain:
            while "%25" in subdomain:
                subdomain = subdomain.replace("%25", "%")
            parsed_subdomain = subdomain.split("%")[-1][2:]
        elif "\\x" in subdomain:
            parsed_subdomain = subdomain.split("\\x")[-1][2:]
        elif "\\u" in subdomain:
            parsed_subdomain = subdomain.split("\\u")[-1][4:]
        else:
            parsed_subdomain = subdomain
        if parsed_subdomain not in SUBDOMAINS_ENUMERATED:
            if args.v:
                ctext(subdomain, "green")
            SUBDOMAINS_ENUMERATED.append(subdomain)
    if len(list(set(SUBDOMAINS_ENUMERATED))) != len(list(set(SITES_VISITED))):
        for site in SUBDOMAINS_ENUMERATED:
            find_scripts(site)

def ascii_banner():
    ctext("", "red")

def main():
    ascii_banner()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if args.f:
        url_list = open(args.f,"r")
        for URL in url_list.readlines():
            find_scripts(URL.strip())
    elif args.u:
        find_scripts(args.u)
    else:
        raise Exception()
    if args.o:
        with open(args.o, "w") as f:
            f.write("".join(x + "\n" for x in SUBDOMAINS_ENUMERATED))

if __name__ == '__main__':
    main(