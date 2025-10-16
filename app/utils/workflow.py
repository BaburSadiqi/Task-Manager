from app.schemas.task import PlaceStatus



ALLOWED_TRANSITONS = {
    PlaceStatus.pending.value: [PlaceStatus.in_progress.value, PlaceStatus.cancelled.value],
    PlaceStatus.in_progress: [PlaceStatus.review.value, PlaceStatus.testing.value, PlaceStatus.cancelled.value],
    PlaceStatus.review: [PlaceStatus.testing.value, PlaceStatus.completed.value],
    PlaceStatus.testing: [PlaceStatus.completed.value, PlaceStatus.in_progress.value],
    PlaceStatus.completed.value: [],
    PlaceStatus.cancelled.value: []
}


def is_valid_transition(current_status, new_status) -> bool:
    """Check if a transition fron current_status to new_status is allowed"""

    if current_status is None or new_status is None:
        return False
    
    if hasattr(current_status, "value"):
        current = current_status.value
    else:
        current = str(current_status).upper
    
    if hasattr(new_status, "value"):
        new_ = new_status.value
    else:
        new_ = str(new_status).upper
    
    allowed = ALLOWED_TRANSITONS.get(current, [])
    return new_ in allowed