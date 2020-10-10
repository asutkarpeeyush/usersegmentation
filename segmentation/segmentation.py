import operator
from typing import Dict, List
from segmentation.operators import Operator, KeyOperator

from sqlalchemy.orm.state import InstanceState
from sqlalchemy_utils import InstrumentedList

from db_utils.models import User, Segment, UserPreference
from db_utils.session_factory import SessionFactory


class Segmentation:
    def __init__(self):
        self.operators = []
        self.session_fact = SessionFactory()
        self.segments = self._get_all_segments()

        # register operators
        ops = ["or", "and"]
        values = [operator.or_, operator.and_]
        for op, value in zip(ops, values):
            self.operators.append(KeyOperator(op, value))

        ops = ["neq", "eq", "gt", "gte", "lt", "lte"]
        values = [operator.ne, operator.eq, operator.gt, operator.ge, operator.lt, operator.le]
        for op, value in zip(ops, values):
            self.operators.append(Operator(op, value))

        self.key_op_map = {ope.name: ope.operation for ope in self.operators if isinstance(ope, KeyOperator)}
        self.normal_op_map = {ope.name: ope.operation for ope in self.operators if not isinstance(ope, KeyOperator)}

    def _get_all_segments(self):
        with self.session_fact.session_scope() as session:
            segments = {seg.name: seg.config for seg in session.query(Segment).all()}
        return segments

    def _resolve_seg_pref(self, pref_key: str, pref_val: Dict, details: Dict):
        op = pref_val.get('operator')
        if not op or op not in self.normal_op_map:
            raise Exception("Invalid operator in segment config")
        elif self.normal_op_map[op](details.get(pref_key), pref_val.get('value')):
            return True

        return False

    def _resolve_seg_ope(self, ope_: operator, val: List, details: Dict):
        assert isinstance(val, list)

        ans = True if self.key_op_map[ope_] == operator.and_ else False
        for sec in val:  # type: Dict
            # expecting the length of dict to be 1
            assert len(sec) == 1
            for k, v in sec.items():
                if k in self.key_op_map:
                    ans = self.key_op_map[ope_](ans, self._resolve_seg_ope(k, v, details))
                else:
                    ans = self.key_op_map[ope_](ans, self._resolve_seg_pref(k, v, details))

        return ans

    def _is_user_in_segment(self, seg: Segment, details: Dict):
        for seg_key, seg_val in seg.items():
            # If the section is an operation like or/and
            if seg_key in self.key_op_map:
                if not self._resolve_seg_ope(seg_key, seg_val, details):
                    return False
            # If the section is not an operation and an attribute to check for
            else:
                if not self._resolve_seg_pref(seg_key, seg_val, details):
                    return False

        return True

    def flatten_details(self, obj_dict: Dict, base_name: str, details: Dict):
        for attr, value in obj_dict.items():
            if isinstance(value, InstanceState):
                continue
            elif isinstance(value, InstrumentedList) or isinstance(value, list):
                name = base_name
                name += "_" if name else ""
                name += attr + "_" + "count"
                details[name] = len(value)
            elif isinstance(value, UserPreference):
                name = base_name
                name += "." if name else ""
                name += attr + "."
                self.flatten_details(value.__dict__, name, details)
            else:
                name = base_name + attr
                details[name] = value

    def get_user_segments(self, user: User):
        if not user or not isinstance(user, User):
            raise Exception("Please provide a valid user object")

        # flatten the user details like preferences, counts, etc
        user_details = {}
        self.flatten_details(user.__dict__, "", user_details)

        # get the user segments
        user_segments = []
        for segment, value in self.segments.items():
            if self._is_user_in_segment(value, user_details):
                user_segments.append(segment)
        return user_segments
