# Web-Monitor-Backend

A backend server for our project web-monitor-dashboard

## Dependencies

- [flask](https://palletsprojects.com/p/flask/): Python server of choise
- [flasgger](https://github.com/flasgger/flasgger): Used to generate the swagger documentation
- [flask-marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/): My favourite serializer
- [apispec](https://apispec.readthedocs.io/en/latest/): Required for the integration between marshmallow and flasgger

## Set Up

1. Clone 本仓库
2. 配置数据库接口，创建 `instance/config.py` 并写入：
    ```python
    MONGODB_SETTINGS = {
        'db': 'MongoDBAtlas',
        'host': "mongodb://......"
    }
    ```
3. 安装依赖
    ```bash
    pip install -r requirements.txt
    ```
4. 启动服务端
    ```bash
    export FLASK_DEBUG=true
    flask run
    ```
5. 访问 http://localhost:port/apidocs 查看 swagger 文档

```