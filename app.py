import asyncio
import streamlit as st
from helpers import (
    save_single_page_pdf,
    save_multi_page_pdf,
    merge_and_send_to_paperless,
)


if __name__ == "__main__":
    st.header("Upload documents from scanner to Paperless")

    if "pdf_streams" not in st.session_state:
        st.session_state.pdf_streams = []

    is_multi_page = st.checkbox("Multiple pages pdf")

    if not is_multi_page:
        single_filename = st.text_input("Enter file name")
        triggered = st.button(
            "Scan to Paperless",
            disabled=not single_filename,
            on_click=lambda: asyncio.run(save_single_page_pdf(single_filename)),
        )
    else:
        st.button(
            "Scan next document",
            on_click=lambda: asyncio.run(save_multi_page_pdf()),
        )
        st.write(f"No. of pages: {len(st.session_state.pdf_streams)}")

        merged_filename = st.text_input("Enter merged document name")

        st.button(
            "Merge document in paperless",
            disabled=not merged_filename or not st.session_state.pdf_streams,
            on_click=lambda: asyncio.run(merge_and_send_to_paperless(merged_filename)),
        )
