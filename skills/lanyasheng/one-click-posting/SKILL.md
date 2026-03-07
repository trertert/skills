---
name: one-click-posting
description: 一键发帖执行技能：把同一条内容快速打包为小红书/X/知乎可发布稿，并按固定门禁完成“预检→老板确认→发布→截图复核→数据归档”。用于用户说“一键发帖”“帮我直接发”“多平台同步发”“先出发布包再发”的场景；也用于发布前质量检查和发布后复盘归档。
---

# One Click Posting

目标：让“发帖”变成可重复执行的流水线，而不是临场手工操作。

## 1) 固定输入（先收齐，再执行）

必须先固定：
- 平台列表（`xiaohongshu` / `x` / `zhihu`）
- 标题、正文、标签
- 封面/配图路径（可为空，但需明确）
- 素材来源与核验状态（已核验/待核实）

可选：
- 发布时间（立即/定时）
- 首评草稿

若输入不完整：先补齐，不进入发布动作。

## 2) 生成发布包（必须先做）

执行：

```bash
python3 skills/one-click-posting/scripts/build_publish_packet.py \
  --title "标题" \
  --body-file "/absolute/path/to/body.md" \
  --platform xiaohongshu --platform x \
  --cover "/absolute/path/to/cover.png" \
  --tags "AI工具,效率,工作流" \
  --source "ainews,trading" \
  --audience "技术人" \
  --core-viewpoint "AI先跑，人来拍板" \
  --first-comment "你最想先外包哪件重复工作？"
```

发布包特性：
- 自动去重与校验平台参数
- 自动生成质量检查项（标题、正文长度、来源、封面等）
- 默认 `approval.granted=false`
- 预留发布后指标回填字段

## 3) 运行预检（强制）

生成发布包后必须执行：

```bash
python3 skills/one-click-posting/scripts/run_preflight.py \
  --packet "/absolute/path/to/publish-packet.json" \
  --require-approval \
  --write-back
```

判定规则：
- 返回 `status: pass` 才可进入发布步骤
- 返回 `status: fail` 时，先修复失败项再继续

## 4) 发布前门禁（硬性）

必须同时满足：
- 内容去 AI 味检查通过（必要时先调用 `content-deai-engine`）
- 来源可追溯，待核实信息已显式标注
- 用户明确口令确认发布（例如：“老板确认发布”）

未满足任一条件：禁止发布。

## 5) 平台执行顺序（建议）

默认顺序：`xiaohongshu -> x -> zhihu`

原因：
- 小红书最依赖封面与图文结构，最容易出现上传/预览异常，优先处理。

## 6) 小红书执行SOP（重点）

按 `references/xiaohongshu-cover-sop.md` 执行，关键规则：
- 封面优先策略：`首图 = 封面`
- 不依赖“替换当前图”单一入口；优先通过图片顺序控制封面
- 发布后必须截图双校验：
  - 编辑区缩略图
  - 右侧封面/笔记预览

若显示“更新成功”但封面未变，按 SOP 重试，不要直接假定成功。

## 7) 发布后必须回填

每个平台至少回填：
- 发布状态（成功/失败/审核中）
- 链接或笔记ID
- 截图路径
- 首小时指标（曝光/点赞/评论/收藏/转发）

并将结果归档到：
- `knowledge/daily/YYYY-MM-DD/`
- `memory/YYYY-MM-DD.md`

## 8) 异常处理

- 元素失效/超时：重新 snapshot 后重试
- 上传成功但展示未变化：以页面视觉结果为准，不以提示文案为准
- 平台波动：先保留发布包，等待用户决定“重试/延后/撤回”

## 9) 输出规范（每次执行后）

固定输出四段：
1. 本次发布平台与结果
2. 审核中/失败项
3. 截图与证据路径
4. 下一步动作建议

## 10) 绝对边界

- 未经用户确认，不执行发布动作
- 不伪造发布结果、截图或平台回执
- 不把“待核实”信息写成确定事实
