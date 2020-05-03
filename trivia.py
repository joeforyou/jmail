import urllib.request, json, ssl

def get_random_question():
    # Calls jService random trivia question.
    request = 'https://jservice.io/api/random'
    try: 
        data = urllib.request.urlopen(request, context=ssl.SSLContext()).read().decode('utf-8')
        return json.loads(data)
    except urllib.error.URLError as e:
        print(e.reason)
