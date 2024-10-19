import os
import io
import logging
import grpc
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.orm import Session
from database.db import get_db
from docx_py_pb2 import DocumentResponse
from docx_py_pb2_grpc import DocxPyServicer, add_DocxPyServicer_to_server
from docxtpl import DocxTemplate

from models.template import Template

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %z'
)
logger = logging.getLogger(__name__)


class DocumentGenerator:
    @staticmethod
    def generate(template_path: str, context: dict) -> bytes:
        logger.info(f"Generating document from template: {template_path}")

        doc = DocxTemplate(template_path)
        doc.render(context)

        output = io.BytesIO()
        doc.save(output)

        return output.getvalue()


class Service(DocxPyServicer):
    def __init__(self, db: Session):
        self.db = db
        self.generator = DocumentGenerator()

    def GenerateDocument(self, request, context):
        logger.info(
            f"Received document generation request for template_id: {request.template_id} and client_uuid: {request.client_uuid}")

        template = self.db.query(Template).filter_by(id=request.template_id, client_uuid=request.client_uuid).first()

        if not template:
            logger.info(f"Template not found for id {request.template_id} and client_uuid {request.client_uuid}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(
                f"Template with id {request.template_id} and client_uuid {request.client_uuid} not found.")
            return DocumentResponse()

        document_as_bytes = self.generator.generate(str(template.path), request.context)

        return DocumentResponse(document=document_as_bytes)


def create_grpc_server(max_workers: int, is_production: bool, port: str):
    server = grpc.server(ThreadPoolExecutor(max_workers=max_workers))

    db = next(get_db())

    add_DocxPyServicer_to_server(Service(db=db), server)

    if is_production:
        cert_file = os.getenv('DOCX_PY_CERT_FILE', 'server.crt')
        key_file = os.getenv('DOCX_PY_KEY_FILE', 'server.key')

        with open(cert_file, 'rb') as f:
            server_cert = f.read()
        with open(key_file, 'rb') as f:
            server_key = f.read()

        server_credentials = grpc.ssl_server_credentials(((server_key, server_cert),))
        server.add_secure_port(f'[::]:{port}', server_credentials)
        logger.info(f"Starting secure gRPC server on port {port}")
    else:
        server.add_insecure_port(f'[::]:{port}')
        logger.info(f"Starting insecure gRPC server on port {port}")

    return server


def main():
    max_workers = int(os.getenv('DOCX_PY_MAX_WORKERS', '10'))
    port = os.getenv('DOCX_PY_PORT', '50051')
    is_production = os.getenv('DOCX_PY_IS_PRODUCTION', 'false').lower() == 'true'

    logger.info("Initializing gRPC server...")
    server = create_grpc_server(max_workers, is_production, port)

    server.start()
    logger.info(f"gRPC server started on port {port}")
    server.wait_for_termination()


if __name__ == '__main__':
    main()
