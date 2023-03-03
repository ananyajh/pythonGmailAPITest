import logging
from googleapiclient.errors import HttpError
from main import get_service

# https://support.google.com/mail/answer/7190


def search_email(query_param):
    """ Keywords supported: from, to, subject,cc,bcc,label,has,category,filename, before, after, in, is
    """

    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f"query parameter {query_param}")
    service = get_service()

    try:
        # call the Gmail API messages list function using query parameters
        results = service.users().messages().list(userId='me', q=query_param).execute()
        if results['resultSizeEstimate'] > 0:
            for message in results["messages"]:
                print(message)
        else:
            print(f"No emails match your search query. Try a different keyword [from,to,subject,label,has,category,"
                  f"filename,before,after,in,is]")

    except HttpError as error:
        print("Exception:", {error})


query_param = input("Enter query parameter to search your emails:")
search_email(query_param)
