import asyncio
import streamlit as st
from helpers import (
    get_merged_pdf_bytes,
    scan_and_upload_to_paperless,
    trigger_scan_and_get_doc,
    merge_and_send_to_paperless,
)
from streamlit_pdf_viewer import pdf_viewer


if __name__ == "__main__":
    st.set_page_config(layout="wide")

    st.header("Upload documents from scanner to Paperless")

    if "pdf_streams" not in st.session_state:
        st.session_state.pdf_streams = []

    is_multi_page = st.checkbox("Multiple pages pdf")

    filename = st.text_input("Enter file name")

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    if is_multi_page:
        with col1:
            st.button(
                "Scan next document",
                on_click=lambda: asyncio.run(trigger_scan_and_get_doc()),
            )
        st.write(f"No. of pages: {len(st.session_state.pdf_streams)}")
        with col2:
            st.button(
                "Merge document in paperless",
                disabled=not filename or not st.session_state.pdf_streams,
                on_click=lambda: asyncio.run(merge_and_send_to_paperless(filename)),
            )
    else:
        with col1:
            st.button(
                "Scan and preview",
                on_click=lambda: asyncio.run(trigger_scan_and_get_doc()),
            )

        with col2:
            st.button(
                "Direct scan to Paperless",
                disabled=not filename,
                on_click=lambda: asyncio.run(scan_and_upload_to_paperless(filename)),
                help="Scan and upload directly to Paperless with specified file name",
            )

    pdf = get_merged_pdf_bytes()
    if pdf:
        with col3:
            st.download_button(
                "Download scanned doc",
                file_name=filename if filename.endswith(".pdf") else f"{filename}.pdf",
                disabled=not filename,
                mime="application/pdf",
                icon=":material/download:",
                data=pdf,
            )
        with col4:
            st.button(
                "Remove pdf", on_click=lambda: st.session_state.pop("pdf_streams")
            )

        pdf_viewer(pdf)
