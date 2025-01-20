import utils.transport
import utils.session
import streamlit as st
import requests
import json
from bs4 import BeautifulSoup

def web_scraper_tool():
    st.header("Web Scraper")

    url = st.text_input("Enter a URL (e.g., https://example.com)")
    if st.button("Scrape"):
        if url:
            try:
                response = requests.get(url)
                response.raise_for_status()
                html_content = response.text

                # Parse HTML
                soup = BeautifulSoup(html_content, "html.parser")
                
                # Example: Extract the page <title>
                page_title = soup.title.string if soup.title else "No title found"
                
                # Example: Extract all <h1> tags
                h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]

                st.write("**Page Title:**", page_title)
                
                if h1_tags:
                    st.write("**H1 Tags:**")
                    for idx, heading in enumerate(h1_tags, start=1):
                        st.write(f"{idx}. {heading}")
                else:
                    st.write("No H1 tags found.")

                # Optionally, display raw HTML content
                with st.expander("View Raw HTML"):
                    st.code(html_content[:1000] + "...", language="html")  # Show partial for demo

            except requests.exceptions.RequestException as e:
                st.error(f"Error scraping {url}: {e}")
        else:
            st.warning("Please enter a valid URL.")

def json_prettifier_tool():
    st.header("JSON Prettifier")

    raw_json = st.text_area("Paste your JSON here:", height=200)
    if st.button("Prettify JSON"):
        if raw_json.strip():
            try:
                parsed = json.loads(raw_json)
                pretty_json = json.dumps(parsed, indent=4)
                st.subheader("Formatted JSON")
                st.code(pretty_json, language="json")
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON: {e}")
        else:
            st.warning("Please paste some JSON to prettify.")

def http_checker_tool():
    st.header("HTTP Status Checker")

    url = st.text_input("Enter a URL to check status:")
    method = st.selectbox("HTTP Method:", ["GET", "POST", "PUT", "DELETE"])
    if st.button("Check Status"):
        if url:
            try:
                if method == "GET":
                    r = requests.get(url)
                elif method == "POST":
                    r = requests.post(url)
                elif method == "PUT":
                    r = requests.put(url)
                else:  # DELETE
                    r = requests.delete(url)

                st.write(f"**Status Code:** {r.status_code}")
                if r.ok:
                    st.success("Request successful!")
                else:
                    st.error("Request returned an error status.")

                # Optional: Show Response Text
                with st.expander("View Response Content"):
                    st.code(r.text[:1000] + "...")  # Partial content

            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching {url}: {e}")
        else:
            st.warning("Please enter a valid URL.")

def main():
    st.title("Developer Toolbox")

    # Sidebar for selecting tools
    tool_selected = st.sidebar.selectbox(
        "Select a Tool",
        ("Web Scraper", "JSON Prettifier", "HTTP Status Checker")
    )

    st.sidebar.write("---")
    st.sidebar.write("A personal toolbox to make a developer’s life easier.")

    if tool_selected == "Web Scraper":
        web_scraper_tool()
    elif tool_selected == "JSON Prettifier":
        json_prettifier_tool()
    else:
        http_checker_tool()

if __name__ == "__main__":
    main()
