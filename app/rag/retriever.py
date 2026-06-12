from ..core import chromadb
# import cohere
# from .. import config
# cohere_client = cohere.Client(config.COHERE_API_KEY)

def retriever_query(input: dict):
     question = input.get("question")
     doc_id = input.get("doc_id")
     docs = retriever(question, doc_id=doc_id) #get the relevant chunks using the retriever
     # docs = reranker(docs, question) rerank the chunks using the reranker
     return docs

def retriever(question, doc_id=None, k=3):
     client = chromadb.get_vectorStore() #get the vector store client
     search_kwargs = {
          "k": k
     }
     if doc_id:
          search_kwargs["filter"] = {"doc_id": doc_id}
     retriever = client.as_retriever(
          search_type="similarity",     
          search_kwargs=search_kwargs
     )
     filtered_docs = []
     docs = retriever.invoke(question)
     for doc in docs:
          text = doc.page_content.lower().strip()
          if text.startswith("questions") or text.startswith("exercise"):
               continue
          filtered_docs.append(doc)
          
     return  filtered_docs

# def reranker(docs, question, k = 5):
#      texts = [doc.page_content for doc in docs]
#      reranked = cohere_client.rerank(
#           model="rerank-v3.5",
#           question=question,
#           documents=texts,
#           top_n=k
#      )
#      print("-----Reranking Results-----")
#      for r in reranked.results:
#           print("score:", r.relevance_score)
#           print("chunk:", docs[r.index].page_content[:500])
#           print("------")     
#      ranked_docs = [docs[r.index] for r in reranked.results] #map using r.index which is the index of the original text of the doc.
#      return ranked_docs