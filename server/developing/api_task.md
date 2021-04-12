# task

| api | method| url |
| :-----| :---- | :---- |
| 显示所有题目 | GET | http://localhost:5000/task/all/<offset>/<per_page>
| 发布题目 | POST | http://localhost:5000/task/add
| 修改题目 | POST | http://localhost:5000/task/edit
| 删除题目 | POST | http://localhost:5000/task/delete|
| 为班组/题目集分配题目| POST | http://localhost:5000/task/assign

## 显示所有题目
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | offset | int | 第几页
    | per_page | int | 一页几条数据

- 返回参数
    ``` 
    {
        "code": 200,
        "data": {
            "tasks": [
                {
                    "answer_video_url": "www.baidu.com",
                    "id": 1,
                    "name": "第1课"
                },
                {
                    "answer_video_url": "www.baidu.com",
                    "id": 2,
                    "name": "第2课"
                }
            ]
        }
    }
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
            "answer_video_url": "www.baidu.com",
            "id": 6,
            "name": "第6课"
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
  
  
## 为班组/题目集分配题目
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | group_id | int | 
    | tasks | array | 存task_id的数组

- 返回参数
    ```
    {
        "code": 200,
        "data": {
            "group_id": 7,
            "group_name": "固定题目集1",
            "tasks": [
                {
                    "answer_video_url": "www.baidu.com",
                    "id": 1,
                    "name": "第1课"
                },
                {
                    "answer_video_url": "www.baidu.com",
                    "id": 2,
                    "name": "第2课"
                }
            ]
        },
        "message": "Assign success."
    }
    ```