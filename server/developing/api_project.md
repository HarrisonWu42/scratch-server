# Project

| api | method| url |
| :-----| :---- | :---- |
| 上传sb3文件 | POST | http://localhost:5000/project/upload
| 下载sb3文件 | GET | http://localhost:5000/project/download/<project_id>

## 上传sb3文件
- 请求参数(form-data)
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | user_id | text | 
    | teacher_id | text | 
    | task_id | text |
    | name | text |  
    | file | file |  
    
- 返回参数
    - code=400, message=File type is not allowed.
    
    ```
    {
        "code": 200,
        "data": {
            "id": 8,
            "name": "作品"
        },
        "message": "Upload success."
    }
    ```

## 下载sb3文件
- 请求参数(form-data)
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | project_id | int | 
    
- 返回参数
    - 应该是个file，不是很确定