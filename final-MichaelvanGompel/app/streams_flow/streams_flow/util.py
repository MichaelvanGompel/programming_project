def get_lastfm(payload):
    headers = {'user_agent': USER_AGENT}
    root = API_ROOT

    payload['api_key'] = API_KEY
    payload['format'] = 'json'
    response = requests.get(API_ROOT, headers=headers, params=payload)
    return response