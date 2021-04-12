# User

| api | method| url |
| :-----| :---- | :---- |
| 修改昵称 | POST | http://localhost:5000/user/edit-name
| 修改邮箱 | POST | http://localhost:5000/user/change-email

## 修改昵称
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | name | string | 
    
- 返回参数
    ```
    {
        "code": 200,
        "data": {
            "email": "303235738@qq.com",
            "id": 1,
            "name": "adminnnn"
        },
        "message": "Edit success"
    }
    ```

## 修改邮箱
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | email | string | 
    
- 返回参数
    ```
    {
        "code": 200,
        "data": {
            "email": "303235738@qq.com",
            "id": 1,
            "name": "adminnnn"
        },
        "message": "Change email success"
    }
    ```