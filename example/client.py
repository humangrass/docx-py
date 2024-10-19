import logging
import os
import sys
import uuid

import grpc
from google.protobuf.struct_pb2 import Struct

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database.db import get_db
from app.models.template import Template
from app.docx_py_pb2 import DocumentRequest
from app.docx_py_pb2_grpc import DocxPyStub

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_template(template_name: str, client_uuid: uuid.UUID, template_path: str) -> Template:
    try:
        with next(get_db()) as db:
            new_template = Template(
                name=template_name,
                client_uuid=client_uuid,
                path=template_path
            )
            db.add(new_template)
            db.commit()
            db.refresh(new_template)
            logger.info(
                f"Added template with ID: {new_template.id}, Name: {new_template.name}, Path: {new_template.path}")
            return new_template
    except Exception as e:
        logger.error(f"Failed to add template: {e}")
        raise


def delete_template(template: Template) -> None:
    try:
        with next(get_db()) as db:
            db.delete(template)
            db.commit()
            logger.info(f"Deleted template with ID: {template.id}")
    except Exception as e:
        logger.error(f"Failed to delete template: {e}")


def run():
    template_path = os.path.join(os.path.dirname(__file__), 'template.docx')
    client_uuid = uuid.uuid4()
    template = add_template('example', client_uuid, template_path)
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = DocxPyStub(channel)

            context = Struct()
            context.update({
                'name': "Bob",
                'total': "$300",
                'orders': [
                    {'id': 123, 'item': 'Sponge', 'price': 100.0},
                    {'id': 321, 'item': 'Shampoo', 'price': 200.0},
                ],
            })

            request = DocumentRequest(
                template_id=template.id,
                client_uuid=str(template.client_uuid),
                context=context,
            )

            response = stub.GenerateDocument(request, timeout=10)

            with open("generated_document.docx", "wb") as f:
                f.write(response.document)
                logger.info("Document generated")
    except Exception as e:
        logger.error(f"Error while generating document: {e}")
    finally:
        delete_template(template)


if __name__ == '__main__':
    run()
