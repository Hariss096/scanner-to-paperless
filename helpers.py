import io
import streamlit as st
from scanner_helpers import trigger_scan, get_scanned_document
from paperless_helpers import send_to_paperless

from pypdf import PdfWriter


async def scan_and_upload_to_paperless(filename: str) -> None:
    scanned_document_url = await trigger_scan()
    print("scanned_document_url:", scanned_document_url)

    pdf_bytes = await get_scanned_document(scanned_document_url)

    await send_to_paperless(filename, pdf_bytes)
    return scanned_document_url


async def trigger_scan_and_get_doc() -> None:
    scanned_document_url = await trigger_scan()
    print("scanned_document_url:", scanned_document_url)

    return await get_scanned_document(scanned_document_url)


def get_merged_pdf_bytes() -> bytes | None:
    if not st.session_state.pdf_streams:
        return None
    merger = PdfWriter()

    for stream in st.session_state["pdf_streams"]:
        pdf_file = io.BytesIO(stream)
        merger.append(pdf_file)

    output = io.BytesIO()
    merger.write(output)
    merger.close()

    return output.getvalue()


async def merge_and_send_to_paperless(doc_name: str) -> None:
    if not st.session_state.pdf_streams:
        st.toast(":red[No documents to merge]", icon="⚠️")
        return

    doc_id = await send_to_paperless(doc_name, get_merged_pdf_bytes())
    if doc_id:
        st.toast(
            f":green[Merged document uploaded to Paperless with ID: {doc_id}]",
            icon="✅",
        )
