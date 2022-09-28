from ..models import PhishingInfo, BotnetInfo, C2Info

INTELLIGENCE_SERVER_MAP = {
    "phishing": PhishingInfo,
    "botnet": BotnetInfo,
    'c2': C2Info
}

LANGERAGE_MAP = {'phishing': '钓鱼网站', 'botnet': '僵尸网络', 'c2': '远控C&C'}
