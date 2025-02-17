from aiohttp import ClientSession
from http import HTTPStatus

from base64 import b64encode
from os import getenv
import streamlit as st
from decorators import client_session
from dotenv import load_dotenv

load_dotenv()


SCANNER_BASIC_AUTH = b64encode(getenv("SCANNER_BASIC_AUTH").encode("utf-8"))
SCANNER_HOST = getenv("SCANNER_HOST")


@client_session
async def trigger_scan(session: ClientSession) -> str | None:
    with open("assets/hp_2700_deskjet.xml", "rb") as f:
        scan_settings = f.read()

    async with session.post(
        url=f"{SCANNER_HOST}eSCL/ScanJobs",
        headers={"Authorization": f"Basic {SCANNER_BASIC_AUTH}"},
        data=scan_settings,  # TODO: Add controls for scan settings
    ) as scan_trigger_response:
        if scan_trigger_response.status == HTTPStatus.CREATED:
            st.toast(
                f":green[Scan request sent successfully...: {scan_trigger_response.status}]",
                icon="✅",
            )
            return scan_trigger_response.headers["Location"]
        else:
            st.toast(
                f":red[Scan request could not be sent: {scan_trigger_response.status}]",
                icon="❌",
            )
            print(
                "Scan trigger response:",
                f"{SCANNER_HOST}eSCL/ScanJobs",
                await scan_trigger_response.read(),
            )
            return


@client_session
async def get_scanned_document(session: ClientSession, location: str) -> bytes | None:
    async with session.get(url=f"{location}/NextDocument") as scanned_doc_response:
        if not scanned_doc_response.status == HTTPStatus.OK:
            st.toast(
                f":red[Document could not be scanned: {scanned_doc_response.status}]",
                icon="❌",
            )
            return

        pdf = await scanned_doc_response.read()

        st.toast(
            f":green[Document scanned successfully...: {scanned_doc_response.status}]",
            icon="✅",
        )
        # async with aiofiles.open("test.pdf", "+wb") as f:
        # await f.write(content)

    return pdf
