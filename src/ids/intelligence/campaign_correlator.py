"""Group related attack sessions into broader campaigns.

CampaignCorrelator uses ECU overlap, attack type similarity, and severity
heuristics to combine related sessions into campaign objects.
"""

import uuid
from typing import List
from collections import defaultdict

from .attack_campaign import AttackCampaign


class CampaignCorrelator:

    def __init__(self):

        self.campaigns: List[AttackCampaign] = []

    def correlate(self, sessions: List):

        for session in sessions:
            self._assign_session(session)

        return self.campaigns

    def _assign_session(self, session):

        for campaign in self.campaigns:

            if self._is_related(session, campaign):
                campaign.add_session(session)
                return

        # create new campaign
        new_campaign = AttackCampaign(
            campaign_id=str(uuid.uuid4())
        )
        new_campaign.add_session(session)
        self.campaigns.append(new_campaign)

    def _is_related(self, session, campaign):

        # RULE 1: shared ECU overlap
        if len(session.involved_ecus & campaign.involved_ecus) > 0:
            return True

        # RULE 2: shared attack types
        if len(session.attack_types & campaign.attack_types) > 0:
            return True

        # RULE 3: severity continuity (heuristic)
        if session.severity_score > 5:
            return True

        return False
