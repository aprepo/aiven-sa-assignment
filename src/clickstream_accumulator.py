
class ClickStreamAccumulator(object):
    def __init__(self):
        self.session_stats = {}

    def add_event(self, click):
        session_id = click['session_id']
        if session_id not in self.session_stats:
            self.session_stats[session_id] = {
                'page_views': 0,
                'button_clicks': 0,
            }
        session = self.session_stats[session_id]
        print(session)
        if click['event_type'] == 'page_view':
            session['page_views'] = session['page_views'] + 1
        elif click['event_type'] == 'button_click':
            session['button_clicks'] = session['button_clicks'] + 1

    def get_session_stats(self, session_id):
        return self.session_stats[session_id]
