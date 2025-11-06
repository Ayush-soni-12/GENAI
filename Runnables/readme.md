# 🧩 Runnables — Quick Guide

This document explains the different **Runnables** used in this project.  
Each section tells you **what it does** and **when to use it** in simple terms.

---

## 🔹 RunnableSequence  
**What it does:**  
Runs tasks one by one. The output of one becomes the input of the next.  

**Use it for:**  
Simple step-by-step flows (for example: `PromptTemplate → Model → Parser`).

---

## 🔹 RunnableParallel  
**What it does:**  
Runs many tasks at the same time and returns all results together.  

**Use it for:**  
When you want multiple outputs from the same input  
(for example: generate both notes and questions at once).

---

## 🔹 RunnableLambda  
**What it does:**  
Lets you use a normal Python function as a runnable.  

**Use it for:**  
Small, quick transformations (like formatting text or doing a small calculation).

---

## 🔹 RunnablePassthrough  
**What it does:**  
Returns the same input without changing it.  

**Use it for:**  
Keeping the original input safe when combining multiple parts.

---

## 🔹 RunnableBranch  
**What it does:**  
Chooses which runnable to run based on a condition (like `if-else`).  

**Use it for:**  
Decision-making flows (for example: if input matches condition A → run chain A, else → run chain B).

---

## Examples

- **Linear pipeline:**  
  ```python
  PromptTemplate | Model | Parser
