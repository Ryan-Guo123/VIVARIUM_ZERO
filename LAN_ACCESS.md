# 🌐 VIVARIUM ZERO - 局域网访问指南

## ✅ 服务器已启动

**服务器地址**: `192.168.139.89:8000`

---

## 📱 从局域网内其他设备访问

### 方式 1: 直接访问 (推荐)

在同一局域网的任何设备上打开浏览器，访问：

```
http://192.168.139.89:8000
```

### 方式 2: 本机访问

如果在运行服务器的机器上访问：

```
http://localhost:8000
```

或

```
http://127.0.0.1:8000
```

---

## 🔍 测试连接

### API 健康检查

```bash
curl http://192.168.139.89:8000/api/health
```

预期输出：
```json
{
  "status": "healthy",
  "tick": 12345,
  "population": 150,
  "generation": 25
}
```

### WebSocket 连接

前端会自动连接到 WebSocket：
```
ws://192.168.139.89:8000/ws
```

---

## 🖥️ 多设备同时观看

可以从多个设备同时访问：
- 📱 **手机**: 打开浏览器访问 `http://192.168.139.89:8000`
- 💻 **平板**: 同样的地址
- 🖥️ **其他电脑**: 同样的地址

所有设备会看到相同的实时模拟画面！

---

## 🎮 控制面板

每个连接的客户端都可以控制模拟：
- **⏸ 暂停**: 所有客户端同步暂停
- **▶️ 继续**: 恢复运行
- **⏭ 单步**: 执行一帧
- **🔄 重置**: 重新开始

---

## 🔧 服务器管理

### 查看服务器日志

```bash
# 查看最近的日志
tail -f /home/home/VIVARIUM_ZERO/backend/nohup.out

# 或查看进程
ps aux | grep uvicorn
```

### 停止服务器

```bash
pkill -f uvicorn
```

### 重启服务器

```bash
cd /home/home/VIVARIUM_ZERO
source backend/venv/bin/activate
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
```

---

## 📊 当前状态

查看实时统计：
```bash
curl http://192.168.139.89:8000/api/statistics
```

---

## 🔒 防火墙配置（如果无法访问）

如果局域网内其他设备无法访问，可能需要开放端口：

```bash
# 检查防火墙状态
sudo ufw status

# 如果防火墙开启，允许 8000 端口
sudo ufw allow 8000/tcp

# 或暂时关闭防火墙（不推荐生产环境）
sudo ufw disable
```

---

## 📱 移动设备最佳体验

在手机/平板上访问时：
1. 使用 **横屏模式** 以获得更好的视野
2. 确保与服务器在 **同一 WiFi** 网络
3. 如果卡顿，可以降低目标 FPS（修改 `.env` 中的 `TARGET_FPS=30`）

---

## 🚀 性能优化建议

### 如果设备过多导致卡顿

编辑 `/home/home/VIVARIUM_ZERO/.env`：

```bash
# 降低更新频率
TARGET_FPS=30

# 减少人口上限
MAX_POPULATION=200

# 减少食物生成
FOOD_SPAWN_COUNT=2
```

然后重启服务器。

---

## 🐛 故障排查

### 问题: 无法连接到服务器

**解决方法**:
1. 确认服务器正在运行：
   ```bash
   curl http://localhost:8000/api/health
   ```

2. 检查 IP 地址是否正确：
   ```bash
   hostname -I
   ```

3. 确保客户端和服务器在同一网络

### 问题: WebSocket 连接失败

**解决方法**:
1. 打开浏览器开发者工具 (F12)
2. 查看 Console 是否有错误
3. 查看 Network → WS 标签页
4. 刷新页面重新连接

### 问题: 画面卡顿

**解决方法**:
1. 降低 `TARGET_FPS` 到 30
2. 减少 `MAX_POPULATION`
3. 使用有线网络而非 WiFi
4. 减少同时连接的客户端数量

---

## 📝 示例：二维码分享

可以将访问地址生成二维码，方便手机扫码访问：

```bash
# 安装 qrencode
sudo apt install qrencode

# 生成二维码
qrencode -t UTF8 "http://192.168.139.89:8000"
```

---

## ✨ 享受观察进化！

现在你可以：
- 🔬 在大屏幕上观察整体演化趋势
- 📱 在手机上实时监控
- 🎮 从任何设备控制模拟
- 👥 与朋友一起观看人工生命的诞生

**访问地址**: http://192.168.139.89:8000
