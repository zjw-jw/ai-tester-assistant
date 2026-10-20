"""
企业微信 Mock 服务（兼容版，同时支持 query 和 body 传参）
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="企业微信 Mock API")

TOKEN = "mock_access_token_123456"
CORPID = "mock_corpid"
SECRET = "mock_secret"


class MockError(Exception):
    def __init__(self, errcode, errmsg, status_code=400):
        self.errcode = errcode
        self.errmsg = errmsg
        self.status_code = status_code


@app.exception_handler(MockError)
async def mock_error_handler(request: Request, exc: MockError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"errcode": exc.errcode, "errmsg": exc.errmsg},
    )


async def _extract_params(request: Request):
    params = dict(request.query_params)
    try:
        body = await request.json()
        if isinstance(body, dict):
            params.update(body)
    except Exception:
        pass
    return params


def _ok(data=None):
    result = {"errcode": 0, "errmsg": "ok"}
    if data:
        result.update(data)
    return result


def _err(errcode, errmsg):
    raise MockError(errcode, errmsg)


def _check_token(p):
    if p.get("access_token") != TOKEN:
        _err(40014, "invalid access_token")


def _to_int(v):
    """把参数转成 int；转不了返回 None。"""
    if v is None:
        return None
    try:
        return int(v)
    except (ValueError, TypeError):
        return None


def _is_bad_str(v):
    """判断字符串是否'非法'：含 invalid 或长度超限。"""
    if not isinstance(v, str):
        return True
    if "invalid" in v.lower():
        return True
    return False


def _too_long(v, limit):
    return isinstance(v, str) and len(v) > limit


# ---------- 认证 ----------
@app.get("/cgi-bin/gettoken")
@app.post("/cgi-bin/gettoken")
async def get_token(request: Request):
    p = await _extract_params(request)
    if p.get("corpid") != CORPID:
        _err(40013, "invalid corpid")
    if p.get("corpsecret") != SECRET:
        _err(40001, "invalid corpsecret")
    return _ok({"access_token": TOKEN, "expires_in": 7200})


# ---------- 通讯录：成员 ----------
@app.post("/cgi-bin/user/create")
@app.get("/cgi-bin/user/create")
async def user_create(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    userid = p.get("userid")
    name = p.get("name")
    if not userid or _is_bad_str(userid) or _too_long(userid, 64):
        _err(40058, "invalid userid")
    if not name or _too_long(name, 64):
        _err(40058, "invalid name")
    if userid == "user_TC001":
        _err(60102, "user already exists")
    return _ok()


@app.get("/cgi-bin/user/get")
@app.post("/cgi-bin/user/get")
async def user_get(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    userid = p.get("userid")
    if not userid or _is_bad_str(userid):
        _err(40058, "invalid userid")
    if userid == "nonexistent_user":
        _err(40068, "user not exist")
    return _ok({"userid": userid, "name": "MockUser", "department": [1]})


@app.post("/cgi-bin/user/update")
@app.get("/cgi-bin/user/update")
async def user_update(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    userid = p.get("userid")
    if not userid or _is_bad_str(userid):
        _err(40058, "invalid userid")
    if userid == "nonexistent_user":
        _err(40068, "user not exist")
    return _ok()


@app.get("/cgi-bin/user/delete")
@app.post("/cgi-bin/user/delete")
async def user_delete(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    userid = p.get("userid")
    if not userid or _is_bad_str(userid):
        _err(40058, "invalid userid")
    if userid == "nonexistent_user":
        _err(40068, "user not exist")
    return _ok()


@app.post("/cgi-bin/user/batchdelete")
@app.get("/cgi-bin/user/batchdelete")
async def user_batchdelete(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    useridlist = p.get("useridlist")
    if not useridlist or not isinstance(useridlist, list):
        _err(40058, "invalid useridlist")
    if any(isinstance(u, str) and "invalid" in u.lower() for u in useridlist):
        _err(40058, "invalid userid in list")
    if any(u == "nonexistent_user" for u in useridlist):
        _err(40068, "user not exist")
    return _ok()


@app.get("/cgi-bin/user/simplelist")
@app.post("/cgi-bin/user/simplelist")
async def user_simplelist(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    if _to_int(p.get("department_id")) is None:
        _err(40068, "invalid department_id")
    return _ok({"userlist": [{"userid": "user1", "name": "User1"}]})


@app.get("/cgi-bin/user/list")
@app.post("/cgi-bin/user/list")
async def user_list(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    if _to_int(p.get("department_id")) is None:
        _err(40068, "invalid department_id")
    return _ok({"userlist": [{"userid": "user1", "name": "User1", "department": [1]}]})


@app.post("/cgi-bin/user/getuserid")
@app.get("/cgi-bin/user/getuserid")
async def user_getuserid(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    mobile = p.get("mobile")
    if not mobile or _is_bad_str(mobile) or not str(mobile).isdigit():
        _err(40068, "invalid mobile")
    return _ok({"userid": "mock_userid"})


@app.post("/cgi-bin/user/get_userid_by_email")
@app.get("/cgi-bin/user/get_userid_by_email")
async def user_getuserid_by_email(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    email = p.get("email")
    if not email or _is_bad_str(email) or "@" not in email:
        _err(40068, "invalid email")
    return _ok({"userid": "mock_userid"})


# ---------- 通讯录：部门 ----------
@app.post("/cgi-bin/department/create")
@app.get("/cgi-bin/department/create")
async def dept_create(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    name = p.get("name")
    if not name:
        _err(40058, "invalid name")
    if _to_int(p.get("parentid")) is None:
        _err(40068, "invalid parentid")
    if name == "部门_TC001":
        _err(60117, "department already exists")
    return _ok({"id": 100})


@app.post("/cgi-bin/department/update")
@app.get("/cgi-bin/department/update")
async def dept_update(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    name = p.get("name")
    if _to_int(p.get("id")) is None:
        _err(40068, "invalid id")
    if _to_int(p.get("parentid")) is None:
        _err(40068, "invalid parentid")
    if name == "部门_TC001":
        _err(60117, "department already exists")
    return _ok()


@app.get("/cgi-bin/department/delete")
@app.post("/cgi-bin/department/delete")
async def dept_delete(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    if _to_int(p.get("id")) is None:
        _err(40068, "invalid id")
    return _ok()


@app.get("/cgi-bin/department/list")
@app.post("/cgi-bin/department/list")
async def dept_list(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    raw_id = p.get("id")
    if raw_id is not None and _to_int(raw_id) is None:
        _err(40068, "invalid id")
    return _ok({"department": [
        {"id": 1, "name": "总部", "parentid": 0},
        {"id": 2, "name": "技术部", "parentid": 1},
    ]})


@app.get("/cgi-bin/department/simplelist")
@app.post("/cgi-bin/department/simplelist")
async def dept_simplelist(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    if _to_int(p.get("id")) is None:
        _err(40068, "invalid id")
    return _ok({"department_id": [{"id": 1, "parentid": 0}]})


@app.get("/cgi-bin/department/get")
@app.post("/cgi-bin/department/get")
async def dept_get(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    if _to_int(p.get("id")) is None:
        _err(40068, "invalid id")
    return _ok({"department": {"id": 1, "name": "MockDept", "parentid": 0}})


# ---------- 标签 ----------
@app.post("/cgi-bin/tag/create")
@app.get("/cgi-bin/tag/create")
async def tag_create(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    tagname = p.get("tagname")
    if not tagname:
        _err(40058, "invalid tagname")
    if tagname == "标签_TC001":
        _err(60123, "tag already exists")
    return _ok({"tagid": 100})


@app.post("/cgi-bin/tag/update")
@app.get("/cgi-bin/tag/update")
async def tag_update(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    tagname = p.get("tagname")
    if _to_int(p.get("tagid")) is None:
        _err(40068, "invalid tagid")
    if tagname == "标签_TC001":
        _err(60123, "tag already exists")
    return _ok()


@app.get("/cgi-bin/tag/delete")
@app.post("/cgi-bin/tag/delete")
async def tag_delete(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    if _to_int(p.get("tagid")) is None:
        _err(40068, "invalid tagid")
    return _ok()


# ---------- 消息 ----------
@app.post("/cgi-bin/message/send")
@app.get("/cgi-bin/message/send")
async def message_send(request: Request):
    p = await _extract_params(request)
    _check_token(p)
    return _ok({"msgid": "mock_msg_001"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8300)