# Admin

| api | method| url |
| :-----| :---- | :---- |
| 查看所有用户的权限| GET | http://localhost:5000/admin/users
| 查看所有权限| GET | http://localhost:5000/admin/roles
| 修改用户权限| POST | http://localhost:5000/admin/edit-role/<user_id>


## 查看所有用户的权限
- 请求参数
    无
    
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

## 查看所有权限
- 请求参数
    无
    
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

## 修改用户权限
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | role | string | 
    
- 返回参数
    ``` 
    {
        "code": 200,
        "data": {
            "email": "jieliang@fangwu.cn",
            "id": 3,
            "name": "蒋畅",
            "role": "Teacher"
        },
        "message": "Edit success"
    }
    ```