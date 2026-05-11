# 00 — 阶段化开发流程详解

> 每个阶段的目标、步骤、验收标准和常见坑

## 阶段 -1：需求分析

### 目标
把模糊的需求变成清晰的功能清单和技术方案。

### 步骤
1. **和用户对齐需求**
   - 这个工具解决什么问题？
   - 核心功能是？边界功能是？
   - 谁用？自己用还是给别人用？
2. **确定技术栈**（执行技术栈决策树 `05-tech-stack-guide.md`）
3. **确定项目名称**（英文/拼音，短且有意义）
4. **输出 PRD**
   - 项目名称、目录位置
   - 功能清单（按优先级排列）
   - 技术栈清单

### 验收标准
- [ ] 有书面的功能清单，用户确认
- [ ] 技术栈已确定
- [ ] 项目名称和路径已确定

### 常见坑
- 需求太模糊就开干 → 先出功能清单再动手
- 技术栈选太重 → 小工具别上微服务

---

## 阶段 0：项目脚手架

### 目标
搭好项目骨架，确保能跑起来。这一步决定了后面的开发体验。

### 步骤
1. **创建目录结构**
   ```
   project-name/
   ├── run.py                    # 启动入口
   ├── requirements.txt          # 依赖
   ├── config.yaml               # 配置文件
   ├── backend/
   │   ├── .env                  # 环境变量
   │   └── app/
   │       ├── __init__.py
   │       ├── main.py           # FastAPI 应用
   │       ├── config.py         # 配置读取
   │       ├── models/           # 数据模型
   │       │   ├── __init__.py
   │       │   ├── schemas.py
   │       │   └── task_store.py
   │       ├── services/         # 业务逻辑
   │       │   └── __init__.py
   │       └── api/              # API 接口
   │           └── __init__.py
   ├── 启动.bat                  # 快捷启动
   └── 安装必要组件.bat          # 依赖安装
   ```
2. **编写配置文件**
   - `config.yaml`：可修改的配置（端口、路径、开关）
   - `.env`：环境变量（密钥、敏感信息）
   - `config.py`：读取配置 + 路径自动检测
3. **编写入口文件 `run.py`**
   - 开发模式：`python run.py` 启动 uvicorn
   - 桌面模式：`python run.py -d` 启动 pywebview
4. **生成快捷启动**
   - `启动.bat`：双击启动 dev 模式
   - `安装必要组件.bat`：pip install + playwright install
5. **验证 `python run.py` 能跑**

### 验收标准
- [ ] `python run.py` 能启动，浏览器能打开页面
- [ ] 配置文件能被读取，修改配置生效
- [ ] 快捷批处理文件双击可用
- [ ] `requirements.txt` 完整无遗漏

### 常见坑
- 硬编码路径 → 用 `Path(__file__).parent` 取相对路径
- 忘记 `__init__.py` → Python 包导入会失败
- pywebview 端口写死 → 先检测端口占用，自动找可用端口

---

## 阶段 1：后端核心

### 目标
实现全部后端业务逻辑，API 可调用。

### 步骤
1. **数据模型 `models/schemas.py`**
   - 定义请求/响应的 Pydantic 模型
   - 定义枚举类型（如 MediaType）
   - 参考 `Ptu: schemas.py`
2. **数据持久化 `models/task_store.py`**
   - JSON 文件存储（适合简单场景）
   - SQLite（适合复杂场景）
3. **业务服务 `services/`**
   - 一个文件一个 Service 类
   - 关注点分离：每个服务只做一件事
   - 错误用中文提示（参考 `06-cn-error-handling.md`）
4. **API 路由 `api/routers/`**
   - 一个路由文件一组相关接口
   - RESTful 命名
   - WebSocket 实时进度（`router_ws.py`）
5. **应用组装 `main.py`**
   - FastAPI 实例化
   - 路由注册
   - 静态文件挂载
   - CORS 中间件
   - 异常处理器（全局中文异常处理）

### 验收标准
- [ ] 所有 API 端点返回 200
- [ ] 错误场景返回中文错误信息
- [ ] WebSocket 连接正常
- [ ] 数据能正确读写

### 常见坑
- models/services/routers 耦合 → service 不直接依赖 router，通过参数传递
- 异常没处理 → API 层要有全局异常处理器
- 任务状态不同步 → WebSocket 推送 + 任务状态轮询双重保障

---

## 阶段 2：前端 / UI

### 目标
让用户可以通过界面操作所有功能。

### 步骤
1. **基础布局 `templates/base.html`**
   - 通用头部、样式引入
   - 中文错误消息展示区域
2. **主页面 `templates/index.html`**
   - 输入区域（URL 输入 + 粘贴按钮）
   - 结果展示（列表 / 画廊）
   - 操作按钮（下载、渲染、删除）
   - 进度显示
3. **样式 `static/css/app.css`**
   - 暗色主题（参考 Ptu 的 Noir+Indigo）
   - 响应式布局
   - 组件样式
4. **交互 `static/js/app.js`**
   - API 调用封装
   - WebSocket 连接
   - 状态管理
   - 错误消息展示

### 验收标准
- [ ] 所有功能可通过界面完成
- [ ] 错误信息用中文显示
- [ ] 操作有反馈（加载中、成功、失败）
- [ ] 页面无 CDN 依赖（离线可用）

### 常见坑
- 前端直接暴露 API 地址 → 全部走相对路径 `/api/...`
- 高耦合 JS → 模块化组织，命名空间隔离
- 缺少粘贴按钮 → 用户不习惯右键粘贴

---

## 阶段 3：桌面端（可选）

### 目标
通过 pywebview 把 Web 应用包装成原生桌面应用。

### 步骤
1. 编写 `desktop_app.py`
2. 实现 JsApi 桥接（文件对话框、系统通知、打开文件夹）
3. 系统托盘 + 最小化到托盘
4. 单实例锁（防止重复启动）
5. 窗口位置记忆

详见 `04-desktop-pattern.md`

### 验收标准
- [ ] 双击 `python run.py -d` 显示原生窗口
- [ ] 系统托盘正常
- [ ] JS 能调用 Python 方法
- [ ] 窗口位置下次启动能恢复

---

## 阶段 4：打包发布

### 目标
打包成可分发 EXE，用户双击就能用。

### 步骤
1. 编写 `setup_check.py` — 运行时自动检测依赖、下载缺失组件
2. 编写 `build.spec` — PyInstaller 配置
3. 编写 `build_exe.bat` — 一键打包
4. 打包后冒烟测试：在干净环境运行 EXE
5. （可选）Inno Setup 制作安装包

详见 `03-packaging-guide.md`

### 验收标准
- [ ] EXE 在其他机器能正常运行
- [ ] 缺失组件自动下载（Chrome/FFmpeg）
- [ ] 打包后所有功能正常
- [ ] 错误信息用中文显示

### 常见坑
- `hiddenimports` 遗漏 → 打包后 ModuleNotFoundError（最常见的闪退原因）
- 资源文件路径不对 → 用 `sys.frozen` + `sys._MEIPASS` 判断
- gbk 编码问题 → `open(..., encoding='utf-8')`
- 80% 的打包失败都是 hiddenimports 问题，排查优先
