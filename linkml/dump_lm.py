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

from models.linkml_models import (
    Base,
    DashboardUser,
)

from api.models import( 
    DashboardUser as DashboardUserApi
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

    u1 = users[0]
    
    dbuser = {
        "email": u1.email,
        "id": u1.id,
        "active": u1.active,
        "submissions": [
            {
                "submitted_to_ncei": u1.submissions[0].submitted_to_ncei,
                "created": u1.submissions[0].created,
                "modified": u1.submissions[0].modified,
                "oads_metadata": [{
                    "id": u1.submissions[0].oads_metadata[0].id,
                    "title": u1.submissions[0].oads_metadata[0].title,
                    "abstract": u1.submissions[0].oads_metadata[0].abstract,
                    "data_license": u1.submissions[0].oads_metadata[0].data_license,
                    "related_datasets": u1.submissions[0].oads_metadata[0].related_datasets,
                    "investigators": [
                        {
                            "id": u1.submissions[0].oads_metadata[0].investigators[0].id,
                            "first_name": u1.submissions[0].oads_metadata[0].investigators[0].first_name,
                            "last_name": u1.submissions[0].oads_metadata[0].investigators[0].last_name,
                        },
                    ],
                    "data_submitter": [
                        {
                            "id": u1.submissions[0].oads_metadata[0].data_submitters[0].id,
                            "first_name": u1.submissions[0].oads_metadata[0].data_submitters[0].first_name,
                            "last_name": u1.submissions[0].oads_metadata[0].data_submitters[0].last_name,
                        },
                    ]
                }],
            }
        ]
    }

    with open('lm_dump.json', "w") as f:
        json.dump(dbuser, f, indent=4)

    adapter = TypeAdapter(List[DashboardUserApi])
    try:
        schema_users = adapter.validate_python(users)
        print(json.dumps(schema_users, default=pydantic_encoder, indent=4))
    except ValidationError as e:
        print(e)


    try:
        DashboardUserApi.model_validate(u1)
    except ValidationError as ve:
        print(ve)
    
