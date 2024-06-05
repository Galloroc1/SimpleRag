import abc
from FlagEmbedding import BGEM3FlagModel
from typing import List
from rag.fileQA.base import MetaData,Document
from abc import ABC,abstractmethod

class BaseEmbedding(ABC):

    @abstractmethod
    def encode(self,sentences,**kwargs):
        raise

    @abstractmethod
    def encode_document(self,sentences,**kwargs):
        raise


class EmbeddingBgeM3(BaseEmbedding):

    def __init__(self):
        """
        embedding model from https://huggingface.co/BAAI/bge-m3
        """
        self.model = BGEM3FlagModel('BAAI/bge-m3',
                                    use_fp16=True)

    def encode(self,sentences:List[str],max_length=8192):
        """
        todo: just support dense vec now

        :param sentences:
        :param max_length:
        :return:
        """
        # def forward(self,
        #     text_input: Dict[str, Tensor] = None,
        #     return_dense: bool = True,
        #     return_sparse: bool = False,
        #     return_colbert: bool = False,
        #     return_sparse_embedding: bool = False):

        embeddings = self.model.encode(sentences,
                                    batch_size=12,
                                    max_length=max_length,
                                    )['dense_vecs']
        return embeddings

    def encode_document(self,sentences:Document,max_length=8192,batch_size=12):
        """
        todo: just support dense vec now

        :param sentences:
        :param max_length:
        :return:
        """
        # def forward(self,
        #     text_input: Dict[str, Tensor] = None,
        #     return_dense: bool = True,
        #     return_sparse: bool = False,
        #     return_colbert: bool = False,
        #     return_sparse_embedding: bool = False):
        texts =  list(map(lambda x:x.meta,sentences.metas))
        embeddings = self.model.encode(texts,
                                    batch_size=batch_size,
                                    max_length=max_length,
                                    )['dense_vecs']
        return embeddings



if __name__ == '__main__':
    model = EmbeddingBgeM3()
    sentences = ['hello','my friends']
    embeddings = model.encode(sentences)
    print(embeddings)
    scores = embeddings[0] @ embeddings[1]
    print(scores)
