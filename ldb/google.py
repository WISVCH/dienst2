from google.oauth2 import service_account
from googleapiclient.discovery import build
from ldb.hardcoded_google_groups import get_indirect_groups

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
    return build("admin", "directory_v1", credentials=delegated_credentials)


def get_groups_by_user_key(
    userKey, domains=["wisv.ch", "ch.tudelft.nl"], indirect=False
) -> list:
    """
    Returns all Google Groups that a member is a DIRECT member of

    :param userKey: Email or immutable ID of the user if only those groups are to be listed, the given user is a member of. If it's an ID, it should match with the ID of the user object.
    :param domains: Domains to search for groups. Ensure that these are set to prevent group name attacks by using other domains.
    :param indirect: Whether to include indirect groups

    :return: List of group email addresses

    (https://developers.google.com/admin-sdk/directory/reference/rest/v1/groups/list)
    """

    # User memberKey
    # https://developers.google.com/admin-sdk/directory/v1/reference/members/list

    service = get_google_service(
        [
            "https://www.googleapis.com/auth/admin.directory.group.readonly",
            "https://www.googleapis.com/auth/admin.directory.group.member.readonly",
        ]
    )

    groups: list = []
    for domain in domains:
        data = service.groups().list(userKey=userKey, domain=domain).execute()
        if "groups" in data:
            for group in data["groups"]:
                groups.append(group["email"])

    if indirect:
        indirect_groups = get_indirect_groups(groups)
        groups.extend(indirect_groups)

    return groups


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


if __name__ == "__main__":
    groups = get_groups_by_user_key("joepj@ch.tudelft.nl")

    groups.append("choco_2022@ch.tudelft.nl")

    print("Direct groups:")
    print(groups)

    print("Indirect groups:")
    print(get_indirect_groups(groups))
