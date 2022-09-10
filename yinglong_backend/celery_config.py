from __future__ import absolute_import

broker_url = 'redis://127.0.0.1:6379/0'

result_backend = 'redis://127.0.0.1:6379/1'

task_serializer = 'json'

result_serializer = 'json'

accept_content = ['json']

timezone = 'Asia/Shanghai'

worker_hijack_root_logger = False

result_expires = 60 * 60 * 24
