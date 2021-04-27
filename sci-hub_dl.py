import requests
import re
import os
import sys
os.system("")

HOSTS = ["sci-hub.mksa.top", "sci-hub.do",
         "sci-hub.se", "sci-hub.ren", "sci-hub.st"]


def fetchDOI(pdf_page_url):
    print("\033[0m", end='')
    print("[\033[34m●\033[0m] Finding DOI from page.", end='\r')
    doi_pattern = re.compile(
        r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>?;])\S)+)\b')
    doi = doi_pattern.search(pdf_page_url)
    if doi:
        print("[\033[32m●\033[0m] Found DOI \033[32m\033[45m{}\033[0m".format(
            doi.group(0)))
        return doi.group(0)
    page = requests.get(pdf_page_url).text
    doi = doi_pattern.search(page)
    if doi:
        print("[\033[32m●\033[0m] Found DOI \033[32m\033[45m{}\033[0m".format(
            doi.group(0)))
    else:
        print("[\033[33m●\033[0m] Unable to find DOI.")
    return doi.group(0)


def fetchPDF(doi):
    print("[\033[34m●\033[0m] Finding PDF file.", end='\r')
    success = False
    for host in HOSTS:
        try:
            print("Trying {}...".format(host), end='\r')
            r = requests.get("https://{}/{}".format(host, doi), verify=False)
            success = True
            break
        except:
            print(
                "[\033[33m●\033[0m] Access to {} is unavailable. Retrying.".format(host), end='\r')
    if not success:
        print("[\033[33m●\033[0m] No host available.")
        raise KeyboardInterrupt
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
    try:
        r = requests.get("https:" + pdf_page_url.group(0))
    except:
        print("\033[2K", end='\r')
        print(
            "[\033[33m●\033[0m] Unable to download PDF file. Please copy the URL above and download manually.")
    filename = re.findall(
        "\/([-a-zA-Z0-9()@:%_\+.~#?&=]*?\.pdf)$", pdf_page_url.group(0))
    with open(os.path.join(os.environ['USERPROFILE'], "Downloads", filename[0]), 'wb') as pdf:
        pdf.write(r.content)
        pdf.flush()
        pdf.close()
    print("\033[2K", end='\r')
    print("[\033[32m●\033[0m] Downloaded as \033[35m{}\033[0m".format(filename[0]))
    return filename[0]
    pass


def startFile(filename):
    os.startfile(os.path.abspath(os.path.join(
        os.environ['USERPROFILE'], "Downloads", filename)))


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
    print("\033[2K", end='\r')
    print("[\033[33m●\033[0m] \033[33mCancelled.\033[0m")
except:
    print("\033[2K", end='\r')
    print("[\033[33m●\033[0m] \033[33mUnknown error occurred. Program exiting.\033[0m")
print("\033[0m", end="")
os.remove(sys.argv[0])
