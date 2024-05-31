from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Iterator, Any, Iterable


class BaseDataLoader(ABC):
    path = None

    @abstractmethod
    def load(self):
        raise

    def parse(self):
        raise


class MetaData:
    source = None
    meta = None
    size = None

    # def __call__(self, *args, **kwargs):
    #     pass

    def __init__(self, source, meta):
        self.source = source
        self.meta = meta

    def update_other_item(self, params: dict):
        for key, value in params.items():
            if key in self.__dict__:
                print(f"warning: the key {key} exist in MetaData!")
            setattr(self, key, value)

    def update_source(self, source: str):
        self.source = source

    def as_format(self):
        raise

    def __str__(self):
        strings = f"lens:{len(self.meta)}\t\tsource:{self.source}\nmeta:{[self.meta]}"
        return strings


class Document(Iterable):

    def __init__(self, datas: List[MetaData], source: str = None):
        self.datas = datas
        self.source = source

    def __iter__(self) -> Iterator[MetaData]:
        return iter(self.datas)

    def __getitem__(self, item: int) -> MetaData:
        return self.datas[item]

    def __str__(self):
        strings = f"lens:{len(self.datas)}\t\tsource:{self.source}"
        return strings
