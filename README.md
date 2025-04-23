# 📊 Finance Management App

A personal finance dashboard built with **Streamlit**.  
Upload your bank statement CSV, categorize transactions, and visualize expenses — all in your browser.

---

Finance_Management_cwj/
├── main.py                # Main Streamlit app
├── categories.json        # Auto-generated category mappings
├── sample_bank_statement.csv (optional)
├── .gitignore
└── README.md

---

## 🧩 Features

- 🔁 **Upload CSV** bank statements (format: `Date`, `Details`, `Amount`, `Debit/Credit`)
- 🧠 **Smart Categorization** using keyword matching
- ✍️ **Manual Category Editing** with dropdown editor
- 📊 **Summary View** of expenses by category
- 🥧 **Interactive Pie Chart** (powered by Plotly)
- 💾 **Persistent Categories** saved to a JSON file

---

## 🚀 Getting Started

### 1. Install Requirements

```bash
pip install streamlit pandas plotly

### 2. Run the app

streamlit run main.py

### 3. Upload a Sample File
Format: CSV with columns like Date, Details, Amount, Debit/Credit
Example: sample_bank_statement.csv (if provided)




### Credits
This was built with the guidance of [TechWithTim](https://github.com/techwithtim)
