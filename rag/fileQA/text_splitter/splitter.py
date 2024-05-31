from langchain.text_splitter import CharacterTextSplitter
from rag.fileQA.base import Document, MetaData
from copy import deepcopy
from functools import reduce
from typing import List


def split_by_character_lc(text, separator="\n", chunk_size=500, chunk_overlap=100, ):
    text_splitter = CharacterTextSplitter(
        separator=separator,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    return text_splitter.split_text(text)


class CharacterSplitter(CharacterTextSplitter):
    """
    split text by character
    """
    def __init__(self, separator="\n", chunk_size=500, chunk_overlap=100, length_function=len,
                 is_separator_regex=False, **kwargs):
        super().__init__(separator=separator,
                         chunk_size=chunk_size,
                         chunk_overlap=chunk_overlap,
                         is_separator_regex=is_separator_regex,
                         length_function=length_function, **kwargs)

    def split_meta(self, meta: MetaData):

        split_texts: List[str] = self.split_text(meta.meta)
        org_source: dict = meta.source

        new_source = [deepcopy(org_source) for _ in range(len(split_texts))]
        for index, value in enumerate(new_source):
            new_source[index].update({"part": index,"part_count":len(split_texts)})
        new_metas = list(map(lambda new_meta, source: MetaData(new_meta, source), split_texts, new_source))
        return new_metas

    def split_document(self, document: Document):
        r = list(map(lambda x: self.split_meta(x), document))
        new_document = Document(reduce(lambda item1, item2: item1 + item2, r), source=document.source)
        return new_document
