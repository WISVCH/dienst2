from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import environ

env = environ.Env()


def getGoogleService(scopes=[]):
    """Returns a Google Directory API service object"""
    # Load the service account from the project root
    service_account_filepath = "google-service-account.json"
    credentials = service_account.Credentials.from_service_account_file(service_account_filepath, scopes=scopes)
    delegated_credentials = credentials.with_subject(env.str("GOOGLE_SERVICE_ACCOUNT_DELEGATED_USER"))
    return build("admin", "directory_v1", credentials=delegated_credentials)



def getGroupsByUserKey(userKey, domains=["wisv.ch", "ch.tudelft.nl"]) -> list:
    """
    Returns all Google Groups that a member is a DIRECT member of

    :param userKey: Email or immutable ID of the user if only those groups are to be listed, the given user is a member of. If it's an ID, it should match with the ID of the user object.
    :param domains: Domains to search for groups. Ensure that these are set to prevent group name attacks by using other domains.

    :return: List of group email addresses
    
    (https://developers.google.com/admin-sdk/directory/reference/rest/v1/groups/list)
    """

    # User memberKey
    # https://developers.google.com/admin-sdk/directory/v1/reference/members/list

    service = getGoogleService(
        [
            "https://www.googleapis.com/auth/admin.directory.group.readonly",
            "https://www.googleapis.com/auth/admin.directory.group.member.readonly",
        ]
    )

    groups : list = []
    for domain in domains:
        data = service.groups().list(userKey=userKey, domain=domain).execute()
        if "groups" in data:
            for group in data["groups"]:
                groups.append(group["email"])

    return groups

# def getGoogleGroups(domains=["wisv.ch", "ch.tudelft.nl"]):
#     """Returns all Google Groups"""
#     service = getGoogleService(
#         [
#             "https://www.googleapis.com/auth/admin.directory.group.readonly",
#             "https://www.googleapis.com/auth/admin.directory.group.member.readonly",
#         ]
#     )

#     groups = []
#     for domain in domains:
#         data = service.groups().list(domain=domain).execute()
#         if "groups" in data:
#             groups += data["groups"]
#     return groups

# def addMemberToGoogleGroup(email, group_name, role="MEMBER", logfile=None):
#     """Adds a member to a Google Group"""
#     service = getGoogleService(["https://www.googleapis.com/auth/admin.directory.group.member"])
#     member = {"email": email, "role": role}

#     try:
#         service.members().insert(groupKey=group_name, body=member).execute()
#     except HttpError as e:
#         if e.resp.status == 409:
#             print("- ERROR: Member {} already exists in group {}".format(email, group_name), file=logfile)
#         elif e.resp.status == 412:
#             print("- ERROR: Member {} cannot be added to group {} because it does not meet the required group permissions".format(email, group_name), file=logfile)
#         else:
#             print("- ERROR: Failed to add member {} to group {}".format(email, group_name), file=logfile)
#             raise e


if __name__ == "__main__":
    print(getGroupsByUserKey("joepj@ch.tudelft.nl"))
