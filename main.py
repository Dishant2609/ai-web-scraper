import streamlit as st
from scrape import(
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content,
                              
 )
from parse import parse_with_openai

page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://i.postimg.cc/RZ5Xg1LC/wp7795859-4k-laptop-black-wallpapers.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0);  /* transparent header */
}
[data-testid="stToolbar"] {
    right: 2rem;
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)


st.title("AI web scraper")
url = st.text_input("Enter a website URL")


if st.button("scrape site"):
    st.write("scraping begins...")
    
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("View DOM content"):
        st.text_area("DOM Content", cleaned_content, height=300)


if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")


            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_openai(dom_chunks, parse_description)
            st.write(result)