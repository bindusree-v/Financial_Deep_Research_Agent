"""
RAG System Module
This module contains the RAGSystem class for loading PDF documents,
creating a vector database, and querying it using LangChain and Chroma.
"""

# 1. Imports
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"

class RAGSystem:
    """
    Retrieval-Augmented Generation (RAG) System.
    Handles loading PDFs, chunking text, storing in ChromaDB, and retrieving relevant information.
    """
    
    def __init__(self):
        """
        Initializes the RAG System, embedding model, and loads any existing database.
        """
        try:
            # Set target folders
            self.documents_folder = "documents"
            self.db_folder = "vectordb"
            
            # Initialize the embedding model
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            
            # Initialize vectordb variable
            self.vectordb = None
            
            # Print initialization message
            print("RAG System initialized")
            
            # Load existing database if available
            self.load_existing_db()
        except Exception as e:
            print(f"Error during RAG System initialization: {e}")

    def load_existing_db(self):
        """
        Loads an existing Chroma vector database from the db_folder if it exists.
        """
        try:
            # Check if the database folder exists and contains files
            if os.path.exists(self.db_folder) and os.listdir(self.db_folder):
                # Load the existing ChromaDB
                self.vectordb = Chroma(
                    persist_directory=self.db_folder, 
                    embedding_function=self.embeddings
                )
                print("Loaded existing vector database")
            else:
                print("No existing database found")
        except Exception as e:
            print(f"Error loading existing database: {e}")

    def load_documents(self, folder_path: str = "documents"):
        """
        Loads PDF files from the specified folder, splits them into chunks,
        and stores them in a new Chroma vector database.
        
        Args:
            folder_path (str): The directory containing PDF documents.
        """
        try:
            # Create documents folder if it doesn't exist
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created documents folder at: {folder_path}")
            
            # Check for PDF files in the folder
            pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
            
            # If no PDFs, print message and return
            if not pdf_files:
                print("No PDF files found in documents folder")
                return
            
            all_chunks = []
            
            # Initialize text splitter
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            
            # Loop through each PDF file
            for filename in pdf_files:
                file_path = os.path.join(folder_path, filename)
                try:
                    # Load PDF using PyPDFLoader
                    loader = PyPDFLoader(file_path)
                    documents = loader.load()
                    
                    # Split into chunks
                    chunks = text_splitter.split_documents(documents)
                    all_chunks.extend(chunks)
                    
                    # Print success message for this file
                    print(f"Loaded: {filename}")
                except Exception as file_error:
                    print(f"Error loading {filename}: {file_error}")
                    
            if not all_chunks:
                print("No text could be extracted from the provided PDFs.")
                return
                
            # Store all chunks in ChromaDB and save to vectordb folder
            self.vectordb = Chroma.from_documents(
                documents=all_chunks,
                embedding=self.embeddings,
                persist_directory=self.db_folder
            )
            
            # Print success message with chunk count
            print(f"Vector database created with {len(all_chunks)} chunks")
            
        except Exception as e:
            print(f"Error processing documents: {e}")

    def query(self, question: str, top_k: int = 3) -> str:
        """
        Searches the vector database for chunks relevant to the question.
        
        Args:
            question (str): The search query.
            top_k (int): Number of top results to return.
            
        Returns:
            str: The combined relevant text from the database.
        """
        try:
            # Check if vector database is loaded
            if self.vectordb is None:
                return "No documents loaded in RAG system"
            
            # Search vectordb for relevant chunks
            results = self.vectordb.similarity_search(question, k=top_k)
            
            # If no results found
            if not results:
                return "No relevant information found"
                
            # Combine top_k results into a single string
            combined_results = "\n\n".join([doc.page_content for doc in results])
            
            return combined_results
            
        except Exception as e:
            error_msg = f"Error during query execution: {e}"
            print(error_msg)
            return error_msg
