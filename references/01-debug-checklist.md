# 01 — 问题排查清单

> 基于 Ptu 项目 17+ bug 的实战经验总结

## 一、快速定位：问题分类

| 症状 | 最可能的原因 | 优先级 |
|------|-------------|--------|
| 打包后闪退 | hiddenimports 缺失 | 🔴 高 |
| 启动报错 | 配置/路径不对 | 🔴 高 |
| API 返回异常 | 登录态/Cookie 失效 | 🟡 中 |
| 抓取数据不对 | 平台页面结构变了 | 🟡 中 |
| 前端没反应 | API 地址不对 / CORS | 🟡 中 |
| 桌面端窗口异常 | pywebview 版本问题 | 🟢 低 |
| 编码乱码 | gbk ↔ UTF-8 | 🟢 低 |

---

## 二、逐类排查

### A. 打包后闪退（最频繁的问题）

**排查顺序：**

1. **检查 `build.spec` 的 `hiddenimports`**
   - 你的项目导入了什么模块？每个模块是否都在 hiddenimports 里？
   - 常见遗漏：`uvicorn`、`multipart`、`websockets`、`httpx`、`yaml`
   - 如果你的项目有 `js_api.py`，必须在 hiddenimports 里

2. **检查路径**
   - 使用 Path 和 `sys.frozen`/`sys._MEIPASS` 判断路径
   - 不要用 `os.getcwd()`，不要用硬编码路径

3. **检查资源文件**
   - `templates/`、`static/` 是否被 `build.spec` 的 `datas` 包含？

4. **在 dev 模式下测试**
   ```python
   # 快速验证打包环境
   import sys
   if getattr(sys, 'frozen', False):
       base = sys._MEIPASS
   else:
       base = Path(__file__).parent
   ```

### B. API 返回异常

1. **检查登录态**
   - Cookie 是否过期？`msToken`/`ttwid`/`sessionid` 是否有效？
   - 登录态是否在打包后丢失？→ Cookie 存储路径硬编码了吗？

2. **检查请求参数**
   - 参数名是否正确？参数类型是否正确？
   - Serialize 时枚举类型是否正确？（Pydantic 枚举可能被序列化为字符串）

3. **检查平台端点**
   - 目标平台 API 是否更新？
   - 是否需要双端重试（如 `/aweme/detail/` + `/note/detail/`）

### C. 抓取数据不对

1. **数量不对**
   - 是否混入了推荐/广告内容？→ 按位置/尺寸过滤
   - 懒加载没处理？→ 检查 `data-src`、`data-url` 属性
   - 分页没处理？→ 查看是否有「查看更多」

2. **类型识别错误**
   - 视频被识别为实况？→ 检查视频检测优先级
   - 实况被识别为图片？→ 检查是否有 `video` 字段
   - 混合内容没处理？→ 需要增加 `COMPREHENSIVE` 类型

3. **Playwright 提取失败**
   - 页面加载超时？→ 增加等待时间
   - 页面结构变了？→ 打开浏览器手动看 HTML 结构
   - 浏览器路径不对？→ 检查 `setup_check.py` 的 `get_chromium_path()`
   - headless VS headless_shell 用错？→ `chromium_headless_shell` 单独安装

### D. 桌面端问题

1. **pywebview 窗口不显示**
   - WebView2 装了没？→ Windows 10/11 默认有
   - 端口是否被占用？→ 启动前检测端口

2. **JS-Python 桥接失败**
   - `js_api.py` 是否在打包配置的 `hiddenimports` 里？
   - JS 端的调用名和 Python 端是否一致？

3. **打包后桌面模式报错**
   - `win32event`、`win32api`、`win32gui` 是否在 hiddenimports？
   - `GetLastError()` 方法是否存在？→ 检查 pywin32 版本

### E. 编码问题

1. **症状**
   - gbk 无法编码字符 `€`、`✓`
   - 打印 emoji 报错

2. **解决方案**
   ```python
   # 所有文件打开指定 UTF-8
   with open(path, 'r', encoding='utf-8') as f:
   
   # 日志/控制台输出时捕获编码错误
   import sys
   if sys.stdout.encoding != 'utf-8':
       sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
   ```

---

## 三、通用调试流程

```
1. 复现问题
   └─ 记下完整的错误信息和复现步骤
   
2. 缩小范围
   ├─ 是 dev 模式还是打包后的问题？
   ├─ 是某个特定输入还是所有输入都会触发？
   └─ 用二分法注释代码缩小范围

3. 根因分析
   ├─ 不要只修表面现象，要找到根源
   ├─ 一层层问为什么
   └─ 一次修完所有相关的问题

4. 修复
   ├─ 改动最小化
   ├─ 同步更新相关代码
   └─ 添加中文错误提示

5. 验证闭环
   ├─ 确认修好了
   ├─ 确认没引入新的问题
   └─ 确保以后同样的错误能被正确捕获
```
