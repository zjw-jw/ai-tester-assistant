# 企业微信 API 文档（Mock 版）

> 基础路径：http://127.0.0.1:8300
> 所有请求和响应均为 JSON 格式。
>
> **重要：以下规则适用于本文档里出现的所有接口。**
>
> **1. 本系统通过 corpid + corpsecret 换取 access_token，所有业务接口都必须带 access_token 参数。**
>
> **2. 获取 access_token 的接口不需要 access_token，但其他接口都需要。**
>
> **3. 测试用 corpid = mock_corpid，corpsecret = mock_secret，access_token = mock_access_token_123456。**

## 一、认证

### 1. 获取 access_token
- **方法：GET**
- **路径：/cgi-bin/gettoken**
- **Query 参数**：corpid（必填，值固定为 mock_corpid）、corpsecret（必填，值固定为 mock_secret）
- **成功**：HTTP 200，返回 `{ "errcode": 0, "errmsg": "ok", "access_token": "mock_access_token_123456", "expires_in": 7200 }`
- **失败**：40013 INVALID_CORPID / 40001 INVALID_SECRET

## 二、通讯录 - 成员

### 2. 创建成员
- **方法：POST**，**路径：/cgi-bin/user/create**
- **Query**：access_token（必填）
- **Body**：userid（必填，1-64字符）、name（必填，1-32字符）、department（必填，数组）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`
- **失败**：40014 INVALID_ACCESS_TOKEN / 40058 INVALID_USERID / 60102 USER_EXIST

### 3. 读取成员
- **方法：GET**，**路径：/cgi-bin/user/get**
- **Query**：access_token（必填）、userid（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "userid": "...", "name": "...", "department": [...] }`

### 4. 更新成员
- **方法：POST**，**路径：/cgi-bin/user/update**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 5. 删除成员
- **方法：GET**，**路径：/cgi-bin/user/delete**
- **Query**：access_token（必填）、userid（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 6. 批量删除成员
- **方法：POST**，**路径：/cgi-bin/user/batchdelete**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 7. 获取部门成员
- **方法：GET**，**路径：/cgi-bin/user/simplelist**
- **Query**：access_token（必填）、department_id（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "userlist": [...] }`

### 8. 获取部门成员详情
- **方法：GET**，**路径：/cgi-bin/user/list**
- **Query**：access_token（必填）、department_id（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "userlist": [...] }`

### 9. 手机号获取 userid
- **方法：POST**，**路径：/cgi-bin/user/getuserid**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "userid": "..." }`

### 10. 邮箱获取 userid
- **方法：POST**，**路径：/cgi-bin/user/get_userid_by_email**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "userid": "..." }`

## 三、通讯录 - 部门

### 11. 创建部门
- **方法：POST**，**路径：/cgi-bin/department/create**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "id": 100 }`

### 12. 更新部门
- **方法：POST**，**路径：/cgi-bin/department/update**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 13. 删除部门
- **方法：GET**，**路径：/cgi-bin/department/delete**
- **Query**：access_token（必填）、id（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 14. 获取部门列表
- **方法：GET**，**路径：/cgi-bin/department/list**
- **Query**：access_token（必填）、id（选填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "department": [...] }`

### 15. 获取子部门 ID 列表
- **方法：GET**，**路径：/cgi-bin/department/simplelist**
- **Query**：access_token（必填）、id（选填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "department_id": [...] }`

### 16. 获取单个部门详情
- **方法：GET**，**路径：/cgi-bin/department/get**
- **Query**：access_token（必填）、id（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "department": {...} }`

## 四、通讯录 - 标签

### 17. 创建标签
- **方法：POST**，**路径：/cgi-bin/tag/create**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "tagid": 100 }`

### 18. 更新标签名字
- **方法：POST**，**路径：/cgi-bin/tag/update**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 19. 删除标签
- **方法：GET**，**路径：/cgi-bin/tag/delete**
- **Query**：access_token（必填）、tagid（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

## 五、消息推送

### 20. 发送应用消息
- **方法：POST**，**路径：/cgi-bin/message/send**
- **Query**：access_token（必填）
- **Body**：touser、msgtype、agentid、text.content
- **成功**：`{ "errcode": 0, "errmsg": "ok", "msgid": "..." }`

### 21. 撤回应用消息
- **方法：POST**，**路径：/cgi-bin/message/recall**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 22. 创建群聊会话
- **方法：POST**，**路径：/cgi-bin/appchat/create**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "chatid": "..." }`

### 23. 修改群聊会话
- **方法：POST**，**路径：/cgi-bin/appchat/update**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 24. 获取群聊会话
- **方法：GET**，**路径：/cgi-bin/appchat/get**
- **Query**：access_token（必填）、chatid（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "chat_info": {...} }`

### 25. 应用推送消息到群聊
- **方法：POST**，**路径：/cgi-bin/appchat/send**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "msgid": "..." }`

## 六、日程与日历

### 26. 创建日历
- **方法：POST**，**路径：/cgi-bin/oa/calendar/add**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "cal_id": "..." }`

### 27. 更新日历
- **方法：POST**，**路径：/cgi-bin/oa/calendar/update**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 28. 获取日历详情
- **方法：POST**，**路径：/cgi-bin/oa/calendar/get**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "calendar": {...} }`

### 29. 删除日历
- **方法：POST**，**路径：/cgi-bin/oa/calendar/del**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 30. 创建日程
- **方法：POST**，**路径：/cgi-bin/oa/schedule/add**
- **Query**：access_token（必填）
- **Body**：schedule.admins、schedule.start_time、schedule.end_time
- **成功**：`{ "errcode": 0, "errmsg": "ok", "schedule_id": "..." }`

### 31. 更新日程
- **方法：POST**，**路径：/cgi-bin/oa/schedule/update**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 32. 新增日程参与者
- **方法：POST**，**路径：/cgi-bin/oa/schedule/add_attendees**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 33. 删除日程参与者
- **方法：POST**，**路径：/cgi-bin/oa/schedule/del_attendees**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 34. 获取日程详情
- **方法：POST**，**路径：/cgi-bin/oa/schedule/get**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "schedule": {...} }`

### 35. 取消日程
- **方法：POST**，**路径：/cgi-bin/oa/schedule/del**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

## 七、会议

### 36. 创建预约会议
- **方法：POST**，**路径：/cgi-bin/meeting/create**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "meetingid": "..." }`

### 37. 查询会议列表
- **方法：POST**，**路径：/cgi-bin/meeting/list**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "meetingid_list": [...] }`

### 38. 获取会议详情
- **方法：POST**，**路径：/cgi-bin/meeting/get**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "meeting": {...} }`

### 39. 取消会议
- **方法：POST**，**路径：/cgi-bin/meeting/cancel**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 40. 更新会议受邀成员
- **方法：POST**，**路径：/cgi-bin/meeting/update**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 41. 查询会议室
- **方法：POST**，**路径：/cgi-bin/meeting/rooms/search**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "rooms": [...] }`

### 42. 查询会议室楼栋
- **方法：POST**，**路径：/cgi-bin/meeting/rooms/buildings/list**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "buildings": [...] }`

### 43. 拉取会议转写原文
- **方法：POST**，**路径：/cgi-bin/meeting/transcript/get**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "transcript": "..." }`

## 八、审批

### 44. 获取审批模板详情
- **方法：POST**，**路径：/cgi-bin/oa/gettemplatedetail**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "template": {...} }`

### 45. 提交审批申请
- **方法：POST**，**路径：/cgi-bin/oa/applyevent**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "sp_no": "..." }`

### 46. 获取审批申请详情
- **方法：POST**，**路径：/cgi-bin/oa/getapprovaldetail**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "info": {...} }`

### 47. 批量获取审批编号
- **方法：POST**，**路径：/cgi-bin/oa/getapprovalinfo**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "sp_no_list": [...] }`

## 九、打卡

### 48. 获取打卡规则
- **方法：POST**，**路径：/cgi-bin/checkin/getcheckinoption**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "info": [...] }`

### 49. 获取打卡记录
- **方法：POST**，**路径：/cgi-bin/checkin/getcheckindata**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "data": [...] }`

### 50. 获取打卡日报
- **方法：POST**，**路径：/cgi-bin/checkin/getcheckin_daydata**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "data": [...] }`

## 十、文档

### 51. 新建文档
- **方法：POST**，**路径：/cgi-bin/wedoc/create_doc**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "docid": "...", "url": "..." }`

### 52. 读取文档内容
- **方法：POST**，**路径：/cgi-bin/wedoc/get_doc_content**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "content": "..." }`

### 53. 编辑文档内容
- **方法：POST**，**路径：/cgi-bin/wedoc/mod_doc_content**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok" }`

### 54. 上传文档素材
- **方法：POST**，**路径：/cgi-bin/wedoc/upload_doc_media**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "file_id": "..." }`

### 55. 下载文档素材
- **方法：POST**，**路径：/cgi-bin/wedoc/download_doc_media**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "download_url": "..." }`

## 十一、客户联系

### 56. 获取客户列表
- **方法：GET**，**路径：/cgi-bin/externalcontact/list**
- **Query**：access_token（必填）、userid（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "external_userid": [...] }`

### 57. 获取客户详情
- **方法：GET**，**路径：/cgi-bin/externalcontact/get**
- **Query**：access_token（必填）、external_userid（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "external_contact": {...} }`

### 58. 添加企业群发消息
- **方法：POST**，**路径：/cgi-bin/externalcontact/add_msg_template**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "msgid": "..." }`

### 59. 获取群发消息结果
- **方法：POST**，**路径：/cgi-bin/externalcontact/get_group_msg_result**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "group_msg_list": [...] }`

### 60. 配置客户联系「联系我」方式
- **方法：POST**，**路径：/cgi-bin/externalcontact/add_contact_way**
- **Query**：access_token（必填）
- **成功**：`{ "errcode": 0, "errmsg": "ok", "config_id": "...", "qr_code": "..." }`