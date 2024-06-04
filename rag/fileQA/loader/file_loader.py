from abc import ABC,abstractmethod
from rag.fileQA.base import Document,MetaData
import logging

import requests
from bs4 import BeautifulSoup
import os
import requests
logger = logging.getLogger(__name__)


class BaseDataLoader(ABC):
    path = None

    @abstractmethod
    def load(self):
        raise

    def parse(self):
        raise


class PDFLoader(BaseDataLoader, ABC):

    def __init__(self,path):
        self.path = path

    def load(self):
        pass


class PDFLoaderUnstructured(BaseDataLoader, ABC):

    def __init__(self,path):
        self.path = path

    def load(self):
        pass


class CSVLoader(BaseDataLoader,ABC):

    def __init__(self,path):
        self.path = path

    def load(self):
        pass


class DocLoader(BaseDataLoader,ABC):

    def __init__(self,path):
        self.path = path

    def load(self):
        pass


class DocxLoader(BaseDataLoader,ABC):

    def __init__(self, path):
        self.path = path


class ExcelLoader(BaseDataLoader,ABC):

    def __init__(self, path):
        self.path = path


class JsonLoader(BaseDataLoader,ABC):

    def __init__(self, path):
        self.path = path


class TxtLoader(BaseDataLoader,ABC):

    def __init__(self, path):
        self.path = path

    def load(self):
        text = ""
        try:
            with open(self.path,'r') as f:
                text = f.read()
        except:
            logger.debug("file read fail, we will return empty file", self.path)
        if len(text)==0:
            raise f"{self.path} has not content"
        data = MetaData(meta=text, source={"path":self.path, "type":"txt"})
        return Document([data], source=self.path)

class HtmlLoader(BaseDataLoader,ABC):


    def __init__(self,url,short_lens=20):
        self.path = url
        self.short_lens = short_lens

    def load(self):
        text = ""
        response = requests.get(self.path)
        if response.status_code == 200:
            try:
                encoding = response.apparent_encoding
                if encoding:
                    response.encoding = encoding
                else:
                    response.encoding = 'utf-8'  # 或者你可以使用一个默认值

                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                paragraphs = soup.find_all('p')

                for i, paragraph in enumerate(paragraphs):
                    now_text = paragraph.get_text(strip=True)
                    if len(now_text)>self.short_lens:
                        text = text + now_text + "\n"
            except:
                print("warning:has no sparse anything!")
        else:
            raise print(f'Failed to retrieve the page. Status code: {response.status_code}')
        data = MetaData(meta=text, source={"path":self.path, "type":"url"})
        return Document([data], source=self.path)

