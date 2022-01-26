import logging
class DbActions:

    def process(self, action, args):
        self.logger = logging.getLogger('DbActions')
        if action == 'init':
            self.logger.info('wot!')
