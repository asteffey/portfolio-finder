"""
pytests for portfoliofinder.Contributions module
"""

from portfoliofinder.contributions import InitialContribution
from portfoliofinder.contributions import RegularContributions
from portfoliofinder.contributions import ScheduledContributions
from portfoliofinder.contributions import DEFAULT_CONTRIBUTION


def test_initial_contribution():
    """
    verify that InitialContribution returns starting_value
    for initial year, and nothing for subsequent years
    """
    contributions = InitialContribution(500)
    assert contributions.get_contribution_for_year(0) == 500
    assert contributions.get_contribution_for_year(1) == 0
    assert contributions.get_contribution_for_year(10) == 0


def test_regular_contributions():
    """
    verify that RegularContributions returns starting_value
    for initial year, and annual_contribution for subsequent years
    """
    contributions = RegularContributions(500, 100)
    assert contributions.get_contribution_for_year(0) == 500
    assert contributions.get_contribution_for_year(1) == 100
    assert contributions.get_contribution_for_year(10) == 100


def test_scheduled_contributions():
    """
    verify that ScheduledContributions returns contributions
    for those years provided in scheduled_contributions dict
    """
    contributions = ScheduledContributions({0: 500, 10: 200})
    assert contributions.get_contribution_for_year(0) == 500
    assert contributions.get_contribution_for_year(1) == 0
    assert contributions.get_contribution_for_year(10) == 200


def test_default_contribution():
    """
    verify DEFAULT_CONTRIBUTION is an InitialContribution
    with a starting_value of 1
    """
    assert DEFAULT_CONTRIBUTION.get_contribution_for_year(0) == 1
    assert DEFAULT_CONTRIBUTION.get_contribution_for_year(1) == 0
