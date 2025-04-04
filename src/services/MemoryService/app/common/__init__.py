import sys
import os

# Абсолютный путь до реального пакета common
real_common_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../common")
)

if real_common_path not in sys.path:
    sys.path.insert(0, real_common_path)
