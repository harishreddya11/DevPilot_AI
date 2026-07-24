from app.models.document import Document
from app.parsers.parser_factory import ParserFactory


class DocumentProcessingService:

    def extract_text(
        self,
        document: Document,
    ) -> str:

        parser = ParserFactory.get_parser(document.filename)

        return parser.extract_text(document.storage_path)