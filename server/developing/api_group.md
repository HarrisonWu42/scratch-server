# group

| api | method| url |
| :-----| :---- | :---- |
| 创建班组 | POST | http://localhost:5000/group/add
| 修改班组 | POST | http://localhost:5000/group/edit
| 删除班组 | POST | http://localhost:5000/group/delete
| 关闭班组 | POST | http://localhost:5000/group/close
| 邀请用户加入班组 | POST | http://localhost:5000/group/invite
| 把某人踢出某班组 |POST | http://localhost:5000/group/kick
| 显示某个老师的班组 | GET | http://localhost:5000/group/teacher/<teacher_id>/<offset>/<page_size>
| 显示某个班组的所有学生 | GET | http://localhost:5000/group/<group_id>/<offset>/<page_size>
| 一键导入学生到某个班级 | POST | http://localhost:5000/group/import_excel/<group_id>
| 导出某个班级的学生成绩 | GET | http://localhost:5000/group/output_excel/<group_id>
| 为班级分配题目集| POST | http://localhost:5000/taskset/assign

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
            "invite_code": "492308",
            "name": "D班",
            "teacher_id": 2,
            "type": 1
        },
        "message": "Add group success."
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
        "message": "Edit group success."
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
        "message": "Delete group success."
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
        "message": "Close group success."
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

## 导出某个班级的学生成绩
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | group_id | int | 
    
- 返回参数
    - 一个excel的数据

## 一键导入学生到某个班级
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | group_id | int | 
    | file | file | excel文件
    
- 返回参数
    | code | Message| 说明 |
    | :-----| :---- | :---- |
    | 200 | Import success. | 
    | 403 | Import students error. | 同时会传回来exception
    
## 为班级分配题目集
- 请求参数
    
    | 参数名 | 类型| 说明 |
    | :-----| :---- | :---- |
    | group_id | int | 
    | tasksets | array | 存taskset_id的数组

- 返回参数
    ```
    {
        "code": 200,
        "data": {
            "group_id": 1,
            "group_name": "A班",
            "tasksets": [
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
            ]
        },
        "message": "Assign taskset success."
    }
    ```