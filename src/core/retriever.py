from . import chromadb
import cohere
# from .. import config
# cohere_client = cohere.Client(config.COHERE_API_KEY)

def query(query):
     docs = retriever(query) #get the relevant chunks using the retriever
     # docs = reranker(docs, query) rerank the chunks using the reranker
     return docs

def retriever(query, k=5):
     client = chromadb.get_vectorStore() #get the vector store client
     retriever = client.as_retriever(
          search_type="similarity",     
          search_kwargs={"k": k},
     )
     filtered_docs = []
     docs = retriever.invoke(query)
     for doc in docs:
          text = doc.page_content.lower()
          if text.startswith("questions") or text.startswith("exercise"):
               continue
          filtered_docs.append(doc)
          
     return  filtered_docs

# def reranker(docs, query, k = 5):
#      texts = [doc.page_content for doc in docs]
#      reranked = cohere_client.rerank(
#           model="rerank-v3.5",
#           query=query,
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
