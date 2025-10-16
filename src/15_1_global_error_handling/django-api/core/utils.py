def get_error_message(e):
    if hasattr(e, 'detail'):
        if isinstance(e.detail, list):
            return str(e.detail[0])
        elif isinstance(e.detail, dict):
            return next(iter(e.detail.values()))[0] if e.detail.values() else str(e.detail)
        else:
            return str(e.detail)
    return str(e)