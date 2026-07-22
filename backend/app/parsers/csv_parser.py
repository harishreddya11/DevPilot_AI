from pathlib import Path

import pandas as pd

from app.parsers.base_parser import BaseParser


class CSVParser(BaseParser):
    """
    Parser for CSV files.
    """

    def extract_text(
        self,
        file_path: str,
    ) -> str:

        dataframe = pd.read_csv(Path(file_path))

        return dataframe.to_string(index=False)