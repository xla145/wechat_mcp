# 微信公众号文章自动发布系统 (WeChat MCP)

这是一个基于微信公众号的文章自动发布管理系统，提供文章管理、定时发布、内容编辑等功能。

## 功能特性

- 微信公众号文章管理
- 文章定时发布
- 文章内容编辑和管理
- 发布状态监控
- 文章素材库管理
- 发布历史记录

## 技术栈

- Python 3.8+
- FastAPI (Web框架)
- SQLAlchemy (ORM)
- APScheduler (定时任务)
- WeChatpy (微信公众号SDK)
- Vue.js (前端框架)

## 项目结构

```
wechat_mcp/
├── backend/                 # 后端服务
│   ├── app/                # 应用主目录
│   │   ├── api/           # API路由
│   │   ├── core/          # 核心配置
│   │   ├── models/        # 数据模型
│   │   ├── schemas/       # 数据验证
│   │   └── services/      # 业务逻辑
│   ├── tests/             # 测试用例
│   └── requirements.txt   # 依赖包
├── frontend/              # 前端应用
│   ├── src/              # 源代码
│   └── package.json      # 前端依赖
└── docker/               # Docker配置
```

## 安装说明

1. 克隆项目
```bash
git clone [项目地址]
cd wechat_mcp
```

2. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

3. 安装前端依赖
```bash
cd frontend
npm install
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息
```

5. 启动服务
```bash
# 启动后端服务
cd backend
uvicorn app.main:app --reload

# 启动前端服务
cd frontend
npm run serve
```

## 使用说明

1. 访问系统
- 打开浏览器访问 `http://localhost:8080`
- 使用管理员账号登录系统

2. 配置微信公众号
- 在系统设置中配置微信公众号信息
- 获取并配置必要的API密钥

3. 管理文章
- 创建新文章
- 编辑文章内容
- 设置发布时间
- 预览文章效果

4. 发布管理
- 查看发布队列
- 监控发布状态
- 查看发布历史

## 开发说明

- 遵循 PEP 8 编码规范
- 使用 Git Flow 工作流
- 提交信息使用中文描述

## 许可证

MIT License
