#i don't have any idea how to take on testing pdf readers in python, this is output from the chat

import os
import pytest
from pypdf import PdfWriter, PdfReader
from PDF_conversions import decryption, reorder_pages, add_pages


@pytest.fixture
def sample_pdfs(tmp_path):
    """Creates sample PDFs for testing."""
    file1 = tmp_path / "file1.pdf"
    file2 = tmp_path / "file2.pdf"

    # Create two simple PDFs
    w1 = PdfWriter()
    w1.add_blank_page(width=100, height=100)
    w1.add_blank_page(width=100, height=100)
    with open(file1, "wb") as f:
        w1.write(f)

    w2 = PdfWriter()
    w2.add_blank_page(width=100, height=100)
    with open(file2, "wb") as f:
        w2.write(f)

    return file1, file2


def test_reorder_pages(tmp_path, sample_pdfs):
    file1, _ = sample_pdfs
    output = tmp_path / "out.pdf"

    reorder_pages(file1, output, "2,1")

    reader = PdfReader(output)
    assert len(reader.pages) == 2


def test_add_pages(tmp_path, sample_pdfs):
    file1, file2 = sample_pdfs
    output = tmp_path / "merged.pdf"

    add_pages(file1, file2, output)

    reader = PdfReader(output)
    # file1 has 2 pages, file2 has 1 page
    assert len(reader.pages) == 3


def test_decrypt_pdf_unencrypted(tmp_path, sample_pdfs, monkeypatch):
    file1, _ = sample_pdfs
    output = tmp_path / "decrypted.pdf"

    # Monkeypatch input() since the file isn’t encrypted
    monkeypatch.setattr("builtins.input", lambda _: "password")

    decryption(file1, output)

    assert os.path.exists(output)
