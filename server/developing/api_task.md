# task

| api | method| url |
| :-----| :---- | :---- |
| 创建题目 | POST | http://localhost:5000/task/add
| 修改题目 | POST | http://localhost:5000/task/edit
| 删除题目 | POST | http://localhost:5000/task/delete
| 查看某题目信息| GET | http://localhost:5000/task/<task_id>
| 查看某人某题目的所有提交列表| GET| http://localhost:5000/task/project/<user_id>/<task_id>

## 创建题目
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | name | string | 
    | description | text| 
    | answer_video_url | string | 

- 返回参数
    ```
    {
        "code": 200,
        "data": {
            "answer_video_url": "www.baidu.com",
            "description": "xxxx",
            "id": 6,
            "name": "第1课"
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
    | description | text| 
    | answer_video_url | string | 

- 返回参数

    ```
    {
        "code": 200,
        "data": {
            "answer_video_url": "www.123.com",
            "description": "aaa",
            "id": 6,
            "name": "第x课"
        },
        "message": "Edit task success."
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
            "answer_video_url": "www.baidu.com",
            "description": "xxxx",
            "id": 13,
            "name": "第1课"
        },
        "message": "Delete task success"
    }
    ```

## 查看某题目信息
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | task_id | int |

- 返回参数
    ```
    {
        "code": 200,
        "data": {
            "answer_video_url": "www.baidu.com",
            "description": "Stop structure.",
            "id": 1,
            "name": "Allison Rodgers"
        }
    }
    ```

## 查看某人某任务的所有提交列表
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | user_id | int | 
    | task_id | int |

- 返回参数
    ```
    {
        "code": 200,
        "data": {
            "projects": [
                {
                    "commit_timestamp": "Wed, 14 Apr 2021 07:17:18 GMT",
                    "id": 6,
                    "name": "作品"
                },
                {
                    "commit_timestamp": "Wed, 14 Apr 2021 07:17:17 GMT",
                    "id": 4,
                    "name": "作品"
                },
                {
                    "commit_timestamp": "Wed, 14 Apr 2021 07:17:17 GMT",
                    "id": 5,
                    "name": "作品"
                },
            ]
        }
    }
    ```