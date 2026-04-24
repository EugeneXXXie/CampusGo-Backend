# CampusGo 后端项目说明

## 1. 项目简介

本项目是“校园活动组队平台”的后端部分，项目目录名称为 `CampusGoPY`。  
后端使用 `FastAPI + SQLAlchemy + Alembic + MySQL` 开发，提供用户登录、活动管理、报名、收藏、评论、消息等核心接口，为前端 `CampusGo` 提供真实数据支持。

本项目主要服务于课程作业场景，目标不是构建高复杂度商业系统，而是完成一个结构清晰、功能完整、可本地演示、可和前端联调的后端系统。

当前后端已经完成：

- MySQL 数据库接入
- Alembic 数据迁移
- 演示用户初始化
- 演示活动初始化
- 登录鉴权
- 活动列表与详情
- 活动发布
- 活动报名
- 活动收藏
- 评论查看与发布
- 消息查询与已读
- 自动化测试

---

## 2. 技术栈

后端主要使用以下技术：

- `Python`
- `FastAPI`
- `SQLAlchemy 2`
- `Alembic`
- `MySQL`
- `PyMySQL`
- `Pydantic v2`
- `Uvicorn`
- `Pytest`

---

## 3. 项目目录位置

后端项目目录位于：

`C:\Users\33151\Desktop\CampusGoPY`

---

## 4. 项目目录结构

后端核心结构如下：

```text
CampusGoPY
├─ alembic                  数据迁移目录
├─ app
│  ├─ api                   路由与依赖
│  │  └─ routes             各模块接口
│  ├─ core                  配置与安全
│  ├─ db                    数据库连接与 Base
│  ├─ models                SQLAlchemy 数据模型
│  ├─ schemas               Pydantic 数据结构
│  ├─ services              业务逻辑层
│  ├─ utils                 工具函数与种子数据
│  └─ main.py               FastAPI 启动入口
├─ tests                    测试目录
├─ .env                     本地环境配置
├─ .env.example             环境变量示例
├─ alembic.ini              Alembic 配置
├─ requirements.txt         Python 依赖
└─ README.md
```

各目录职责说明如下：

### `app/api`

用于定义接口路由和依赖注入。  
例如：

- 登录接口
- 活动接口
- 收藏接口
- 报名接口
- 评论接口
- 消息接口

### `app/core`

负责：

- 项目配置读取
- token 相关安全逻辑
- CORS 设置相关配置

### `app/db`

负责：

- SQLAlchemy 基础声明
- 数据库引擎
- Session 创建

### `app/models`

用于定义数据库表模型。  
当前核心模型包括：

- `users`
- `activity_categories`
- `activities`
- `activity_signups`
- `activity_comments`
- `favorites`
- `messages`

### `app/schemas`

用于定义接口的请求参数和响应数据结构。

### `app/services`

用于实现业务逻辑，例如：

- 登录验证
- 活动创建与查询
- 报名逻辑
- 评论逻辑
- 收藏逻辑
- 消息逻辑
- 数据序列化

### `app/utils`

当前主要用于初始化种子数据，例如：

- 初始化活动分类
- 初始化演示账号
- 初始化演示活动

---

## 5. 当前已实现的业务模块

### 5.1 认证模块

已实现：

- 用户登录
- 获取当前登录用户信息

### 5.2 活动模块

已实现：

- 活动列表查询
- 活动详情查询
- 创建活动
- 修改活动
- 删除活动

### 5.3 报名模块

已实现：

- 报名活动
- 查询报名列表
- 审核通过
- 审核拒绝
- 取消报名

### 5.4 收藏模块

已实现：

- 收藏活动
- 取消收藏

### 5.5 评论模块

已实现：

- 查询活动评论
- 发表评论
- 删除评论

### 5.6 消息模块

已实现：

- 获取消息列表
- 标记单条消息已读
- 全部标记已读

---

## 6. 数据库设计

当前数据库名称为：

`campus_go`

核心表如下：

### 6.1 `users`

存储用户基础信息，包括：

- 手机号
- 密码哈希
- 昵称
- 学院
- 年级
- 简介
- 角色
- 状态

### 6.2 `activity_categories`

存储活动分类，例如：

- 羽毛球
- 篮球
- 自习
- 桌游
- 探店
- 摄影
- 骑行
- 音乐

### 6.3 `activities`

存储活动主体信息，包括：

- 发起人
- 活动分类
- 标题
- 描述
- 时间
- 地点
- 最大人数
- 当前人数
- 是否审核
- 状态
- 联系方式

### 6.4 `activity_signups`

存储用户报名记录，包括：

- 活动 ID
- 用户 ID
- 报名状态
- 备注

### 6.5 `activity_comments`

存储活动评论。

### 6.6 `favorites`

存储用户收藏活动关系。

### 6.7 `messages`

存储站内消息，例如：

- 报名提醒
- 审核结果
- 评论提醒
- 系统消息

---

## 7. 本地环境要求

建议环境如下：

- `Python 3.11+` 或更高版本
- `MySQL 8.x`
- `pip`

如果本地已创建虚拟环境，也可以直接使用项目中的 `.venv`。

---

## 8. 数据库连接配置

当前项目通过 `.env` 文件读取数据库配置。

本地使用的主要参数如下：

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=Eugene
MYSQL_PASSWORD=994666Wzh
MYSQL_DB=campus_go
DATABASE_URL=mysql+pymysql://Eugene:994666Wzh@localhost:3306/campus_go
```

如果你的 MySQL 用户、密码、数据库名不同，需要自行修改 `.env`。

---

## 9. 首次运行步骤

### 9.1 进入项目目录

```powershell
cd C:\Users\33151\Desktop\CampusGoPY
```

### 9.2 创建虚拟环境

如果还没有 `.venv`，执行：

```powershell
python -m venv .venv
```

### 9.3 安装依赖

```powershell
.\.venv\Scripts\python -m pip install -r requirements.txt
```

### 9.4 配置数据库

确认 `.env` 中的数据库连接配置正确，并且 MySQL 已经启动。

### 9.5 执行迁移

```powershell
.\.venv\Scripts\python -m alembic upgrade head
```

### 9.6 初始化种子数据

```powershell
.\.venv\Scripts\python -c "from app.db.session import SessionLocal; from app.utils.seed import seed_initial_data; db = SessionLocal(); seed_initial_data(db); db.close(); print('seed ok')"
```

这一步会初始化：

- 8 个活动分类
- 1 个演示账号
- 4 条演示活动

### 9.7 启动项目

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

启动后访问：

`http://127.0.0.1:8000/health`

如果返回：

```json
{"status":"ok"}
```

说明后端启动成功。

---

## 10. 常用命令

### 启动开发服务

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 执行数据库迁移

```powershell
.\.venv\Scripts\python -m alembic upgrade head
```

### 重新执行种子数据

```powershell
.\.venv\Scripts\python -c "from app.db.session import SessionLocal; from app.utils.seed import seed_initial_data; db = SessionLocal(); seed_initial_data(db); db.close(); print('seed ok')"
```

### 运行测试

```powershell
.\.venv\Scripts\python -m pytest -q
```

---

## 11. 演示账号

当前已内置演示账号：

- 手机号：`18800001111`
- 密码：`123456`

该账号可直接用于前后端联调和作业展示。

---

## 12. 已实现接口列表

以下接口已经可以直接使用。

### 12.1 健康检查

- `GET /health`

### 12.2 认证接口

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`

### 12.3 活动接口

- `GET /api/activities`
- `GET /api/activities/{activity_id}`
- `POST /api/activities`
- `PUT /api/activities/{activity_id}`
- `DELETE /api/activities/{activity_id}`

### 12.4 报名接口

- `POST /api/activities/{activity_id}/signup`
- `GET /api/activities/{activity_id}/signups`
- `POST /api/signups/{signup_id}/approve`
- `POST /api/signups/{signup_id}/reject`
- `POST /api/signups/{signup_id}/cancel`

### 12.5 评论接口

- `GET /api/activities/{activity_id}/comments`
- `POST /api/activities/{activity_id}/comments`
- `DELETE /api/comments/{comment_id}`

### 12.6 收藏接口

- `POST /api/activities/{activity_id}/favorite`
- `DELETE /api/activities/{activity_id}/favorite`

### 12.7 消息接口

- `GET /api/messages`
- `POST /api/messages/read/{message_id}`
- `POST /api/messages/read-all`

---

## 13. 认证说明

当前项目使用的是轻量 token 鉴权方案。  
登录成功后会返回：

- `access_token`
- `token_type`
- 当前用户信息

前端后续请求时，需要在请求头中携带：

```http
Authorization: Bearer <access_token>
```

未登录访问需要授权的接口时，后端会返回 `401`。

---

## 14. 与前端联调说明

前端项目位于：

`C:\Users\33151\Desktop\CampusGo`

当前前端默认请求：

`http://127.0.0.1:8000`

所以联调时需要：

1. 先启动后端
2. 再启动前端

联调建议顺序如下：

### 第一步：启动后端

```powershell
cd C:\Users\33151\Desktop\CampusGoPY
.\.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 第二步：启动前端

```powershell
cd C:\Users\33151\Desktop\CampusGo
npm run dev:h5
```

### 第三步：访问前端页面

浏览器打开：

`http://127.0.0.1:3000`

---

## 15. 测试说明

后端已经编写并通过了一组基础测试，主要用于验证：

- 基础健康检查
- 认证逻辑
- 安全逻辑
- 关键 API 行为

执行命令：

```powershell
.\.venv\Scripts\python -m pytest -q
```

如果测试全部通过，说明当前后端核心功能基本可用。

---

## 16. 种子数据说明

后端当前种子数据主要定义在：

- [app/utils/seed.py](/abs/path/c:/Users/33151/Desktop/CampusGoPY/app/utils/seed.py)

种子数据包含：

- 8 个活动分类
- 演示用户 1 个
- 演示活动 4 条

这样做的目的，是让前端在刚接入后端时就能直接看到活动数据，而不是打开页面后空白。

---

## 17. 关键文件说明

### 启动入口

- [app/main.py](/abs/path/c:/Users/33151/Desktop/CampusGoPY/app/main.py)

### 配置文件

- [app/core/config.py](/abs/path/c:/Users/33151/Desktop/CampusGoPY/app/core/config.py)

### 鉴权与安全

- [app/core/security.py](/abs/path/c:/Users/33151/Desktop/CampusGoPY/app/core/security.py)
- [app/api/deps.py](/abs/path/c:/Users/33151/Desktop/CampusGoPY/app/api/deps.py)

### 路由层

- [app/api/routes/auth.py](/abs/path/c:/Users/33151/Desktop/CampusGoPY/app/api/routes/auth.py)
- [app/api/routes/activities.py](/abs/path/c:/Users/33151/Desktop/CampusGoPY/app/api/routes/activities.py)
- [app/api/routes/signups.py](/abs/path/c:/Users/33151/Desktop/CampusGoPY/app/api/routes/signups.py)
- [app/api/routes/comments.py](/abs/path/c:/Users/33151/Desktop/CampusGoPY/app/api/routes/comments.py)
- [app/api/routes/favorites.py](/abs/path/c:/Users/33151/Desktop/CampusGoPY/app/api/routes/favorites.py)
- [app/api/routes/messages.py](/abs/path/c:/Users/33151/Desktop/CampusGoPY/app/api/routes/messages.py)

### 业务逻辑层

- `app/services/*.py`

### 数据模型层

- `app/models/*.py`

### 数据迁移

- `alembic/`

---

## 18. 已知说明

### 18.1 项目定位是课程作业项目

本项目优先保证：

- 功能完整
- 结构清晰
- 本地可运行
- 能与前端联调

因此没有按商业项目标准继续引入更复杂的架构，例如：

- JWT 完整权限体系
- Redis 缓存
- 分布式任务
- 文件对象存储
- WebSocket 实时推送

### 18.2 当前更适合演示与答辩

这个后端版本已经足够支撑：

- 课程作业提交
- 项目答辩展示
- 前后端联调说明
- 数据库设计说明
- 接口设计说明

---

## 19. 作业展示时可以这样描述后端

你在演示或答辩时，可以这样总结后端部分：

1. 后端使用 FastAPI + SQLAlchemy + MySQL 开发
2. 通过 Alembic 管理数据库迁移
3. 完成了用户、活动、报名、评论、收藏、消息等核心表设计
4. 实现了登录、活动查询、活动发布、报名、收藏、消息等核心接口
5. 已与 Taro 前端完成联调，能够展示完整业务闭环

这样的表达既完整，也比较符合老师常看的项目汇报逻辑。

---

## 20. 后续可扩展方向

如果还要继续完善，可以考虑：

- 增加注册页与注册流程联调
- 增加管理员审核接口
- 增加文件上传功能
- 增加活动封面上传
- 增加更完整的消息触发逻辑
- 增加接口文档页面整理
- 增加更多测试用例
- 增加 Docker 部署方案

---

## 21. 总结

`CampusGoPY` 已经具备一个课程作业后端应有的主要能力：

- 能启动
- 能连 MySQL
- 能自动建表
- 能初始化演示数据
- 能提供真实接口
- 能和前端联调
- 能完成基础测试

对于当前项目目标来说，这套后端已经足够支撑完整展示和提交。
