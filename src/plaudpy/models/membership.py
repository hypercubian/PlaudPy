"""Membership and subscription models."""

from pydantic import BaseModel


class FreeTrialStatus(BaseModel):
    """Free trial status information."""

    model_config = {"extra": "allow"}

    eligible: bool | None = None
    active: bool | None = None
    days_remaining: int | None = None


class StripePrice(BaseModel):
    """Stripe pricing information."""

    model_config = {"extra": "allow"}

    id: str | None = None
    product: str | None = None
    currency: str | None = None
    unit_amount: int | None = None
    interval: str | None = None


class StripeSubscription(BaseModel):
    """Stripe subscription information."""

    model_config = {"extra": "allow"}

    id: str | None = None
    status: str | None = None
    current_period_start: str | None = None
    current_period_end: str | None = None
    plan: str | None = None
