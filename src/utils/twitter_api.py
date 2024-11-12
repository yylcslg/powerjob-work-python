import random
import string

from fake_useragent import UserAgent
from curl_cffi.requests import Session
from loguru import logger
import time
import urllib.parse
import uuid

from src.utils.tools_utils import read_proxy_ip

ua = UserAgent()

bearer_token = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

twitter_auth_url = 'https://twitter.com/i/api/2/oauth2/authorize'

##
#  会封号。。。。。。
#
class TwitterApi:

    def __init__(self, auth_token, client_id):
        print(auth_token)
        self.auth_token = auth_token
        self.client_id = client_id,
        self.Twitter = self.build_session()
        self.X = self.build_session()
        self.auth_code = None
        self.auth_success = False  # 增加标志位记录授权是否成功
        self.build_plume_x_params()
        self.init_csrf_token()

    def build_session(self):
        proxy = read_proxy_ip()[0]
        proxies = {"http": proxy, "https": proxy}

        defaulf_cookies = {
            "auth_token": self.auth_token,
        }

        defaulf_headers = {
            "authority": "x.com",
            "origin": "https://x.com",
            "x-twitter-active-user": "yes",
            "x-twitter-client-language": "en",
            "authorization": bearer_token,
            "user-agent": ua.edge,
            "x-client-uuid": str(uuid.uuid4())

        }
        session = Session(headers=defaulf_headers, proxies=proxies, cookies=defaulf_cookies, timeout=120, impersonate='edge99')

        return session

    def init_csrf_token(self):
        self.Twitter.get(twitter_auth_url)
        self.Twitter.headers.update({"x-csrf-token": self.Twitter.cookies["ct0"]})
        self.X.get('https://x.com/i/api/graphql/Yka-W8dz7RaEuQNkroPkYw/UserByScreenName')
        self.X.headers.update({"x-csrf-token": self.X.cookies["ct0"]})

    def build_plume_x_params(self):
        rand_string = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=32))
        self.code_challenge = rand_string
        self.redirect_uri = 'https://www.baidu.com/get/userById'
        self.scope = 'tweet.read%20offline.access%20tweet.write%20tweet.moderate.write%20users.read%20follows.read%20follows.write'



    def set_scope(self, scope_data):
        self.scope = scope_data


    def get_auth_code(self):
        # 如果已经授权成功，直接返回 True，不再进行授权
        if self.auth_success:
            logger.info(f'{self.auth_token} 已成功授权，跳过重新授权')
            return True
        try:
            params = {
                'code_challenge': urllib.parse.unquote(self.code_challenge),
                'code_challenge_method': urllib.parse.unquote('plain'),
                'client_id': self.client_id,
                'redirect_uri': urllib.parse.unquote(self.redirect_uri),
                'response_type': urllib.parse.unquote('code'),
                'scope': urllib.parse.unquote(self.scope),
                'state': 'profile'
            }

            response = self.Twitter.get(twitter_auth_url, params=params)

            if "code" in response.json() and response.json()["code"] == 353:
                self.Twitter.headers.update({"x-csrf-token": response.cookies["ct0"]})
                logger.warning(f'{response.json()}')
                return self.get_auth_code()
            elif response.status_code == 429:
                time.sleep(5)
                return self.get_auth_code()
            elif 'auth_code' in response.json():
                self.auth_code = response.json()['auth_code']
                return True
            logger.error(f'{self.auth_token} 获取auth_code失败')
            return False
        except Exception as e:
            logger.error(e)
            return False

    def twitter_authorize(self):
        # 如果已经授权成功，直接返回 True，不再进行授权
        if self.auth_success:
            logger.info(f'{self.auth_token} 已成功授权，跳过重新授权')
            return True

        try:
            if not self.get_auth_code():
                return False
            data = {
                'approval': 'true',
                'code': self.auth_code,
            }
            response = self.Twitter.post(twitter_auth_url, data=data)
            if 'redirect_uri' in response.text:
                self.auth_success = True  # 授权成功，设置标志位
                return True
            elif response.status_code == 429:
                time.sleep(5)
                return self.twitter_authorize()
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
            print('resp:', response.status_code,resp)
        except:
            raise ValueError(response.text)
        assert resp.get('errors') is None or 'already' in str(resp.get('errors')), str(resp.get('errors'))
        return resp

    def get_rest_id(self, screen_name, query_id='Yka-W8dz7RaEuQNkroPkYw'):
        params = {
            'variables': '{"screen_name":"%s","withSafetyModeUserFields":true}' % (screen_name),
            'features': '{"hidden_profile_subscriptions_enabled":true,"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_is_identity_verified_enabled":true,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"responsive_web_twitter_article_notes_tab_enabled":true,"subscriptions_feature_can_gift_premium":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
            'fieldToggles': '{"withAuxiliaryUserLabels":false}',
        }
        response = self.X_http(f'https://x.com/i/api/graphql/{query_id}/UserByScreenName', type='GET',data=params)

        return response.get('data', {}).get('user', {}).get('result', {}).get('rest_id')

    # # 有问题  关注
    def create(self, screen_name):
        user_id = self.get_rest_id(screen_name)
        print('user_id:', user_id)
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

    ## 有问题 取消关注
    def destroy(self, screen_name):
        user_id = self.get_rest_id(screen_name)
        print(user_id)
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
    def like(self, tweet_id, query_id= 'lI07N6Otwv1PhnEgXILM7A'):
        json_data = {
            'variables': {
                'tweet_id': tweet_id,
            },
            'queryId': query_id,
        }
        response = self.X_http(f'https://x.com/i/api/graphql/{query_id}/FavoriteTweet', data=json_data)
        return response

    # 取消点赞
    def cancel_like(self, tweet_id, query_id='ZYKSe-w7KEslx3JhSIk5LA'):
        json_data = {
            'variables': {
                'tweet_id': tweet_id,
            },
            'queryId': query_id,
        }
        response = self.X_http(f'https://x.com/i/api/graphql/{query_id}/UnfavoriteTweet', data=json_data)
        return response


    # 有问题
    def retweet(self, tweet_id, query_id='iQtK4dl5hBmXewYZuEOKVw'):
        json_data = {
            'variables': {
                'tweet_id': tweet_id,
                'dark_request': False,
            },
            'queryId': query_id,
        }
        response = self.X_http(f'https://x.com/i/api/graphql/{query_id}/CreateRetweet', data=json_data)
        return response


    def quote_retweet(self, url, msg='', query_id='iQtK4dl5hBmXewYZuEOKVw'):
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
            'queryId': query_id,
        }
        response = self.X_http(f'https://x.com/i/api/graphql/{query_id}/CreateTweet', data=json_data)
        return response


    def reply_retweet(self, tweet_id, msg='', query_id='znq7jUAqRjmPj7IszLem5Q'):
        json_data = {
          "variables": {
            "tweet_text": msg,
            "reply": {
              "in_reply_to_tweet_id": tweet_id,
              "exclude_reply_user_ids": []
            },
            "dark_request": False,
            "media": {
              "media_entities": [],
              "possibly_sensitive": False
            },
            "semantic_annotation_ids": [],
            "disallowed_reply_options": None
          },
          "features": {
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "creator_subscriptions_quote_tweet_preview_enabled": False,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "articles_preview_enabled": True,
            "rweb_video_timestamps_enabled": True,
            "rweb_tipjar_consumption_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_enhance_cards_enabled": False
          },
          "queryId": query_id
        }
        response = self.X_http(f'https://x.com/i/api/graphql/{query_id}/CreateTweet', data=json_data)
        return response

    def cancel_retweet(self, tweet_id, query_id='iQtK4dl5hBmXewYZuEOKVw'):
        json_data = {
            'variables': {
                'source_tweet_id': tweet_id,
            },
            'queryId': query_id,
        }
        response = self.X_http(f'https://x.com/i/api/graphql/{query_id}/DeleteRetweet', data=json_data)
        return response





if __name__ == '__main__':
    cls = TwitterApi('d932440070f68e47d19b540f160884852225ddad', 'd1RSZW84R3A2TG1keUtMUDM3LXM6MTpjaQ')

    #if cls.twitter_authorize():
        #cls.create('loadingman5862')
        #cls.destroy('loadingman5862')


        #cls.like('1855524233650254217')  # 点赞
        #cls.cancel_like('1855524233650254217')
        #cls.cancel_retweet('1855524233650254217')


        #cls.quote_retweet('https://x.com/loadingman5862/status/1855524233650254217', 'good job')
        #cls.reply_retweet('1855524233650254217', 'good done ')
        #pass
    print('finish............')


