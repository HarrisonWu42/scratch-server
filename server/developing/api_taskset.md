# taskset

| api | method| url |
| :-----| :---- | :---- |
| 创建题目集 | POST | http://localhost:5000/taskset/add
| 修改题目集 | POST | http://localhost:5000/taskset/edit
| 删除题目集 | POST | http://localhost:5000/taskset/delete
| 为题目集分配题目|  POST | http://localhost:5000/taskset/assign
| 查询题目集的的所有题目 | GET | http://localhost:5000/taskset/task/<taskset_id>/<offset>/<page_size>
| 查询某人某题目集的得分（得分/总分）| GET | http://localhost:5000/taskset/<user_id>/<taskset_id>
| 查询某个人的题目集| GET| http://localhost:5000/taskset/<user_id>/<offset>/<page_size>

## 创建题目集
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | name | string | 
    | type | int | type=0:个人题目集, type=固定题目集

- 返回参数
    ```
    {
        "code": 200,
        "data": {
            "id": 5,
            "name": "题目集3",
            "type": 0
        },
        "message": "Add taskset success."
    }
    ```

## 修改题目集
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | id | int | 
    | name | string | 
    | type | int |

- 返回参数

    ```
    {
        "code": 200,
        "data": {
            "id": 5,
            "name": "题目集xxx",
            "type": 0
        },
        "message": "Edit taskset success."
    }
    ```
  

## 删除题目集
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | id | int | 

- 返回参数
    ```
    {
        "code": 200,
        "data": {
            "id": 5,
            "name": "题目集xxx",
            "type": 0
        },
        "message": "Delete taskset success"
    }
    ```
  
  

## 为题目集分配题目
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | taskset_id | int | 
    | tasks | array | 存task_id的数组

- 返回参数
    ```
    {
        "code": 200,
        "data": {
            "tasks": [
                {
                    "answer_video_url": "www.123.com",
                    "id": 6,
                    "name": "第x课"
                },
                {
                    "answer_video_url": "www.baidu.com",
                    "id": 7,
                    "name": "第2课"
                },
                {
                    "answer_video_url": "www.baidu.com",
                    "id": 8,
                    "name": "第3课"
                }
            ],
            "taskset_id": 1,
            "taskset_name": "题目集1"
        },
        "message": "Assign task success."
    }
    ```
  
  

## 查询题目集的的所有题目
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | taskset_id | int | 

- 返回参数
    ``` 
    {
        "code": 200,
        "data": {
            "tasks": [
                {
                    "answer_video_url": "www.baidu.com",
                    "commit_num": 0,
                    "description": "成为我的更新标准文章就是不同之后游戏.",
                    "id": 2,
                    "name": "任务242818",
                    "perfect_num": 0,
                    "perfect_rate": null
                }
            ]
        }
    }
    ```

## 查询某人某题目集的得分（得分/总分）
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | user_id | int | 
    | taskset_id | int | 

- 返回参数
    ``` 
    {
        "code": 200,
        "data": {
            "score": 20,
            "total_score": 40
        }
    }
    ```


## 查询某个人的题目集
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | user_id | int | 
    | offset | int | 
    | page_size | int |

- 返回参数
    ``` 
    {
        "code": 200,
        "data": {
            "tasksets": [
                {
                    "id": 6,
                    "name": "固定题目集1",
                    "type": 1
                },
                {
                    "id": 1,
                    "name": "题目集1",
                    "type": 0
                },
                {
                    "id": 4,
                    "name": "题目集2",
                    "type": 0
                }
            ],
            "total_pages": 1,
            "user_id": 5,
            "user_name": "a"
        }
    }
    ```