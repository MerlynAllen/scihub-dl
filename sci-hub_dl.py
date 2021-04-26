import requests
import re
import os
import sys
os.system("")


def fetchDOI(pdf_page_url):
    print("\033[0m", end='')
    print("[\033[34m●\033[0m] Finding DOI from page.", end='\r')
    page = requests.get(pdf_page_url).text
    doi_pattern = re.compile(
        r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>?;])\S)+)\b')
    doi = doi_pattern.search(page)
    try:
        print("[\033[32m●\033[0m] Found DOI \033[32m\033[45m{}\033[0m".format(doi.group(0)))
    except AttributeError:
        print("[\033[33m●\033[0m] Unable to find DOI.")
    return doi.group(0)


def fetchPDF(doi):
    print("[\033[34m●\033[0m] Finding PDF file", end='\r')
    r = requests.get("https://sci-hub.se/{}".format(doi), verify=False)
    pattern = re.compile(
        "\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\/(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*?)\.pdf")
    pdf_page_url = pattern.search(r.text)
    try:
        print("[\033[32m●\033[0m] Found url of PDF file at \033[33m\033[45mhttps:{}\033[0m".format(
        pdf_page_url.group(0)))
    except AttributeError:
        print("[\033[33m●\033[0m] Unable to find PDF.")
    return pdf_page_url


def downloadPDF(pdf_page_url):
    print("[\033[34m●\033[0m] Downloading from \033[35mhttps:{}\033[0m".format(
        pdf_page_url.group(0)), end='\r')
    r = requests.get("https:" + pdf_page_url.group(0))
    filename = re.findall(
        "\/([-a-zA-Z0-9()@:%_\+.~#?&=]*?\.pdf)$", pdf_page_url.group(0))
    with open(os.path.join(os.environ['HOME'], "Downloads", filename[0]), 'wb') as pdf:
        pdf.write(r.content)
        pdf.flush()
        pdf.close()
    print("\033[2K", end='\r')
    print("[\033[32m●\033[0m] Downloaded as \033[35m{}\033[0m".format(filename[0]))
    return filename[0]
    pass


def startFile(filename):
    os.startfile(os.path.abspath(os.path.join(
        os.environ['HOME'], "Downloads", filename)))


def interactiveMode():
    print("Target page > \033[35m", end='')
    URL = input()
    startFile(downloadPDF(fetchPDF(fetchDOI(URL))))


try:
    if len(sys.argv) > 1:
        if "--doi" in sys.argv:
            try:
                DOI = sys.argv[sys.argv.index("--doi") + 1]
                startFile(downloadPDF(fetchPDF(DOI)))
            except IndexError:
                print("Needs parameter: <DOI>. Entering interactive mode.")
                interactiveMode()
        elif "--url" in sys.argv:
            try:
                URL = sys.argv[sys.argv.index("--url") + 1]
                startFile(downloadPDF(fetchPDF(fetchDOI(URL))))
            except IndexError:
                print("Needs parameter: <URL>. Entering interactive mode.")
                interactiveMode()
        else:
            print("Invalid syntax. Entering interactive mode.")
            interactiveMode()
    else:
        interactiveMode()

except KeyboardInterrupt:
    print("Cancelled.")
except:
    print("Unknown error occurred. Program exiting.")
    os.system("pause")
print("\033[0m", end="")
os.remove(sys.argv[0])
