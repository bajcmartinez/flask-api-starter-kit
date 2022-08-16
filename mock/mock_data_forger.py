"""
mock_data_forger.py
- forge mocked data into database

Created by Xiong Kaijie on 2022-08-01.
Contributed by: Xiong Kaijie
Copyright © 2022 team Root of ByteDance Youth Camp. All rights reserved.
"""

from flask import Blueprint
import click
from ..api.model.models import User, RequestData, ErrorData
from .data_generator import UserMaterial, RequestMaterial, ErrorMaterial
from ..util.data_process import merge_failed_request

cmd = Blueprint('cmd', __name__)

@cmd.cli.command()
def forgeuser():
    users = UserMaterial().generate_user_data()

    for user in users:
        new_user = User(**user)
        new_user.save()
    
    click.echo('Users data added')


@cmd.cli.command()
def forgerequest():
    users = User.objects[:5]

    reqs = RequestMaterial().generate_request_data(users)

    for req in reqs:
        new_req = RequestData(**req)
        new_req.save()
    
    click.echo('Request data added')


@cmd.cli.command()
def forgeerror():
    users_a = User.objects[:20]
    users_b = User.objects[10:30]
    users_c = User.objects[20:40]
    users = list(users_a) + list(users_b) + list(users_c)

    errors = ErrorMaterial().generate_error_data(users)

    for er in errors:
        new_error = ErrorData(**er)
        new_error.save()
    
    merge_failed_request(None)
    
    click.echo('Error data added')