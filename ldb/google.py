from urllib.parse import urlencode

from google.oauth2 import service_account
from googleapiclient.discovery import build

import environ

env = environ.Env()


def get_google_service(scopes=[]):
    """Returns a Google Directory API service object"""
    # Load the service account from the project root
    service_account_filepath = "google-service-account.json"
    credentials = service_account.Credentials.from_service_account_file(
        service_account_filepath, scopes=scopes
    )
    delegated_credentials = credentials.with_subject(
        env.str("GOOGLE_SERVICE_ACCOUNT_DELEGATED_USER")
    )
    return build("cloudidentity", "v1", credentials=delegated_credentials)


# Source: https://cloud.google.com/identity/docs/how-to/
# query-memberships#searching_for_all_group_memberships_of_a_member
def search_transitive_groups(service, member, page_size):
    groups = []
    next_page_token = ""
    while True:
        query_params = urlencode(
            {
                "query": (
                    "member_key_id == '{}' &&"
                    " 'cloudidentity.googleapis.com/groups.discussion_forum' in labels"
                    .format(member)
                ),
                "page_size": page_size,
                "page_token": next_page_token,
            }
        )
        request = (
            service.groups().memberships().searchTransitiveGroups(parent="groups/-")
        )
        request.uri += "&" + query_params
        response = request.execute()

        if "memberships" in response:
            groups += response["memberships"]

        if "nextPageToken" in response:
            next_page_token = response["nextPageToken"]
        else:
            next_page_token = ""

        if len(next_page_token) == 0:
            break

    return groups


def get_groups_by_user_key(userKey) -> list:
    """
    Returns all Google Groups that a member is a direct or indirectmember of

    :param userKey: Email or immutable ID of the user if only those groups are
    to be listed, the given user is a member of. If it's an ID, it should match
    with the ID of the user object.
    :param domains: Domains to search for groups. Ensure that these are set to
    prevent group name attacks by using other domains.

    :return: List of group email addresses

    (https://developers.google.com/admin-sdk/directory/reference/rest/v1/groups/list)
    """

    # User memberKey
    # https://developers.google.com/admin-sdk/directory/v1/reference/members/list

    service = get_google_service(
        [
            "https://www.googleapis.com/auth/cloud-identity.groups.readonly",
        ]
    )

    groups: list = []

    transitive_groups = search_transitive_groups(service, userKey, 50)
    for group in transitive_groups:
        print("group:", group)
        groups.append(group["groupKey"]["id"])

    # Replace "@ch.tudelft.nl" from the group names
    # 1. Replace "-commissie@ch.tudelft.nl" with ""
    # 2. Replace "-group@ch.tudelft.nl" with ""
    # 3. Replace "@ch.tudelft.nl" with ""

    return_groups = []
    for group in groups:
        group = group.replace("-commissie@ch.tudelft.nl", "")
        group = group.replace("-group@ch.tudelft.nl", "")
        group = group.replace("@ch.tudelft.nl", "")

        return_groups.append(group)

    return return_groups


def get_parent_group(group: str):
    """
    Returns the parent group of a group
    :param group: The group to get the parent group of
    :return: The parent group
    """

    service = get_google_service(
        [
            "https://www.googleapis.com/auth/admin.directory.group.readonly",
            "https://www.googleapis.com/auth/admin.directory.group.member.readonly",
        ]
    )

    data = service.groups().get(groupKey=group).execute()
    if "parent" in data:
        return data["parent"]
    return None
