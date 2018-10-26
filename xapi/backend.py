import logging
import uuid
from tincan import (
    RemoteLRS,
    Statement,
    Agent,
    Verb,
    Activity,
    Context,
    LanguageMap,
    ActivityDefinition,
    StateDocument,
)

logger = logging.getLogger(__name__)


class xAPIBackend(object):
    """Event tracker that sends event to an xAPI server"""

    def send(self, event):
        """Send xAPI formatted event to the xAPI proxy"""

        lrs = RemoteLRS(
            version="1.0.1",
            endpoint="http://xapi:8081/data/xAPI/",
            auth="YmRkYzY5YTQyMGM1NTM0ZTcxMDcyYzJmMTg4Y2EyNTE4MjQ1YzJhYzo0NzhjMjcxNjA4NzNmOGY3YjhkY2IxODZjZjg3NjBlMWI5NWI0M2Jm",
        )

        actor = Agent(name="UserMan", mbox="mailto:tincanpython@tincanapi.com")

        logger.debug("Received an event: {}".format(event))
        logger.debug("LRS about: {}".format(lrs.about()))

        if event.get("name") == u"seek_video":
            verb = Verb(
                id="http://adlnet.gov/expapi/verbs/experienced",
                display=LanguageMap({"en-US": "experienced"}),
            )
            object = Activity(
                id="http://tincanapi.com/TinCanPython/Example/0",
                definition=ActivityDefinition(
                    name=LanguageMap({"en-US": "TinCanPython Library"}),
                    description=LanguageMap(
                        {
                            "en-US": "Use of, or interaction with, the TinCanPython Library"
                        }
                    ),
                ),
            )
            context = Context(
                registration=uuid.uuid4(),
                instructor=Agent(
                    name="Lord TinCan", mbox="mailto:lordtincan@tincanapi.com"
                ),
                # language='en-US',
            )
            statement = Statement(
                actor=actor, verb=verb, object=object, context=context
            )
            response = lrs.save_statement(statement)

        # seek = {
        #     "timestamp": datetime.datetime(2018, 10, 26, 13, 53, 24, 967935),
        #     "data": {
        #         u"code": u"b7xgknqkQk8",
        #         u"new_time": 0.65,
        #         u"old_time": 0,
        #         u"duration": 195,
        #         u"type": u"onCaptionSeek",
        #         u"id": u"0b9e39477cf34507a7a48f74be381fdd",
        #     },
        #     "name": u"seek_video",
        #     "context": {
        #         "username": u"",
        #         "user_id": None,
        #         "accept_language": u"en-US,en;q=0.5",
        #         "ip": "172.30.0.1",
        #         "org_id": u"edX",
        #         "agent": u"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0",
        #         "event_source": "browser",
        #         "host": u"2958fe98c2b4",
        #         "session": "",
        #         "referer": u"http://localhost:8000/courses/course-v1:edX+DemoX+Demo_Course/courseware/d8a6192ade314473a78242dfeedfbf5b/edx_introduction/1?activate_block_id=block-v1%3AedX%2BDemoX%2BDemo_Course%2Btype%40vertical%2Bblock%40vertical_0270f6de40fc",
        #         "client_id": None,
        #         "course_id": u"course-v1:edX+DemoX+Demo_Course",
        #         "path": u"/event",
        #         "page": u"http://localhost:8000/courses/course-v1:edX+DemoX+Demo_Course/courseware/d8a6192ade314473a78242dfeedfbf5b/edx_introduction/1?activate_block_id=block-v1%3AedX%2BDemoX%2BDemo_Course%2Btype%40vertical%2Bblock%40vertical_0270f6de40fc",
        #     },
        # }

        # load = {
        #     "timestamp": datetime.datetime(2018, 10, 26, 13, 52, 24, 132921),
        #     "data": {
        #         u"duration": 195,
        #         u"code": u"b7xgknqkQk8",
        #         u"id": u"0b9e39477cf34507a7a48f74be381fdd",
        #     },
        #     "name": u"load_video",
        #     "context": {
        #         "username": u"11127afb82c047bcb39c4c29c261ba",
        #         "user_id": 6,
        #         "accept_language": u"en-US,en;q=0.5",
        #         "ip": "172.30.0.1",
        #         "org_id": u"edX",
        #         "agent": u"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0",
        #         "event_source": "browser",
        #         "host": u"2958fe98c2b4",
        #         "session": "aff96cf91b2d9fa8eee85dead64aee71",
        #         "referer": u"http://localhost:8000/courses/course-v1:edX+DemoX+Demo_Course/courseware/d8a6192ade314473a78242dfeedfbf5b/edx_introduction/1?activate_block_id=block-v1%3AedX%2BDemoX%2BDemo_Course%2Btype%40vertical%2Bblock%40vertical_0270f6de40fc",
        #         "client_id": None,
        #         "course_id": u"course-v1:edX+DemoX+Demo_Course",
        #         "path": u"/event",
        #         "page": u"http://localhost:8000/courses/course-v1:edX+DemoX+Demo_Course/courseware/d8a6192ade314473a78242dfeedfbf5b/edx_introduction/1?activate_block_id=block-v1%3AedX%2BDemoX%2BDemo_Course%2Btype%40vertical%2Bblock%40vertical_0270f6de40fc",
        #     },
        # }
