import oauth2
import json
import webbrowser

def auth_error(response, content):
    status_json_data = json.loads(content)
    status_error_data = status_json_data['errors'][0]
    print('\nError! 無効なステータスです。'
        +'\nstatus: {}, ErrorCode: {}'.format(response.status, status_error_data['code'])
        +'\nErrorMessage: {}'.format(status_error_data['message']))
    exit()

def parse_response_content(content):
    content = content.decode('utf-8')
    content_list = content.split('&')

    content_dict = dict()

    for c in content_list:
        c_list = c.split('=')
        content_dict.update({ c_list[0]: c_list[1] })

    return content_dict

def get_access_token(pin, consumer, oauth_token, oauth_secret):
    oauth2_token = oauth2.Token(oauth_token, oauth_secret)
    oauth2_client = oauth2.Client(consumer, oauth2_token)
    response, content = oauth2_client.request("https://api.twitter.com/oauth/access_token", "POST", body="oauth_verifier={0}".format(pin))

    if response.status != 200:
        auth_error(response, content)

    access_token = parse_response_content(content)

    print('\n認証成功！\nAccessToken: {}\nAccessTokenSecret: {}'.format(access_token['oauth_token'], access_token['oauth_token_secret']))

def get_oauth_link(consumer_key, consumer_secret):
    oauth2_consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
    oauth2_client = oauth2.Client(oauth2_consumer)
    response, content = oauth2_client.request("https://api.twitter.com/oauth/request_token?oauth_callback=oob", "GET")
    
    if response.status != 200:
        auth_error(response, content)

    request_token = parse_response_content(content)

    webbrowser.open_new('https://api.twitter.com/oauth/authorize?oauth_token={}'.format(request_token['oauth_token']))

    print('\n認証ページを開きました。認証し、PINコードを入力してください。')

    input_pin = input('PIN >>> ')

    get_access_token(input_pin, oauth2_consumer, request_token['oauth_token'], request_token['oauth_token_secret'])


def input_token():
    print('\n初めにConsumerKey, Secretを入力してください')
    
    consumer_key = input('ConsumerKey >>> ')
    consumer_secret = input('ConsumerSecret >>> ')

    print('\nConsumerKey: {}\nConsumerSecret: {}\n以上の情報でOAuth認証を行います。'.format(consumer_key, 
                                                                            consumer_secret))

    get_oauth_link(consumer_key, consumer_secret)

if __name__ == "__main__":
    print('ようこそTwitterTokenOAutherへ')
    input_token()