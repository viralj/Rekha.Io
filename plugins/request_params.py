from django.utils.http import urlencode

REQUEST_LOGIN = {'_req': 'login'}


def get_request_param(param, optional: dict = None):
    """
    This function will return get url string using param and optional dict.

    :param param:   String or dict of string to get parameters
    :param optional:    Option dict to add params in return query string
    :return:    url query string
    """
    z = dict()

    if param is None:
        raise Exception("Param object cannot be None!")

    if isinstance(param, list):
        for x in param:
            for k, v in x.items():
                z[k] = v
    else:
        for k, v in param.items():
            z[k] = v

    if optional is not None:
        for k, v in optional.items():
            z[k] = v

    return "?" + urlencode(z)
