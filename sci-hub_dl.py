import requests
import re
import os, sys
try:
    print("Target page > \033[35m", end='')
    pdf_page_url = input()
    print("\033[0m",end='')
    print("[\033[34m●\033[0m] Finding DOI from page.",end='\r')
    page = requests.get(pdf_page_url).text
    doi_pattern = re.compile(r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>?;])\S)+)\b')
    doi = doi_pattern.search(page)
    print("[\033[32m●\033[0m] Found DOI \033[32m\033[45m{}\033[0m".format(doi.group(0)))
    doi = doi.group(0)

    print("[\033[34m●\033[0m] Finding PDF file",end='\r')
    r = requests.get("https://sci-hub.mksa.top/{}".format(doi), verify=False)
    pattern = re.compile(
        "\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\/(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*?)\.pdf")
    pdf_page_url = pattern.search(r.text)
    print("[\033[32m●\033[0m] Found url of PDF file at \033[33m\033[45mhttps:{}\033[0m".format(pdf_page_url.group(0)))
    print("[\033[34m●\033[0m] Downloading from \033[35mhttps:{}\033[0m".format(pdf_page_url.group(0)),end='\r')
    r = requests.get("https:" + pdf_page_url.group(0))
    filename = re.findall("\/([-a-zA-Z0-9()@:%_\+.~#?&=]*?\.pdf)$", pdf_page_url.group(0))
    with open(os.path.join(os.environ['HOME'], "Downloads", filename[0]), 'wb') as pdf:
        pdf.write(r.content)
        pdf.flush()
        pdf.close()
    print("\033[2K",end='\r')
    print("[\033[32m●\033[0m] Downloaded as \033[35m{}\033[0m".format(filename[0]))
    print("[\033[32m●\033[0m] Openning \033[35m{}\033[0m".format(filename[0]))
    os.startfile(os.path.abspath(os.path.join(os.environ['HOME'], "Downloads", filename[0])))
except:pass
os.remove(sys.argv[0])
