"""Unit tests for Membership API."""

from unittest.mock import MagicMock

import httpx
import pytest

from plaudpy.api.membership import MembershipAPI
from plaudpy.config import PlaudConfig
from plaudpy.models.membership import FreeTrialStatus, StripePrice, StripeSubscription


@pytest.fixture
def membership_api():
    config = PlaudConfig(username="test", password="test")
    client = MagicMock(spec=httpx.Client)
    api = MembershipAPI(config, client)
    api.set_access_token("test-token")
    return api


class TestMembershipAPI:

    def test_get_free_trial_status(self, membership_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"eligible": True, "active": False, "days_remaining": 7}
        membership_api.client.get.return_value = response

        result = membership_api.get_free_trial_status()

        assert isinstance(result, FreeTrialStatus)
        assert result.eligible is True
        assert result.days_remaining == 7

    def test_get_stripe_prices(self, membership_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {
            "data": [{"id": "price_1", "product": "pro", "currency": "usd", "unit_amount": 999, "interval": "month"}]
        }
        membership_api.client.get.return_value = response

        result = membership_api.get_stripe_prices()

        assert len(result) == 1
        assert isinstance(result[0], StripePrice)
        assert result[0].unit_amount == 999

    def test_get_stripe_subscription(self, membership_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"id": "sub_1", "status": "active", "plan": "pro"}
        membership_api.client.get.return_value = response

        result = membership_api.get_stripe_subscription()

        assert isinstance(result, StripeSubscription)
        assert result.status == "active"

    def test_create_stripe_session(self, membership_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"url": "https://checkout.stripe.com/session-id"}
        membership_api.client.post.return_value = response

        result = membership_api.create_stripe_session("price_1")

        call_url = membership_api.client.post.call_args[0][0]
        assert "/membership/stripe/create-session" in call_url

    def test_get_shopify_url(self, membership_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"url": "https://shop.plaud.ai"}
        membership_api.client.get.return_value = response

        result = membership_api.get_shopify_url()
        assert result["url"] == "https://shop.plaud.ai"
