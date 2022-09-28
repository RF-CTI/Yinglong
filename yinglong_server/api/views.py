import json
import time
from flask import jsonify, request
from ..models import (db, User, DataRecordInfo, IntelligenceTypeInfo,
                      DataSourceInfo)
from .service import BasicAPI
from utils import getTodayTimestamp
from ..common import INTELLIGENCE_SERVER_MAP, LANGERAGE_MAP


class DaliyReportAPI(BasicAPI):

    def post(self):
        today = getTodayTimestamp() - 12 * 3600
        todayList = []
        totalList = []
        lastItem = []
        for key in INTELLIGENCE_SERVER_MAP.keys():
            todayList.append(
                INTELLIGENCE_SERVER_MAP.get(key).query.filter(
                    INTELLIGENCE_SERVER_MAP.get(key).timestamp > today).count(
                    ))
            totalList.append(INTELLIGENCE_SERVER_MAP.get(key).query.count())
            lasttime = INTELLIGENCE_SERVER_MAP.get(key).query.order_by(
                INTELLIGENCE_SERVER_MAP.get(key).timestamp.desc()).limit(
                    1).first().timestamp
            lastItem.append(lasttime)
        last_update = max(lastItem)
        total = sum(totalList)
        today = sum(todayList)
        return jsonify({
            "today":
            today,
            "total":
            total,
            "last_update":
            time.strftime("%Y-%m-%d %H:%M:%S",
                          time.localtime(float(last_update))),
            "collected_source":
            ', '.join([
                LANGERAGE_MAP.get(key)
                for key in INTELLIGENCE_SERVER_MAP.keys()
            ]),
            "updated_source":
            list(LANGERAGE_MAP.values())[lastItem.index(last_update)]
        })


class GetDataAPI(BasicAPI):

    def get(self):
        sourceType = request.args.get('source_type')
        if sourceType is None:
            self.setCodeAndMessage(300, 'Missing required parameter!')
        else:
            today = getTodayTimestamp() - 12 * 3600
            datasource = DataSourceInfo.query.filter_by(
                name=sourceType).first()
            intel_type = IntelligenceTypeInfo.query.filter_by(
                id=datasource.intelligence_type).first()
            st = INTELLIGENCE_SERVER_MAP.get(intel_type.name)
            new_query_res = st.query.filter(
                st.source == datasource.id).order_by(
                    st.id.desc()).limit(100).all()
            new_result = [res.to_json_simple() for res in new_query_res]
            history_query_res = st.query.filter(
                st.source == datasource.id,
                st.timestamp < today).order_by(st.id.desc()).limit(100).all()
            history_result = [
                res.to_json_simple() for res in history_query_res
            ]
            return jsonify({
                "new": new_result,
                "history": history_result,
                "code": self.CODE,
                "msg": self.MESSAGE
            })
        return jsonify({"code": self.CODE, "msg": self.MESSAGE})


class DataRecordAPI(BasicAPI):

    def get(self):
        result = {}
        for item in IntelligenceTypeInfo.query.all():
            datas = DataRecordInfo.query.filter(
                DataRecordInfo.intelligence_type == item.id).all()
            result[item.name] = {
                'data': [data.to_json() for data in datas],
                'name_zh': LANGERAGE_MAP.get(item.name)
            }
        return jsonify({'result': result})


class SubscribeAPI(BasicAPI):

    def post(self):
        data = json.loads(request.data)
        username = data.get('username')
        sc_id = data.get('id')
        if username and sc_id:
            user = db.session.query(User).filter(
                User.username == username).first()
            if user.subscribe_content is None or user.subscribe_content == '':
                ct = []
            else:
                ct = json.loads(user.subscribe_content)['content']
            if sc_id in ct:
                ct.remove(sc_id)
            else:
                ct.append(sc_id)
            user.subscribe_content = json.dumps({"content": ct})
            db.session.commit()
            return jsonify({'code': 200, 'msg': 'ok'})
        else:
            return jsonify({'code': 400, 'msg': 'faild'})
