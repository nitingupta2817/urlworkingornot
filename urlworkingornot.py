import streamlit as st
import requests
import pandas as pd
from urllib.parse import urlparse

st.title("Smart URL Working Checker")

urls_input = st.text_area("Enter URLs (one per line)")
timeout = 10

if st.button("Check URLs"):

    if not urls_input.strip():
        st.warning("Please enter URLs.")
    else:
        urls = [u.strip() for u in urls_input.split("\n") if u.strip()]
        results = []

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        for url in urls:
            try:
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=timeout,
                    allow_redirects=True
                )

                code = response.status_code

                if code in [200, 301, 302, 403]:
                    status = "OK ✅"
                else:
                    status = "Not Working ❌"

            except:
                code = "Error"
                status = "Not Working ❌"

            domain = urlparse(url).netloc

            results.append({
                "URL": f'<a href="{url}" target="_blank">{url}</a>',
                "Domain": domain,
                "Status Code": code,
                "Result": status
            })

        df = pd.DataFrame(results)

        st.success("Checking Completed ✅")

        # Clickable table
        st.markdown(
            df.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

        # -------------------
        # 📊 SUMMARY SECTION
        # -------------------

        total_urls = len(df)
        working = df[df["Result"] == "OK ✅"].shape[0]
        not_working = total_urls - working
        unique_domains = df["Domain"].nunique()

        st.markdown("## 📊 Summary")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total URLs", total_urls)
        col2.metric("Working", working)
        col3.metric("Not Working", not_working)
        col4.metric("Unique Domains", unique_domains)

        # Domain wise count
        st.markdown("### 🌐 Domain-wise Link Count")
        domain_count = df["Domain"].value_counts().reset_index()
        domain_count.columns = ["Domain", "Link Count"]

        st.dataframe(domain_count, use_container_width=True)

        # CSV download
        clean_df = df.copy()
        clean_df["URL"] = clean_df["URL"].str.replace(
            r'<a href="(.*?)".*?>.*?</a>', r'\1', regex=True
        )

        csv = clean_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Results as CSV",
            csv,
            "url_results.csv",
            "text/csv"
        )
