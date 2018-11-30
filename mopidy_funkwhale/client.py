import logging

logger = logging.getLogger(__name__)


class FunkwhaleClient:
    def __init__(self, host, session):
        self.host = host
        self.session = session
        self.token = None
        self.login()

    def login(self):
        r = self.session.post('%s/api/v1/token' % self.host)
        if r.ok:
            self.token = r.json()
            self.session.headers.update({'Authentication': 'JWT %s' % self.token})
            self.session.auth = None
            logger.warning('Authenticated successfully; token is %s' % self.token)
        else:
            logger.warning('Authentication failed: %s' % r.status_code)
