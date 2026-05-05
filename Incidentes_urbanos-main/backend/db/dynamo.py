import boto3
import os
<<<<<<< HEAD
=======
from botocore.exceptions import ClientError
>>>>>>> 5748750 (Proyecto pruebas para despliegue)
from dotenv import load_dotenv

load_dotenv()

DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT", None)
<<<<<<< HEAD
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

def get_dynamodb():
    if DYNAMODB_ENDPOINT:
        return boto3.resource(
            "dynamodb",
            region_name=AWS_REGION,
            endpoint_url=DYNAMODB_ENDPOINT,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "local"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "local"),
        )
    else:
        return boto3.resource(
            "dynamodb",
            region_name=AWS_REGION,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

def get_table():
    db = get_dynamodb()
    return db.Table("Incidentes")

def create_table_if_not_exists():
    db = get_dynamodb()
    existing = [t.name for t in db.tables.all()]

    if "Incidentes" in existing:
        print("✅ Tabla 'Incidentes' ya existe.")
        return

    db.create_table(
        TableName="Incidentes",
        KeySchema=[
            {"AttributeName": "CiudadZona", "KeyType": "HASH"},
            {"AttributeName": "FechaID",    "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "CiudadZona", "AttributeType": "S"},
            {"AttributeName": "FechaID",    "AttributeType": "S"},
            {"AttributeName": "categoria",  "AttributeType": "S"},
            {"AttributeName": "estado",     "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
=======
AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def get_dynamodb():
    params = {
        "region_name": AWS_REGION,
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
    }
    if DYNAMODB_ENDPOINT:
        params["endpoint_url"] = DYNAMODB_ENDPOINT
        print(f"🔌 Conectando a DynamoDB Local en: {DYNAMODB_ENDPOINT}")
    else:
        print(f"☁️  Conectando a AWS DynamoDB — región: {AWS_REGION}")
    return boto3.resource("dynamodb", **params)


def get_table(table_name: str = "Incidentes"):
    return get_dynamodb().Table(table_name)


# ─── Definiciones de tablas ────────────────────────────────────────────────────

TABLES = {
    "Incidentes": {
        "KeySchema": [
            {"AttributeName": "CiudadZona", "KeyType": "HASH"},
            {"AttributeName": "FechaID", "KeyType": "RANGE"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "CiudadZona", "AttributeType": "S"},
            {"AttributeName": "FechaID", "AttributeType": "S"},
            {"AttributeName": "categoria", "AttributeType": "S"},
            {"AttributeName": "estado", "AttributeType": "S"},
            {"AttributeName": "incidente_id", "AttributeType": "S"},
        ],
        "GlobalSecondaryIndexes": [
>>>>>>> 5748750 (Proyecto pruebas para despliegue)
            {
                "IndexName": "GSI-categoria",
                "KeySchema": [{"AttributeName": "categoria", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
            {
                "IndexName": "GSI-estado",
                "KeySchema": [{"AttributeName": "estado", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
<<<<<<< HEAD
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    print("✅ Tabla 'Incidentes' creada correctamente.")
=======
            {
                "IndexName": "GSI-incidente-id",
                "KeySchema": [{"AttributeName": "incidente_id", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },
    "Usuarios": {
        "KeySchema": [
            {"AttributeName": "usuario_id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "usuario_id", "AttributeType": "S"},
            {"AttributeName": "email", "AttributeType": "S"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "GSI-email",
                "KeySchema": [{"AttributeName": "email", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },
    "AuditLog": {
        "KeySchema": [
            {"AttributeName": "audit_id", "KeyType": "HASH"},
            {"AttributeName": "timestamp", "KeyType": "RANGE"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "audit_id", "AttributeType": "S"},
            {"AttributeName": "timestamp", "AttributeType": "S"},
            {"AttributeName": "usuario_id", "AttributeType": "S"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "GSI-usuario",
                "KeySchema": [{"AttributeName": "usuario_id", "KeyType": "HASH"},
                              {"AttributeName": "timestamp", "KeyType": "RANGE"}],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },
}


def _create_table(db, name: str, definition: dict):
    try:
        table = db.Table(name)
        table.table_status  # raises ResourceNotFoundException if missing
        print(f"✅ Tabla '{name}' ya existe.")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            print(f"🚀 Creando tabla '{name}'...")
            db.create_table(TableName=name, **definition)
            waiter = db.meta.client.get_waiter("table_exists")
            waiter.wait(TableName=name)
            print(f"✅ Tabla '{name}' creada.")
        else:
            print(f"❌ Error en tabla '{name}': {e}")
            raise


def create_all_tables():
    db = get_dynamodb()
    for name, definition in TABLES.items():
        _create_table(db, name, definition)
>>>>>>> 5748750 (Proyecto pruebas para despliegue)
