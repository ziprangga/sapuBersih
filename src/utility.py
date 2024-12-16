import os
import sys


# Fungsi resource_path untuk akses sumber daya
def resource_path(relative_path):
    """Dapatkan path absolut ke file sumber daya."""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)
