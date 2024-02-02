import streamlit as st
import pandas as pd

# Load the CSV file into a DataFrame
def load_data():
    data = pd.read_csv('data.csv')
    return data

# Main app function
def main():
    st.title('Sentiment and Category Search')

    # Load the data
    data = load_data()

    # Sidebar for selection
    st.sidebar.header('Search Filters')

    # Selectbox for sentiment (multiple selection enabled)
    selected_sentiments = st.sidebar.multiselect('Sentiment', options=data['sentiment'].unique(), default=data['sentiment'].unique())

    # Selectbox for category (multiple selection enabled)
    selected_categories = st.sidebar.multiselect('Category', options=data['category'].unique(), default=data['category'].unique())

    # Filter data based on selection
    filtered_data = data[(data['sentiment'].isin(selected_sentiments)) & (data['category'].isin(selected_categories))]

    # Display filtered data
    if not filtered_data.empty:
        st.write(filtered_data)
    else:
        st.write("No results found based on the filters.")

if __name__ == '__main__':
    main()
