# group

| api | method| url |
| :-----| :---- | :---- |
| 创建班组 | POST | http://localhost:5000/group/add
| 修改班组 | POST | http://localhost:5000/group/edit
| 删除班组 | POST | http://localhost:5000/group/delete
| 关闭班组 | POST | http://localhost:5000/group/close
| 邀请用户加入班组 | POST | http://localhost:5000/group/invite
| 把某人踢出某班组| POST | http://localhost:5000/group/kick
| 显示某个老师的班组| GET | http://localhost:5000/group/teacher/<teacher_id>/<offset>/<page_size>
| 显示某个班组的所有学生| GET | http://localhost:5000/group/<group_id>/<offset>/<page_size>


## 创建班组
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | name | string | 
    | description | Text |
    | teacher_id| int | 老师ID
    
- 返回参数
    ``` 
    {
        "code": 200,
        "data": {
            "description": "xxx",
            "id": 4,
            "invite_code": "793854",
            "name": "4班",
            "teacher_id": 2,
            "type": 1
        },
        "message": "Add success."
    }
    ```

## 修改班组
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | id | int | 
    | name | string | 
    | description | text | 

- 返回参数
    ```
    {
        "code": 200,
        "data": {
            "description": "abbb",
            "id": 4,
            "invite_code": "793854",
            "name": "A班",
            "teacher_id": 2,
            "type": 1
        },
        "message": "Edit success."
    }
    ``` 
  

## 删除班组
- 请求参数

    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | id | int | 

- 返回参数
    ```
    {
        "code": 200,
        "data": {
            "description": "xxx",
            "id": 7,
            "invite_code": "075489",
            "name": "F班",
            "teacher_id": 2,
            "type": 1
        },
        "message": "Delete success."
    }
    ```
  
  

## 关闭班组
- 请求参数

    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | id | int | 

- 返回参数
    ```
    {
        "code": 200,
        "data": {
            "description": "xxx",
            "id": 6,
            "invite_code": "653890",
            "name": "C班",
            "teacher_id": 2,
            "type": 0
        },
        "message": "Close success."
    }
    ```
  

## 邀请用户加入班组
- 请求参数

    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | user_id | int | 
    | invite_code| string| 六位邀请码：数字字符串

- 返回参数
    ```
    {
        "code": 200,
        "data": {
            "email": "2554612591@qq.com",
            "group_id": 1,
            "group_name": "1班",
            "user_id": 3,
            "user_name": "wuhao3"
        },
        "message": "Invite success."
    }
    ```

## 把某人踢出某班组
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | user_id | int | 
    | group_id | int |
    
- 返回参数
    ``` 
    {
        "code": 200,
        "data": {
            "email": "2554612590@qq.com",
            "group_id": 2,
            "group_name": "2班",
            "user_id": 4,
            "user_name": "wuhao4"
        },
        "message": "Invite success."
    }
    ```

## 显示某个老师的班组
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | teacher_id | int | 
    | offset | int |
    | page_size | int |
    
- 返回参数
    ``` 
    {
        "code": 200,
        "data": {
            "groups": [
                {
                    "description": "xxx",
                    "id": 1,
                    "invite_code": "084795",
                    "name": "1班",
                    "teacher_id": 1,
                    "type": 1
                }
            ],
            "total_pages": 4
        }
    }
    ```
 

## 显示某个班组的所有学生
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | group_id | int | 
    | offset | int |
    | page_size | int |
    
- 返回参数
    ``` 
    {
        "code": 200,
        "data": {
            "students": [
                {
                    "email": "2554612592@qq.com",
                    "id": 2,
                    "name": "teacher1"
                },
                {
                    "email": "2554612591@qq.com",
                    "id": 3,
                    "name": "teacher2"
                }
            ],
            "total_pages": 2
        }
    }
    ```