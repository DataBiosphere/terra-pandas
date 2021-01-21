import os

os.environ['GCLOUD_PROJECT'] = os.environ.get('GCLOUD_PROJECT', "firecloud-cgl")
os.environ['WORKSPACE_NAME'] = os.environ.get('WORKSPACE_NAME', "terra-notebook-utils-tests")

cred_data = os.environ.get("TNU_GCP_SERVICE_ACCOUNT_CREDENTIALS_DATA")
if cred_data:
    import base64
    with open("creds.json", "wb") as fh:
        fh.write(base64.b64decode(cred_data))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "creds.json"
