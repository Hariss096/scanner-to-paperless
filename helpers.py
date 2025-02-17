import io
import streamlit as st
from scanner_helpers import trigger_scan, get_scanned_document
from paperless_helpers import send_to_paperless

from pypdf import PdfWriter


async def save_single_page_pdf(filename: str) -> None:
    scanned_document_url = await trigger_scan()
    print("scanned_document_url:", scanned_document_url)

    pdf_bytes = await get_scanned_document(scanned_document_url)

    send_to_paperless(filename, pdf_bytes)
    return scanned_document_url


async def save_multi_page_pdf() -> None:
    scanned_document_url = await trigger_scan()
    print("scanned_document_url:", scanned_document_url)

    pdf_bytes = await get_scanned_document(scanned_document_url)

    if not st.session_state.get("pdf_streams"):
        st.session_state.pdf_streams = [pdf_bytes]
    else:
        st.session_state.pdf_streams.append(pdf_bytes)


async def merge_and_send_to_paperless(doc_name: str) -> None:
    if not st.session_state.pdf_streams:
        st.toast(":red[No documents to merge]", icon="⚠️")
        return

    merger = PdfWriter()

    for stream in st.session_state["pdf_streams"]:
        pdf_file = io.BytesIO(stream)
        merger.append(pdf_file)

    output = io.BytesIO()
    merger.write(output)
    merger.close()

    merged_pdf = output.getvalue()

    doc_id = await send_to_paperless(doc_name, merged_pdf)
    if doc_id:
        st.session_state.pdf_streams = []
        st.toast(
            f":green[Merged document uploaded to Paperless with ID: {doc_id}]",
            icon="✅",
        )
