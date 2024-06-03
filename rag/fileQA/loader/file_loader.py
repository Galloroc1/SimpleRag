from abc import ABC,abstractmethod
from rag.fileQA.base import Document,MetaData
import logging

import os
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

