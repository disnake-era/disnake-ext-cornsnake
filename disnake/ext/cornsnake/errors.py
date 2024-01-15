class ValidationError(Exception):
    """Application command callback signature validation failed."""

class CheckError(Exception):
    """A command check returned ``False``.

    You may want to create your own exceptions subclassing from
    this to have more control over handling different invariants.
    """
