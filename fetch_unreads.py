from __future__ import print_function
import apiclient.discovery
from httplib2 import Http
from oauth2client import file
import base64
from bs4 import BeautifulSoup
import dateutil.parser as parser


def fetch_unreads():
    SCOPES = 'https://mail.google.com/'
    store = file.Storage('credentials.json')
    creds = store.get()
    service = apiclient.discovery.build('gmail', 'v1', http=creds.authorize(Http()))

    label_id_one = 'INBOX'
    label_id_two = 'UNREAD'

    unread_messages = service.users().messages().list(userId='me', labelIds=[label_id_one, label_id_two]).execute()

    msg_list = unread_messages['messages']
    print("Total unread messages in inbox: ", str(len(msg_list)))

    final_list = []
    msg_number = 1
    format = "-->"
    for mssg in msg_list:
        temp_dict = {}
        m_id = mssg['id']  # get id of individual message
        message = service.users().messages().get(userId='me', id=m_id).execute()  # fetch the message using API
        payld = message['payload']  # get payload of the message
        headr = payld['headers']  # get header of the payload

        for one in headr:  # getting the Subject
            if one['name'] == 'Subject':
                msg_subject = one['value']
                temp_dict['Subject'] = msg_subject
            else:
                pass

        for two in headr:  # getting the date
            if two['name'] == 'Date':
                msg_date = two['value']
                date_parse = (parser.parse(msg_date))
                m_date = (date_parse.date())
                temp_dict['Date'] = str(m_date)
            else:
                pass

        for three in headr:  # getting the Sender
            if three['name'] == 'From':
                msg_from = three['value']
                temp_dict['Sender'] = msg_from
            else:
                pass

        temp_dict['Snippet'] = message['snippet']  # fetching message snippet

        try:

            # Fetching message body
            mssg_parts = payld['parts']  # fetching the message parts
            part_one = mssg_parts[0]  # fetching first element of the part
            part_body = part_one['body']  # fetching body of the message
            part_data = part_body['data']  # fetching data from the body
            clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
            clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
            clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
            soup = BeautifulSoup(clean_two, "lxml")
            mssg_body = soup.body()
            # mssg_body is a readable form of message body
            # depending on the end user's requirements, it can be further cleaned
            # using regex, beautiful soup, or any other method
            temp_dict['Message_body'] = mssg_body

        except:
            pass

        final_list.append(temp_dict)  # This will create a dictionary item in the final list

        print(msg_number, format, temp_dict)
        print()
        msg_number = msg_number + 1


def trash_security_updates():
    store = file.Storage('credentials.json')
    creds = store.get()
    service = apiclient.discovery.build('gmail', 'v1', http=creds.authorize(Http()))

    label_id_one = 'INBOX'
    label_id_two = 'UNREAD'

    unread_messages = service.users().messages().list(userId='me', labelIds=[label_id_one, label_id_two]).execute()

    msg_list = unread_messages['messages']
    print("Total unread messages in inbox: ", str(len(msg_list)))

    for mssg in msg_list:
        temp_dict = {}
        m_id = mssg['id']  # get id of individual message
        message = service.users().messages().get(userId='me', id=m_id).execute()  # fetch the message using API
        payld = message['payload']  # get payload of the message
        headr = payld['headers']  # get header of the payload

        for one in headr:  # getting the Subject
            if one['name'] == 'Subject':
                msg_subject = one['value']
                if "Privacy" in msg_subject or "Policy" in msg_subject:
                    print("I FOUND SPAMM")
                    service.users().messages().trash(userId='me', id=m_id).execute()
                    print(m_id + " has been deleted")

                temp_dict['Subject'] = msg_subject
            else:
                pass
