import hashlib

def get_user_hash(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = None
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get("HTTP_USER_AGENT")
    cookies = request.COOKIES
    return hashlib.sha256((str(ip) + str(user_agent) + str(cookies)).encode("utf-8")).hexdigest()

def mean(items):
    return sum(items) / len(items)