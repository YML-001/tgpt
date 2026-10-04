# 问卷调查系统 — 智慧学工设计系统

> 基于 **学工-学生PC端** 设计规范，采用中南主色体系（OPPOSans 字体），
> 为问卷调查产品量身定制的完整设计规范。

---

## 1. 设计风格定位

| 属性 | 值 |
|------|-----|
| **风格类型** | 智慧学工管理平台 (Education SaaS) |
| **设计关键词** | 清新蓝色、白底卡片、数据表格、表单筛选、轻量化操作 |
| **适用场景** | 问卷管理、模板库、统计分析、学生事务 |
| **参考源** | `学工-学生PC端` Figma 文件 |
| **字体** | OPPOSans |
| **无障碍** | ✓ WCAG AA |

### 设计原则

1. **清晰专业** — 以蓝色系为主色调，传达教育行业的信任感
2. **层级清晰** — 通过颜色、字重、间距建立视觉层次
3. **操作可达** — 所有交互元素符合 44px 最小触摸目标
4. **一致性** — 统一的圆角、阴影、间距规范贯穿全局

---

## 2. 色彩系统

> 对齐《学工系统 UI 规范》参考文件 22 个官方色彩变量。

### 2.1 主色板

| 角色 | 色值 | 变量名 | 用途 |
|------|------|--------|------|
| **主题色** | `#3087CC` | 主题色 | 品牌色、主要按钮、活动标签、链接 |
| **主题色 Light** | `#E3F1F9` | 次背景Color | 选中态背景、表头、标签页 |
| **主题色 Dark** | `#006DAD` | — | 按下态、深色强调 |
| **品牌红** | `#DF2027` | 品牌红 | 品牌辅色、错误提示 |
| **浅蓝 6** | `#9CBFDA` | 浅蓝6 | 辅助背景、图表配色 |
| **浅蓝 7** | `#B0CEE4` | 浅蓝7 | 辅助背景、图表配色 |
| **浅蓝 8** | `#D6EAF9` | 浅蓝8 | 辅助背景、图表配色 |

### 2.2 文字色阶

| 角色 | 色值 | 变量名 | 用途 |
|------|------|--------|------|
| **字体黑** | `#3C444F` | 字体黑 | 一级标题、正文强调 |
| **常规文字** | `#696F7D` | 常规文字 | 二级标题、常规段落 |
| **次要文字** | `#9096A2` | 次要文字 | 辅助说明、日期、meta |
| **输入框字** | `#ABB0BA` | 输入框字 | 占位符 placeholder |
| **边框颜色** | `#C8CAD1` | 边框颜色 | 输入框/卡片/表格边框 |
| **背景色** | `#ffffff` | 背景色 | 页面背景、禁用态填充 |

### 2.3 状态语义色（严格遵循规范）

每种状态色都配有文字色、背景色、边框色三个变量：

| 状态 | 文字色 | 背景色 | 边框色 |
|------|--------|--------|--------|
| **成功** | `#1BB975` (成功提示) | `#E8FCF4` (背景颜色成功) | `#A7F3D0` (成功边框Color) |
| **警告** | `#F29100` (警告提示) | `#FFF5E5` (背景颜色警告) | `#FFE0B3` (边框颜色警告) |
| **错误** | `#DF2027` (错误提示) | `#FCE8EA` (背景颜色错误) | `#F6BCBE` (边框颜色错误) |
| **失效** | `#ABB0BA` | `#F1F2F3` | `#C8CAD1` |

### 2.4 数据可视化色板

用于统计图表中区分不同数据系列：

| 序号 | 色值 | 名称 |
|------|------|------|
| 1 | `#3087CC` | 主题色（主数据） |
| 2 | `#9CBFDA` | 浅蓝 6 |
| 3 | `#1BB975` | 成功绿 |
| 4 | `#F29100` | 警告橙 |
| 5 | `#DF2027` | 品牌红 |
| 6 | `#006DAD` | 深蓝 |
| 7 | `#D6EAF9` | 浅蓝 8 |
| 8 | `#9096A2` | 次要灰 |

### 2.5 色彩变量 Token 索引（Figma）

在 Figma 文件中访问方式：`figma.variables.getLocalVariableCollectionsAsync()` → Collection `Colors`

```
主题色 → #3087CC
品牌红 → #DF2027
字体黑 → #3C444F
常规文字 → #696F7D
次要文字 → #9096A2
输入框字 → #ABB0BA
边框颜色 → #C8CAD1
背景色 →rgb(255, 255, 255)

成功提示 → #1BB975
警告提示 → #F29100
错误提示 → #DF2027
背景颜色成功 → #E8FCF4
背景颜色警告 → #FFF5E5
背景颜色错误 → #FCE8EA
成功边框Color → #A7F3D0
边框颜色警告 → #FFE0B3
边框颜色错误 → #F6BCBE

浅蓝 6 → #9CBFDA
浅蓝 7 → #B0CEE4
浅蓝 8 → #D6EAF9
```

### 2.4 数据可视化色板

用于统计图表中区分不同数据系列：

| 序号 | 色值 | 名称 |
|------|------|------|
| 1 | `#3087CC` | 中南蓝（主数据） |
| 2 | `#5BA8DE` | 浅蓝 |
| 3 | `#1EC997` | 翠绿 |
| 4 | `#FF9800` | 琥珀 |
| 5 | `#F43F51` | 珊瑚红 |
| 6 | `#006DAD` | 深蓝 |
| 7 | `#BADEF3` | 雾蓝 |
| 8 | `#627079` | 灰蓝 |

---

## 3. 字体系统

### 3.1 字体家族

| 角色 | 字体 | 字重 | 来源 |
|------|------|------|------|
| **品牌字体** | `OPPOSans` | Regular / Medium / Bold | 学工系统统一字体 |
| **系统降级** | `-apple-system, "PingFang SC", "Microsoft YaHei", sans-serif` | — | 未安装 OPPOSans 时降级 |

### 3.2 字号规范（对齐学工系统规范）

> 规范文件提供了完整的中英文双向字号体系。

#### 中文字号

| 级别 | 样式名 | 大小 | 字重 | 用途 |
|------|--------|------|------|------|
| **一级文字** | 一级文字 | 24px | Bold | 页面主标题、banner 数字 |
| **二级文字** | 二级文字 | 18px | Bold | 区块标题、卡片标题 |
| **次要文字** | 次要文字 | 16px | Regular | 正文、表单输入、按钮文字 |
| **辅助文字** | 辅助文字 | 14px | Regular | 辅助说明、meta、表格内容 |
| **小字** | — | 12px | Regular | 标签、badge、时间戳 |

#### 英文字号（Bold 字重更大）

| 级别 | 样式名 | 大小 | 字重 | 用途 |
|------|--------|------|------|------|
| **一级英文** | 一级英文 | 30px | Bold | 英文大标题、数字强调 |
| **二级英文** | 二级英文 | 18px | Bold | 英文小标题 |
| **三级英文** | 三级英文 | 16px | Regular | 英文正文 |
| **四级英文** | 四级英文 | 14px | Regular | 英文辅助文字 |

### 3.3 字体引用

```css
/* OPPOSans 需要本地安装或从 CDN 引入 */
@font-face {
  font-family: 'OPPOSans';
  src: url('OPPOSans-Regular.woff2') format('woff2');
  font-weight: 400; font-style: normal; font-display: swap;
}
@font-face {
  font-family: 'OPPOSans';
  src: url('OPPOSans-Medium.woff2') format('woff2');
  font-weight: 500; font-style: normal; font-display: swap;
}
@font-face {
  font-family: 'OPPOSans';
  src: url('OPPOSans-Bold.woff2') format('woff2');
  font-weight: 700; font-style: normal; font-display: swap;
}
```

---

## 4. 间距系统

基于 4px 基准网格：

| Token | 值 | 用途 |
|-------|-----|------|
| `spacing-xs` | 4px | 图标与文字间距 |
| `spacing-sm` | 8px | 紧凑元素间距、pill 间距 |
| `spacing-md` | 12px | 卡片内部间距、列表项间距 |
| `spacing-lg` | 16px | 页面边距、区域间距 |
| `spacing-xl` | 20px | 区块分割间距 |
| `spacing-xxl` | 24px | 大区域分割 |

---

## 5. 圆角系统

| Token | 值 | 用途 |
|-------|-----|------|
| `radius-xs` | 3px | Checkbox、小标签 |
| `radius-sm` | 4px | Tab 标签、inline badge |
| `radius-md` | 8px | 卡片、输入框、按钮（学工统一 8px） |
| `radius-lg` | 8px | 弹窗、面板（与 md 一致） |
| `radius-xl` | 12px | Action Sheet 顶部 |
| `radius-pill` | 20px | 分类标签 pill |
| `radius-full` | 50% | 圆形头像、状态点 |

---

## 6. 阴影系统

| 级别 | 值 | 用途 |
|------|-----|------|
| **Shadow SM** | `0 1px 3px rgba(0,0,0,0.06)` | 卡片默认阴影 |
| **Shadow MD** | `0 2px 8px rgba(0,0,0,0.04)` | 模板卡片阴影 |
| **Shadow LG** | `0 4px 12px rgba(0,0,0,0.08)` | 浮动元素、弹窗 |
| **Shadow Top** | `0 -1px 4px rgba(0,0,0,0.06)` | 底部固定栏上方阴影 |

---

## 7. 图标系统

### 7.1 图标库

统一采用 **Hugeicons** 开源图标库（4000+ 图标），Figma 源文件：
[3800+ Free Icons — Open Source Figma Icon Library](https://www.figma.com/design/to08p95mHkZZJxwkzcMZfT)

| 规范 | 值 |
|------|-----|
| **图标库** | Hugeicons (Figma Community) |
| **图标总数** | 4,018 个 |
| **风格** | Line (线性描边) |
| **原始 viewBox** | 24×24 |
| **原始描边** | 1.5px，圆角端点 |
| **默认使用大小** | 14px（按钮内） / 16px（列表项） / 20px（页头 / 大图标） |
| **颜色规则** | 继承父元素文字颜色（通过 `stroke` 设置） |
| **触摸区域** | 最小 44×44px（图标 + padding） |

### 7.2 图标分类索引（60 大类）

| 分类 | 数量 | 分类 | 数量 |
|------|------|------|------|
| Edit Formatting | 545 | Note and Task | 25 |
| Business and finance | 492 | Search | 31 |
| Hand Gestures | 333 | Presentation | 31 |
| Communications | 313 | Geometric Shapes | 31 |
| Arrows (sharp) | 307 | Git | 21 |
| Arrows (Round) | 307 | Home | 17 |
| Mathematics | 297 | Login and Logout | 34 |
| Brand Logo | 270 | Download and Upload | 41 |
| E-Commerce | 265 | Dashboard | 43 |
| Devices | 255 | Award Reward | 53 |
| Files Folders | 251 | Add Remove Delete | 55 |
| Game & Sports | 213 | Filter Sorting | 55 |
| Location & Maps | 199 | Alert Notification | 55 |
| Weather | 193 | More Menu | 53 |
| Food & Drinks | 185 | Link Unlink | 56 |
| Education | 176 | Space Galaxy | 55 |
| Mouse & Courses | 160 | Legal | 75 |
| Energy | 156 | Kitchen | 77 |
| Crypto | 149 | Users | 86 |
| Furniture | 145 | Artificial Intelligence | 87 |
| Transportation | 143 | Islamic | 89 |
| Medical | 138 | Gym & Fitness | 91 |
| Image, Camera & Video | 135 | Setting | 95 |
| Building, Landmark & Places | 131 | Bookmark Favorite | 99 |
| Wifi & Signal | 131 | Date and time | 111 |
| Security | 128 | Animation | 71 |
| Programming language | 125 | Layout & Boarders | 67 |
| Cloth & Accessories | 124 | Science & Technology | 45 |
| Hierarchy | 121 | Check Validation | 84 |
| Smiley & Emojis | 116 | Media | 115 |

### 7.3 常用图标速查表

按系统高频场景预选的图标 `key`（可通过 `figma.importComponentByKeyAsync(key)` 引入）：

#### 操作类

| 图标名 | 用途 | Component Key |
|--------|------|---------------|
| `play` | 启动、使用模板 | `4795a247c0f674492aee52126525e39d75fbd666` |
| `eye` | 预览、查看 | `6fcb4122347cd48bf01204586b985fe2f33d90c5` |
| `edit-02` | 编辑 | `ae74042acc8b10ab596f789e96292033cb8939cf` |
| `delete-02` | 删除 | `58fd94318823149700e0c06e87a3e2e5a770cb05` |
| `copy-01` | 复制 | `952279ab144918d9935b9103395d0fca877d3cb4` |
| `share-01` | 分享 | `9b1c4f1a5904e66e15cb7aaec42d287d5f8c4d7a` |
| `download-01` | 下载 / 导出 | `6781adcfaba28f6d29d28e46b38b7a634d159286` |
| `upload-01` | 上传 | `09b77a560d8e2b6d22bd3776beb3ed5b1abe919c` |
| `refresh` | 刷新 | `cf90e96cd4d2c3189cb79661fee48f6c86f775e5` |
| `reload` | 重新加载 | `a88d55b81d26d45198406820ee66ba4eabd69e28` |

#### 状态类

| 图标名 | 用途 | Component Key |
|--------|------|---------------|
| `tick-01` | 成功 / 确认 | `b0da0e33629e22be9685fb671e069f1713ed75c3` |
| `tick-02` | 已完成 | `95881b8aed1a9f3e3a702f61484fce69e9eb01b1` |
| `checkmark-circle-02` | 完成徽章 | `d79c38740d0975c33749d10775ef868cda1da60c` |
| `alert-01` | 警告提醒 | `bad8ca4a0b6a36b49d9472f00a6ed50a0636c3f7` |
| `notification-01` | 通知 | `71b6254221bd463c82f26b0a5e707a05ec48c383` |
| `question` | 帮助 / 疑问 | `72cb398790e47c2adf40de11b8318eabb246c121` |
| `lock` | 已锁定 / 隐私 | `d682ef5a7f0e590db8e82dc8c3b0e4509c3df9c3` |

#### 数据可视化

| 图标名 | 用途 | Component Key |
|--------|------|---------------|
| `pie-chart` | 单选题分布统计 | `633b2994eb72b0a587c9f8378a6f0f10a8d13578` |
| `analytics-01` | 分析仪表盘 | `5c36fa75204e8395454518c1370c49273dec8eea` |
| `grid-view` | 卡片视图切换 | `80a913e93b7b2e318854f9d4408164a62121f535` |
| `list-view` | 列表视图切换 | `a1739a3119d6d9e2eca421b89783f275f62b5131` |
| `filter` | 筛选 | `b32ee441bde31a4cb628ce9d563615cc58f27d95` |
| `search-02` | 搜索 | `ce5ceb3da1dcd4598e627291bda030a9ab96f70e` |

#### 通用类

| 图标名 | 用途 | Component Key |
|--------|------|---------------|
| `home-01` | 首页 | `e3cc23e2ced88c6ddc237f54e1855a87639c90bf` |
| `user-circle` | 用户 / 个人中心 | `807c74a812a0405372a7427c20d4cacf987c6fb0` |
| `calendar-02` | 日期 | `9ef822226bcc97734d042bd6247db30b83ace73e` |
| `clock-01` | 时间 | `9e1cc9aa23ff0812f8cdabd27bdbf2b01aa56154` |
| `mail-01` | 邮件通知 | `aaa97f4698e16623e152f643345eb378f767b97d` |
| `message-01` | 消息会话 | `32e2add53fd78e8249d78b541190e811407dfed4` |
| `link-01` | 链接分享 | `2d9e582985a7ad00bbae5e62a30bcb510a431ac6` |
| `folder-01` | 文件夹 | `bd7ebe1b016d9f02f72f40c01bee6c180faf40e0` |
| `file-01` | 文档 | `923eb058a8e78ff51de16f09c42a7c1fbb9d58f3` |
| `image-01` | 图片 | `d33c171f81d7b8f86cc95f8a0faa8592449de518` |
| `camera-01` | 拍照上传 | `49c9ff7ef96561cd0ffdaff9acd94a59eee7825f` |
| `menu-01` | 菜单汉堡 | `bbbed7d2593bd506e781663ba53e15b5084e92ea` |
| `more-vertical` | 更多操作 | `6d331a285f02621e202d4bb8d9fa8d95d0a6894d` |
| `pin` | 置顶 | `39c7121db753dbd2dac1b07a0b77b092dd915c01` |
| `star` | 收藏 / 评分 | `9723bcd4f99b7c679be8416a05e3936c1dc6fa1b` |
| `bookmark-01` | 书签 | `23cb58d4b0df35fc844951f6870a09648a588d02` |
| `login-01` | 登录 | `1ecefef2448b35e2b9a3866c8b76b244163dcdf1` |
| `logout-01` | 退出 | `259b8067980e3d5df6bc4fba347a36fde00493cb` |

### 7.4 使用规范

#### 引入方式

```js
// Figma Plugin API 引入（推荐）
const icon = await figma.importComponentByKeyAsync(
  '4795a247c0f674492aee52126525e39d75fbd666'  // play
);
const instance = icon.createInstance();

// 若组件未发布到团队库，使用 exportAsync + createNodeFromSvg
const svgString = await sourceNode.exportAsync({ format: 'SVG_STRING' });
const node = figma.createNodeFromSvg(svgString);
node.rescale(14 / 24);  // 24→14 缩放
```

#### 颜色重载

所有原始图标 stroke 为 `#141B34`，使用时需遍历替换为目标色：

```js
node.findAll(n => {
  if ('strokes' in n && n.strokes.length > 0) {
    n.strokes = [{ type: 'SOLID', color: targetColor }];
  }
  return false;
});
```

#### 尺寸场景

| 使用场景 | 尺寸 | 缩放系数 |
|---------|------|---------|
| 按钮内图标 | 14×14 | `14/24 ≈ 0.583` |
| 列表项图标 | 16×16 | `16/24 ≈ 0.667` |
| 分类导航 / 表单前缀 | 16×16 | `16/24 ≈ 0.667` |
| 页头 / Tab Bar | 20×20 | `20/24 ≈ 0.833` |
| 大号装饰图标 | 24×24 | `1.0` (原始) |
| 卡片头图标容器 | 48×48 渐变容器内填 24×24 图标 | `1.0` |

### 7.5 禁止事项

- **禁止使用 Emoji** 作为界面图标（如 🔍 🎨 ✅）
- **禁止混用多个图标库**（不要混用 Remix / Lucide / Heroicons）
- **禁止修改原始 viewBox**（保持 24×24，通过 `rescale` 调整尺寸）
- **禁止填充线性图标**（图标为 stroke 线性，不要改成 fill）
- **禁止改动描边粗细比例**（缩放时保持描边粗细与尺寸成比例）

---

## 8. 组件规范

> 完整对齐学工系统 UI 规范的 **132 个标准组件**，标注 Figma 变量名称、精确尺寸与状态。

### 8.1 按钮 Button

| 变体 | Figma 名称 | 尺寸 | 背景 | 文字 | 边框 |
|------|-----------|------|------|------|------|
| **一级按钮/主** | `一级按钮/主` | 104×40 | `#3087CC` | `#FFFFFF` 16px | — |
| **一级按钮/副** | `一级按钮/副` | 104×40 | `#FFFFFF` | `#3087CC` 16px | 1px `#3087CC` |
| **一级按钮/主/图标** | `一级按钮/主/图标` | 126×40 | `#3087CC` | `#FFFFFF` + 16px 前置图标 | — |
| **一级按钮/副/图标** | `一级按钮/副/图标` | 126×40 | `#FFFFFF` | `#3087CC` + 16px 前置图标 | 1px `#3087CC` |

- 圆角：8px
- Padding：水平 16px，垂直 10px
- 悬停：主按钮 `#006DAD`；副按钮背景 `#E3F1F9`
- 禁用：透明度 0.5

### 8.2 文本输入框 Input

三种状态：`待输入` / `输入中` / `禁止输入`，尺寸 `280×92`（含 label + input + hint 三层）。

| 状态 | 边框 | 背景 | 文字色 |
|------|------|------|--------|
| **待输入** | `#C8CAD1` | `#FFFFFF` | 占位符 `#ABB0BA` |
| **输入中** (Focus) | `#3087CC` 2px | `#FFFFFF` | `#3C444F` |
| **禁止输入** | `#C8CAD1` | `#F1F2F3` | `#9096A2` |

输入区高度 40px，内 padding 12px，圆角 4px。

### 8.3 选择器 Selector

| 变体 | Figma 名称 | 尺寸 | 特征 |
|------|-----------|------|------|
| **下拉** | `选择器/下拉` | 240×40 | 右侧 chevron-down 图标 |
| **输入** | `选择器/输入` | 220×40 | 可输入 + 清除按钮 |
| **时间** | `选择器/时间` | 220×40 | 右侧 clock 图标 |
| **日期** | `选择器/日期` | 280×40 | 右侧 calendar 图标 + 起止区间 |
| **日历** | `选择器/日历` | 220×40 | 单日期选择 |

### 8.4 勾选与开关

#### 多选框 Checkbox

- Figma：`选择器/多选框` 438×32
- 尺寸：16×16 圆角 2px
- 未选：`#C8CAD1` 边框
- 已选：`#3087CC` 填充 + 白色勾

#### 单选框 Radio

- Figma：`选择器/单选框` 426×32
- 尺寸：16×16 圆形
- 未选：`#C8CAD1` 边框
- 已选：`#3087CC` 边框 + 内圆点

#### Switch 开关

| 变体 | Figma 名称 | 尺寸 | 背景 | 圆点位置 |
|------|-----------|------|------|---------|
| **开** | `选择器/开关/开` | 94×24 | `#3087CC` | 右 |
| **关** | `选择器/开关/关` | 94×24 | `#C8CAD1` | 左 |
| **开/禁用** | `选择器/开关/开/禁用` | 108×24 | `#3087CC` @ 0.4 | 右 + 不可点 |
| **关/禁用** | `选择器/开关/关/禁用` | 108×24 | `#C8CAD1` @ 0.4 | 左 + 不可点 |

### 8.5 标签 Tag

尺寸统一 `70×28`，圆角 4px，字号 12px Medium。

| 类型 | Figma 名称 | 背景 | 文字 | 边框 |
|------|-----------|------|------|------|
| **已完成** | `组件/标签已完成` | `#E8FCF4` | `#1BB975` | `#A7F3D0` |
| **审核中** | `组件/标签已审核中` | `#FFF5E5` | `#F29100` | `#FFE0B3` |
| **失败** | `组件/标签失败` | `#FCE8EA` | `#DF2027` | `#F6BCBE` |
| **失效** | `组件/标签失效` | `#F1F2F3` | `#9096A2` | `#C8CAD1` |

### 8.6 状态插图 Status

尺寸 `72×72` 大尺寸圆形状态图标（用于空状态、结果页）：

| 状态 | Figma 名称 | 背景 | 图标色 |
|------|-----------|------|--------|
| **完成** | `状态-完成` | `#E8FCF4` | `#1BB975` ✓ |
| **警告** | `状态-警告` | `#FFF5E5` | `#F29100` ⚠ |
| **失败** | `状态-失败` | `#FCE8EA` | `#DF2027` × |
| **失效** | `状态-失效` | `#F1F2F3` | `#9096A2` — |

### 8.7 进度条 Progress

| 变体 | Figma 名称 | 尺寸 | 填充色 |
|------|-----------|------|--------|
| **默认/有数据** | `进度条/默认/有数据` | 347×24 | `#3087CC` + 右侧百分比文字 |
| **默认/无数据** | `进度条/默认/无数据` | 320×20 | `#3087CC` |
| **成功** | `进度条/成功/...` | 同上 | `#1BB975` |
| **警告** | `进度条/警告/无数据` | 320×20 | `#F29100` |
| **错误** | `进度条/错误/无数据` | 320×20 | `#DF2027` |

轨道色 `#F1F2F3`，圆角 10px（完全圆）。

### 8.8 提示 Toast / Tooltip

#### 纯文字 Toast（380×48）

| 类型 | Figma 名称 | 边框色 | 背景色 | 文字色 |
|------|-----------|--------|--------|--------|
| **成功** | `提示/纯文字提示/成功` | `#A7F3D0` | `#E8FCF4` | `#1BB975` |
| **警告** | `提示/纯文字提示/警告` | `#FFE0B3` | `#FFF5E5` | `#F29100` |
| **错误** | `提示/纯文字提示/错误` | `#F6BCBE` | `#FCE8EA` | `#DF2027` |
| **失效** | `提示/纯文字提示/失效` | `#C8CAD1` | `#F1F2F3` | `#9096A2` |

#### 带确认按钮 Popover（256×96）

4 个方向：`上 / 下 / 左 / 右`，带三角指针，内含消息文字 + 确认/取消按钮。

#### 图标文字提示 Tooltip（108×42）

4 方向：`上 / 下 / 左 / 右`，深色背景 `#3C444F`，白字 14px，三角指针。

#### 带辅助文字 Notification（400×120）

4 种状态：成功/警告/失败/失效，含主标题 + 副文字 + 关闭按钮。

### 8.9 卡片 Card

| 属性 | 值 |
|------|-----|
| 背景 | `#FFFFFF` |
| 圆角 | 8px |
| 边框 | 1px `#C8CAD1`（可选） |
| 内边距 | 20-24px |
| 阴影 | Shadow SM (`0 1px 3px rgba(0,0,0,0.06)`) |
| 间距 | 卡片之间 16-20px |

### 8.10 日历 Calendar

每个日期格 `103×94`，共 6 种状态组合：

| Figma 名称 | 状态 |
|-----------|------|
| `日历/默认` | 可选普通日 |
| `日历/默认/事件` | 可选，带事件点 |
| `日历/默认/选中` | 当前选中 |
| `日历/默认/选中/事件` | 当前选中且有事件 |
| `日历/失效` | 不可选 |
| `日历/失效/事件` | 不可选但有事件标记 |

### 8.11 文件类型图标 Filetypes

Component Set：`Attachment / Filetypes` 共 9 种：
`PNG / JPG / GIF / PDF / TXT / XLS / word / MOV / MP3`

统一 24×24，带文件格式文字标识。

### 8.12 弹框 Modal

| 类型 | 尺寸 | 用途 |
|------|------|------|
| **登录弹框 (小)** | 400×300 | 简单登录/确认 |
| **登录弹框 (大)** | 800×600 | 完整表单、分步 |
| **填写弹框** | 400×300 | 快速填写表单 |

### 8.13 头像 Avatar

Figma：`默认头像` 100×100 圆形，占位背景 `#F1F2F3`，可替换为用户图片。

### 8.14 底部 Tab Bar（移动端）

| 属性 | 值 |
|------|-----|
| 高度 | 60px (含安全区 83px) |
| 背景 | `#FFFFFF` |
| 顶部边框 | `1px solid #E3F1F9` |
| 图标大小 | 22px |
| 文字大小 | 12px |
| 活动色 | `#3087CC` |
| 非活动色 | `#9096A2` |

---

## 9. 数据可视化规范

### 9.1 图表类型推荐

| 数据类型 | 推荐图表 | 备选 | 场景 |
|----------|---------|------|------|
| 占比分布 | 饼图/环形图 | 堆叠柱状图、Treemap | 单选题统计 |
| 分类比较 | 柱状图 | 分组柱状图 | 多选题统计 |
| 百分比 | 华夫饼图 | 100% 堆叠条 | 完成率展示 |
| 目标达成 | 仪表盘/子弹图 | 温度计 | KPI 目标 |
| 评分分布 | 星级 + 柱状图 | 径向图 | 评分题统计 |
| 矩阵数据 | 热力图/表格 | 分组柱状图 | 矩阵题统计 |
| 趋势变化 | 折线图 | 面积图 | 填写趋势 |

### 9.2 图表交互

- **Hover** — 显示 Tooltip 详细数据
- **点击** — 图表缩放或钻取到详情
- **筛选** — 平滑过渡动画 (300ms ease)
- **加载** — 骨架屏或 Spinner

### 9.3 图表颜色规则

- 最多使用 **5-6 种**颜色
- 大数据优先显示（降序排列）
- 对比度足够（相邻色差值 > 30%）
- 总是添加图例和数值标签

---

## 10. 交互与动效

### 10.1 过渡时间

| 类型 | 时长 | 曲线 |
|------|------|------|
| 颜色变化 | 150ms | ease |
| 布局切换 | 200ms | ease-in-out |
| 展开/折叠 | 300ms | ease |
| 页面切换 | 250ms | ease-in-out |
| 弹窗出现 | 300ms | ease-out |

### 10.2 hover/pressed 状态

| 元素 | Hover | Pressed |
|------|-------|---------|
| Primary Button | `opacity: 0.9` | `background: #3730A3` |
| Card | `shadow-lg` | `scale: 0.98` |
| List Item | `background: #F8FAFC` | `background: #F1F5F9` |
| Icon Button | `color: #4F46E5` | `opacity: 0.7` |

### 10.3 加载状态

| 场景 | 方案 |
|------|------|
| 页面首次加载 | 骨架屏 (animate-pulse) |
| 数据刷新 | Inline spinner |
| 按钮提交 | 按钮内 spinner + 禁用 |
| 图表加载 | 灰色占位图表轮廓 |

---

## 11. 页面布局规范

### 11.1 全局结构

```
┌─────────────────────────┐
│      Status Bar (44px)  │
├─────────────────────────┤
│      Header (44-56px)   │
├─────────────────────────┤
│      Tabs / Pills       │
├─────────────────────────┤
│                         │
│      Content Area       │
│      (scrollable)       │
│                         │
├─────────────────────────┤
│   Bottom Bar (60-83px)  │
└─────────────────────────┘
```

### 11.2 关键尺寸

| 属性 | 值 |
|------|-----|
| 设备宽度 | 375px (iPhone SE/8) |
| 页面左右边距 | 16px |
| Header 高度 | 44px |
| Tab Bar 高度 | 60px (含底部安全区约 83px) |
| 内容区起始 | Header + Tabs 高度之后 |
| 底部固定栏 | 高度 44px + 下内边距 24px (安全区) |

### 11.3 移动端特别注意

- 所有交互元素最小 44x44px 触摸面积
- 底部操作栏 padding-bottom 需考虑 Home Indicator
- 固定 Header 时内容区需留出对应 padding-top
- 横向滚动使用 `-webkit-overflow-scrolling: touch`

---

## 12. 无障碍清单

- [ ] 文字对比度 ≥ 4.5:1（正文）/ ≥ 3:1（大字）
- [ ] 所有图片有 alt 属性
- [ ] 表单控件有关联 label
- [ ] 颜色不是唯一的信息传达方式
- [ ] 聚焦状态清晰可见 (focus-visible)
- [ ] 尊重 `prefers-reduced-motion`
- [ ] 输入框使用正确的 `inputmode`
- [ ] 字体使用 `font-display: swap`

---

## 13. 反模式（避免）

| 反模式 | 为什么 | 正确做法 |
|--------|--------|----------|
| 华丽装饰设计 | 数据看板需要信息密度 | 保持简洁，突出数据 |
| 缺少筛选功能 | 用户需要聚焦特定数据 | 提供分类标签和筛选器 |
| 复杂引导流程 | 用户想快速获取数据 | 直达核心功能 |
| 拥挤的布局 | 虽然数据密度高，但不等于塞满 | 合理的间距和留白 |
| Emoji 作图标 | 不够专业，难以保持一致 | 使用 SVG 图标库 |
| 使用 scale 变换的 hover | 会导致布局偏移 | 使用颜色/透明度变化 |

---

## 14. CSS 变量速查

```css
:root {
  /* === 中南主色体系 === */
  --中南主色: #3087CC;
  --color-primary: #3087CC;
  --color-primary-light: #E3F1F9;
  --color-primary-dark: #006DAD;
  --color-primary-border: #BADEF3;

  /* === 语义色 === */
  --color-success: #1EC997;
  --color-success-light: #E6F9F2;
  --color-warning: #FF9800;
  --color-warning-light: #FFF8E6;
  --color-danger: #F43F51;
  --color-danger-light: #FEF0F1;

  /* === 中性色 === */
  --color-text-primary: #1E293B;
  --color-text-secondary: #627079;  /* 次字体Color */
  --color-text-muted: #94A3B8;
  --color-border: #BADEF3;
  --color-border-light: #E3F1F9;
  --color-bg-page: #FAFAFA;  /* 浅色背景通用 */
  --color-bg-card: #FFFFFF;
  --color-bg-input: #FFFFFF;

  /* === 字体 === */
  --font-family: 'OPPOSans', -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-size-h1: 20px;   /* 一级字体样式20 Bold */
  --font-size-h2: 16px;   /* 二级字体M16 Medium */
  --font-size-body: 14px;  /* 三级字体样式R14 Regular */
  --font-size-caption: 12px;
  --font-size-tiny: 10px;

  /* === 间距 === */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 12px;
  --spacing-lg: 16px;
  --spacing-xl: 20px;
  --spacing-xxl: 24px;

  /* === 圆角 === */
  --radius-xs: 3px;   /* Checkbox */
  --radius-sm: 4px;   /* Tab, 小标签 */
  --radius-md: 8px;   /* 卡片, 输入框 (学工统一 8px) */
  --radius-lg: 8px;   /* 与 md 一致 */
  --radius-pill: 20px;

  /* === 阴影 === */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 2px 8px rgba(0, 0, 0, 0.04);
  --shadow-lg: 0 4px 12px rgba(0, 0, 0, 0.08);
  --shadow-top: 0 -1px 4px rgba(0, 0, 0, 0.06);

  /* === 布局 === */
  --header-height: 44px;
  --tab-bar-height: 60px;
  --input-height: 44px;
  --table-row-height: 48px;
  --table-header-bg: #E3F1F9;

  /* === 过渡 === */
  --transition-fast: 150ms ease;
  --transition-normal: 200ms ease-in-out;
  --transition-slow: 300ms ease;
}
```

---

## 15. 交付前检查清单

### 视觉质量
- [ ] 无 Emoji 用作图标（全部使用 Remix Icon SVG）
- [ ] 所有图标来自统一图标库
- [ ] Hover 状态不导致布局偏移
- [ ] 使用主题色变量，不硬编码颜色

### 交互
- [ ] 所有可点击元素添加 `cursor: pointer`
- [ ] Hover 状态有明确视觉反馈
- [ ] 过渡动画在 150-300ms 之间
- [ ] 键盘导航的 Focus 状态可见

### 响应式
- [ ] 375px (iPhone SE) 正常展示
- [ ] 没有横向滚动溢出
- [ ] 固定元素不遮挡内容
- [ ] 底部安全区正确处理

### 数据展示
- [ ] 图表最多 5-6 种颜色
- [ ] 数值标签清晰可读
- [ ] 加载状态有骨架屏
- [ ] 空状态有友好提示
