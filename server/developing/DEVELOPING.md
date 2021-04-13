# Developing Document

## Code

| Code | Message | Description |
| :-----| :---- | :----
| 200 | Success. | 成功
| 301 | Redirect to home page. | 重定向到首页
| 302 | Redirect to login page. | 重定向到登录页
| 303 | Redirect to main page. | 重定向到主页（登录后的第一页）
| 304 | Redirect to forget_password page. | 重定向到忘记密码
| 305 | Redirect to reset_password page. | 重定向到设置密码
| 400 | Error | 错误, 具体操作看msg
| 401 | User already exist.| 用户已经存在了
| 402 | Excel header error.| ExceL格式错误
| 单元格 | 单元格 |

## 权限管理
### 权限
| 操作 | 权限名称 | 说明 |
| :-----| :---- | :----
| 上传 | SB_UPLOAD | 上传需要评测的sb3文件
| 评测 | SB_EVALUATION | 评测sb3文件
| 下载 | SB_DOWNLOAD | 下载当前版本的sb3文件
| 删除 | SB_DELETE| 删除当前版本的sb3文件
| 任务 | TASK | 发布、修改、删除任务
| 班组 | GROUP | 



### 角色-权限表
| 角色名称 | 权限 | 说明 |
| :-----| :---- | :----
| 游客Guest | 只能浏览页面 | 未登录用户
| 普通用户User | SB_UPLOAD,  | 学生
| 老师Teacher | 除了普通用户的权限还有Teacher的权限 | 老师
| 管理员Administrator| 所有权限| 拥有所有权限的网站管理员