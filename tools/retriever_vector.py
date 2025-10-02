import logging
import os
import threading
from idlelib.debugger_r import DictProxy
from typing import Dict

import numpy as np
from langchain_community.vectorstores import Chroma

from langchain_openai import OpenAIEmbeddings
# read invoice rules and cancelation policy
with open("doc/order_faq.md", "r", encoding="utf-8") as f:
    order_text = f.read()

# create document from  text and split it into chunks by title like "##
doc = [{"page_content": txt} for txt in order_text.split(r"(?\n##)",order_text)]
# create embeddings model
embeddings_model = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    chunk_size=1000,
    chunk_overlap=0,
    model_kwargs={"input_form": "text"}

)

# create vector store from doc and smart text truncation with thread sale mode

def truncate_text(search_text, max_embedding_size):
    pass


class ChromaDBManager:
    """Singleton class to manage ChromaDB vector store to avoid multiple instances and conflicts."""

    _instance = None
    _lock = threading.Lock()
    _collections :Dict[str,any] ={}
    _client = None

    def __init__(self):
       if not self._initialized:
           try :
               # to do list-> check oepration system verion >11 or <
               self.chroma_client = Chroma(persist_directory="./chroma_db", embedding_function=embeddings_model)
               # self.vector_store = Chroma(
               #     client=self.chroma_client,
               #     embedding_function=embeddings_model,
               #     text_splitter=Chroma.get_text_splitter(chunk_size=1000, chunk_overlap=0),
               #     text_key="page_content",
               #     metadatas=[{"source": "order_faq.md"}],
               #     documents=doc
               # )
               self._initialized = True
               print("ChromaDB initialized")
               self.chroma_client.persist()
           except Exception as e:
               logging.error(f"❌ [ChromaDB] initialized failed: {e}")
    def _new__(cls)
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ChromaDBManager, cls).__new__(cls)
                    cls._instance._in
        return cls._instance

    def get_or_create_collection(self, collection_name: str):

        #  create a vector store if not exist with thread safe
        with self._lock:
            if collection_name in self._collections:
                logging.info(f"ChromaDB collection {collection_name} already exists.")
                return self._collections[collection_name]

            try:
                # try to get collection from chroma db client
                collection = self.chroma_client.get_collection(name=collection_name)
                logging.info(f"ChromaDB collection {collection_name} already exists.")
            except Exception as e:
                try:
                    # create a new collection
                    collection = self.chroma_client.create_collection(name=collection_name)
                    logging.info(f"ChromaDB collection {collection_name} created.")
                except Exception as e:
                    # handle current creation, try to get collection again
                    logging.error(f"❌ [ChromaDB] create collection {collection_name} failed: {e} need to try to get it again")
                    try :
                        collection = self.chroma_client.get_collection(name=collection_name)
                        logging.info(f"ChromaDB collection {collection_name} already exists.")
                    except Exception as final_error:
                        logging.error(f"❌ [ChromaDB] get collection {collection_name} failed: {e}")
                        raise final_error

            # add collection to cache
            self._collections[collection_name] = collection
            return collection




    # create a class for enterpris inner policy vector store
    class EnterpriseInnerPolicyVectorStore:
        def __init__(self,name, config):
            self.name = name
            self.config = config

            # configure max embedding size and length check

            self.max_embedding_size = int(os.getenv("max_embedding_size", '50000') )
            self.enable_max_embedding_length = os.getenv("enable_max_embedding_length", 'False').lower() in ('true', '1', 't')
            # create a chroma db manager and get or create a vector store
            self.chroma_db_manager = ChromaDBManager()
            self.collection = self.chroma_db_manager.get_or_create_collection(self.name)



        def get_embedding(self, search_text):
            """get embedding from current policy text with smart truncation""""

            # validate input text
            if not search_text or not isinstance(search_text, str):
                logging.warning("Invalid input text,return empty embedding")
                return np.zeros(self.max_embedding_size)
            text_length = len(search_text)
            if text_length==0:
                loggger.warning("Empty input text, return empty embedding")
                return np.zeros(self.max_embedding_size)

            # truncate text if needed
            if self.enable_max_embedding_length and text_length > self.max_embedding_size:
                search_text = truncate_text(search_text, self.max_embedding_size)
                logging.warning(f"Text length {text_length} exceeds max embedding size {self.max_embedding_size}, truncating to {self.max_embedding_size}")

            # try to embed search text with dashcsope model
            import dashscope
            from dashscope import TextEmbedding
            try:
                # call dashscope api
                embedding_response = TextEmbedding.call(input=search_text, model="text-embedding-v1")
                if embedding_response.status_code == 200:
                    logging.info(f"DashScope get embedding success")
                    return embedding_response
                else:
                    logging.error(f"❌ [DashScope] get embedding failed: {embedding_response.error}")
                    
                    # api response error message
                    error_message = f"{embedding_response.code} - {embedding_response.message}"
                    
                    # check if the error is related to input text length
                    if any(keyword in error_message.lower() for keyword in ["length", "token", "limit", "exceed"]):
                        logging.warning("Text length exceeds DashScope max embedding length, trying to enable max embedding length check")
                        if not self.enable_max_embedding_length:
                            logging.warning("Enabling max embedding length check and retrying")
                            self.enable_max_embedding_length = True
                            truncated_text = truncate_text(search_text, self.max_embedding_size)
                            return self.get_embedding(truncated_text)
                        else:
                            logging.error("Max embedding length check already enabled, cannot retry")
                    
            
                
            except Exception as e:
                logging.error(f"❌ [DashScope] get embedding failed: {e}")
                raise e

        def add_to_embedding(self, policies):
            """Add enterprise inner policy text to vector store with smart truncation"""
            policies_array = []
            ids=[]
            embeddings = []
            offset = self.collection.count()

            for i, policy in enumerate(policies):
                policies_array.append(policy)
                ids.append(str(offset+i))
                embeddings.append(self.get_embedding(policy))

            self.collection.add(
                documents=policies_array,
                metadatas=[{"source": "enterprise_inner_policy.md"}],
                ids=ids,
                embeddings=embeddings
            )



        def search_embedding(self, search_text, k=3):
            """Search enterprise inner policy text in vector store with smart truncation"""
            embedding = self.get_embedding(search_text)
            try:
                results= self.collection.query(query_texts=[search_text], n_results=k, embedding=embedding)

                #deal with results
                memories = []
                for i, result in enumerate(results):
                    memories.append({
                        "id": result["ids"][i],
                        "text": result["documents"][i],
                        "score": 1-result["distances"][i],
                        "source": result["metadatas"][i]["source"]
                    })
                    logging.info(f"[VectorStore] Search result: {memories[i]}")

                return memories
            except Exception as e:
                logging.error(f"❌ [VectorStore] Search failed: {e}")
                raise e
