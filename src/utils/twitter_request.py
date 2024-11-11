import random
import string

import requests
from fake_useragent import UserAgent
from curl_cffi.requests import Session
from loguru import logger
import time
import urllib.parse
import uuid

ua = UserAgent()


class TwitterWrap:

    def __init__(self, auth_token):
        self.auth_token = auth_token
        defaulf_cookies = {
            "auth_token": auth_token,
        }

        bearer_token = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        defaulf_headers = {
            "authority": "x.com",
            "origin": "https://x.com",
            "x-twitter-active-user": "yes",
            "x-twitter-client-language": "en",
            "authorization": bearer_token,
            "user-agent": ua.edge,
            "x-client-uuid": str(uuid.uuid4())

        }
        proxy='127.0.0.1:8889'
        proxies = {"http": proxy, "https": proxy}
        self.Twitter = Session(headers=defaulf_headers, proxies=proxies ,cookies=defaulf_cookies, timeout=120, impersonate='edge99')
        self.X = Session(headers=defaulf_headers, proxies=proxies , cookies=defaulf_cookies, timeout=120, impersonate='edge99')
        self.auth_code = None
        self.auth_success = False  # 增加标志位记录授权是否成功
        self.init_csrf_token()


    def init_csrf_token(self):
        ct0 ='5a7257ab58044eade2066c985cc4c74dd1552d6947f6b438c91a839a2b745fabda4a2903429dc8e630bfe207d52dde555108c6834dec035596ecf139d2080582713312e2e35b741965216e0c058c5882'
        #rsp = self.Twitter.get('https://twitter.com/i/api/2/oauth2/authorize')
        #print('twitter:', rsp.status_code,rsp.text,self.Twitter.cookies)
        self.Twitter.headers.update({"x-csrf-token": ct0})
        #rsp = self.X.get('https://x.com/i/api/graphql/Yka-W8dz7RaEuQNkroPkYw/UserByScreenName')
        #print('x:', rsp.status_code, rsp.text)
        #self.X.headers.update({"x-csrf-token": self.X.cookies["ct0"]})
        self.X.headers.update({"x-csrf-token": ct0})



    def twitter_authorizeV1(self, authenticity_token, oauth_token):
        # 如果已经授权成功，直接返回 True，不再进行授权
        if self.auth_success:
            logger.info(f'{self.auth_token} 已成功授权，跳过重新授权')
            return True

        try:
            data = {
                'authenticity_token': authenticity_token,
                'redirect_after_login': f'https://api.x.com/oauth/authorize?oauth_token={oauth_token}',
                'oauth_token': oauth_token,
            }
            response = self.Twitter.post('https://x.com/oauth/authorize', data=data)
            if 'redirect_uri' in response.text:
                self.auth_success = True  # 授权成功，设置标志位
                return True
            elif response.status_code == 429:
                time.sleep(5)
                return self.twitter_authorizeV1(authenticity_token, oauth_token)
            logger.error(f'{self.auth_token} 推特授权失败')
            return False
        except Exception as e:
            logger.error(f'{self.auth_token} 推特授权异常：{e}')
            return False


    def get_auth_codeV2(self, client_id, state, code_challenge, redirect_uri, scope, code_challenge_method='plain',
                        response_type='code'):
        # 如果已经授权成功，直接返回 True，不再进行授权
        if self.auth_success:
            logger.info(f'{self.auth_token} 已成功授权，跳过重新授权')
            return True

        try:
            params = {
                'code_challenge': urllib.parse.unquote(code_challenge),
                'code_challenge_method': urllib.parse.unquote(code_challenge_method),
                'client_id': urllib.parse.unquote(client_id),
                'redirect_uri': urllib.parse.unquote(redirect_uri),
                'response_type': urllib.parse.unquote(response_type),
                'scope': urllib.parse.unquote(scope),
                'state': state
            }

            response = self.Twitter.get('https://twitter.com/i/api/2/oauth2/authorize', params=params)
            if "code" in response.json() and response.json()["code"] == 353:
                self.Twitter.headers.update({"x-csrf-token": response.cookies["ct0"]})
                logger.warning(f'{response.json()}')
                return self.get_auth_codeV2(client_id, state, code_challenge, redirect_uri, scope,
                                            code_challenge_method, response_type)
            elif response.status_code == 429:
                time.sleep(5)
                return self.get_auth_codeV2(client_id, state, code_challenge, redirect_uri, scope,
                                            code_challenge_method, response_type)
            elif 'auth_code' in response.json():
                self.auth_code = response.json()['auth_code']
                return True
            logger.error(f'{self.auth_token} 获取auth_code失败')
            return False
        except Exception as e:
            logger.error(e)
            return False

    def twitter_authorizeV2(self, client_id, state, code_challenge, redirect_uri, scope,
                            code_challenge_method='plain', response_type='code'):
        # 如果已经授权成功，直接返回 True，不再进行授权
        if self.auth_success:
            logger.info(f'{self.auth_token} 已成功授权，跳过重新授权')
            return True

        try:
            if not self.get_auth_codeV2(client_id, state, code_challenge, redirect_uri, scope,
                                        code_challenge_method, response_type):
                return False
            data = {
                'approval': 'true',
                'code': self.auth_code,
            }
            response = self.Twitter.post('https://twitter.com/i/api/2/oauth2/authorize', data=data)
            if 'redirect_uri' in response.text:
                self.auth_success = True  # 授权成功，设置标志位
                return True
            elif response.status_code == 429:
                time.sleep(5)
                return self.twitter_authorizeV2(client_id, state, code_challenge, redirect_uri, scope,
                                                code_challenge_method, response_type)
            logger.error(f'{self.auth_token} 推特授权失败')
            return False
        except Exception as e:
            logger.error(f'{self.auth_token} 推特授权异常：{e}')
            return False



    def X_http(self, url, type='POST', data=None):
        if type == "GET":
            response = self.X.get(url, params=data)
        elif type == "POST":
            response = self.X.post(url, json=data)
        else:
            raise ValueError(f'不支持{type}')
        self.X.headers.update({'x-csrf-token': self.X.cookies.get('ct0')})
        try:
            resp = response.json()
        except:
            raise ValueError(response.text)
        assert resp.get('errors') is None or 'already' in str(resp.get('errors')), str(resp.get('errors'))
        return resp

    def get_rest_id(self, screen_name):
        params = {
            'variables': '{"screen_name":"%s","withSafetyModeUserFields":true}' % (screen_name),
            'features': '{"hidden_profile_subscriptions_enabled":true,"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_is_identity_verified_enabled":true,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"responsive_web_twitter_article_notes_tab_enabled":true,"subscriptions_feature_can_gift_premium":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
            'fieldToggles': '{"withAuxiliaryUserLabels":false}',
        }
        response = self.X_http('https://x.com/i/api/graphql/Yka-W8dz7RaEuQNkroPkYw/UserByScreenName', type='GET',
                               data=params)
        return response.get('data', {}).get('user', {}).get('result', {}).get('rest_id')

    # 关注
    def create(self, screen_name):
        user_id = self.get_rest_id(screen_name)
        data = {
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'include_ext_is_blue_verified': '1',
            'include_ext_verified_type': '1',
            'include_ext_profile_image_shape': '1',
            'skip_status': '1',
            'user_id': user_id,
        }
        response = self.X_http('https://x.com/i/api/1.1/friendships/create.json', data=data)
        return response

    # 取消关注
    def destroy(self, screen_name):
        user_id = self.get_rest_id(screen_name)
        data = {
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'include_ext_is_blue_verified': '1',
            'include_ext_verified_type': '1',
            'include_ext_profile_image_shape': '1',
            'skip_status': '1',
            'user_id': user_id,
        }
        response = self.X_http('https://x.com/i/api/1.1/friendships/destroy.json', data=data)
        return response


    # 点赞
    def favorite_tweet(self, tweet_id):
        json_data = {
            'variables': {
                'tweet_id': tweet_id,
            },
            'queryId': 'lI07N6Otwv1PhnEgXILM7A',
        }
        response = self.X_http('https://x.com/i/api/graphql/lI07N6Otwv1PhnEgXILM7A/FavoriteTweet', data=json_data)
        return response

    # 取消点赞
    def unfavorite_tweet(self, tweet_id):
        json_data = {
            'variables': {
                'tweet_id': tweet_id,
            },
            'queryId': 'ZYKSe-w7KEslx3JhSIk5LA',
        }
        response = self.X_http('https://x.com/i/api/graphql/ZYKSe-w7KEslx3JhSIk5LA/UnfavoriteTweet', data=json_data)
        return response

    def retweet(self, tweet_id):
        json_data = {
            'variables': {
                'tweet_id': tweet_id,
                'dark_request': False,
            },
            'queryId': 'ojPdsZsimiJrUGLR1sjUtA',
        }
        response = self.X_http('https://x.com/i/api/graphql/ojPdsZsimiJrUGLR1sjUtA/CreateRetweet', data=json_data)
        return response

    def quote_retweet(self, url, msg=''):
        json_data = {
            'variables': {
                'tweet_text': msg,
                'attachment_url': url,
                'dark_request': False,
                'media': {
                    'media_entities': [],
                    'possibly_sensitive': False,
                },
                'semantic_annotation_ids': [],
                'disallowed_reply_options': None,
            },
            'features': {
                'communities_web_enable_tweet_community_results_fetch': True,
                'c9s_tweet_anatomy_moderator_badge_enabled': True,
                'responsive_web_edit_tweet_api_enabled': True,
                'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
                'view_counts_everywhere_api_enabled': True,
                'longform_notetweets_consumption_enabled': True,
                'responsive_web_twitter_article_tweet_consumption_enabled': True,
                'tweet_awards_web_tipping_enabled': False,
                'creator_subscriptions_quote_tweet_preview_enabled': False,
                'longform_notetweets_rich_text_read_enabled': True,
                'longform_notetweets_inline_media_enabled': True,
                'articles_preview_enabled': True,
                'rweb_video_timestamps_enabled': True,
                'rweb_tipjar_consumption_enabled': True,
                'responsive_web_graphql_exclude_directive_enabled': True,
                'verified_phone_label_enabled': False,
                'freedom_of_speech_not_reach_fetch_enabled': True,
                'standardized_nudges_misinfo': True,
                'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
                'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
                'responsive_web_graphql_timeline_navigation_enabled': True,
                'responsive_web_enhance_cards_enabled': False,
            },
            'queryId': 'xT36w0XM3A8jDynpkram2A',
        }
        response = self.X_http('https://x.com/i/api/graphql/xT36w0XM3A8jDynpkram2A/CreateTweet', data=json_data)
        return response

    def cancel_retweet(self, tweet_id):
        json_data = {
            'variables': {
                'source_tweet_id': tweet_id,
            },
            'queryId': 'iQtK4dl5hBmXewYZuEOKVw',
        }
        response = self.X_http('https://x.com/i/api/graphql/iQtK4dl5hBmXewYZuEOKVw/DeleteRetweet', json=json_data)
        return response


if __name__ == '__main__':
    rand_string = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=32))
    print(""+rand_string)
    cls = TwitterWrap('c923183ae37ecfb8018e21ce74f459cb739ea056')

    client_id = str(uuid.uuid4()),
    state = '',
    code_challenge = rand_string
    redirect_uri='http://127.0.0.1:7700'
    scope = ''
    cls.twitter_authorizeV2(client_id, state, code_challenge, redirect_uri, scope)
   # cls.create('loadingman000')
    #params = get_plume_x_params(plume_token)
    #if cls.twitter_authorizeV2(**params):
        # 执行操作
       # cls.create('username')  # 关注用户
      #  cls.like('tweet_id')  # 点赞
       # cls.retweet('tweet_id')

