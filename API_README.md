# Sora2API - API 接口文档

本文档描述了 Sora2API 的所有独立功能 API 接口。每个功能都有专门的端点，使用更加直观和便捷。

## 📋 目录

- [认证](#认证)
- [图片生成](#图片生成)
  - [文生图](#文生图)
  - [图生图](#图生图)
- [视频生成](#视频生成)
  - [文生视频](#文生视频)
  - [图生视频](#图生视频)
  - [Remix 视频](#remix-视频)
  - [视频分镜](#视频分镜)
- [角色功能](#角色功能)
  - [创建角色](#创建角色)
  - [角色生成视频](#角色生成视频)
- [任务查询](#任务查询)
- [异步模式](#异步模式)
- [支持的模型](#支持的模型)
- [视频风格](#视频风格)
- [错误处理](#错误处理)

---

## 认证

所有 API 请求都需要在请求头中包含 API Key：

```
Authorization: Bearer YOUR_API_KEY
```

默认 API Key: `han1234`（建议在管理后台修改）

---

## 图片生成

### 文生图

根据文本描述生成图片。

**端点**: `POST /v1/images/generate`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 图片描述文本 |
| model | string | 否 | 模型名称，默认为 `gpt-image` |
| stream | boolean | 否 | 是否使用流式响应，默认为 `false` |
| async_mode | boolean | 否 | 异步模式：立即返回 task_id，不等待结果，默认为 `false` |

**支持的模型**:
- `gpt-image` - 正方形图片 (360×360)
- `gpt-image-landscape` - 横屏图片 (540×360)
- `gpt-image-portrait` - 竖屏图片 (360×540)

**请求示例**:

```bash
curl -X POST "http://localhost:8000/v1/images/generate" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "一只可爱的小猫咪",
    "model": "gpt-image",
    "stream": true
  }'
```

**Python 示例**:

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/images/generate",
    headers={
        "Authorization": "Bearer han1234",
        "Content-Type": "application/json"
    },
    json={
        "prompt": "一只可爱的小猫咪",
        "model": "gpt-image",
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        print(line.decode("utf-8"))
```

---

### 图生图

基于上传的图片进行创意变换。

**端点**: `POST /v1/images/transform`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 变换描述文本 |
| image | string | 是 | Base64 编码的图片数据（支持 data URI 格式） |
| model | string | 否 | 模型名称，默认为 `gpt-image` |
| stream | boolean | 否 | 是否使用流式响应，默认为 `false` |
| async_mode | boolean | 否 | 异步模式：立即返回 task_id，不等待结果，默认为 `false` |

**请求示例**:

```bash
curl -X POST "http://localhost:8000/v1/images/transform" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "将这张图片变成油画风格",
    "image": "data:image/png;base64,iVBORw0KGgoAAAANS...",
    "model": "gpt-image",
    "stream": true
  }'
```

**Python 示例**:

```python
import requests
import base64

# 读取图片并编码为 Base64
with open("image.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

response = requests.post(
    "http://localhost:8000/v1/images/transform",
    headers={
        "Authorization": "Bearer han1234",
        "Content-Type": "application/json"
    },
    json={
        "prompt": "将这张图片变成油画风格",
        "image": f"data:image/png;base64,{image_data}",
        "model": "gpt-image",
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        print(line.decode("utf-8"))
```

---

## 视频生成

### 文生视频

根据文本描述生成视频。

**端点**: `POST /v1/videos/generate`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 视频描述文本 |
| model | string | 否 | 模型名称，默认为 `sora2-landscape-10s` |
| style | string | 否 | 视频风格ID（如 `anime`, `retro` 等） |
| stream | boolean | 否 | 是否使用流式响应，默认为 `false` |
| async_mode | boolean | 否 | 异步模式：立即返回 task_id，不等待结果，默认为 `false` |

**请求示例**:

```bash
curl -X POST "http://localhost:8000/v1/videos/generate" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "一只小猫在草地上奔跑",
    "model": "sora2-landscape-10s",
    "style": "anime",
    "stream": true
  }'
```

---

### 图生视频

基于图片生成相关视频。

**端点**: `POST /v1/videos/transform`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 视频描述文本 |
| image | string | 是 | Base64 编码的图片数据（支持 data URI 格式） |
| model | string | 否 | 模型名称，默认为 `sora2-landscape-10s` |
| style | string | 否 | 视频风格ID（如 `anime`, `retro` 等） |
| stream | boolean | 否 | 是否使用流式响应，默认为 `false` |
| async_mode | boolean | 否 | 异步模式：立即返回 task_id，不等待结果，默认为 `false` |

**请求示例**:

```bash
curl -X POST "http://localhost:8000/v1/videos/transform" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "这只猫在跳舞",
    "image": "data:image/png;base64,iVBORw0KGgoAAAANS...",
    "model": "sora2-landscape-10s",
    "style": "anime",
    "stream": true
  }'
```

---

### Remix 视频

基于已有视频继续创作。

**端点**: `POST /v1/videos/remix`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 修改描述文本 |
| remix_target_id | string | 是 | Sora 分享链接的视频ID（格式：`s_68e3a06dcd888191b150971da152c1f5`） |
| model | string | 否 | 模型名称，默认为 `sora2-landscape-10s` |
| style | string | 否 | 视频风格ID（如 `anime`, `retro` 等） |
| stream | boolean | 否 | 是否使用流式响应，默认为 `false` |
| async_mode | boolean | 否 | 异步模式：立即返回 task_id，不等待结果，默认为 `false` |

**获取 remix_target_id**:

从 Sora 分享链接中提取：
- 完整链接: `https://sora.chatgpt.com/p/s_68e3a06dcd888191b150971da152c1f5`
- 视频ID: `s_68e3a06dcd888191b150971da152c1f5`

**请求示例**:

```bash
curl -X POST "http://localhost:8000/v1/videos/remix" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "改成水墨画风格",
    "remix_target_id": "s_68e3a06dcd888191b150971da152c1f5",
    "model": "sora2-landscape-10s",
    "style": "retro",
    "stream": true
  }'
```

---

### 视频分镜

生成分镜视频，支持多个场景。

**端点**: `POST /v1/videos/storyboard`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 分镜描述文本，格式：`[时长s]提示词` 或使用代码块格式 |
| model | string | 否 | 模型名称，默认为 `sora2-landscape-10s` |
| style | string | 否 | 视频风格ID（如 `anime`, `retro` 等） |
| stream | boolean | 否 | 是否使用流式响应，默认为 `false` |
| async_mode | boolean | 否 | 异步模式：立即返回 task_id，不等待结果，默认为 `false` |

**分镜格式示例**:

```
[5.0s]猫猫从飞机上跳伞 [5.0s]猫猫降落 [10.0s]猫猫在田野奔跑
```

或使用多行格式：

```
[5.0s]猫猫从飞机上跳伞
[5.0s]猫猫降落
[10.0s]猫猫在田野奔跑
```

**请求示例**:

```bash
curl -X POST "http://localhost:8000/v1/videos/storyboard" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "[5.0s]猫猫从飞机上跳伞 [5.0s]猫猫降落 [10.0s]猫猫在田野奔跑",
    "model": "sora2-landscape-10s",
    "stream": true
  }'
```

---

## 任务查询

所有生成任务（图片和视频）都可以通过统一的任务查询接口查询状态和结果。

**端点**: `GET /v1/tasks/{task_id}`

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| task_id | string | 任务ID（从生成接口返回） |

**响应格式**:

```json
{
  "task_id": "task_xxx",
  "status": "processing",  // processing/completed/failed
  "progress": 45.5,  // 0.0-100.0
  "model": "sora2-landscape-10s",
  "prompt": "一只小猫在草地上奔跑",
  "result_urls": ["http://example.com/video.mp4"],  // 完成后的结果URL列表
  "error_message": null,  // 错误信息（如果有）
  "created_at": "2024-01-01T00:00:00",
  "completed_at": null  // 完成时间（如果已完成）
}
```

**任务状态**:

- `processing` - 处理中
- `completed` - 已完成
- `failed` - 失败

**请求示例**:

```bash
curl -X GET "http://localhost:8000/v1/tasks/task_xxx" \
  -H "Authorization: Bearer han1234"
```

**Python 示例**:

```python
import requests
import time

def poll_task_status(task_id, max_wait=300, interval=5):
    """轮询任务状态直到完成或超时"""
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        response = requests.get(
            f"http://localhost:8000/v1/tasks/{task_id}",
            headers={"Authorization": "Bearer han1234"}
        )
        
        task = response.json()
        status = task["status"]
        progress = task["progress"]
        
        print(f"任务状态: {status}, 进度: {progress}%")
        
        if status == "completed":
            print(f"任务完成！结果: {task['result_urls']}")
            return task
        elif status == "failed":
            print(f"任务失败: {task.get('error_message', 'Unknown error')}")
            return task
        
        time.sleep(interval)
    
    print("轮询超时")
    return None

# 使用示例
task_id = "task_xxx"
result = poll_task_status(task_id)
```

---

## 异步模式

所有生成接口都支持异步模式（`async_mode=true`）。在异步模式下：

1. **立即返回**: 提交任务后立即返回 `task_id`，不等待结果
2. **后台处理**: 任务在后台异步处理
3. **轮询查询**: 使用 `/v1/tasks/{task_id}` 接口查询任务状态和结果

**异步模式的优势**:

- ✅ 避免长时间等待，提高响应速度
- ✅ 适合批量任务提交
- ✅ 可以灵活控制轮询频率
- ✅ 避免连接超时问题

**使用示例**:

```python
import requests
import time

# 1. 提交任务（异步模式）
response = requests.post(
    "http://localhost:8000/v1/videos/generate",
    headers={
        "Authorization": "Bearer han1234",
        "Content-Type": "application/json"
    },
    json={
        "prompt": "一只小猫在草地上奔跑",
        "model": "sora2-landscape-10s",
        "async_mode": True  # 启用异步模式
    }
)

result = response.json()
task_id = result["task_id"]
print(f"任务已提交，task_id: {task_id}")

# 2. 轮询任务状态
while True:
    status_response = requests.get(
        f"http://localhost:8000/v1/tasks/{task_id}",
        headers={"Authorization": "Bearer han1234"}
    )
    
    task = status_response.json()
    
    if task["status"] == "completed":
        print(f"任务完成！结果: {task['result_urls']}")
        break
    elif task["status"] == "failed":
        print(f"任务失败: {task.get('error_message')}")
        break
    else:
        print(f"处理中... 进度: {task['progress']}%")
        time.sleep(5)  # 每5秒查询一次
```

**注意事项**:

- 异步模式下，`stream` 参数会被忽略（因为不等待结果）
- 任务完成后，结果会保存在数据库中，可以通过 `task_id` 查询
- 建议轮询间隔设置为 5-10 秒，避免过于频繁的请求

---

## 角色功能

### 创建角色

上传视频提取角色信息，获取角色名称和头像。

**端点**: `POST /v1/characters/create`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| video | string | 是 | Base64 编码的视频数据或视频URL（支持 data URI 格式） |
| stream | boolean | 否 | 是否使用流式响应，默认为 `false`（**注意：角色创建必须使用流式模式**） |

**请求示例**:

```bash
curl -X POST "http://localhost:8000/v1/characters/create" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "video": "data:video/mp4;base64,AAAAIGZ0eXBpc29t...",
    "stream": true
  }'
```

**Python 示例**:

```python
import requests
import base64

# 读取视频文件并编码为 Base64
with open("video.mp4", "rb") as f:
    video_data = base64.b64encode(f.read()).decode("utf-8")

response = requests.post(
    "http://localhost:8000/v1/characters/create",
    headers={
        "Authorization": "Bearer han1234",
        "Content-Type": "application/json"
    },
    json={
        "video": f"data:video/mp4;base64,{video_data}",
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        print(line.decode("utf-8"))
```

**响应示例**:

流式响应中会包含角色信息：
```
✨ 角色已识别: Character Name (@username123)
角色创建成功，角色名@username123
```

---

### 角色生成视频

上传视频创建角色，然后使用该角色生成新视频。

**端点**: `POST /v1/characters/generate`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 视频描述文本 |
| video | string | 是 | Base64 编码的视频数据或视频URL（支持 data URI 格式） |
| model | string | 否 | 模型名称，默认为 `sora2-landscape-10s` |
| stream | boolean | 否 | 是否使用流式响应，默认为 `false`（**注意：角色生成视频必须使用流式模式**） |

**请求示例**:

```bash
curl -X POST "http://localhost:8000/v1/characters/generate" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "角色做一个跳舞的动作",
    "video": "data:video/mp4;base64,AAAAIGZ0eXBpc29t...",
    "model": "sora2-landscape-10s",
    "stream": true
  }'
```

**Python 示例**:

```python
import requests
import base64

# 读取视频文件并编码为 Base64
with open("video.mp4", "rb") as f:
    video_data = base64.b64encode(f.read()).decode("utf-8")

response = requests.post(
    "http://localhost:8000/v1/characters/generate",
    headers={
        "Authorization": "Bearer han1234",
        "Content-Type": "application/json"
    },
    json={
        "prompt": "角色做一个跳舞的动作",
        "video": f"data:video/mp4;base64,{video_data}",
        "model": "sora2-landscape-10s",
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        print(line.decode("utf-8"))
```

---

## 支持的模型

### 图片模型

| 模型 | 说明 | 尺寸 |
|------|------|------|
| `gpt-image` | 文生图（正方形） | 360×360 |
| `gpt-image-landscape` | 文生图（横屏） | 540×360 |
| `gpt-image-portrait` | 文生图（竖屏） | 360×540 |

### 视频模型

#### 标准版（Sora2）

| 模型 | 时长 | 方向 | 说明 |
|------|------|------|------|
| `sora2-landscape-10s` | 10秒 | 横屏 | 文生视频/图生视频 |
| `sora2-landscape-15s` | 15秒 | 横屏 | 文生视频/图生视频 |
| `sora2-landscape-25s` | 25秒 | 横屏 | 文生视频/图生视频 |
| `sora2-portrait-10s` | 10秒 | 竖屏 | 文生视频/图生视频 |
| `sora2-portrait-15s` | 15秒 | 竖屏 | 文生视频/图生视频 |
| `sora2-portrait-25s` | 25秒 | 竖屏 | 文生视频/图生视频 |

#### Pro 版（需要 ChatGPT Pro 订阅）

| 模型 | 时长 | 方向 | 说明 |
|------|------|------|------|
| `sora2pro-landscape-10s` | 10秒 | 横屏 | Pro 质量文生视频/图生视频 |
| `sora2pro-landscape-15s` | 15秒 | 横屏 | Pro 质量文生视频/图生视频 |
| `sora2pro-landscape-25s` | 25秒 | 横屏 | Pro 质量文生视频/图生视频 |
| `sora2pro-portrait-10s` | 10秒 | 竖屏 | Pro 质量文生视频/图生视频 |
| `sora2pro-portrait-15s` | 15秒 | 竖屏 | Pro 质量文生视频/图生视频 |
| `sora2pro-portrait-25s` | 25秒 | 竖屏 | Pro 质量文生视频/图生视频 |

#### Pro HD 版（需要 ChatGPT Pro 订阅，高清质量）

| 模型 | 时长 | 方向 | 说明 |
|------|------|------|------|
| `sora2pro-hd-landscape-10s` | 10秒 | 横屏 | Pro 高清文生视频/图生视频 |
| `sora2pro-hd-landscape-15s` | 15秒 | 横屏 | Pro 高清文生视频/图生视频 |
| `sora2pro-hd-portrait-10s` | 10秒 | 竖屏 | Pro 高清文生视频/图生视频 |
| `sora2pro-hd-portrait-15s` | 15秒 | 竖屏 | Pro 高清文生视频/图生视频 |

> **注意：** Pro 系列模型需要 ChatGPT Pro 订阅（`plan_type: "chatgpt_pro"`）。如果没有 Pro 账号，请求这些模型会返回错误。

---

## 视频风格

Sora2API 支持为生成的视频应用预设风格。

### 支持的风格

| 风格ID | 显示名称 | 说明 |
|--------|----------|------|
| `festive` | Festive | 节日风格 |
| `kakalaka` | 🪭👺 | 混沌风格 |
| `news` | News | 新闻风格 |
| `selfie` | Selfie | 自拍风格 |
| `handheld` | Handheld | 手持风格 |
| `golden` | Golden | 金色风格 |
| `anime` | Anime | 动漫风格 |
| `retro` | Retro | 复古风格 |
| `nostalgic` | Vintage | 怀旧风格 |
| `comic` | Comic | 漫画风格 |

### 使用方法

在视频生成请求中设置 `style` 参数：

```json
{
  "prompt": "一只小猫在草地上奔跑",
  "model": "sora2-landscape-10s",
  "style": "anime",
  "stream": true
}
```

---

## 响应格式

### 流式响应

当 `stream=true` 时，响应为 Server-Sent Events (SSE) 格式：

```
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk",...}

data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk",...}

data: [DONE]
```

### 非流式响应

当 `stream=false` 时，响应为 JSON 格式：

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "sora",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "![Generated Image](http://example.com/image.png)"
    },
    "finish_reason": "stop"
  }]
}
```

---

## 错误处理

所有错误响应都遵循统一的格式：

```json
{
  "error": {
    "message": "错误描述",
    "type": "错误类型",
    "param": "参数名（如果有）",
    "code": "错误代码（如果有）"
  }
}
```

### 常见错误类型

- `invalid_request_error` - 请求参数错误
- `server_error` - 服务器内部错误
- `authentication_error` - 认证失败

### 常见错误场景

1. **无效的模型名称**
   ```json
   {
     "error": {
       "message": "Invalid model: invalid-model",
       "type": "invalid_request_error",
       "param": "model",
       "code": null
     }
   }
   ```

2. **缺少必填参数**
   ```json
   {
     "error": {
       "message": "prompt is required",
       "type": "invalid_request_error",
       "param": "prompt",
       "code": null
     }
   }
   ```

3. **认证失败**
   ```json
   {
     "error": {
       "message": "Invalid API key",
       "type": "authentication_error",
       "param": null,
       "code": null
     }
   }
   ```

4. **无可用 Token**
   ```json
   {
     "error": {
       "message": "No available tokens for video generation. All tokens are either disabled, cooling down, Sora2 quota exhausted, don't support Sora2, or expired.",
       "type": "server_error",
       "param": null,
       "code": null
     }
   }
   ```

---

## 完整示例

### Python 完整示例

```python
import requests
import base64
import json

API_BASE = "http://localhost:8000"
API_KEY = "han1234"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 1. 文生图
def generate_image(prompt, model="gpt-image"):
    response = requests.post(
        f"{API_BASE}/v1/images/generate",
        headers=headers,
        json={
            "prompt": prompt,
            "model": model,
            "stream": True
        },
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            data = line.decode("utf-8")
            if data.startswith("data: "):
                chunk = json.loads(data[6:])
                if chunk.get("choices") and chunk["choices"][0].get("delta", {}).get("content"):
                    print(chunk["choices"][0]["delta"]["content"], end="", flush=True)
            elif data == "data: [DONE]":
                print("\n完成！")
                break

# 2. 图生图
def transform_image(prompt, image_path, model="gpt-image"):
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    response = requests.post(
        f"{API_BASE}/v1/images/transform",
        headers=headers,
        json={
            "prompt": prompt,
            "image": f"data:image/png;base64,{image_data}",
            "model": model,
            "stream": True
        },
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            data = line.decode("utf-8")
            if data.startswith("data: "):
                chunk = json.loads(data[6:])
                if chunk.get("choices") and chunk["choices"][0].get("delta", {}).get("content"):
                    print(chunk["choices"][0]["delta"]["content"], end="", flush=True)
            elif data == "data: [DONE]":
                print("\n完成！")
                break

# 3. 文生视频
def generate_video(prompt, model="sora2-landscape-10s", style=None):
    payload = {
        "prompt": prompt,
        "model": model,
        "stream": True
    }
    if style:
        payload["style"] = style
    
    response = requests.post(
        f"{API_BASE}/v1/videos/generate",
        headers=headers,
        json=payload,
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            data = line.decode("utf-8")
            if data.startswith("data: "):
                chunk = json.loads(data[6:])
                if chunk.get("choices") and chunk["choices"][0].get("delta", {}).get("content"):
                    print(chunk["choices"][0]["delta"]["content"], end="", flush=True)
            elif data == "data: [DONE]":
                print("\n完成！")
                break

# 使用示例
if __name__ == "__main__":
    # 文生图
    print("生成图片...")
    generate_image("一只可爱的小猫咪")
    
    # 图生图
    print("\n变换图片...")
    transform_image("将这张图片变成油画风格", "input.png")
    
    # 文生视频（带风格）
    print("\n生成视频...")
    generate_video("一只小猫在草地上奔跑", style="anime")
```

---

## 注意事项

1. **流式响应**: 推荐使用流式响应（`stream=true`）以获得更好的用户体验和实时反馈。

2. **Base64 编码**: 图片和视频数据需要 Base64 编码，支持完整的 data URI 格式（如 `data:image/png;base64,xxx`）。

3. **角色功能**: 角色创建和角色生成视频功能必须使用流式模式（`stream=true`）。

4. **Pro 模型**: 使用 Pro 系列模型需要确保至少有一个 Token 具有 ChatGPT Pro 订阅。

5. **超时设置**: 视频生成可能需要较长时间，请设置合适的超时时间（建议至少 5 分钟）。

6. **并发限制**: 系统支持 Token 级别的并发限制，如果遇到并发限制错误，请稍后重试。

---

## 兼容性说明

本 API 接口与原有的 `/v1/chat/completions` 端点完全兼容，所有功能都可以通过两种方式调用：

1. **独立端点**（推荐）：使用本文档描述的功能端点，更加直观和易用。
2. **统一端点**：继续使用 `/v1/chat/completions` 端点，保持向后兼容。

两种方式的功能和效果完全相同，您可以根据需要选择使用。

---

## 更多信息

- 项目主页: [GitHub](https://github.com/TheSmallHanCat/sora2api)
- 问题反馈: [GitHub Issues](https://github.com/TheSmallHanCat/sora2api/issues)
- 讨论区: [GitHub Discussions](https://github.com/TheSmallHanCat/sora2api/discussions)

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
