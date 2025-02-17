import aiohttp
from http import HTTPStatus
from decorators import client_session

from os import getenv
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

PAPERLESS_URL = getenv("PAPERLESS_URL")
PAPERLESS_API_TOKEN = getenv("PAPERLESS_API_TOKEN")


@client_session
async def send_to_paperless(session: aiohttp.ClientSession, filename: str, pdf: bytes) -> str | None:
    if not filename.endswith(".pdf"):
        filename += ".pdf"
    async with session.post(
        f"{PAPERLESS_URL}api/documents/post_document/",
        headers={"Authorization": f"Token {PAPERLESS_API_TOKEN}"},
        data={"title": filename, "document": pdf},
    ) as paperless_response:
        if paperless_response.status == HTTPStatus.OK:
            st.toast(
                f":green[Document uploaded to paperless successfully...: {paperless_response.status}]",
                icon="✅",
            )
            return await paperless_response.json()
        else:
            st.toast(
                f":red[Document could not be uploaded to paperless: {paperless_response.status}]",
                icon="❌",
            )
