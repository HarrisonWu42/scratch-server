# group

| api | method| url |
| :-----| :---- | :---- |
| 创建班组 | POST | http://localhost:5000/group/add
| 修改题目 | POST | http://localhost:5000/group/edit
| 删除题目 | POST | http://localhost:5000/group/delete
| 删除题目 | POST | http://localhost:5000/group/delete
| 删除题目 | POST | http://localhost:5000/group/delete


## 创建班组
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | name | string | 
    | description | Text |
    | teacher_id| int | 老师ID
    
- 返回参数
    ``` 
    ```
 
## 发布题目
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | name | string | 
    | answer_video_url | string | 

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
            "type": "1"
        },
        "message": "Add task success."
    }
    ```


## 修改题目
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | id | int | 
    | name | string | 
    | answer_video_url | string | 

- 返回参数

    ```
    {
        "code": 200,
        "data": {
            "answer_video_url": "www.123.com",
            "id": 5,
            "name": "第x课"
        },
        "message": "Add task success."
    }
    ```
  
## 删除题目
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | id | int | 

- 返回参数

    ```
    {
        "code": 200,
        "data": {
            "answer_video_url": "www.123.com",
            "id": 5,
            "name": "第x课"
        },
        "message": "Delete success"
    }
    ```