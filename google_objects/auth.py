import os

import httplib2
from apiclient import discovery


def service_account_creds(creds_path, delegated_user=None, scope=None):
    """Return httplib2 client, used for discovery.build usage."""
    from oauth2client.service_account import ServiceAccountCredentials

    # use env vars if parameters aren't given
    if not creds_path:
        creds_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_CREDENTIALS')
    if not delegated_user:
        user = os.getenv('GOOGLE_DELEGATED_USER')

    creds_path = os.path.expanduser(creds_path)
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        creds_path, _gen_scopes(scope)
    )

    # create delegated if user exists
    if user:
        creds = creds.create_delegated(user)

    return creds.authorize(httplib2.Http())


def build_resource(service, version, creds=None, api_key=None, **kwargs):
    """Create an API specific HTTP resource."""

    if not (api_key or creds):
        raise ValueError('Credentials or API Key Required')

    if api_key:
        resource = discovery.build(
            service, version, developerKey=api_key, **kwargs
        )

    if creds:
        http = creds.authorize(httplib2.Http())
        resource = discovery.build(service, version, http=http, **kwargs)

    return resource
