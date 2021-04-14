# task

| api | method| url |
| :-----| :---- | :---- |
| 创建题目 | POST | http://localhost:5000/task/add
| 修改题目 | POST | http://localhost:5000/task/edit
| 删除题目 | POST | http://localhost:5000/task/delete|

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
  
  