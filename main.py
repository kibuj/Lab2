from datetime import datetime
from hashlib import sha256

USER_SCHEME = ("id", "first_name", "second_name", "email", "password")
RECORD_SCHEME = ("id", "date", "content", "user", "title")
ENTITIES = ('User', 'Record')
DATABASE = []


def _get_entity(s: str) -> str:
    if ENTITIES[0] in s:
        return ENTITIES[0]
    elif ENTITIES[1] in s:
        return ENTITIES[1]
    else:
        return ""


def parse_string(string: str) -> dict:
    """Parses input string into a dictionary."""
    entity = _get_entity(s=string)
    if entity == ENTITIES[0]:
        data = {}
        for item in USER_SCHEME:
            if item + "=" in string:
                idx = string.index(item + "=")
                start_idx = idx + len(item + "=")
                end_idx = string.find(",", start_idx)
                if end_idx == -1:
                    end_idx = len(string) - 1
                data[item] = string[start_idx:end_idx].strip()
        data["password"] = sha256(data["password"].encode()).hexdigest()
        return data
    elif entity == ENTITIES[1]:
        data = {}
        for item in RECORD_SCHEME:
            if item + "=" in string:
                idx = string.index(item + "=")
                start_idx = idx + len(item + "=")
                end_idx = string.find(",", start_idx)
                if end_idx == -1:
                    end_idx = len(string) - 1
                data[item] = string[start_idx:end_idx].strip()
        return data
    else:
        return {}


def create_record(record: str) -> dict:
    data = parse_string(record)
    if data:
        data["date"] = datetime.strptime(data["date"], "%d.%m.%Y")
        DATABASE.append(data)
        return data
    return {}


def create_user(user: str) -> dict:
    data = parse_string(user)
    if data:
        DATABASE.append(data)
        return data
    return {}


def update_record(record: str) -> dict:
    data = parse_string(record)
    if data:
        for i, r in enumerate(DATABASE):
            if r["id"] == data["id"]:
                DATABASE[i].update(data)
                return data
    return {}


def read_record(record_content: str) -> dict:
    for record in DATABASE:
        if record["content"] == record_content:
            return record
    return {}


def delete_record(record_id: int) -> dict:
    for i, record in enumerate(DATABASE):
        if record["id"] == record_id:
            return DATABASE.pop(i)
    return {}


user_1 = "User(id=1, first_name=test name, second_name=test surname, email=test@test.test, password=123)"
record_1 = "Record(id=1, date=26.02.2004, content=Some example, user=1, title=Example title)"

create_user(user_1)
create_record(record_1)
print(DATABASE)
