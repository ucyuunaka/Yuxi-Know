# 🎯 您的个性化Docker安装指南

> **基于您的系统状态定制** - 避免重复安装，只做必要的配置

---

## 📊 您当前系统状态

| 组件 | 状态 | 备注 |
|------|------|------|
| ✅ Hyper-V | **已安装并运行** | vmms服务正在运行 |
| ✅ WSL2 | **已安装并运行** | Ubuntu发行版正在运行，版本2 |
| ❌ Docker Desktop | **未安装** | 需要安装 |
| ✅ 端口状态 | **可用** | 5173、5050等端口未被占用 |

**好消息！** 您已经完成了80%的安装工作，只需要安装Docker Desktop即可！

---

## 🚀 剩余安装步骤（仅需1步）

### 只需安装Docker Desktop

由于您的Hyper-V和WSL2都已经正确安装并运行，您只需要：

1. **下载Docker Desktop**
   - 访问：https://www.docker.com/products/docker-desktop/
   - 下载Windows版本

2. **安装Docker Desktop**
   - 双击下载的安装文件
   - 一路点击Next → 接受协议 → 点击Finish
   - 安装完成后会自动启动

3. **验证安装**
   - 通知栏出现小鲸鱼图标
   - 打开PowerShell，运行：
   ```powershell
   docker --version
   docker run hello-world
   ```

---

## ⚡ 快速启动Yuxi-Know项目

Docker安装完成后，直接启动项目：

```powershell
# 进入项目目录
cd F:\Code\From-github\Yuxi-Know

# 启动项目
make start
```

如果出现命令未找到，使用：
```powershell
docker compose up -d
```

---

## 📝 配置API密钥

编辑 `.env` 文件，至少配置一个AI服务：

```bash
# 推荐使用硅基流动（免费额度大）
SILICONFLOW_API_KEY=your_siliconflow_key_here

# 或者使用其他服务
OPENAI_API_KEY=your_openai_key_here
ZHIPUAI_API_KEY=your_zhipuai_key_here
```

---

## 🎯 项目访问地址

启动成功后访问：
- **前端界面**: http://localhost:5173
- **API文档**: http://localhost:5050/docs
- **Neo4j浏览器**: http://localhost:7474

---

## 📋 检查清单（您的版本）

- [x] Hyper-V已安装并运行
- [x] WSL2已安装并运行
- [ ] Docker Desktop下载并安装
- [ ] 验证docker命令可用
- [ ] 配置.env文件API密钥
- [ ] 启动Yuxi-Know项目
- [ ] 访问http://localhost:5173测试

---

## ⚠️ 可能遇到的问题

### 1. Docker Desktop安装问题
- **问题**：安装失败提示WSL2问题
- **解决**：您的WSL2已正常，重试安装即可

### 2. Docker启动问题
- **问题**：Docker Desktop无法启动
- **解决**：重启电脑，然后启动Docker Desktop

### 3. 项目启动问题
- **问题**：端口被占用
- **解决**：您的端口都可用，如有问题重启Docker服务

---

## 🎉 完成时间预估

- **Docker Desktop下载**：5-10分钟（取决于网速）
- **Docker Desktop安装**：2-3分钟
- **项目首次启动**：5-10分钟（下载镜像）
- **总时间**：约15-20分钟

**比全新安装节省了约30分钟！** 🚀

---

## 📞 需要帮助？

如果遇到问题：
1. 确认Docker Desktop通知栏图标是否显示
2. 检查PowerShell中docker命令是否可用
3. 查看项目日志：`docker compose logs`

**您已经完成了大部分工作，很快就能体验Yuxi-Know了！** ✨