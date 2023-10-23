import datetime
from .models import Player
from django.core.cache import cache
from django.conf import settings


class ActiveUserMiddleware():
    def __init__(self, get_response):
        """Initializes the perennial list of online users with no one online"""
        empty_dict = {}
        cache.set("last_seen_online",empty_dict,None)
        self.get_response = get_response

    def __call__(self, request):
        # If session already has a nickname, defaults to false
        nickname = request.session.get("Nickname", False)
        if nickname:
            now = datetime.datetime.now()
            #get dict {user:last seen online} from cache
            seen_online = cache.get("last_seen_online")
            #goes over dict and removes all those whom we haven't seen in USER_ONLINE_TIMEOUT (5 minutes)
            candidates_for_removal = []
            for player in seen_online:
                if seen_online[player] < now - datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                    candidates_for_removal.append(player)
            #removes all the players in candidates for removal list from the seen_online
            for player in candidates_for_removal:
                seen_online.pop(player)
            #sets current player's last seen online as now
            seen_online[nickname]=now
            #sets the cache with the updated list of users last seen online
            cache.set("last_seen_online", seen_online, None)
            return self.get_response(request)
        else:
            return self.get_response(request)