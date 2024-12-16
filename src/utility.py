import os
import sys
from pathlib import Path


# Fungsi resource_path untuk akses sumber daya
def resource_path(relative_path):
    """Dapatkan path absolut ke file sumber daya."""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


# Konstanta global
ERROR_TITLE = "Error"
RECEIPT_PATH = Path("/private/var/db/receipts")
