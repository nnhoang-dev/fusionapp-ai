# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_community.document_loaders import TextLoader
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from dotenv import load_dotenv
# import mimetypes
# import re
# from langchain_openai import ChatOpenAI
# from langchain_openai import OpenAIEmbeddings

# # Load environment variables
# load_dotenv()
# app = FastAPI()



# llm = ChatOpenAI(
#     model="gpt-4o",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
# )

# embeddings = OpenAIEmbeddings(
#     model="text-embedding-3-large",
# )
# # Cấu hình Gemini API
# # llm = ChatGoogleGenerativeAI(
# #     model="gemini-1.5-pro",
# #     temperature=0,
# #     max_tokens=None,
# #     timeout=None,
# #     max_retries=2,
# # )

# # embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# # Định nghĩa schema đầu vào
# class CodeRequest(BaseModel):
#     input: str
#     directory_address: str

# def extract_code_from_response(response):
#     content = response.content if hasattr(response, "content") else ""
#     match = re.search(r"```[a-zA-Z]*\n([\s\S]*?)\n```", content)
#     return match.group(1).strip() if match else content.strip()

# def write_code_to_file(directory_address: str, content: str):
#     os.makedirs(os.path.dirname(directory_address), exist_ok=True)
    
#     # Ghi đè nội dung mới trực tiếp vào file
#     with open(directory_address, "w", encoding="utf-8") as file:
#         file.write(content)

# def get_root_directory(directory_address: str):
#     # Tách các phần của đường dẫn
#     path_parts = directory_address.split('/')
#     # Lấy phần tử đầu tiên làm thư mục gốc (nếu có nhiều hơn 1 phần)
#     return path_parts[0] if len(path_parts) > 1 else os.path.dirname(directory_address)

# def get_directory_content(directory_address: str):
#     # Lấy thư mục gốc từ directory_address
#     root_dir = get_root_directory(directory_address)
    
#     if not os.path.exists(root_dir):
#         os.makedirs(root_dir)
#         return "No existing files found in directory"

#     file_contents = []
#     for root, dirs, files in os.walk(root_dir):
#         if "node_modules" in root:  # Bỏ qua thư mục node_modules
#             continue
#         for file in files:
#             file_path = os.path.join(root, file)
#             mime_type, _ = mimetypes.guess_type(file_path)
#             # Chỉ đọc các file text có phần mở rộng phổ biến
#             if (mime_type and mime_type.startswith("text")) or file.endswith((".ts", ".js", ".json", ".txt")):
#                 try:
#                     with open(file_path, "r", encoding="utf-8") as f:
#                         content = f.read()
#                         # Ghi rõ tên file và nội dung để dễ theo dõi
#                         file_contents.append(f"File: {file_path}\n{content}\n{'='*50}")
#                 except Exception as e:
#                     file_contents.append(f"Error reading {file_path}: {str(e)}\n{'='*50}")
    
#     if not file_contents:
#         return "No readable text files found in directory"
    
#     return "\n".join(file_contents)

# @app.post("/generate-code")
# def generate_code(request: CodeRequest):
#     try:
#         # Lấy thư mục gốc từ directory_address 
#         root_directory = get_root_directory(request.directory_address)
        
#         # Lấy tất cả nội dung trong thư mục gốc
#         context = get_directory_content(request.directory_address)
#         print(context)
#         # Tạo prompt với yêu cầu thêm route /hi
#         prompt = f"""
#         Bạn là một trợ lý lập trình AI chuyên tạo mã nguồn.
#         Bạn phải viết full 1 file code.

#         📂 **Thư mục gốc:** `{root_directory}`
        
#         🔍 **Nội dung các file trong thư mục gốc:**
#         {context}

#         📝 **Yêu cầu từ người dùng:**
#         {request.input}

#         🎯 **Nhiệm vụ:**
#         - Chỉ trả về code, không thêm giải thích
        
#         Đảm bảo rằng code có thể chạy được.
#         Chắc chắn rằng import đã đúng.
#         Tôi nhận thấy bạn thường import sai.

#         Hãy tạo mã nguồn phù hợp.
#         """

#         # Gọi LLM để tạo code
#         response = llm.invoke(prompt)
#         code_content = extract_code_from_response(response)

#         # Thêm code vào file đích
#         write_code_to_file(request.directory_address, code_content)

#         # Chỉ trả về code trong response
#         return code_content
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
    
    
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import re
import mimetypes
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# # Load environment variables
load_dotenv()

app = FastAPI()

# Cấu hình LLM (có thể chọn GPT-4o hoặc Gemini)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Định nghĩa schema đầu vào
class CodeRequest(BaseModel):
    input: str
    root_directory: str
    directory_address: str

# Hàm trích xuất code từ phản hồi của AI
def extract_code_from_response(response):
    content = response.content if hasattr(response, "content") else ""
    match = re.search(r"```[a-zA-Z]*\n([\s\S]*?)\n```", content)
    return match.group(1).strip() if match else content.strip()

# Hàm ghi code vào file
def write_code_to_file(directory_address: str, content: str):
    os.makedirs(os.path.dirname(directory_address), exist_ok=True)
    with open(directory_address, "w", encoding="utf-8") as file:
        file.write(content)
        
def get_root_directory(directory_address: str):
    # Tách các phần của đường dẫn
    path_parts = directory_address.split(os.sep)
    # path_parts = directory_address.split('/')
    # Lấy phần tử đầu tiên làm thư mục gốc (nếu có nhiều hơn 1 phần)
    return path_parts[0] if len(path_parts) > 1 else os.path.dirname(directory_address)

# Lưu trữ nội dung thư mục vào cache để tối ưu hiệu suất
def get_directory_content(root_directory: str):
    if not os.path.exists(root_directory):
        return "No existing files found in directory"

    file_contents = []
    for root, _, files in os.walk(root_directory):
        if "node_modules" in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            mime_type, _ = mimetypes.guess_type(file_path)
            if (mime_type and mime_type.startswith("text")) or file.endswith((".ts", ".js", ".json", ".txt")):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        file_contents.append(f"File: {file_path}\n{content[:500]}...\n{'='*50}")  # Chỉ lấy 500 ký tự đầu tiên
                except Exception as e:
                    file_contents.append(f"Error reading {file_path}: {str(e)}\n{'='*50}")
    
    return "\n".join(file_contents) if file_contents else "No readable text files found in directory"

@app.post("/generate-code")
def generate_code(request: CodeRequest):
    try:
        root_directory = request.root_directory
        print('root_directory', root_directory)
        context = get_directory_content(root_directory)
        
        print('context', context)
        
        prompt = f"""
        Bạn là một trợ lý lập trình AI chuyên tạo mã nguồn.
        Nhiệm vụ của bạn là dựa vào các file trong folder để có thể tạo ra một api phù hợp với yêu cầu từ người dùng.
        Xem kỹ template của file tôi chỉ định và thêm code vào.

        📂 **Thư mục gốc:** `{root_directory}`
        
        **Thu mục cần thay đổi:** `{request.directory_address}`        
        🔍 **Nội dung quan trọng từ các file trong thư mục gốc:**
        {context}
        
        📝 **Yêu cầu từ người dùng:**
        {request.input}
        
        🎯 **Nhiệm vụ:**
        - Chỉ trả về code, không thêm giải thích.
        - Đảm bảo import chính xác.
        - Code phải chạy được mà không có lỗi.
        """
        
        response = llm.invoke(prompt)
        code_content = extract_code_from_response(response)
        write_code_to_file(request.directory_address, code_content)
        
        return {"message": "Code generated successfully", "file": request.directory_address, "code": code_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






# from langchain_community.vectorstores import FAISS
# from langchain_core.documents import Document
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# import pickle

# # Khởi tạo vector store FAISS
# vector_store_path = "faiss_index"

# def save_documents_to_vectorstore(root_directory):
#     """ Lưu trữ nội dung thư mục dưới dạng embedding vào FAISS """
#     if not os.path.exists(root_directory):
#         return None
    
#     documents = []
#     for root, _, files in os.walk(root_directory):
#         if "node_modules" in root:
#             continue
#         for file in files:
#             file_path = os.path.join(root, file)
#             mime_type, _ = mimetypes.guess_type(file_path)
#             if (mime_type and mime_type.startswith("text")) or file.endswith((".ts", ".js", ".json", ".txt")):
#                 try:
#                     with open(file_path, "r", encoding="utf-8") as f:
#                         content = f.read()
#                         doc = Document(page_content=content, metadata={"source": file_path})
#                         documents.append(doc)
#                 except Exception:
#                     continue
    
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     split_docs = text_splitter.split_documents(documents)
    
#     vector_store = FAISS.from_documents(split_docs, embeddings)
#     with open(vector_store_path, "wb") as f:
#         pickle.dump(vector_store, f)

#     return "Vector store updated successfully"

# def retrieve_relevant_docs(query, top_k=3):
#     """ Tìm kiếm tài liệu liên quan đến yêu cầu của người dùng """
#     try:
#         with open(vector_store_path, "rb") as f:
#             vector_store = pickle.load(f)
#     except FileNotFoundError:
#         return "No vector database found. Please update the index first."
    
#     results = vector_store.similarity_search(query, k=top_k)
#     return "\n".join([f"🔹 **{doc.metadata['source']}**\n{doc.page_content[:500]}..." for doc in results])

# @app.post("/generate-code")
# def generate_code(request: CodeRequest):
#     try:
#         root_directory = get_root_directory(request.directory_address)
#         print('root_directory', root_directory)
#         # Cập nhật index trước khi truy vấn
#         save_documents_to_vectorstore(root_directory)
        
#         # Lấy thông tin quan trọng từ thư mục bằng RAG
#         context = retrieve_relevant_docs(request.input)
        
#         prompt = f"""
#         Bạn là một trợ lý lập trình AI chuyên tạo mã nguồn.
#         Bạn phải viết toàn bộ file code.

#         📂 **Thư mục gốc:** `{root_directory}`
#         **Thu mục cần thay đổi:** `{request.directory_address}`        
        
#         🔍 **Các tài liệu liên quan từ thư mục:** 
#         {context}

#         📝 **Yêu cầu từ người dùng:**
#         {request.input}
        
#         🎯 **Nhiệm vụ:**
#         - Chỉ trả về code, không thêm giải thích.
#         - Đảm bảo import chính xác.
#         - Code phải chạy được mà không có lỗi.
#         """
        
#         response = llm.invoke(prompt)
#         code_content = extract_code_from_response(response)
#         write_code_to_file(request.directory_address, code_content)
        
#         return {"message": "Code generated successfully", "file": request.directory_address, "code": code_content}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
