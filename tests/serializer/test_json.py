import json
from rick.serializer.json.json import CamelCaseJsonEncoder

class SomeRecord:

    def asdict(self) -> dict:
        return {
            "first_name": "first_name",
            "last_name": "last_name",
        }

def test_camelcase_json_encoder():

    record = SomeRecord()
    serialized = json.dumps(record, cls=CamelCaseJsonEncoder)
    result = json.loads(serialized)
    assert len(result) == 2
    assert result["firstName"] == "first_name"
    assert result["lastName"] == "last_name"