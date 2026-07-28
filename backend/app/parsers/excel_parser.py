import pandas as pd

from app.parsers.base_parser import BaseParser


class ExcelParser(BaseParser):
    """
    Parser for Excel (.xlsx/.xls) files.
    """

    def extract_text(
        self,
        file_path: str,
    ) -> str:

        excel = pd.ExcelFile(file_path)

        sheets = []

        for sheet in excel.sheet_names:

            dataframe = pd.read_excel(
                excel,
                sheet_name=sheet,
            )

            sheets.append(f"Sheet: {sheet}")
            sheets.append(dataframe.to_string(index=False))

        return "\n\n".join(sheets)