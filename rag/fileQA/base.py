from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Iterator, Any, Iterable
from typing import Union
from numpy import ndarray
import numpy as np


class MetaData:
    source = None
    meta = None
    size = None

    # def __call__(self, *args, **kwargs):
    #     pass

    def __init__(self, meta:str, source:dict,):
        """
        :param meta:
        :param source:source is a dict, you can put any thing into therr
        """
        self.source = source
        self.meta = meta

    def update_other_item(self, params: dict):
        """
        :param params: update other item, this may not use,
        :return:
        """
        for key, value in params.items():
            if key in self.__dict__:
                print(f"warning: the key {key} exist in MetaData!")
            setattr(self, key, value)

    def update_source(self, source: dict):
        """
        update source: just like dict.update
        :param source:
        :return:
        """
        self.source.update(source)

    def as_format(self):
        """
        may use
        :return:
        """
        raise

    def __str__(self):
        out_meta = self.meta[0:20]+"......"+self.meta[-20:] if len(self.meta)>500 else self.meta
        strings = f"lens:{len(self.meta)}\nsource:{self.source}\nmeta:{[out_meta]}"
        return strings

    def __len__(self):
        return len(self.meta)


class Document(Iterable):

    def __init__(self, metas: List[MetaData], source: dict = None):
        """
        a Document include some MetaData, just like a List
        source is Document's source, you can put some information into it,
        Document's source is different with MetaData's source,
        Document's source is the information used to describe the entire document,
        Meta's source is the information used to describe the part of document's content
        :param metas:
        :param source:
        """
        self.metas = metas
        self.source = source

    def __iter__(self) -> Iterator[MetaData]:
        return iter(self.metas)

    def __getitem__(self, item: int) -> Union[List[MetaData],MetaData,'Document']:

        if isinstance(item, slice):
            start, stop, step = item.start, item.stop, item.step
            new_obj = self.metas[start:stop:step]
            if len(new_obj)==1:
                new_obj = [new_obj]
        elif isinstance(item, int) or isinstance(item,np.int64) or isinstance(item,np.int32):
            new_obj = self.metas[item]
            return new_obj
        elif isinstance(item, list) or isinstance(item,ndarray):
            new_obj = [self.metas[i] for i in item]
        else:
            raise TypeError("Invalid argument type.")
        return Document(new_obj, source=self.source)

    def __str__(self):
        strs = ""
        for i in self.metas:
            strs = strs + i.__str__()+"\n"
        strings = (f"lens:{len(self.metas)}\t\tsource:{self.source}\t"
                   f"\n{strs}\n")
        return strings

    def __len__(self):
        return len(self.metas)

