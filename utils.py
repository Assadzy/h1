import re
import json
import os
import errno
import uuid
def readFile(filepath):
    """
    Reads the file passed to this method.
    Returns json object if file extension is .json
    else returns str
    """
    try:
        with open(filepath) as file:
            if filepath.endswith('.json'):
                file = json.loads(file.read())
            else:
                file = file.read()
            return file
    except Exception as e:
        message = f"{e} NO CONFIGURATION FILE: {filepath}"
        return False


def create_file_name_from_url(url):
    return re.sub('\W+', '', url) + '.html'


def write_file(file_name_with_path, content):
    if not os.path.exists(os.path.dirname(file_name_with_path)):
        try:
            os.makedirs(os.path.dirname(file_name_with_path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    with open(file_name_with_path, "w", encoding='utf-8') as f:
        f.write(content)


def convert_to_text(url):
    import cv2
    from urllib.request import urlopen
    import numpy as np
    import pytesseract
    import time

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

    # image = cv2.imread('a.png', cv2.IMREAD_UNCHANGED)
    trans_mask = image[:, :, 3] == 0
    image[trans_mask] = [255, 255, 255, 255]
    # cv2.imwrite('test.png', image)
    text = pytesseract.image_to_string(image, lang='eng')
    return text.strip()
def generateuuid(url):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, url))
def savefile(url, filepath, response):
    try:
        os.mkdir(filepath)
    except Exception as ex:
        print('FAILED TO CREATE FOLDER_', ex)
        pass
    filename = re.sub('\W+','',url)+'.html'
    with open(filepath+'/'+filename, 'w', encoding='utf-8') as f:
        f.write(response.text)
    return filename
def doi_pmi(response):
    pub_med = re.findall("pubmed\/\\d+", response.text)
    if pub_med:
        pub_med = [x for x in pub_med]
    else:
        pub_med = []
    pmc = re.findall("((PMID|PMCID)\\s*:?\\s*\\d+)", response.text)  # PMC
    if pmc:
        pmc = [x if y in x else x+y for x, y in pmc]
    else:
        pmc = []
    pub_med = pub_med + pmc
    doi = ' | '.join([d.strip('.') for d in list(set(re.findall(r'.*?(10[.][0-9]{4,}(?:[.][0-9]+)*\/(?:(?!["&\'<>])\S)+).*?', response.text)))])
    pmid = ' | '.join(pub_med)
    return doi, pmid
# print(convert_to_text('https://www.pharm.muni.cz/a.aspx?a=dmF2ZXJrb3ZhdkBwaGFybS5tdW5pLmN6'))
