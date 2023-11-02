import base64


def authenticate(request, source):
    if source.username and source.password:
        # Basic auth
        auth_header = request.META.get(source.token_header) or request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return False
        encoded_credentials = auth_header.split(' ')[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
        return source.username == username and source.authenticate(password)
    elif source.token:
        # Token auth
        return source.authenticate(request.META.get(source.token_header))
    return True
