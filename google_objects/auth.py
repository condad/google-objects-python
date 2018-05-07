import os

import httplib2
# from apiclient import discovery

_SCOPES = {
    'drive',
    'spreadsheets',
    'slides'
}


def _gen_scopes(scopes):
    return ['https://www.googleapis.com/auth/' + each for each in scopes]


def service_account_creds(creds_path, delegated_user=None, scope=None):
    """Return httplib2 client, used for discovery.build usage."""
    from oauth2client.service_account import ServiceAccountCredentials

    # use env vars if parameters aren't given
    if not creds_path:
        creds_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_CREDENTIALS')
    if not delegated_user:
        delegated_user = os.getenv('GOOGLE_DELEGATED_USER')

    creds_path = os.path.expanduser(creds_path)
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        creds_path, _gen_scopes(scope)
    )

    # create delegated if user exists
    if delegated_user:
        creds = creds.create_delegated(delegated_user)

    return creds.authorize(httplib2.Http())
