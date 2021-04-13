# Auth

| api | method| url |
| :-----| :---- | :---- |
| 登录 | POST | http://localhost:5000/auth/login
| 登出 | POST | http://localhost:5000/auth/logout
| 注册 | POST | http://localhost:5000/auth/register
| 确认 | GET | http://localhost:5000/auth/confirm/<token>
| 重新发送确认邮件| GET | http://localhost:5000/auth/resend-confirm-email
| 忘记密码 | GET | http://localhost:5000/auth/forget-password
| 重置密码 | GET | http://localhost:5000/auth/reset-password/<token>

## 登录
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | email | string | 
    | password | string | 
    
- 返回参数
    ```
    {
        "code": 200,
        "data": {
            "confirmed": false,
            "email": "303235738@qq.com",
            "id": 6,
            "name": "wuhao"
        },
        "message": "Login success."
    }
    ```

## 登出
- 请求参数
    - 无
    
- 返回参数
    ``` 
    {
        "code": 200,
        "message": "Logout success."
    }
    ```

## 注册
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | name | string | 
    | email | string | 
    | password | string | 
    | password2 | string |  
    
- 返回参数
    ``` 
    {
        "code": 302,
        "data": {
            "id": 6
        },
        "message": "Register success, redirect to login page."
    }
    ```

## 确认
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | token | string | 
    
- 返回参数
    | code | Message| 说明 |
    | :-----| :---- | :---- |
    | 200 | Confirm success. | 
    | 303 | Redirect to main page.|
    | 400 | Error, invalid or expired token.|

## 重新发送确认邮件
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | name | string | 
    
- 返回参数
``` 

```

## 忘记密码
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | name | string | 
    
- 返回参数
``` 

```

## 重置密码
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | name | string | 
    
- 返回参数
``` 

```
