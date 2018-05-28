from __future__ import print_function
import apiclient.discovery
from email.mime.text import MIMEText
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import fetch_unreads

# Setup the Gmail API
SCOPES = 'https://mail.google.com/'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = apiclient.discovery.build('gmail', 'v1', http=creds.authorize(Http()))


#
# # Call the Gmail API
# results = service.users().labels().list(userId='me').execute()
# labels = results.get('labels', [])


def create_draft(service, user_id, message_body):
    try:
        message = {'message': message_body}
        draft = service.users().drafts().create(userId=user_id, body=message).execute()

        print('Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))

        return draft
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None


def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
            .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def deleteDraft(service, user_id, draft_id):
    try:
        service.users().drafts().delete(userId=user_id, id=draft_id).execute()
        print('Draft with id: %s deleted successfully.' % draft_id)
    except errors.HttpError as  error:
        print('An error occurred: %s' % error)


def getDraftId(draft):
    draft_id = draft['id']
    return draft_id


def ListDrafts(service, user_id):
    try:
        response = service.users().drafts().list(userId=user_id).execute()
        drafts = response['drafts']
        return drafts
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def getDraft(service, user_id, draft_id):
    try:
        draft = service.users().drafts().get(user_id=user_id, id=draft_id).execute()

        print('Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))

        return draft
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def listInbox(p_service, user_id):  # gets the ID's of the inbox elements
    try:
        response = p_service.users().messages().list(userId=user_id).execute()
        mails = response['messages']
        return mails
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


fetch_unreads.fetch_unreads()
fetch_unreads.trash_security_updates()
