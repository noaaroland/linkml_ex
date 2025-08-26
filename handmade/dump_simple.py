from typing import List
from dash.html import Sub
import models.shared
import flask
from flask import jsonify
import os
from pathlib import Path
from sqlalchemy import select, and_
from pydantic.json import pydantic_encoder
import json

from models.extras.metadata import (
    Base,
    DashboardUser,
    DashboardUserSchema,
)

import constants

from sqlalchemy.orm import Session

from pydantic import ValidationError, TypeAdapter

db = models.shared.db
server = flask.Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:docker@127.0.0.1:5432"
)
server.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
db.init_app(server)

with server.app_context():
    Base.metadata.create_all(bind=constants.postgres_engine)

# book1 = Book(title="A Good Book")
# book2 = Book(title="A Better Book")
# author = Author(name="Joe Blow", books=[book1, book2])

with Session(constants.postgres_engine) as session:
    session = Session(constants.postgres_engine)
    users = session.query(DashboardUser).all()
    adapter = TypeAdapter(List[DashboardUserSchema])
    try:
        schema_users = adapter.validate_python(users)
        print(json.dumps(schema_users, default=pydantic_encoder, indent=4))
    except ValidationError as e:
        print(e)
    
    
