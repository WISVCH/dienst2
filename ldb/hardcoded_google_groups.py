import datetime

"""
TODO: This file contains hardcoded Google Groups that are not retrieved from Google. This is because Dienst2 currently is not able to cache the Google Groups. This is a temporary solution to continue with the cloud migration. Please implement cachin ASAP.
"""


def get_book_year() -> int:
    # Get the current book year. The year starts at the 1st of September
    now = datetime.datetime.now()

    if now.month < 9:
        return now.year - 1

    return now.year


def get_board_year() -> int:
    """
    Return the current board year.
    Under the assumption that the board year starts at the 1st of September and that from now on only complete years are made.
    """
    return get_book_year() - 1956


YEAR = str(get_book_year())
BOARD_YEAR = str(get_board_year())
HARDCODED_PARENT_GROUPS = {
    "bestuur-group@ch.tudelft.nl": ["bestuur" + BOARD_YEAR + "@ch.tudelft.nl"],
    "vc": ["vc_" + YEAR + "@ch.tudelft.nl"],
    "galacie@ch.tudelft.nl": ["galacie" + YEAR + "@ch.tudelft.nl"],
    "hackdelft-commissie@ch.tudelft.nl": ["hackdelft_" + YEAR + "@ch.tudelft.nl"],
    "icom-commissie@ch.tudelft.nl": ["icom_" + YEAR + "@ch.tudelft.nl"],
}

SENAAT_GROUP = "senaat@ch.tudelft.nl"
HARDCODED_COMMITTEE_GROUPS = [
    "akcie",
    "annucie",
    "choco",
    "coh",
    "comma",
    "dies",
    "eiweiw",
    "facie",
    "flitcie",
    "lancie",
    "machazine",
    "maphya",
    "match",
    "sjaarcie",
    "symposium",
    "wiewie",
    "wifi",
    "wocky",
]


def get_parent_committee_group(group: str) -> str:
    """
    Returns the parent committee group of a group
    :param group: The group to get the parent committee group of
    :return: The parent committee group

    This function assigns for example choco_2022@ch.tudelft.nl to choco@ch.tudelft.nl in the year 2022-2023.
    """

    # Split the group name on the underscore and the @
    group_name = group.split("@")[0]
    if len(group_name.split("_")) < 2:
        return None
    committee = group_name.split("_")[0]
    year = group_name.split("_")[1]

    if year == YEAR and committee in HARDCODED_COMMITTEE_GROUPS:
        return committee + "@" + group.split("@")[1]

    return None


def get_indirect_groups(groups: list) -> list:
    """
    Returns all Google Groups that a member is an INDIRECT member of

    :param groups: List of groups to get the indirect groups of
    :return: List of indirect group email addresses
    """

    indirect_groups = []
    groups = groups.copy()

    while len(groups) > 0:
        group = groups.pop()

        # TODO: enable retrieval of parent groups via Google.
        # parent_group = get_parent_group(group)
        # if parent_group is not None:
        #     groups.append(parent_group)

        # Check if group begins with "bestuur" or "board"
        if group.startswith("bestuur") or group.startswith("board"):
            if group.endswith("@ch.tudelft.nl"):
                indirect_groups.append(SENAAT_GROUP)

        # Check if group has a committee parent group
        if get_parent_committee_group(group) is not None:
            indirect_groups.append(get_parent_committee_group(group))

        # Check if group is in values of HARDCODED_PARENT_GROUPS
        for key, value in HARDCODED_PARENT_GROUPS.items():
            if group in value:
                indirect_groups.append(key)

    return indirect_groups
