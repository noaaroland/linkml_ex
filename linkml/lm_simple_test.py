from typing import List
from dash.html import Sub
import models.shared
import flask
from flask import jsonify
import os
from pathlib import Path
from sqlalchemy import select

# from models.metadata import Book, Author, Document, File, Submission, Submitter
from models.linkml_models import (
    Base,
    DashboardUser,
    Person,
    MetadataRole,
    OadsMetadata,
    Submission,
)

import constants

from sqlalchemy.orm import Session

db = models.shared.db
server = flask.Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:docker@127.0.0.1:5432"
)
server.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
db.init_app(server)

with server.app_context():
    Base.metadata.create_all(bind=constants.postgres_engine)

with Session(constants.postgres_engine) as session:
    stmt = select(MetadataRole).where(MetadataRole.name=='Data Submitter')
    data_submitter_role = session.scalars(stmt).one()
    stmt2 = select(MetadataRole).where(MetadataRole.name=='Investigator')
    investigator_role = session.scalars(stmt2).one()
    user = DashboardUser(email='roland.schweitzer@noaa.gov')

    # TypeError: 'dashboard_user' is an invalid keyword argument for Person

    # So make the people separately without the dashboard_user property and attach them to the user.abs

    investigator = Person(
                            first_name="Only",
                            last_name="Investigator",
    )
    
    submitter = Person(first_name="First",
                                last_name="Labworker",
    )

    user.people = [investigator, submitter]

    submission = Submission(
        # TypeError: Incompatible collection type: OadsMetadata is not list-like
        # Is there ever more than one
                oads_metadata=[OadsMetadata(
                    title="Data",
                    abstract="An Abstract",
                    data_license="free",
                    investigators=[
                        investigator
                    ],
                    data_submitters=[
                        submitter
                    ]
                )],
            )
  
    user.submissions = [submission]

    session.add(user)
    session.commit()