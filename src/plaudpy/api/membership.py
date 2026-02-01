"""Membership and subscription API endpoints."""

from ..models.membership import FreeTrialStatus, StripePrice, StripeSubscription
from .base import BaseAPI


class MembershipAPI(BaseAPI):
    """API for membership, subscriptions, and billing."""

    def get_free_trial_status(self) -> FreeTrialStatus:
        """Get free trial eligibility and status."""
        data = self._get("/membership/free-trial/status")
        return FreeTrialStatus.model_validate(data)

    def get_stripe_prices(self) -> list[StripePrice]:
        """List available Stripe subscription prices."""
        data = self._get("/membership/stripe/prices")
        items = data if isinstance(data, list) else data.get("data", [])
        return [StripePrice.model_validate(item) for item in items]

    def get_stripe_subscription(self) -> StripeSubscription:
        """Get the current Stripe subscription."""
        data = self._get("/membership/stripe/subscription")
        return StripeSubscription.model_validate(data)

    def create_stripe_session(self, price_id: str, **kwargs) -> dict:
        """Create a Stripe checkout session.

        Args:
            price_id: Stripe price ID.
            **kwargs: Additional session parameters.
        """
        payload = {"price_id": price_id, **kwargs}
        return self._post("/membership/stripe/create-session", json=payload)

    def get_shopify_url(self) -> dict:
        """Get Shopify store URL."""
        return self._get("/membership/shopify/url")
