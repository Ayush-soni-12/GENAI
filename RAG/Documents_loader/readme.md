# 📘 LangChain Document Loaders — Quick Memory Guide

## 🧠 What Are Document Loaders?
Document Loaders in **LangChain** are used to **load and read data** from different sources like websites, PDFs, text files, CSVs, and directories into a **document format** that language models can process.

---

## 🌐 1. WebBaseLoader
**Purpose:**  
Used to **fetch and load content from web pages or URLs**.

**Key Points:**  
- Extracts raw text from online websites.  
- Useful for blogs, documentation, and articles.  
- Requires setting a **USER_AGENT** environment variable to identify your request.  
- Think: “**Web = from URL**”.

---

## 📄 2. TextLoader
**Purpose:**  
Used to **load plain text files (.txt)** into documents.

**Key Points:**  
- Reads entire text files into memory.  
- Ideal for small files like notes, logs, or summaries.  
- Simple and fast for single-document data.  
- Think: “**Text = single file**”.

---

## 🧾 3. CSVLoader
**Purpose:**  
Used to **load CSV (Comma-Separated Values)** files into documents.

**Key Points:**  
- Each **row** becomes a separate document.  
- Perfect for structured data and datasets.  
- Commonly used for **data-driven QA systems**.  
- Think: “**CSV = tabular data**”.

---

## 📁 4. DirectoryLoader
**Purpose:**  
Used to **load multiple files from a folder or directory**.

**Key Points:**  
- Can recursively load all supported files in a directory.  
- Works with any loader like TextLoader or PyPDFLoader.  
- Great for large document collections or dataset folders.  
- Think: “**Directory = folder of files**”.

---

## 📕 5. PyPDFLoader
**Purpose:**  
Used to **extract text from PDF documents**, one page at a time.

**Key Points:**  
- Each page is loaded as a separate document.  
- Works well for research papers, e-books, and reports.  
- Maintains page separation for better indexing and retrieval.  
- Think: “**PDF = page-by-page loading**”.

---

## ⚡ Summary Table

| Loader Name        | Source Type         | Key Feature                       | Common Use Case        |
|--------------------|--------------------|-----------------------------------|------------------------|
| WebBaseLoader      | Website URL        | Fetches content from web pages    | Blog posts, docs       |
| TextLoader         | `.txt` file        | Loads plain text files            | Notes, logs            |
| CSVLoader          | `.csv` file        | Loads structured tabular data     | Datasets, records      |
| DirectoryLoader    | Folder             | Loads multiple files recursively  | Bulk documents         |
| PyPDFLoader        | `.pdf` file        | Loads PDFs page by page           | Reports, research papers |

---

## 🧭 Quick Memory Trick

> 🔤 **W-T-C-D-P**  
> **Web**, **Text**, **CSV**, **Directory**, **PDF**  
> Mnemonic:  
> **"Websites To Collect Data Papers"**

---

## ✅ Summary
- **WebBaseLoader:** For online content.  
- **TextLoader:** For single text files.  
- **CSVLoader:** For table-like data.  
- **DirectoryLoader:** For folders with many files.  
- **PyPDFLoader:** For PDFs, page by page.

---

