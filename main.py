import pandas as pd
import numpy as np
import plotly.express as px
import json
import os
import streamlit as st

st.set_page_config(
    page_title="Finance APP",
    page_icon="📈",
    layout="wide"
)


# st.markdown(
#     """
#     <style>
#     .stApp {
#         background-color: 	#2f2d52; /* Replace with your preferred color */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

catfile = "categories.json"


if "Categories" not in st.session_state:
    st.session_state.categories = {
        "Uncategorized": []
    }
if os.path.exists(catfile):
    with open(catfile, "r") as f:
        st.session_state.categories = json.load(f)


def save_categories():
    with open(catfile, "w") as f:
        json.dump(st.session_state.categories, f)


def categorize_transaction(df):
    if "Details" not in df.columns:
        st.error("The 'Details' column is missing from the uploaded file.")
        return df

    df["Category"] = "Uncategorized"
    for category, keywords in st.session_state.categories.items():
        if category == "Uncategorized" or not keywords:  # Skip if no keywords
            continue
        lowered_keywords = [keyword.lower().strip() for keyword in keywords]
        for idx, row in df.iterrows():
            details = row["Details"].lower().strip()
            if details in lowered_keywords:
                df.at[idx, "Category"] = category
                # Prevent duplicates
                if row["Details"] not in st.session_state.categories[category]:
                    st.session_state.categories[category].append(row["Details"])
    return df

def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Drop unnamed columns
        df["Amount"] = df["Amount"].astype(str).str.replace(",", "").astype(float)  # Remove commas and convert to float
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y", errors="coerce")  # Parse dates
        st.write(df)
        return categorize_transaction(df)
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")

def add_category_to_category(category, keyword):
    keywords = keyword.strip()                      #strip the keyword for easier handling.
    if keyword and keyword not in st.session_state.categories[category]:        #check if the keyword is not empty and not already in the category.
        st.session_state.categories[category].append(keywords)      #if not, append it to the category.
        save_categories()       #save the categories to the file.

def main():
    st.title("Finance Dashboard")
    uploaded_file = st.file_uploader("sample_bank_statement.csv", type=["csv"])

    if uploaded_file is not None:
        df = load_transactions(uploaded_file)

        if df is not None:
            st.subheader("Data Overview")

            debits_df = df[df["Debit/Credit"] == "Debit"].copy()
            credits_df = df[df["Debit/Credit"] == "Credit"].copy()

            st.session_state.debits_df = debits_df.copy()

            tab1, tab2 = st.tabs(["Expenses (Debit)", "Payments (Credit)"])

            with tab1:
                new_category = st.text_input("New category name")
                add_button = st.button("Add Category")
                if add_button and new_category:
                    if new_category not in st.session_state.categories:
                        st.session_state.categories[new_category] = []
                        save_categories()
                    st.rerun()

                st.subheader("Your Expenses")
                edited_df = st.data_editor(
                    st.session_state.debits_df[["Date", "Details", "Amount", "Category"]],      ##display the dataframe with the columns Date, Details, Amount and Category.
                    column_config={
                    "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),              ##format the date column.
                    "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED"),        ##format the amount column.
                    "Category": st.column_config.SelectboxColumn("Category", options=list(st.session_state.categories.keys())),         ##display the categories as a selectbox.
                    },
                    hide_index=True,            ##hide the index of the dataframe.
                    use_container_width=True,       ##use the full width of the container.
                    key = "category_editor",        ##key for the dataframe editor.
                )

                save_button = st.button("Save Changes", type="primary")
                if save_button:
                    for idx, row in edited_df.iterrows():         ##iterate through the edited dataframe.
                        new_category = row["Category"]
                        if new_category == st.session_state.debits_df.at[idx, "Category"]:
                            continue

                        details = row["Details"]
                        st.session_state.debits_df.at[idx, "Category"] = new_category
                        add_category_to_category(new_category, details)

                st.subheader("Expenses Summary")
                category_totals = st.session_state.debits_df.groupby("Category")["Amount"].sum().reset_index()
                category_totals = category_totals.sort_values(by="Amount", ascending=False)
                
                st.dataframe(
                    category_totals, 
                    column_config = {
                    "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED"),
                    },
                use_container_width=True,
                hide_index=True
            )
                

                fig = px.pie(
                    category_totals, 
                    values="Amount", 
                    names="Category", 
                    title="Expenses by Category"
                    )
                
                st.plotly_chart(fig, use_container_width=True)



            with tab2:
                st.write(credits_df)
        else:
            st.warning("Please upload a CSV file to see the data.")

main() 