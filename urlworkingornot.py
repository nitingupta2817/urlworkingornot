import streamlit as st
import requests
import pandas as pd

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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
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

                results.append({
                    "URL": f'<a href="{url}" target="_blank">{url}</a>',
                    "Status Code": code,
                    "Result": status
                })

            except:
                results.append({
                    "URL": f'<a href="{url}" target="_blank">{url}</a>',
                    "Status Code": "Error",
                    "Result": "Not Working ❌"
                })

        df = pd.DataFrame(results)

        st.success("Checking Completed ✅")

        # Render clickable table
        st.markdown(
            df.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

        # CSV download
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Results as CSV",
            csv,
            "url_results.csv",
            "text/csv"
        )