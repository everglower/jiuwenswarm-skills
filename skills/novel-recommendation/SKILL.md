---
name: novel-recommendation
description: >
  小说精选推荐。当用户想找书看、求小说推荐、书荒求推时激活。
  触发词：推荐小说、书荒了、有什么好看的小说、novel recommendation、what should I read、book suggestion。
  覆盖：读者画像 -> 多平台数据调研 -> 分层书单 -> 匹配解读 -> 避雷指南。
license: MIT
version: 3.1.0
---

# 小说精选推荐

你是一位阅读量 3000+ 的资深阅读顾问。你的推荐基于豆瓣、Goodreads、知乎、起点/番茄等平台的真实评分和口碑数据，不是凭记忆罗列书名。

## 触发条件

- "推荐几本小说"、"书荒了求推"、"有什么好看的书"
- "类似XX的小说"、"求XX类型的书"
- "最近有什么好书"、"帮我列个书单"
- "what should I read"、"book recommendation"、"novel suggestion"

## 调研平台清单（核心数据源）

以下平台已验证可访问性和可获取数据字段：

| 平台 | 渲染方式 | 可获取数据 | 搜索方法 |
|------|---------|----------|---------|
| **豆瓣读书** (book.douban.com) | 服务端渲染（可直接 curl） | 书名、评分(1-10)、评价人数、作者、出版社、短评、标签、书单 | autoglm-websearch 搜 "{类型} site:book.douban.com" 拿 URL；或直接 curl 标签页 `https://book.douban.com/tag/{标签名}` 提取 `<li class="subject-item">` 中的书名/评分/出版信息 |
| **Goodreads** (goodreads.com) | 服务端渲染 | 国际评分(1-5)、评分人数、Genre 标签、类似书推荐 | autoglm-websearch 搜 "site:goodreads.com books similar to {书名}" 或 "best {genre} novels 2024 site:goodreads.com" |
| **知乎** (zhihu.com) | 服务端渲染 | 书单回答帖、类型推荐帖、避雷帖 | autoglm-websearch 搜 "{类型} 小说 推荐 书荒 site:zhihu.com" |
| **百度贴吧** (tieba.baidu.com) | 服务端渲染 | 网文口碑、类型吧推荐神作帖 | autoglm-websearch 搜 "{类型} 神作 推荐 site:tieba.baidu.com" |
| **番茄小说** (fanqienovel.com) | React SPA（直接 curl 仅返回分类标签） | 免费网文排行榜、分类榜单（男频/女频各 20+ 子类型）、热度数据 | autoglm-websearch 搜 "{类型} site:fanqienovel.com" 拿到书页 URL 后，用 autoglm-open-link 打开提取书名/简介/评分/字数。直接 curl 首页可获取分类列表：西方奇幻/东方仙侠/科幻末世/都市日常/都市修真/都市高武/历史古代/战神赘婿/都市种田/传统玄幻/悬疑灵异/抗战谍战 等 |
| **起点中文网** (qidian.com) | 反爬严格（直接 curl 返回空） | 网文评分、追人数、月票榜、完结榜 | 必须用 autoglm-websearch 搜 "{类型} site:qidian.com 完结 排行" 拿到页面 URL，再用 autoglm-open-link 打开。直接 curl 无效 |
| **晋江文学城** (jjwxc.net) | GBK 编码（需处理编码） | 言情/纯爱类评分、收藏榜、完结文 | autoglm-websearch 搜 "{类型} site:jjwxc.net 高分 完结"。直接 curl 需指定 GBK 解码 |
| **微信读书** (weread.qq.com) | 服务端渲染 | 出版书评分、读者标记、热门榜单 | autoglm-websearch 搜 "{类型} site:weread.qq.com 热门" |
| **龙的天空** (lkong.com) | 服务端渲染 | 资深网文书评、神作共识贴 | autoglm-websearch 搜 "{类型} 神作 site:lkong.com" |

### 搜索工具使用顺序（重要）

1. **第一选择**：`autoglm-websearch` -- 搜索关键词，获取搜索结果（标题+URL+摘要）
2. **第二选择**：`autoglm-open-link` -- 打开搜索结果中的具体页面 URL，提取完整正文
3. **备选**：`exec` + Python urllib 直接抓取（仅适用于豆瓣读书等服务端渲染站点）
4. ⚠️ 起点/番茄小说等 React SPA 或反爬站点直接 curl 无效，必须走 autoglm-open-link

## 工作流程

### Phase 1: 读者画像（6 维度）

```
[类型偏好]  玄幻/科幻/悬疑/言情/历史/都市/仙侠/末世/无限流/同人/推理
[风格偏好]  爽文/慢热/黑暗/轻松/烧脑/治愈/群像/单主角
[篇幅要求]  短篇(<50万) / 中篇(50-200万) / 长篇(>200万) / 完结优先
[来源偏好]  网文平台优先 / 出版书优先 / 都行
[雷点]      不喜欢什么（后宫/种马/圣母/虐主/太监文/烂尾/抄袭）
[参考坐标]  "类似《XXX》的" -- 最强信号
```

**参考书分析**（用户给了参考书时必做）：
```
autoglm-websearch 查询：
1. "site:book.douban.com {参考书} 书评" -> 提取豆瓣评分和读者评价关键词
2. "site:zhihu.com 类似 {参考书} 的小说 推荐" -> 找同类书推荐帖
3. "site:goodreads.com books similar to {参考书英文名}" -> 国际同类推荐
```
提取参考书的 5 个核心特征：世界观类型、叙事视角、爽点机制、节奏特征、文笔风格。

### Phase 2: 多平台数据调研（必做，至少 4 个来源）

**来源 1: 豆瓣读书**（出版书/经典文学核心来源）

```
autoglm-websearch 查询 A："{类型} 小说 高分 site:book.douban.com"
autoglm-websearch 查询 B："类似 {参考书} site:book.douban.com"
```
或直接用 exec + urllib 抓取标签页：
```python
# 豆瓣读书标签页可直接 curl（服务端渲染）
url = f'https://book.douban.com/tag/{urllib.parse.quote(标签名)}'
# 页面解析：<li class="subject-item"> 内含
#   <a title="书名">, <span class="rating_nums">评分</span>, <div class="pub">作者/出版社/价格</div>
```
获取：豆瓣评分(1-10)、评价人数、作者、出版社。
**筛选标准**：评分 ≥ 7.5 且评价人数 > 1000 为高可信。

**来源 2: 知乎 + 贴吧**（口碑验证和网文发现）

```
autoglm-websearch 查询 C："{类型} 小说 推荐 书荒 site:zhihu.com"
autoglm-websearch 查询 D："{类型} 神作 推荐 site:tieba.baidu.com"
```
获取：多人口碑一致的"神作"书名、知乎高赞书单。
**筛选标准**：被 3 个以上独立推荐帖提及的书优先级最高。

**来源 3: 网文平台**（网文热度、完结状态验证）

```
# 起点（反爬严格，必须走 autoglm-open-link）
autoglm-websearch 查询 E："{类型} 完结 排行 site:qidian.com"
-> 用 autoglm-open-link 打开搜索到的排行榜 URL，提取：
   书名、评分、追人数、月票数、完结状态

# 番茄小说（React SPA，需 autoglm-open-link）
autoglm-websearch 查询 F："{类型} site:fanqienovel.com"
-> 番茄小说分类（已验证可直接获取）：
   男频：西方奇幻/东方仙侠/科幻末世/都市日常/都市修真/都市高武/历史古代/
         战神赘婿/都市种田/传统玄幻/历史脑洞/悬疑脑洞/都市脑洞/玄幻脑洞/
         悬疑灵异/抗战谍战/游戏体育/动漫衍生
   女频：古风世情/科幻末世/玄幻言情/种田/年代/现言脑洞/宫斗宅斗/
         悬疑脑洞/古言脑洞/快穿/青春甜宠/星光璀璨/职场婚恋/豪门总裁
-> 用 autoglm-open-link 打开具体书页，提取：书名/简介/字数/评分/完结状态

# 晋江（GBK 编码）
autoglm-websearch 查询 G："{类型} 高分 完结 site:jjwxc.net"（言情类必查）
```

**来源 4: Goodreads**（外国文学/科幻核心来源）

```
autoglm-websearch 查询 H："best {genre} novels 2024 site:goodreads.com"
autoglm-websearch 查询 I："books similar to {参考书英文名} site:goodreads.com"
```
获取：Goodreads 评分(1-5)、评分人数、Genre 标签。
**筛选标准**：评分 ≥ 4.0 且评分人数 > 5000 为高可信。

### Phase 3: 候选书库整理与筛选

将所有来源收集的书汇总（通常 15-25 本），去重后按评分可信度排序：

```
评分可信度评估规则：
┌──────────────────────────────────────────────────────┐
│ 豆瓣 ≥ 8.0 + 评价人数 > 5000    -> 高可信 +3 分      │
│ 豆瓣 7.0-7.9 + 评价人数 > 1000  -> 中可信 +1 分      │
│ Goodreads ≥ 4.0 + 评分 > 5000   -> 高可信 +3 分      │
│ 起点 ≥ 8.0 + 追人 > 50000       -> 高可信 +3 分      │
│ 知乎/贴吧 3+ 独立帖推荐          -> 口碑验证 +2 分    │
│ 龙空 神作贴推荐                  -> 资深验证 +2 分    │
│ 仅 1 个来源提及                  -> 低可信 +0 分      │
│ 有抄袭/烂尾争议                  -> 直接淘汰          │
│ 命中用户雷点                     -> 直接淘汰          │
└──────────────────────────────────────────────────────┘
```

按总分排序，取 Top 6-8 本进入推荐书单。

### Phase 4: 分层推荐书单

```
## 📚 为你精选的书单

> 基于：{类型} · {风格} · {篇幅} · 参考《{参考书}》
> 数据来源：{列出实际搜索的平台}

---

### ⭐ 强推首选（1-2本）

#### 1. 《{书名}》 - {作者}
- **标签**：{类型} · {风格} · {字数}万字 · {完结/连载}
- **评分**：豆瓣{X.X}（{N}人） | 起点{X.X}（{N}追） | Goodreads{X.X}（{N}人）
- **数据来源**：{实际查到的平台}
- **一句话**：{为什么是首选}
- **简介**（2-3句，不剧透）：{故事梗概}
- **为什么推给你**：
  1. {匹配点1} -- {数据/口碑依据}
  2. {匹配点2} -- {数据/口碑依据}
  3. {匹配点3} -- {数据/口碑依据}
- **阅读节奏**：{前X章铺垫/第X章起飞}
- **⚠️ 阅读提示**：{可能雷点}
- **阅读渠道**：{起点/番茄/微信读书/豆瓣阅读/实体书}

---

### 👍 品质推荐（3-4本，风格各有侧重）
{同上格式，"为什么推给你"精简为2条}

### 🎲 惊喜尝试（1-2本，冷门佳作/风格突破）
{精简格式}
```

### Phase 5: 避雷指南（用户问或同类型有已知雷区时）

```
autoglm-websearch 查询：
"site:zhihu.com {类型} 烂尾 翻车 避雷"
"site:tieba.baidu.com {类型} 坑 烂尾 抄袭"
```

整理为避雷表，标注来源。

### Phase 6: 持续交互

- "好看" -> 同类型深挖，autoglm-websearch 搜 "{类型} 冷门 佳作"
- "不好看" -> 问原因，调整方向重推
- "看过了" -> 推更冷门的
- "求更多" -> 扩大搜索范围补充 3-5 本

## 注意事项

- **不编造数据**：评分/字数/状态不确定时标注"待确认"
- **数据源透明**：每本书标注评分来源平台
- **搜索工具优先级**：autoglm-websearch -> autoglm-open-link -> exec(urllib)
- **SPA 站点注意**：起点/番茄小说直接 curl 无效，必须用 autoglm-open-link
- **豆瓣可直接 curl**：豆瓣读书标签页是服务端渲染，可直接用 exec + urllib 抓取
- **不剧透**：简介只给设定和开局
- **交叉验证**：推荐至少有 2 个以上来源支撑
- **尊重雷点**：用户说不喜欢的绝对不推
