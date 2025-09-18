# Mini Project 2 – Pandas Data Exploration  
**Author:** Janelle Holcomb  
**Class:** INF 601 – Programming with Python  
**Repository:** miniproject2janelleholcomb  

---

## Project Question
For this project, I am exploring a retail-style dataset to answer the question:  

**“Which product categories generate the most revenue, and how has revenue changed by month?”**

The dataset is generated using the **Faker** Python package to simulate customer orders. Each order includes category, quantity, price, discount, and order date. From there, I calculate gross and net revenue and use Pandas and Matplotlib to analyze the results.

---

## Features
- **Synthetic dataset** generated with Faker (realistic, but fake orders).  
- **Stored in a Pandas DataFrame** for easy data manipulation.  
- **Computed fields**: gross revenue, net revenue, and order month.  
- **Matplotlib visualizations** created and saved to `charts/`.  
- **Customizable**: can be switched to a CSV or API dataset later.  

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/jadette32/miniproject2janelleholcomb.git
cd miniproject2janelleholcomb

### 2. Create and activate a virtual environment

python -m venv .venv
. .venv\Scripts\Activate.




