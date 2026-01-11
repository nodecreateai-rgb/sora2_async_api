# Dokploy + Nixpacks 部署指南

本文档说明如何在 Dokploy 中使用 Nixpacks 部署 Sora2API，并配置数据持久化存储。

## ⚠️ 重要：数据持久化配置

在 Dokploy 中，每次重新部署时容器会被重建，**必须配置持久化存储卷**才能保留数据。

## 部署步骤

### 1. 在 Dokploy 中创建应用

1. 登录 Dokploy 管理界面
2. 创建新应用，选择你的 Git 仓库
3. 构建方式选择 **Nixpacks**

### 2. 配置持久化存储卷（重要！）

在 Dokploy 应用设置中，添加以下持久化存储卷：

#### 存储卷配置

| 挂载路径 | 说明 | 必需 |
|---------|------|------|
| `/app/data` | 数据库文件存储目录 | ✅ 是 |
| `/app/tmp` | 缓存文件存储目录 | ⚠️ 推荐 |

#### 在 Dokploy 中配置步骤：

1. 进入应用设置 → **Volumes** 或 **存储卷**
2. 添加持久化卷：
   - **名称**: `sora2api-data`
   - **挂载路径**: `/app/data`
   - **类型**: Persistent Volume（持久化卷）
   
3. 添加缓存卷（可选，但推荐）：
   - **名称**: `sora2api-cache`
   - **挂载路径**: `/app/tmp`
   - **类型**: Persistent Volume（持久化卷）

### 3. 配置环境变量

在 Dokploy 应用设置中，添加以下环境变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `DATA_DIR` | `/app/data` | 数据库文件目录（必须与持久化卷路径一致） |
| `CACHE_DIR` | `/app/tmp` | 缓存文件目录（必须与持久化卷路径一致） |
| `PYTHONUNBUFFERED` | `1` | Python 输出缓冲设置 |

### 4. 配置端口

- **端口**: `8000`
- **协议**: HTTP

### 5. 部署应用

1. 点击 **部署** 或 **Deploy**
2. 等待构建完成
3. 检查日志确认应用启动成功

## 验证数据持久化

### 📋 部署前检查清单

在部署前，请确认以下配置：

- [ ] ✅ 已创建持久化卷 `/app/data`（类型：Persistent Volume）
- [ ] ✅ 已设置环境变量 `DATA_DIR=/app/data`
- [ ] ✅ 已设置环境变量 `CACHE_DIR=/app/tmp`（可选）
- [ ] ✅ 卷挂载路径与环境变量值**完全一致**

### 🧪 测试步骤：

1. **首次部署后**：
   - 登录管理后台（默认：`admin`/`admin`）
   - 添加一个测试 Token
   - 确认 Token 已保存
   - 📝 **记录**：记下添加的 Token 信息，用于后续验证

2. **检查启动日志**：
   - 在 Dokploy 中查看应用日志
   - 确认看到以下输出：
     ```
     📁 Data directory: /app/data
     📁 Cache directory: /app/tmp
     ```
   - 如果路径不正确，说明环境变量未正确设置

3. **重新部署测试**：
   - 在 Dokploy 中触发重新部署（例如：推送代码或手动重新部署）
   - 等待部署完成

4. **验证数据**：
   - 重新登录管理后台
   - 检查之前添加的 Token 是否还在
   - ✅ **如果 Token 还在** → 持久化配置成功！🎉
   - ❌ **如果 Token 丢失** → 请参考下面的"数据丢失问题检查清单"

## 常见问题

### Q: 重新部署后数据丢失了

**A:** 这是最常见的问题，通常是因为持久化卷配置不正确。请按照以下检查清单逐一排查：

#### 🔍 数据丢失问题检查清单

**步骤 1：检查持久化卷配置**
- [ ] 进入 Dokploy → 你的应用 → **Volumes** 或 **存储卷**
- [ ] 确认存在名为 `sora2api-data` 的卷（或类似名称）
- [ ] 确认卷的**挂载路径**为 `/app/data`
- [ ] 确认卷的**类型**为 **Persistent Volume**（持久化卷），而不是临时卷
- [ ] ⚠️ **重要**：如果卷类型是 "Temporary" 或 "Empty"，数据会在容器重启时丢失

**步骤 2：检查环境变量配置**
- [ ] 进入 Dokploy → 你的应用 → **Environment Variables** 或 **环境变量**
- [ ] 确认存在 `DATA_DIR` 环境变量，值为 `/app/data`
- [ ] 确认存在 `CACHE_DIR` 环境变量，值为 `/app/tmp`（可选但推荐）
- [ ] ⚠️ **重要**：环境变量的值必须与卷挂载路径**完全一致**

**步骤 3：检查应用启动日志（重要！）**
- [ ] 查看应用启动日志，查找以下诊断信息：
  ```
  🔍 Directory Diagnostics
  📁 Data Directory: /app/data
     Environment variable DATA_DIR: /app/data
     ✓ Directory exists
     ✓ Directory is writable
     ✓ Database file exists: /app/data/hancat.db
  ```
- [ ] **关键检查点**：
  - ✅ 如果看到 `✓ Database file exists` → 数据库文件存在，应该能保留数据
  - ❌ 如果看到 `ℹ️ Database file does not exist yet` → 每次都是首次启动，说明数据未持久化
  - ❌ 如果看到 `❌ Directory is NOT writable!` → 权限问题，需要检查卷挂载
  - ❌ 如果看到 `❌ Directory does not exist!` → 卷未正确挂载
- [ ] 检查数据库初始化日志：
  - ✅ 如果看到 `🔄 Existing database detected` → 数据持久化正常
  - ❌ 如果每次都是 `🎉 First startup detected` → **数据未持久化，需要检查卷配置**

**步骤 4：验证卷挂载（如果日志显示问题）**
- [ ] 在 Dokploy 中进入应用的 **Terminal** 或 **Shell**
- [ ] 执行以下命令检查目录是否存在：
  ```bash
  ls -la /app/data
  ```
- [ ] 检查数据库文件是否存在：
  ```bash
  ls -la /app/data/hancat.db
  ```
- [ ] 检查目录权限：
  ```bash
  touch /app/data/test.txt && rm /app/data/test.txt
  ```
  - ✅ 如果成功 → 目录可写，权限正常
  - ❌ 如果失败 → 权限问题，需要检查卷挂载配置
- [ ] 检查卷挂载点：
  ```bash
  mount | grep /app/data
  ```
  - 应该能看到卷的挂载信息

**步骤 5：常见错误配置**

❌ **错误配置示例 1**：卷挂载路径不匹配
```
卷挂载路径: /data
环境变量 DATA_DIR: /app/data
```
→ 结果：应用写入 `/app/data`，但卷挂载在 `/data`，数据不会持久化

❌ **错误配置示例 2**：使用临时卷
```
卷类型: Temporary Volume
```
→ 结果：容器重启时数据丢失

✅ **正确配置示例**：
```
卷名称: sora2api-data
卷类型: Persistent Volume
挂载路径: /app/data
环境变量 DATA_DIR: /app/data
```
→ 结果：数据正确持久化

### Q: 每次启动都显示 "First startup detected"，数据无法持久化

**A:** 这是一个严重的问题，说明数据库文件没有被正确持久化。请按照以下步骤排查：

#### 🔍 问题诊断

查看启动日志，如果看到：
```
🎉 First startup detected. Initializing database and configuration from setting.toml...
```

**同时检查诊断日志**：
- ❌ 如果看到 `ℹ️ Database file does not exist yet` → 数据库文件未创建或未持久化
- ❌ 如果看到 `❌ Directory is NOT writable!` → 权限问题
- ❌ 如果看到 `❌ Directory does not exist!` → 卷未挂载

#### 🛠️ 解决方案

**方案 1：检查持久化卷类型（最常见原因）**

1. 进入 Dokploy → 你的应用 → **Volumes**
2. 检查 `/app/data` 卷的**类型**：
   - ✅ **Persistent Volume**（持久化卷）→ 正确
   - ❌ **Temporary Volume**（临时卷）→ **这是问题所在！**
   - ❌ **Empty Volume**（空卷）→ **这也是问题！**

3. 如果卷类型不正确：
   - 停止应用
   - 删除错误的卷
   - 创建新的 **Persistent Volume**
   - 挂载路径：`/app/data`
   - 重新部署

**方案 2：检查卷挂载路径**

1. 确认卷的挂载路径是 `/app/data`（不是 `/data` 或其他路径）
2. 确认环境变量 `DATA_DIR=/app/data` 已设置
3. 路径必须**完全一致**

**方案 3：检查卷是否被清空**

某些 Dokploy 配置可能会在重新部署时清空卷。检查：
1. 卷的保留策略设置
2. 是否有自动清理配置
3. 卷的存储位置是否正确

**方案 4：手动验证（高级）**

1. 部署应用后，添加一个测试 Token
2. 在 Dokploy Terminal 中执行：
   ```bash
   ls -la /app/data/hancat.db
   ```
3. 如果文件存在，检查文件大小：
   ```bash
   du -h /app/data/hancat.db
   ```
4. 触发重新部署
5. 再次检查文件：
   ```bash
   ls -la /app/data/hancat.db
   ```
6. 如果文件消失或大小变为 0 → 卷在重新部署时被清空

#### 🛠️ 修复步骤

如果发现配置错误，按以下步骤修复：

1. **停止应用**（在 Dokploy 中停止应用）

2. **删除错误的卷**（如果存在）：
   - 进入 Volumes 设置
   - 删除挂载路径错误的卷

3. **创建正确的持久化卷**：
   - 卷名称：`sora2api-data`
   - 卷类型：**Persistent Volume**
   - 挂载路径：`/app/data`

4. **设置环境变量**：
   - `DATA_DIR=/app/data`
   - `CACHE_DIR=/app/tmp`

5. **重新部署应用**

6. **验证数据持久化**（按照上面的测试步骤）

### Q: 如何备份数据？

**A:** 在 Dokploy 中：

1. 进入应用 → Volumes
2. 找到 `sora2api-data` 卷
3. 下载或导出卷数据（具体操作取决于 Dokploy 版本）

或者通过 SSH 连接到服务器：

```bash
# 找到卷的实际存储位置（取决于 Dokploy 的配置）
# 通常位于 /var/lib/dokploy/volumes/ 或类似路径
# 备份数据库文件
cp /path/to/volume/data/hancat.db /backup/hancat.db.backup
```

### Q: 如何迁移数据到新部署？

**A:** 

1. **备份旧数据**：
   - 导出旧部署的持久化卷数据
   - 或直接复制 `hancat.db` 文件

2. **在新部署中恢复**：
   - 在新部署中创建持久化卷
   - 将备份的 `hancat.db` 文件复制到 `/app/data/` 目录
   - 重启应用

### Q: 缓存文件占用空间太大怎么办？

**A:** 

1. **清理缓存**：
   - 在管理后台可以清理缓存
   - 或手动删除 `/app/tmp` 目录中的文件

2. **调整缓存超时**：
   - 在 `config/setting.toml` 中调整 `cache.timeout` 值
   - 或在管理后台修改缓存配置

3. **禁用缓存**：
   - 在配置中设置 `cache.enabled = false`

## 数据目录说明

### `/app/data` 目录

存储以下数据：
- `hancat.db` - SQLite 数据库文件（包含所有 Token、任务、配置等）
- 这是**最重要的目录**，必须配置持久化存储

### `/app/tmp` 目录

存储以下数据：
- 生成的图片和视频缓存文件
- 临时文件
- 可以定期清理，不影响核心功能

## 最佳实践

1. ✅ **始终配置持久化卷**：确保 `/app/data` 目录使用持久化存储
2. ✅ **定期备份**：定期备份 `hancat.db` 文件
3. ✅ **监控存储空间**：注意持久化卷的存储空间使用情况
4. ✅ **测试部署流程**：在正式环境部署前，先在测试环境验证持久化配置

## 相关文件

- `nixpacks.toml` - Nixpacks 构建配置
- `config/setting.toml` - 应用配置文件
- `README.md` - 项目主文档

---

**如果遇到问题，请检查：**
1. Dokploy 的持久化卷配置文档
2. Nixpacks 的构建日志
3. 应用启动日志中的数据库路径信息
