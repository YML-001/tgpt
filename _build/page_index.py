# 原型导航页 index.html：演示入口、演示剧本、角色权限、功能清单、业务流程、审核流程、状态体系、页面目录
import lib
from lib import icon, tag, write
from data import ROLES
from styles import BASE_CSS

# ---------- 页面目录：（文件, 页面名, 图标, 说明） ----------
PC_PAGES = {
    'correspondent': [
        ('submit-news', '新闻投稿', 'file', '富文本、配图与简介选填、多附件上传、身份切换、指导老师搜索、敏感词检测'),
        ('submit-video', '视频投稿', 'video', '永久云盘链接提示、时长格式校验、视频用途、多附件上传'),
        ('submit-photo', '照片投稿', 'image', '批量上传原图、单张备注、涉及重要领导'),
        ('submit-clue', '新闻线索', 'bulb', '是否接受采访联动显示可采访时间段'),
        ('submit-success', '提交成功', 'check-circle', '按投稿身份显示下一个审核节点（学生：指导老师；教师：副书记）'),
        ('my-submissions', '我的投稿', 'inbox', 'PC 端首页；状态筛选，“新建投稿”进入投稿表单，“导出”弹窗'),
        ('submission-detail-video', '稿件档案 · 视频', 'video', '时长、云盘链接与提取码、封面、简介、附件'),
        ('submission-detail-photo', '稿件档案 · 照片', 'image', '拍摄信息、涉及领导、原图与单张备注'),
        ('submission-detail-clue', '稿件档案 · 线索', 'bulb', '线索类型、内容、时间地点、联系人、处置状态'),
        ('submission-detail', '稿件档案', 'archive', '稿件内容、流转时间轴、历次审核意见'),
        ('version-history', '版本对比', 'compare', '新旧版本并排差异，附当时退回意见'),
        ('resubmit', '退回修改', 'undo', '顶部固定退回意见，修改后重新提交'),
        ('college-stats', '本院统计', 'chart', '本院本学年数据，仅限本院'),
        ('ranking', '全校排行榜', 'trophy', '学年 / 学期切换，点击他院进入无权页'),
        ('messages', '消息通知', 'bell', '点击标记已读并跳转，支持全部已读'),
        ('no-permission', '无权查看', 'lock', '学院之间数据隔离的提示页'),
    ],
    'teacher': [
        ('dashboard', '我的待办 · 待办', 'inbox', '统一待办列表：流程名称、当前节点、发起人、发起与到达时间，可按时效筛选'),
        ('review', '办理', 'file-check', '表单信息 / 流程图 / 审批记录 / 操作日志；通过后提交副书记审核'),
        ('review-video', '办理 · 视频', 'video', '视频类稿件的完整字段与审核'),
        ('review-reject', '退回弹窗', 'undo', '退回意见必填，可插入常用模板'),
        ('history', '我的待办 · 已办', 'history', '流程状态、意见、处理时间与时效'),
        ('done-detail', '已办详情', 'file', '基础信息、稿件内容、节点流程图与操作日志'),
        ('cc', '催办 / 抄送', 'bell', '超时自动催办与终审结果抄送'),
        ('batch', '批量审批', 'layers', '按流程分类勾选，批量通过 / 批量不通过（意见必填）'),
        ('submissions', '稿件查询', 'search', '本人审核过的学生稿件（通过 / 退回），按学院、类型、状态、审核结果、时间筛选'),
        ('submission-detail-video', '稿件档案 · 视频', 'video', '从稿件查询进入，按类型展示完整字段'),
        ('messages', '消息通知', 'bell', '新待审稿件、超时提醒'),
    ],
    'deputy': [
        ('todo', '我的待办 · 待办', 'inbox', 'PC 端首页；本院稿件到达副书记审核节点，超时优先'),
        ('review', '办理', 'file-check', '通过报送一审 / 退回（意见必填、模板、敏感词、时限）'),
        ('review-photo', '办理 · 照片', 'image', '教师照片稿件：提交后直接到达副书记'),
        ('review-reject', '退回弹窗', 'undo', '退回意见必填，可插入常用模板'),
        ('history', '我的待办 · 已办', 'history', '通过 / 退回记录与时效'),
        ('done-detail', '已办详情', 'file', '稿件内容、节点流程图与审批记录'),
        ('cc', '催办 / 抄送', 'bell', '超时自动催办与审核结果抄送'),
        ('batch', '批量审批', 'layers', '批量通过 / 批量不通过（意见必填）'),
        ('submissions', '稿件查询', 'search', '本院、本人审核过的稿件（通过 / 退回），按类型、状态、审核结果、身份、时间筛选'),
        ('submission-detail-clue', '稿件档案 · 线索', 'bulb', '从稿件查询进入，按类型展示完整字段'),
        ('messages', '消息通知', 'bell', '新待审稿件、教师投稿到达、超时提醒'),
    ],
    'vice': [
        ('todo', '我的待办 · 待办', 'inbox', 'PC 端首页；本部门职能部门老师的稿件，超时优先'),
        ('review', '办理', 'file-check', '通过报送学生一审 / 退回（意见必填、模板、敏感词、时限）'),
        ('review-video', '办理 · 视频', 'video', '视频类稿件的完整字段与审核'),
        ('review-reject', '退回弹窗', 'undo', '退回意见必填，可插入常用模板'),
        ('history', '我的待办 · 已办', 'history', '通过 / 退回记录与时效'),
        ('done-detail', '已办详情', 'file', '稿件内容、节点流程图与审批记录'),
        ('cc', '催办 / 抄送', 'bell', '超时自动催办与审核结果抄送'),
        ('batch', '批量审批', 'layers', '批量通过 / 批量不通过（意见必填）'),
        ('submissions', '稿件查询', 'search', '本部门、本人审核过的稿件，按部门、类型、状态、审核结果、时间筛选'),
        ('messages', '消息通知', 'bell', '新待审稿件、超时提醒'),
    ],
    'reviewer': [
        ('todo', '我的待办 · 待办', 'inbox', 'PC 端首页；统一待办列表，超时标红优先'),
        ('review', '办理', 'file-check', '表单信息 / 流程图 / 审批记录 / 操作日志、敏感词检测'),
        ('review-reject', '退回弹窗', 'undo', '退回意见必填，可插入常用模板'),
        ('submissions', '稿件查询', 'search', '按学院、类型、时间、状态组合筛选'),
        ('submission-detail', '稿件档案', 'package', '已采用新闻稿可复制升华网正文、导出素材包'),
        ('submission-detail-video', '稿件档案 · 视频', 'video', '云盘链接、封面、附件与审核流程'),
        ('my-ledger', '我的待办 · 已办', 'list', '流程状态、意见、处理时间与时效'),
        ('done-detail', '已办详情', 'file', '基础信息、稿件内容、节点流程图与操作日志'),
        ('cc', '催办 / 抄送', 'bell', '超时自动催办与终审结果抄送'),
        ('batch', '批量审批', 'layers', '按流程分类勾选，批量通过 / 批量不通过'),
        ('messages', '消息通知', 'bell', '新待办、超时预警'),
    ],
    'admin': [
        ('dashboard', '统计驾驶舱', 'dashboard', '总量、类型分布、采用 / 退回、学院对比、时效'),
        ('final-list', '我的待办 · 待办', 'inbox', '二审通过、等待三审终审的待办，超时优先'),
        ('final-done', '我的待办 · 已办', 'history', '终审采用 / 不采用记录'),
        ('final-cc', '催办 / 抄送', 'bell', '超时自动催办与审核环节抄送'),
        ('final-batch', '批量审批', 'layers', '批量终审采用 / 不采用'),
        ('final-review', '办理（三审终审）', 'file-check', '终审采用 / 不采用'),
        ('final-reject', '不采用弹窗', 'x-circle', '终审意见必填，标记不计入采用'),
        ('archive', '稿件档案库', 'archive', '多条件检索；“导出”弹窗含全校总表、分学院明细'),
        ('archive-detail', '档案详情', 'file', '内容、流转、版本、操作日志（含 IP）'),
        ('archive-detail-photo', '档案详情 · 照片', 'image', '原图与单张备注、涉及领导'),
        ('archive-detail-clue', '档案详情 · 线索', 'bulb', '线索内容、联系人、处置状态'),
        ('publish-export', '升华网发布素材', 'globe', '清洗正文、一键复制、ZIP 素材包、标记已发布'),
        ('clue-tracking', '线索跟进', 'bulb', '待跟进 → 已跟进 → 已转为正式新闻'),
        ('timeout-ledger', '超时台账', 'clock', '按节点和人员筛选，及时率，导出'),
        ('ranking', '学院排行榜', 'trophy', '投稿、采用、退回、采用率排名'),
        ('reviewer1-manage', '一审员名单', 'users', '新增、编辑、启用 / 停用、批量操作'),
        ('reviewer2-manage', '二审员名单', 'users', '按学年换届，批量替换'),
        ('teacher-manage', '指导老师名单', 'user', '维护可选指导老师，支持导入'),
        ('vice-manage', '副职领导名单', 'user', '按职能部门配置副职领导，同部门可多人；工号回显、导入导出、学年换届'),
        ('params', '业务参数', 'sliders', '审核时限、节假日、统计周期、类型字典'),
        ('opinion-templates', '审核意见模板', 'message', '各节点常用意见的增删改'),
        ('sensitive-words', '敏感词库', 'alert', '三个词库；“检测设置”弹窗可切换模式并试测'),
        ('operation-logs', '操作日志', 'history', '只读不可删除，含操作 IP'),
        ('messages', '消息通知', 'bell', '待三审、超时、待发布提醒'),
    ],
}

M_PAGES = {
    'correspondent': [
        ('home', '首页', 'home', '个人统计、四类投稿入口；底栏“+”弹出投稿类型面板'),
        ('submit-news', '新闻投稿', 'file', '身份切换、指导老师、正文、配图与附件（选填）'),
        ('submit-video', '视频投稿', 'video', '永久云盘链接、附件'),
        ('submit-photo', '照片投稿', 'image', '拍照或相册多选，单张备注'),
        ('submit-clue', '新闻线索', 'bulb', '采访意愿联动'),
        ('submit-success', '提交成功', 'check-circle', '按身份显示下一节点'),
        ('my-submissions', '我的投稿', 'inbox', '状态分段筛选'),
        ('detail', '稿件档案', 'archive', '退回意见、流转记录'),
        ('detail-video', '稿件档案 · 视频', 'video', '云盘链接、封面、附件'), ('detail-photo', '稿件档案 · 照片', 'image', '原图与单张备注'),
        ('detail-clue', '稿件档案 · 线索', 'bulb', '线索内容与联系人'),
        ('resubmit', '修改重提', 'undo', '历次意见 + 修改表单'),
        ('ranking', '全校排行榜', 'trophy', '学年 / 学期切换'),
        ('messages', '消息', 'bell', '点击已读、全部已读'),
        ('profile', '我的', 'user', '本院统计、投稿须知、退出'),
    ],
    'teacher': [
        ('todo', '待审稿件', 'inbox', '超时筛选'), ('review', '审核稿件', 'file-check', '底部面板填写意见'),
        ('history', '审核记录', 'history', '通过 / 退回筛选'), ('messages', '消息', 'bell', '新待审提醒'),
    ],
    'vice': [
        ('todo', '待审稿件', 'inbox', '本部门稿件，超时筛选'), ('review', '审核稿件', 'file-check', '通过报送学生一审 / 退回'),
        ('history', '审核记录', 'history', '通过 / 退回筛选'), ('messages', '消息', 'bell', '新待审提醒'),
    ],
    'deputy': [
        ('todo', '待审稿件', 'inbox', '本院稿件，超时筛选'), ('review', '审核稿件', 'file-check', '通过报送一审 / 退回'),
        ('review-video', '审核 · 视频', 'video', '教师视频稿件'), ('history', '审核记录', 'history', '通过 / 退回筛选'), ('messages', '消息', 'bell', '新待审提醒'),
    ],
    'reviewer': [
        ('todo', '待办', 'inbox', '超时优先'), ('review', '审核稿件', 'file-check', '通过 / 退回'),
        ('ledger', '审核台账', 'list', '及时率'), ('messages', '消息', 'bell', '超时预警'),
    ],
    'admin': [
        ('home', '看板', 'dashboard', '核心指标、排行摘要'), ('final-list', '待三审', 'inbox', '超时优先'),
        ('final-review', '三审终审', 'file-check', '采用 / 不采用'), ('messages', '消息', 'bell', '待办提醒'),
    ],
}

ROLE_ORDER = ['correspondent', 'teacher', 'deputy', 'vice', 'reviewer1', 'reviewer2', 'admin']
ROLE_ICON = {'correspondent': 'edit', 'teacher': 'user', 'deputy': 'flag', 'vice': 'award', 'reviewer1': 'file-check', 'reviewer2': 'shield', 'admin': 'settings'}

# ---------- 权限矩阵：Y 有，N 无，C 仅本院，S 仅本人相关 ----------
MATRIX_COLS = ['投稿人（学生）', '投稿人（教师）', '投稿人（职能部门老师）', '指导老师', '副书记', '副职领导', '一审员', '二审员', '管理员']
MATRIX = [
    ('投稿', [
        ('新闻 / 视频 / 照片 / 线索投稿', 'YYYNNNNNN'),
        ('保存草稿、退回修改重提', 'YYYNNNNNN'),
        ('必须指定指导老师', 'YNNNNNNNN'),
        ('查看我的投稿与稿件档案', 'SSSNNNNNN'),
    ]),
    ('审核', [
        ('指导老师审核（学生稿件）', 'NNNSNNNNN'),
        ('副书记审核（本院学生 / 教师稿件）', 'NNNNCNNNN'),
        ('副职领导审核（本部门职能部门老师稿件）', 'NNNNNSNNN'),
        ('一审', 'NNNNNNYNN'),
        ('二审', 'NNNNNNNYN'),
        ('三审终审（采用 / 不采用）', 'NNNNNNNNY'),
        ('查看敏感词检测结果', 'NNNYYYYYY'),
    ]),
    ('查询与统计', [
        ('稿件查询与档案', 'CCCSSSYYY'),
        ('本院统计', 'CCNNCNNNY'),
        ('全校学院排行榜', 'YYYNNNNNY'),
        ('我的待办 · 已办（本人处理记录）', 'NNNSSSSSN'),
        ('统计驾驶舱、超时台账', 'NNNNNNNNY'),
        ('数据导出', 'CCCNNNNNY'),
    ]),
    ('发布', [
        ('升华网正文复制 / 素材包导出', 'NNNNNNNYY'),
        ('标记“已发布”', 'NNNNNNNNY'),
        ('线索跟进', 'NNNNNNNNY'),
    ]),
    ('系统配置', [
        ('人员名单（含副职领导名单，按部门配置）', 'NNNNNNNNY'),
        ('业务参数', 'NNNNNNNNY'),
        ('意见模板、敏感词库', 'NNNNNNNNY'),
        ('操作日志（只读）', 'NNNNNNNNY'),
    ]),
]


# ---------- 审核流程 ----------
def node(title, sub='', cls='', ic='', timer=False, href=None):
    t = f'<span class="fn-timer">{icon("clock", 11)}限 3 个工作日</span>' if timer else ''
    inner = f'<span class="fn-ic">{icon(ic, 16)}</span><b>{title}</b><small>{sub}</small>{t}'
    if href:
        return f'<a class="fn {cls}" href="{href}">{inner}</a>'
    return f'<div class="fn {cls}">{inner}</div>'


def flow_html():
    main = ''.join([
        node('草稿 / 提交', '投稿人', 'fn-start', 'edit', href='pc/correspondent/submit-news.html'),
        node('待指导老师审核', '仅学生稿件', 'fn-review', 'user', True, 'pc/teacher/review.html'),
        node('待副书记审核', '本院副书记 · 学工系统', 'fn-review', 'flag', True, 'pc/deputy/review.html'),
        node('待一审', '一审员', 'fn-review', 'file-check', True, 'pc/reviewer1/review.html'),
        node('待二审', '二审员', 'fn-review', 'shield', True, 'pc/reviewer2/review.html'),
        node('待三审', '管理员终审', 'fn-review', 'award', True, 'pc/admin/final-review.html'),
        node('已终审采用', '计入采用', 'fn-ok', 'check-circle', href='pc/admin/archive-detail.html'),
        node('已发布', '仅新闻类', 'fn-pub', 'globe', href='pc/admin/publish-export.html'),
    ])
    return f'''<div class="flow-scroll"><div class="flow">
<div class="flow-main">{main}</div>
<div class="flow-bypass"><span>{icon("arrow-r", 13)}教师投稿：跳过指导老师，从副书记审核开始</span></div>
<div class="flow-vice"><a class="fn fn-review" href="pc/vice/review.html"><span class="fn-ic">{icon("award", 16)}</span><b>待副职领导审核</b><small>职能部门老师投稿 · 按部门配置</small><span class="fn-timer">{icon("clock", 11)}限 3 个工作日</span></a><span>{icon("arrow-r", 13)}通过后进入待一审（学生一审）、待二审（学生二审）、待三审；跳过指导老师和副书记</span></div>
<div class="flow-no">{node('已终审不采用', '不计入采用，意见必填', 'fn-no', 'x-circle')}</div>
<div class="flow-back"><div class="fb-ups"><i>{icon("undo", 13)}退回</i><i>{icon("undo", 13)}退回</i><i>{icon("undo", 13)}退回</i><i>{icon("undo", 13)}退回</i></div>
<a class="fb-bar" href="pc/correspondent/resubmit.html">{icon("repeat", 15)}<b>已退回</b><span>退回意见必填 → 投稿人修改后重新提交 → 生成新版本（旧版本与意见永久保留）→ 回到起点重新流转</span></a></div>
</div></div>
<div class="rule-grid">
<div class="rule"><span class="rule-ic">{icon("clock", 18)}</span><b>计时规则</b><p>每个审核节点从稿件到达时开始计时，默认 3 个工作日（后台可改）；剩余不足 1 天标橙，超时标红并记入超时台账。</p></div>
<div class="rule"><span class="rule-ic">{icon("undo", 18)}</span><b>退回规则</b><p>指导老师、副书记、副职领导、一审、二审均可退回，意见必填、可选模板；投稿人收到消息后修改重提，版本号递增。</p></div>
<div class="rule"><span class="rule-ic">{icon("award", 18)}</span><b>终审规则</b><p>三审二选一：采用计入学院采用统计；不采用必须填写意见，不计入采用。</p></div>
<div class="rule"><span class="rule-ic">{icon("globe", 18)}</span><b>发布规则</b><p>仅已终审采用的新闻类稿件可导出升华网素材；人工发布后由管理员标记“已发布”。</p></div>
</div>'''


def status_html():
    def col(title, desc, tags):
        return f'<div class="card st-col"><h4>{title}</h4><p>{desc}</p><div class="tags">{"".join(tags)}</div></div>'
    flow = [tag(s) for s in ['草稿', '待指导老师审核', '待副书记审核', '待副职领导审核', '待一审', '待二审', '待三审', '已退回', '已终审采用', '已终审不采用', '已发布']]
    clue = [tag(s) for s in ['无需处理', '待跟进', '已跟进', '已转为正式新闻']]
    stat = [tag(s) for s in ['计入采用', '不计入采用']]
    timer = [f'<span class="tag tag-dot {c}">{t}</span>' for c, t in [('tag-success', '剩余 ≥ 1 个工作日'), ('tag-warn', '即将超时（不足 1 天）'), ('tag-danger', '已超时 · 记入超时台账')]]
    timer += [tag('及时'), tag('超时')]
    return (f'<div class="notice notice-info">{icon("info", 15)}<div>稿件的流转状态、线索处置状态、统计归档属性分开记录，互不混用；审核时效是每个审核节点单独计算的标识，不是稿件状态。</div></div>'
            f'<div class="grid g4 mt16">'
            + col('流转状态', '所有稿件，决定谁能看到、谁能处理', flow)
            + col('线索处置状态', '仅新闻线索，终审采用后由管理员跟进', clue)
            + col('统计归档属性', '终审后生成，决定是否计入学院采用数', stat)
            + col('审核时效标识', '每个节点默认 3 个工作日，后台可配置', timer) + '</div>')


# ---------- 原型导航页各区块 ----------
ROLE_COLOR = {'投稿人': '#2A8DC7', '指导老师': '#F29100', '副书记': '#D9480F', '副职领导': '#9C36B5', '一审员': '#1BB975', '二审员': '#6B5BD2', '管理员': '#1F77AD'}
ROLE_OF = {'correspondent': '投稿人', 'teacher': '指导老师', 'deputy': '副书记', 'vice': '副职领导', 'reviewer1': '一审员', 'reviewer2': '二审员', 'admin': '管理员'}


def hero(total):
    return f'''<header class="hero"><div class="wrap-in">
  <div class="hero-logo">稿</div>
  <h1>中南大学团学组织新闻投稿平台 · 原型页面导航</h1>
  <p class="lead">覆盖团学新闻稿件<b>投稿 → 指导老师审核 → 副书记审核 → 一审 → 二审 → 三审终审 → 采用归档 → 升华网发布 → 统计排行</b>全流程的交互原型（教师投稿从副书记审核开始；职能部门老师投稿走“副职领导 → 学生一审 → 学生二审 → 终审”）。<br>
  <b>全校师生均可投稿</b>（统一身份认证登录，无需单独开通投稿账号）；<b>PC 管理后台（投稿人 / 指导老师 / 副书记 / 副职领导 / 一审员 / 二审员 / 管理员）+ 移动端（全部角色）</b>，15 条演示剧本贯穿各角色，业务逻辑闭环、按钮均可点击。</p>
  <div class="pills">
    <span class="pill blue">{icon("file", 15)}高保真交互原型</span>
    <span class="pill">{icon("layers", 15)}每页独立 HTML · 样式内联</span>
    <span class="pill">{icon("flow", 15)}演示剧本可一路点通</span>
  </div>
  <div class="nums">
    <div><b>{total}</b><span>HTML 页面</span></div>
    <div><b>2</b><span>终端形态</span></div>
    <div><b>7</b><span>核心角色</span></div>
    <div><b>3</b><span>条审核流程（学生 5 级 · 教师 / 职能部门老师 4 级）</span></div>
    <div><b>15</b><span>演示剧本</span></div>
  </div>
</div></header>
<div class="tipbar"><div class="wrap-in flex gap8">{icon("info", 15)}
  演示建议：先看“角色权限”与“审核流程”讲清规则，再按“演示剧本”逐步点击；PC 页面右上角“原型导航”、移动端页面右侧说明栏均可一键返回本导航页；PC 端头像下拉可切换演示角色。审核结果通过网址参数带到下一页，演示数据固定、不跨角色实时同步。
</div></div>
<nav class="anchor"><div class="wrap-in">
  <a href="#entry">演示入口</a><a href="#scenario">演示剧本</a><a href="#role">角色权限</a><a href="#feature">功能清单</a>
  <a href="#flow">业务流程</a><a href="#audit">审核流程</a><a href="#status">状态体系</a><a href="#pages">页面目录</a>
</div></nav>'''


def sec(id_, ic, title, desc, body):
    return (f'<section class="sec" id="{id_}"><div class="wrap-in"><div class="sec-hd"><span class="sec-ic">{icon(ic, 18)}</span>'
            f'<div><h2>{title}</h2><p>{desc}</p></div></div>{body}</div></section>')


def box(title, body, extra=''):
    return f'<div class="card"><div class="card-hd"><span class="card-title">{title}</span>{extra}</div><div class="card-bd">{body}</div></div>'


def entries():
    items = [
        ('PC 端 · 投稿人（全校师生）', '计算机学院 陈雨桐：四类投稿、跟踪进度、退回修改、本院统计', 'edit', '#2A8DC7', 'pc/correspondent/my-submissions.html', 1440,
         [('新闻投稿', 'pc/correspondent/submit-news.html'), ('稿件档案', 'pc/correspondent/submission-detail.html'), ('视频详情', 'pc/correspondent/submission-detail-video.html'), ('退回修改', 'pc/correspondent/resubmit.html'),
          ('本院统计', 'pc/correspondent/college-stats.html'), ('全校排行榜', 'pc/correspondent/ranking.html')]),
        ('PC 端 · 指导老师', '计算机学院 王海峰：审核指定本人为指导老师的学生稿件', 'user', '#F29100', 'pc/teacher/dashboard.html', 1440,
         [('办理', 'pc/teacher/review.html'), ('已办', 'pc/teacher/history.html'), ('批量审批', 'pc/teacher/batch.html'), ('稿件查询', 'pc/teacher/submissions.html')]),
        ('PC 端 · 副书记', '计算机学院 杨振华：学工系统固定角色，审核本院学生稿件（指导老师通过后）与教师稿件，无需配置', 'flag', '#D9480F', 'pc/deputy/todo.html', 1440,
         [('办理', 'pc/deputy/review.html'), ('办理 · 教师照片稿', 'pc/deputy/review-photo.html'), ('已办', 'pc/deputy/history.html'), ('稿件查询', 'pc/deputy/submissions.html')]),
        ('PC 端 · 副职领导', '党委宣传部副部长 秦志远：按部门配置，审核本部门职能部门老师的稿件，通过后报送学生一审', 'award', '#9C36B5', 'pc/vice/todo.html', 1440,
         [('办理', 'pc/vice/review.html'), ('已办', 'pc/vice/history.html'), ('稿件查询', 'pc/vice/submissions.html'), ('副职领导名单', 'pc/admin/vice-manage.html')]),
        ('PC 端 · 一审员', '校团委宣传部 刘子涵：我的待办（待办 / 已办 / 催办抄送 / 批量审批）、稿件查询', 'file-check', '#1BB975', 'pc/reviewer1/todo.html', 1440,
         [('办理', 'pc/reviewer1/review.html'), ('已办', 'pc/reviewer1/my-ledger.html'), ('批量审批', 'pc/reviewer1/batch.html'), ('稿件查询', 'pc/reviewer1/submissions.html')]),
        ('PC 端 · 二审员', '校团委宣传部 周明轩：待二审稿件、升华网正文复制与素材导出', 'shield', '#6B5BD2', 'pc/reviewer2/todo.html', 1440,
         [('办理', 'pc/reviewer2/review.html'), ('已办', 'pc/reviewer2/my-ledger.html'), ('稿件档案 · 升华网素材', 'pc/reviewer2/submission-detail.html')]),
        ('PC 端 · 校团委管理员', '校团委宣传部 张静：三审终审、统计驾驶舱、发布、名单与系统配置', 'settings', '#1F77AD', 'pc/admin/dashboard.html', 1440,
         [('我的待办', 'pc/admin/final-list.html'), ('已办', 'pc/admin/final-done.html'), ('稿件档案库', 'pc/admin/archive.html'), ('升华网发布素材', 'pc/admin/publish-export.html'),
          ('线索跟进', 'pc/admin/clue-tracking.html'), ('超时台账', 'pc/admin/timeout-ledger.html'), ('一审员名单', 'pc/admin/reviewer1-manage.html')]),
        ('移动端 · 投稿人（全校师生）', '陈雨桐：随时投稿、查看进度、收到退回后修改重提', 'mobile', '#2A8DC7', 'mobile/correspondent/home.html', 1100,
         [('新闻投稿', 'mobile/correspondent/submit-news.html'), ('我的投稿', 'mobile/correspondent/my-submissions.html'),
          ('修改重提', 'mobile/correspondent/resubmit.html'), ('消息', 'mobile/correspondent/messages.html')]),
        ('移动端 · 审核角色', '指导老师 / 副书记 / 副职领导 / 一审员 / 二审员：待办、底部面板填写意见、审核台账', 'file-check', '#1BB975', 'mobile/reviewer1/todo.html', 1100,
         [('指导老师待审', 'mobile/teacher/todo.html'), ('副书记待审', 'mobile/deputy/todo.html'), ('副职领导待审', 'mobile/vice/todo.html'), ('一审待办', 'mobile/reviewer1/todo.html'), ('二审待办', 'mobile/reviewer2/todo.html'), ('审核稿件', 'mobile/reviewer1/review.html')]),
        ('移动端 · 校团委管理员', '张静：统计看板、三审终审、超时与发布提醒', 'dashboard', '#1F77AD', 'mobile/admin/home.html', 1100,
         [('待三审', 'mobile/admin/final-list.html'), ('三审终审', 'mobile/admin/final-review.html'), ('消息', 'mobile/admin/messages.html')]),
    ]
    cards = ''
    for title, desc, ic, color, href, vw, links in items:
        scale = 560 / vw
        link_html = ''.join(f'<a href="{h}">{t}</a>' for t, h in links)
        cards += f'''<div class="entry">
  <a class="entry-hd" href="{href}"><span class="entry-ic" style="background:{color}">{icon(ic, 24)}</span>
    <div class="grow"><h3>{title}</h3><div class="small muted">{desc}</div></div><span class="entry-go">进入{icon("chev-r", 14)}</span></a>
  <a class="preview" href="{href}" aria-label="{title}页面预览"><iframe src="{href}" loading="lazy" tabindex="-1" title="{title}预览"
    style="width:{vw}px;height:{int(230 / scale)}px;transform:scale({scale:.4f})"></iframe></a>
  <div class="entry-links">{link_html}</div>
</div>'''
    return f'<div class="grid g2">{cards}</div>'


SCENARIOS = [
    ('file', '学生投新闻稿', '学生身份必须指定指导老师（默认本院，可搜索他院）；不填直接提交会标红定位，高危敏感词拦截、低危词提醒。', [
        ('投稿人', '我的投稿 · 新建投稿', 'pc/correspondent/my-submissions.html'), ('投稿人', '填写新闻投稿', 'pc/correspondent/submit-news.html'),
        ('投稿人', '提交成功 · 待指导老师审核', 'pc/correspondent/submit-success.html?type=新闻&identity=学生'),
        ('投稿人', '我的投稿 · 新稿件高亮', 'pc/correspondent/my-submissions.html?new=TG2026093005')]),
    ('user', '教师投稿', '身份切换为“教师”后指导老师字段隐藏，提交后先由本院副书记审核，再进入一审，比学生稿件少一级。', [
        ('投稿人', '新闻投稿 · 切换教师身份', 'pc/correspondent/submit-news.html'),
        ('投稿人', '提交成功 · 待副书记审核', 'pc/correspondent/submit-success.html?type=新闻&identity=教师'),
        ('副书记', '副书记待办 · 教师稿件', 'pc/deputy/review-photo.html'), ('一审员', '一审待办', 'pc/reviewer1/todo.html')]),
    ('layers', '视频、照片、线索投稿', '视频须提供永久云盘链接、时长为“分:秒”，可上传多个附件；照片多选后每张可备注；线索按是否接受采访联动显示时间段；各类型稿件详情完整展示表单字段。', [
        ('投稿人', '视频投稿', 'pc/correspondent/submit-video.html'), ('投稿人', '视频详情', 'pc/correspondent/submission-detail-video.html'),
        ('投稿人', '照片详情', 'pc/correspondent/submission-detail-photo.html'), ('投稿人', '线索详情', 'pc/correspondent/submission-detail-clue.html')]),
    ('user', '指导老师审核', '只看到指定本人为指导老师的学生稿件；通过后提交学院副书记审核，退回意见必填并可一键插入模板。', [
        ('指导老师', '我的待办 · 待办', 'pc/teacher/dashboard.html'), ('指导老师', '办理', 'pc/teacher/review.html'),
        ('指导老师', '退回 · 意见必填', 'pc/teacher/review-reject.html'), ('指导老师', '已办', 'pc/teacher/history.html'),
        ('指导老师', '稿件查询 · 审核过的稿件', 'pc/teacher/submissions.html')]),
    ('flag', '副书记审核', '副书记为投稿人所在学院副书记，取自学工系统、无需配置；学生稿件在指导老师通过后到达，教师稿件提交后直接到达；通过报送一审，退回意见必填。', [
        ('副书记', '我的待办 · 待办', 'pc/deputy/todo.html'), ('副书记', '办理 · 通过报送一审', 'pc/deputy/review.html'),
        ('副书记', '退回 · 意见必填', 'pc/deputy/review-reject.html'), ('副书记', '已办', 'pc/deputy/history.html'),
        ('副书记', '稿件查询 · 审核过的稿件', 'pc/deputy/submissions.html')]),
    ('award', '职能部门老师投稿与副职领导审核', '职能部门老师选择所属部门，提交后直接进入该部门副职领导的待办（同部门多人时任一人审核即可）；通过后进入学生一审、学生二审和终审；副职领导名单由管理员按部门配置。', [
        ('投稿人', '新闻投稿 · 选择职能部门老师', 'pc/correspondent/submit-news.html'),
        ('投稿人', '提交成功 · 待副职领导审核', 'pc/correspondent/submit-success.html?type=新闻&identity=职能部门老师'),
        ('副职领导', '副职领导待办', 'pc/vice/todo.html'), ('副职领导', '办理 · 通过报送学生一审', 'pc/vice/review.html'),
        ('管理员', '副职领导名单 · 按部门配置', 'pc/admin/vice-manage.html')]),
    ('file-check', '一审、二审', '统一待办按超时优先排序、超时标红；办理页显示敏感词检测结果；处理后稿件从待办消失并出现在“已办”。', [
        ('一审员', '一审待办', 'pc/reviewer1/todo.html'), ('一审员', '一审办理', 'pc/reviewer1/review.html'), ('一审员', '已办', 'pc/reviewer1/my-ledger.html'),
        ('二审员', '二审待办', 'pc/reviewer2/todo.html'), ('二审员', '二审办理', 'pc/reviewer2/review.html'), ('一审员', '批量审批', 'pc/reviewer1/batch.html')]),
    ('award', '三审终审', '终审二选一：采用计入学院采用统计；不采用必须填写终审意见，标记为不计入采用。', [
        ('管理员', '我的待办 · 待三审', 'pc/admin/final-list.html'), ('管理员', '三审终审办理', 'pc/admin/final-review.html'),
        ('管理员', '不采用 · 意见必填', 'pc/admin/final-reject.html'), ('管理员', '档案详情', 'pc/admin/archive-detail.html')]),
    ('undo', '退回重提', '投稿人点退回消息进入修改页，顶部固定显示历次退回意见；重新提交生成新版本，可对比新旧差异。', [
        ('投稿人', '消息 · 稿件被退回', 'pc/correspondent/messages.html'), ('投稿人', '退回修改', 'pc/correspondent/resubmit.html'),
        ('投稿人', '版本对比', 'pc/correspondent/version-history.html'), ('投稿人', '稿件档案', 'pc/correspondent/submission-detail.html')]),
    ('globe', '升华网发布', '已终审采用的新闻稿可复制清洗后的正文、导出 ZIP 素材包；人工发布后由管理员标记“已发布”。', [
        ('二审员', '稿件档案 · 复制正文', 'pc/reviewer2/submission-detail.html'), ('管理员', '升华网发布素材', 'pc/admin/publish-export.html'),
        ('管理员', '操作日志', 'pc/admin/operation-logs.html')]),
    ('bulb', '线索跟进', '新闻线索终审采用后进入跟进：待跟进 → 已跟进 → 已转为正式新闻（弹窗关联一篇正式稿件）。', [
        ('投稿人', '提交新闻线索', 'pc/correspondent/submit-clue.html'), ('管理员', '三审终审', 'pc/admin/final-review.html'),
        ('管理员', '线索跟进', 'pc/admin/clue-tracking.html')]),
    ('clock', '超时台账', '每个节点默认 3 个工作日，剩余不足 1 天标橙、超时标红并记入台账；管理员按节点和人员查看及时率并催办。', [
        ('一审员', '待办 · 超时标红', 'pc/reviewer1/todo.html'), ('管理员', '超时台账', 'pc/admin/timeout-ledger.html'),
        ('管理员', '统计驾驶舱', 'pc/admin/dashboard.html')]),
    ('shield', '人员与参数', '新增 / 停用审核员，二审员按学年换届批量替换；修改审核时限后保存即生效并写入操作日志。角色权限为固定规则，不在后台配置。', [
        ('管理员', '二审员名单', 'pc/admin/reviewer2-manage.html'), ('管理员', '指导老师名单', 'pc/admin/teacher-manage.html'),
        ('管理员', '业务参数', 'pc/admin/params.html'), ('管理员', '操作日志', 'pc/admin/operation-logs.html')]),
    ('alert', '敏感词', '在高危、低危、白名单中维护词条；“检测设置”弹窗可切换语义 / 精准匹配并现场试测；投稿与审核页同步展示命中结果。', [
        ('管理员', '敏感词库 · 检测设置', 'pc/admin/sensitive-words.html'), ('投稿人', '投稿时检测', 'pc/correspondent/submit-news.html'),
        ('一审员', '审核页检测结果', 'pc/reviewer1/review.html')]),
    ('lock', '数据隔离', '投稿人只能看到本院统计与稿件；点击其他学院进入“无权查看”提示页。', [
        ('投稿人', '全校排行榜', 'pc/correspondent/ranking.html'), ('投稿人', '无权查看', 'pc/correspondent/no-permission.html'),
        ('投稿人', '本院统计', 'pc/correspondent/college-stats.html')]),
    ('mobile', '移动端投稿与审核', '手机上完成投稿、指导老师审核、副书记审核、一审到终审；审核意见在底部面板填写，右侧说明栏给出下一步链路。', [
        ('投稿人', '移动端首页', 'mobile/correspondent/home.html'), ('投稿人', '新闻投稿', 'mobile/correspondent/submit-news.html'),
        ('指导老师', '移动待审', 'mobile/teacher/todo.html'), ('副书记', '移动审核', 'mobile/deputy/review.html'), ('一审员', '移动审核', 'mobile/reviewer1/review.html'),
        ('管理员', '移动终审', 'mobile/admin/final-review.html')]),
]


def scenarios():
    cards = ''
    for no, (ic, title, desc, steps) in enumerate(SCENARIOS, 1):
        sh = ''
        for i, (who, text, path) in enumerate(steps, 1):
            if i > 1:
                sh += f'<span class="scn-arrow">{icon("chev-r", 12)}</span>'
            sh += f'<a class="scn-step" href="{path}" title="{who}"><i style="background:{ROLE_COLOR[who]}">{i}</i>{text}</a>'
        cards += f'''<div class="card scn">
  <div class="flex gap12"><span class="scn-no">{no}</span><div class="grow"><div class="scn-t">{icon(ic, 17)}{title}</div>
  <div class="small muted">{len(steps)} 步 · 起点：{steps[0][0]}</div></div>
  <a class="btn btn-light btn-sm" href="{steps[0][2]}">从头演示{icon("arrow-r", 14)}</a></div>
  <p class="fs13 sub">{desc}</p>
  <div class="scn-steps">{sh}</div>
</div>'''
    legend = ''.join(f'<span class="flex gap6 small"><span class="legend-dot" style="background:{c}"></span>{k}</span>' for k, c in ROLE_COLOR.items())
    return f'<div class="flex gap16 mb16 wrap"><span class="small muted">步骤颜色：</span>{legend}</div><div class="grid g2">{"".join(cards)}</div>'


def cell(v):
    return {'Y': '<td><span class="yes">√</span></td>', 'C': '<td><span class="part">本院</span></td>',
            'S': '<td><span class="part">本人相关</span></td>'}.get(v, '<td><span class="no">—</span></td>')


def roles():
    pc_t, m_t = '<span class="tag tag-primary">PC</span>', '<span class="tag tag-success">移动</span>'
    rows = [('投稿人（学生）', '全校学生，统一身份认证登录', '本院稿件与本院统计；全校排行榜', '无审核权；投稿、存草稿、修改重提'),
            ('投稿人（教师）', '全校教职工，统一身份认证登录', '同上', '无审核权；投稿不经过指导老师，先由本院副书记审核'),
            ('指导老师', '学生投稿时指定的老师；下拉默认本院名单，也可按工号指定', '指定本人为指导老师的学生稿件；稿件查询（本人审核过的）', '学生稿件第一道审核：通过提交副书记审核 / 退回'),
            ('投稿人（职能部门老师）', '党委宣传部、教务处等职能部门的老师', '本人稿件', '无审核权；投稿后先由所属部门的副职领导审核，再进入学生一审'),
            ('副职领导', '职能部门副职领导，<b>由管理员在“副职领导名单”中按部门配置</b>，同部门可多人', '本部门职能部门老师的稿件；稿件查询（本人审核过的）', '职能部门老师稿件第一道审核：通过报送学生一审 / 退回；同部门多人时任一人审核即可'),
            ('副书记', '投稿人所在学院的副书记，<b>取自学工系统，无需配置</b>', '本院稿件（副书记审核环节）；稿件查询（本人审核过的）', '学生稿件第二道、教师稿件第一道审核：通过报送一审 / 退回'),
            ('一审员', '校团委宣传部学生干部', '分配给本人的待一审稿件；全校稿件查询', '一审：通过流转二审 / 退回'),
            ('二审员', '校团委宣传部高年级学生干部', '分配给本人的待二审稿件；全校稿件查询', '二审：通过流转三审 / 退回；升华网素材导出'),
            ('校团委管理员', '校团委宣传部老师', '全校全部稿件、统计与配置', '三审终审：采用 / 不采用；系统配置')]
    body = ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td><td>{pc_t} {m_t}</td></tr>' for a, b, c, d in rows)
    role_tbl = f'<div class="table-wrap"><table class="table"><thead><tr><th>用户角色</th><th>主要使用人员</th><th>可查看数据范围</th><th>审核权限</th><th>终端</th></tr></thead><tbody>{body}</tbody></table></div>'
    heads = '<th>功能</th>' + ''.join(f'<th>{c}</th>' for c in MATRIX_COLS)
    mrows = ''
    for group, items in MATRIX:
        mrows += f'<tr class="grp"><td colspan="{len(MATRIX_COLS) + 1}">{group}</td></tr>'
        mrows += ''.join(f'<tr><td><b>{n}</b></td>{"".join(cell(v) for v in vals)}</tr>' for n, vals in items)
    mtx = (f'<div class="table-wrap"><table class="table matrix"><thead><tr>{heads}</tr></thead><tbody>{mrows}</tbody></table></div>'
           f'<div class="flex gap20 mt12 small muted wrap"><span><span class="yes">√</span> 具有该功能权限</span><span><span class="part">本院 / 本人相关</span> 仅限本院数据或与本人相关的稿件</span><span><span class="no">—</span> 不具有该权限</span></div>')
    n_func = sum(len(i) for _, i in MATRIX)
    design = box('权限设计要点', f'''<div class="grid g2">
  <div><div class="notice notice-warn">{icon("alert", 15)}<div><b>全校师生均可投稿，无需单独开通账号。</b>区别只在投稿身份：学生稿件指定指导老师（默认本院已配置名单，也可按工号查找），经指导老师、学院副书记审核后进入校团委一审；教师稿件不选人，先由学院副书记审核，再进入一审；职能部门老师选择所属部门并指定负责领导（默认该部门副职领导），先由副职领导审核，再进入学生一审、学生二审。</div></div>
  <div class="mt12 fs13 sub">指导老师下拉默认只列投稿人本学院已配置的老师。输入工号可回显人员库中的其他老师并指定，指定后该老师在“我的待办 · 待办”中看到这篇稿件。
  <div class="flex gap8 mt8 wrap"><a class="btn btn-light btn-sm" href="pc/correspondent/submit-news.html">{icon("user", 14)}查看指导老师选择</a><a class="btn btn-light btn-sm" href="pc/admin/teacher-manage.html">{icon("users", 14)}指导老师名单</a></div></div></div>
  <div><div class="bold mb8">固定规则与可调参数</div>
  <ul class="dots"><li>角色与数据范围为产品固定规则（见上方矩阵），不提供在线权限配置</li><li>副书记是学工系统的固定角色（投稿人所在学院副书记），按学院自动路由，<b>无需配置</b></li><li>副职领导在“副职领导名单”中按部门配置，同部门多人时稿件同时进入每人待办，任一人审核即可</li><li>一审员、二审员为学生干部，不能操作三审；三审终审仅限校团委管理员，可查看全部稿件</li><li>一审员、二审员名单按学年换届，可批量替换</li><li>审核时限、节假日、统计周期在“业务参数”中调整</li><li>所有配置变更写入只读的操作日志（含操作 IP）</li></ul>
  <div class="flex gap8 mt8 wrap"><a class="btn btn-light btn-sm" href="pc/admin/reviewer1-manage.html">{icon("users", 14)}一审员名单</a><a class="btn btn-light btn-sm" href="pc/admin/params.html">{icon("sliders", 14)}业务参数</a></div></div>
</div>''')
    return (box('用户角色及数据权限', role_tbl) + '<div class="mt16"></div>' +
            box(f'主要功能权限矩阵（{n_func} 项功能 × {len(MATRIX_COLS)} 类角色）', mtx) + '<div class="mt16"></div>' + design)


FEATURE_MODS = [
    ('edit', '四类投稿', '新闻、视频、照片、线索四类表单，学生必须指定指导老师；新闻、视频支持多附件', ['新闻', '视频', '照片', '线索', '多附件', '敏感词检测'], 'pc/correspondent/submit-news.html'),
    ('inbox', '稿件跟踪', '按状态筛选我的投稿，查看流转时间轴与历次意见', ['状态筛选', '流转时间轴', '版本对比', '修改重提'], 'pc/correspondent/my-submissions.html'),
    ('user', '指导老师审核', '只审核指定本人为指导老师的学生稿件', ['仅本人指导', '通过提交副书记', '退回意见必填', '意见模板'], 'pc/teacher/dashboard.html'),
    ('flag', '副书记审核', '学院副书记（学工系统固定角色，无需配置）审核本院学生 / 教师稿件', ['按学院路由', '通过报送一审', '退回意见必填', '本院范围'], 'pc/deputy/todo.html'),
    ('award', '副职领导审核', '职能部门老师稿件由所属部门副职领导审核，名单按部门配置', ['按部门路由', '同部门多人', '通过报送学生一审', '退回意见必填'], 'pc/vice/todo.html'),
    ('file-check', '一审 / 二审', '校团委两级审核，统一待办：待办 / 已办 / 催办抄送 / 批量审批', ['超时优先', '敏感词结果', '已办记录', '批量审批'], 'pc/reviewer1/todo.html'),
    ('award', '三审终审', '管理员终审二选一，决定是否计入学院采用', ['终审采用', '不采用意见必填', '计入 / 不计入采用'], 'pc/admin/final-list.html'),
    ('globe', '升华网发布', '已采用新闻稿的正文清洗、素材打包与发布标记', ['清洗正文', '一键复制', 'ZIP 素材包', '标记已发布'], 'pc/admin/publish-export.html'),
    ('bulb', '线索跟进', '终审采用的线索由管理员跟进，可关联正式新闻', ['待跟进', '已跟进', '转为正式新闻'], 'pc/admin/clue-tracking.html'),
    ('dashboard', '统计驾驶舱', '全校投稿总量、类型分布、学院对比与审核时效', ['类型分布', '采用 / 退回', '学院对比', '审核时效'], 'pc/admin/dashboard.html'),
    ('trophy', '排行与本院统计', '全校学院排行榜，投稿人只看本院明细', ['学年 / 学期', '采用率', '本院统计', '数据隔离'], 'pc/correspondent/ranking.html'),
    ('clock', '超时台账', '按节点、人员查看超时记录与及时率', ['3 个工作日时限', '及时率', '催办', '导出'], 'pc/admin/timeout-ledger.html'),
    ('users', '人员名单', '一审员、二审员、指导老师名单；工号回显、导入导出、学年换届', ['一审员', '二审员换届', '指导老师', '导入导出'], 'pc/admin/reviewer1-manage.html'),
    ('sliders', '系统配置', '业务参数、意见模板、敏感词库与操作日志', ['业务参数', '意见模板', '敏感词库', '操作日志'], 'pc/admin/params.html'),
]


def features():
    cards = ''.join(
        f'<a class="card card-hover mod" href="{h}"><h4><span class="sec-ic sm">{icon(ic, 16)}</span>{t}</h4>'
        f'<p class="fs13 sub mb8">{d}</p><ul>{"".join(f"<li>{x}</li>" for x in tags)}</ul></a>'
        for ic, t, d, tags, h in FEATURE_MODS)
    return f'<div class="grid g3">{cards}</div>'


def nd(t, cls='', href=None):
    if href:
        return f'<a class="node {cls}" href="{href}">{t}</a>'
    return f'<span class="node {cls}">{t}</span>'


ARROW = f'<span class="scn-arrow">{icon("arrow-r", 14)}</span>'


def lanes(rows):
    return ''.join(f'<div class="lane"><div class="lane-hd"><span class="legend-dot" style="background:{ROLE_COLOR.get(who, "#9096A2")}"></span>{who}</div>'
                   f'<div class="lane-bd">{ARROW.join(nodes)}</div></div>' for who, nodes in rows)


def flows():
    life = [('01', '投稿', '投稿人提交四类稿件，学生指定指导老师'), ('02', '指导老师审核', '仅学生稿件，教师稿件跳过'),
            ('03', '副书记审核', '本院副书记，取自学工系统'), ('04', '一审', '校团委宣传部学生干部'), ('05', '二审', '高年级学生干部'),
            ('06', '三审终审', '管理员：采用 / 不采用'), ('07', '采用归档', '计入学院采用统计'), ('08', '升华网发布', '仅新闻类，人工发布后标记'),
            ('09', '统计排行', '驾驶舱、排行榜、超时台账')]
    life_html = ''.join(f'<div class="life-item"><div class="life-no">{n}</div><b>{t}</b><p>{d}</p></div>' for n, t, d in life)
    submit = lanes([
        ('投稿人', [nd('新建投稿', 'start', 'pc/correspondent/my-submissions.html'), nd('选择学生身份'), nd('指定指导老师', href='pc/correspondent/submit-news.html'), nd('提交')]),
        ('指导老师', [nd('审核学生稿件', href='pc/teacher/review.html'), nd('通过 · 提交副书记')]),
        ('副书记', [nd('审核本院稿件', href='pc/deputy/review.html'), nd('通过 · 报送一审')]),
        ('一审员', [nd('一审', href='pc/reviewer1/review.html'), nd('通过 · 流转二审')]),
        ('二审员', [nd('二审', href='pc/reviewer2/review.html'), nd('通过 · 流转三审')]),
        ('管理员', [nd('三审终审', href='pc/admin/final-review.html'), nd('已终审采用', 'end'), nd('不采用 · 不计入', 'none')]),
    ])
    back = lanes([
        ('投稿人', [nd('收到退回消息', 'start', 'pc/correspondent/messages.html'), nd('对照意见修改', href='pc/correspondent/resubmit.html'), nd('重新提交 · 生成新版本'), nd('回到首个审核节点', 'end')]),
        ('二审员', [nd('复制升华网正文', href='pc/reviewer2/submission-detail.html'), nd('导出 ZIP 素材包')]),
        ('管理员', [nd('发布素材', href='pc/admin/publish-export.html'), nd('标记已发布', 'end')]),
    ])
    clue = lanes([
        ('管理员', [nd('线索终审采用', 'start'), nd('待跟进', href='pc/admin/clue-tracking.html'), nd('已跟进'), nd('已转为正式新闻', 'end')]),
        ('系统', [nd('审核时限可配置', 'cfg', 'pc/admin/params.html'), nd('剩余不足 1 天标橙'), nd('超时记入台账', href='pc/admin/timeout-ledger.html')]),
    ])
    return (box('稿件全流程', f'<div class="life">{life_html}</div>') + '<div class="grid g2 mt16">' +
            box('学生稿件审核流程（泳道）', submit + '<div class="small muted mt12">教师稿件：投稿 → 副书记审核 → 一审 → 二审 → 三审终审（不经过指导老师）<br>职能部门老师稿件：投稿（选择所属部门） → 副职领导审核 → 学生一审 → 学生二审 → 三审终审（不经过指导老师和副书记）</div>') + box('退回重提 · 升华网发布', back + '<div class="divider"></div>' + clue) + '</div>')


def audits():
    A = f'<span class="scn-arrow">{icon("arrow-r", 12)}</span>'
    rows = [
        ('学生新闻 / 视频 / 照片投稿', '学生投稿人', [nd('指导老师审核'), nd('副书记审核'), nd('一审'), nd('二审'), nd('三审终审')], '采用 / 不采用', 'pc/teacher/review.html'),
        ('教师投稿', '教师投稿人', [nd('指导老师审核', 'none'), nd('副书记审核'), nd('一审'), nd('二审'), nd('三审终审')], '采用 / 不采用', 'pc/deputy/review-photo.html'),
        ('职能部门老师投稿', '职能部门老师', [nd('副职领导审核', 'cfg'), nd('学生一审'), nd('学生二审'), nd('三审终审')], '采用 / 不采用', 'pc/vice/review.html'),
        ('新闻线索', '投稿人', [nd('指导老师审核（学生）'), nd('副书记审核'), nd('一审'), nd('二审'), nd('三审终审')], '采用后进入线索跟进', 'pc/admin/clue-tracking.html'),
        ('退回重提', '投稿人', [nd('回到首个审核节点'), nd('重新逐级流转')], '生成新版本', 'pc/correspondent/resubmit.html'),
        ('升华网发布', '二审员 / 管理员', [nd('复制正文 / 导出素材'), nd('管理员标记')], '已发布', 'pc/admin/publish-export.html'),
    ]
    body = ''.join(f'<tr><td><b>{b}</b></td><td>{who}</td><td><div class="flex gap6 wrap">{A.join(nodes)}</div></td>'
                   f'<td><span class="tag tag-success">{res}</span></td><td><a class="link" href="{h}">查看</a></td></tr>' for b, who, nodes, res, h in rows)
    tbl = f'<div class="table-wrap"><table class="table"><thead><tr><th>业务事项</th><th>发起人</th><th>审核节点</th><th>最终结果</th><th>演示</th></tr></thead><tbody>{body}</tbody></table></div>'
    legend = (f'<div class="flex gap16 mt12 small muted wrap"><span class="flex gap6"><span class="node cfg" style="height:22px">虚线橙色</span>可在后台配置（副职领导按部门配置）</span>'
              f'<span class="flex gap6"><span class="node none" style="height:22px">灰色</span>无需该节点</span>'
              f'<span>副书记取自学工系统，按投稿人所在学院自动确定，无需配置</span><span>每个审核节点默认 3 个工作日，可在“业务参数”中修改</span><a class="link" href="pc/admin/params.html">打开业务参数 →</a></div>')
    branches = box('每个审核节点的分支（闭环设计）', f'''<div class="grid g4">
  <div><span class="tag tag-success">通过</span><div class="fs13 sub mt8">进入下一节点；三审终审采用后计入学院采用统计</div></div>
  <div><span class="tag tag-danger">退回</span><div class="fs13 sub mt8">意见必填、可选模板；投稿人修改后重新提交，版本号递增</div></div>
  <div><span class="tag tag-gray">终审不采用</span><div class="fs13 sub mt8">仅三审可选，意见必填，标记为不计入采用</div></div>
  <div><span class="tag tag-warn">超时</span><div class="fs13 sub mt8">不足 1 天标橙提醒，超时标红并记入超时台账</div></div>
</div>''')
    return (box('审核流转图（点击节点进入对应页面）', flow_html()) + '<div class="mt16"></div>' +
            box('业务审核流程表', tbl + legend) + '<div class="mt16"></div>' + branches)


def directory():
    groups = []
    for r in ROLE_ORDER:
        key = 'reviewer' if r.startswith('reviewer') else r
        groups.append(('PC 端', r, f'pc/{r}', PC_PAGES[key]))
    for r in ROLE_ORDER:
        key = 'reviewer' if r.startswith('reviewer') else r
        groups.append(('移动端', r, f'mobile/{r}', M_PAGES[key]))
    out = ''
    n = 0
    for term, r, d, pages in groups:
        cards = ''
        for f, t, ic, desc in pages:
            n += 1
            cards += f'<a class="pg" href="{d}/{f}.html"><span class="pg-no">{n}</span><div class="grow"><b>{t}</b><span>{desc}</span></div><code>{f}.html</code></a>'
        role = ROLES[r]
        out += (f'<div class="dir-hd"><span class="entry-ic" style="background:{ROLE_COLOR[ROLE_OF[r]]}">{icon(ROLE_ICON[r], 20)}</span>'
                f'<div><h3>{term} · {role["name"]}</h3><div class="small muted">{role["user"]} · {role["dept"]}</div></div>'
                f'<span class="cnt">{len(pages)} 页 · {d}/</span></div><div class="grid g2">{cards}</div>')
    return out


INDEX_CSS = """
body{background:#E3F1F9}
.wrap-in{max-width:1200px;margin:0 auto;padding:0 24px}
.grow{flex:1;min-width:0}.wrap{flex-wrap:wrap}.gap6{gap:6px}.gap16{gap:16px}.gap20{gap:20px}.mb8{margin-bottom:8px}
.small{font-size:12px}.muted{color:var(--text-3)}.sub{color:var(--text-2)}.fs13{font-size:13px}.bold{font-weight:600}
.grid{display:grid;gap:16px}.g2{grid-template-columns:repeat(2,minmax(0,1fr))}.g3{grid-template-columns:repeat(3,minmax(0,1fr))}.g4{grid-template-columns:repeat(4,minmax(0,1fr))}
.card{background:#fff;border-radius:8px;border:1px solid #fff;color:var(--text)}
.card-hover{transition:box-shadow .2s,border-color .2s,transform .2s}.card-hover:hover{box-shadow:var(--shadow-lg);border-color:var(--blue7);transform:translateY(-1px)}
.card-hd{display:flex;align-items:center;justify-content:space-between;padding:16px 20px 6px}
.card-title{display:flex;align-items:center;gap:8px;font-size:17px;font-weight:600;color:#1E323F;position:relative;padding-bottom:10px}
.card-title::after{content:'';position:absolute;left:0;bottom:0;width:32px;height:6px;background:var(--brace) no-repeat}
.card-bd{padding:20px}
.divider{height:1px;background:var(--line);margin:14px 0}
.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:8px;background:#fff}
.table{width:100%;border-collapse:collapse;font-size:13px}
.table th{background:#D6EAF9;color:#2A8DC7;font-weight:700;text-align:left;padding:12px;white-space:nowrap;border-right:1px solid #BADEF3}
.table th:last-child{border-right:0}
.table td{padding:11px 12px;border-bottom:1px solid var(--line);vertical-align:middle}
.table tr:last-child td{border-bottom:none}
.table tbody tr:hover td{background:#F3F9FD}
.matrix td,.matrix th{text-align:center}
.matrix td:first-child,.matrix th:first-child{text-align:left}
.matrix tr.grp td{background:#F7F9FB!important;text-align:left;color:var(--primary);font-weight:600;font-size:12px;padding:7px 12px}
.yes{color:var(--success);font-weight:700}.no{color:var(--border)}.part{color:var(--warn);font-weight:500;font-size:12px}
.btn-light{background:var(--primary-light);border-color:var(--primary-light);color:var(--primary)}
.btn-light:hover{background:#D3E8F6;border-color:#D3E8F6}
.btn-sm{height:30px;padding:0 12px;font-size:13px;border-radius:6px}
.legend-dot{width:10px;height:10px;border-radius:3px;display:inline-block}
ul.dots{list-style:none;display:grid;gap:6px;font-size:13px;color:var(--text-2)}
ul.dots li{display:flex;gap:8px;line-height:1.6}
ul.dots li::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--blue7);margin-top:8px;flex:none}
.hero{text-align:center;padding:56px 0 36px;background:radial-gradient(900px 400px at 50% -10%,#CDE6F7 0%,transparent 70%)}
.hero-logo{width:76px;height:76px;border-radius:50%;margin:0 auto 20px;display:grid;place-items:center;font-size:34px;font-weight:800;color:#fff;background:linear-gradient(145deg,#4A92DB,#1F7FC1);border:3px solid #fff;box-shadow:0 0 0 1px #BADEF3,0 14px 30px rgba(42,141,199,.35)}
.hero h1{font-size:34px;letter-spacing:1px}
.hero .lead{max-width:780px;margin:14px auto 0;color:var(--text-2);font-size:15px;line-height:1.9}
.hero .lead b{color:var(--text)}
.pills{display:flex;justify-content:center;gap:10px;margin-top:22px;flex-wrap:wrap}
.pill{display:inline-flex;align-items:center;gap:6px;height:36px;padding:0 16px;border-radius:18px;background:#fff;border:1px solid var(--line);font-size:13px;font-weight:500}
.pill.blue{background:var(--primary-light);border-color:var(--blue7);color:var(--primary)}
.nums{display:flex;justify-content:center;gap:64px;margin-top:30px}
.nums b{display:block;font-size:40px;line-height:1.1;color:var(--primary);font-variant-numeric:tabular-nums}
.nums span{font-size:13px;color:var(--text-2)}
.tipbar{background:var(--primary-light);border-top:1px solid var(--blue7);border-bottom:1px solid var(--blue7);color:#1F5F92;font-size:13px;padding:10px 0}
.tipbar .ic{margin-top:3px;align-self:flex-start}
.anchor{position:sticky;top:0;z-index:40;background:rgba(255,255,255,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.anchor .wrap-in{display:flex;gap:4px;overflow-x:auto;height:52px;align-items:center}
.anchor a{padding:6px 14px;border-radius:8px;font-size:14px;color:var(--text-2);white-space:nowrap}
.anchor a:hover{background:var(--primary-light);color:var(--primary)}
.sec{padding:40px 0 8px;scroll-margin-top:52px}
.sec-hd{display:flex;align-items:center;gap:12px;margin-bottom:18px}
.sec-ic{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:var(--primary-light);color:var(--primary);flex:none}
.sec-ic.sm{width:28px;height:28px;border-radius:8px}
.sec-hd h2{font-size:22px}
.sec-hd p{font-size:13px;color:var(--text-3)}
.entry{display:flex;flex-direction:column;overflow:hidden;border-radius:14px;background:#fff;border:1px solid #E3ECF5;box-shadow:var(--shadow-sm);transition:box-shadow .2s,border-color .2s}
.entry:hover{box-shadow:var(--shadow-lg);border-color:var(--blue7)}
.entry-hd{display:flex;align-items:center;gap:14px;padding:18px 20px;color:var(--text)}
.entry-ic{width:50px;height:50px;border-radius:14px;display:grid;place-items:center;color:#fff;flex:none}
.entry h3{font-size:17px}
.entry-go{margin-left:auto;color:var(--primary);font-weight:600;font-size:14px;display:flex;align-items:center;gap:2px;white-space:nowrap}
.preview{height:230px;overflow:hidden;position:relative;background:#EEF3F8;border-top:1px solid var(--line);display:block}
.preview iframe{position:absolute;top:0;left:0;border:0;transform-origin:0 0;pointer-events:none}
.preview::after{content:'';position:absolute;inset:0}
.entry-links{display:flex;flex-wrap:wrap;gap:6px;padding:12px 20px 16px;border-top:1px solid var(--line)}
.entry-links a{font-size:12px;padding:3px 10px;border-radius:12px;background:var(--bg);color:var(--text-2)}
.entry-links a:hover{background:var(--primary-light);color:var(--primary)}
.scn{padding:20px;display:flex;flex-direction:column;gap:12px}
.scn-no{width:40px;height:40px;border-radius:12px;background:var(--primary);color:#fff;display:grid;place-items:center;font-weight:700;flex:none}
.scn-t{font-size:16px;font-weight:600;display:flex;align-items:center;gap:8px}
.scn-t .ic{color:var(--primary)}
.scn-steps{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.scn-step{display:inline-flex;align-items:center;gap:6px;padding:4px 10px 4px 4px;border-radius:14px;background:var(--bg);font-size:12px;border:1px solid transparent;color:var(--text)}
.scn-step:hover{border-color:var(--blue7);background:#fff;color:var(--primary)}
.scn-step i{font-style:normal;min-width:20px;height:20px;border-radius:10px;display:grid;place-items:center;color:#fff;font-size:11px;font-weight:600;padding:0 5px}
.scn-arrow{color:var(--border);display:inline-flex}
.mod{padding:18px 20px;display:block}
.mod h4{font-size:15px;display:flex;align-items:center;gap:8px;margin-bottom:8px}
.mod ul{list-style:none;display:flex;flex-wrap:wrap;gap:6px}
.mod li{font-size:12px;padding:2px 8px;border-radius:4px;background:var(--bg);color:var(--text-2)}
.life{display:flex;align-items:stretch;overflow-x:auto;padding-bottom:4px}
.life-item{flex:1;min-width:104px;position:relative;padding:14px 12px;background:#fff;border:1px solid var(--line);border-radius:12px;margin-right:18px}
.life-item:last-child{margin-right:0}
.life-item::after{content:'';position:absolute;right:-15px;top:50%;width:12px;height:12px;border-top:2px solid var(--blue7);border-right:2px solid var(--blue7);transform:translateY(-50%) rotate(45deg)}
.life-item:last-child::after{display:none}
.life-no{font-size:12px;color:var(--primary);font-weight:700}
.life-item b{display:block;font-size:15px;margin:2px 0 4px}
.life-item p{font-size:12px;color:var(--text-3);line-height:1.6}
.lane{display:grid;grid-template-columns:96px 1fr;border-bottom:1px dashed var(--line)}
.lane:last-child{border-bottom:none}
.lane-hd{padding:14px 0;font-weight:600;font-size:13px;display:flex;align-items:center;gap:8px}
.lane-bd{display:flex;align-items:center;gap:8px;padding:10px 0;flex-wrap:wrap}
.node{display:inline-flex;align-items:center;gap:6px;height:30px;padding:0 12px;border-radius:15px;font-size:13px;background:#fff;border:1px solid var(--line);color:var(--text);white-space:nowrap}
a.node:hover{border-color:var(--primary);color:var(--primary)}
.node.cfg{border-style:dashed;border-color:var(--warn);color:#A86400;background:var(--warn-bg)}
.node.end{background:var(--success-bg);border-color:var(--success-bd);color:#0E8A55}
.node.start{background:var(--primary-light);border-color:var(--blue7);color:var(--primary)}
.node.none{color:var(--text-3);background:var(--gray-bg);border-color:var(--line)}
.st-col{padding:20px}
.st-col h4{font-size:15px;margin-bottom:4px}
.st-col p{font-size:12px;color:var(--text-3);margin-bottom:12px}
.st-col .tags{display:flex;flex-direction:column;gap:8px;align-items:flex-start}
.dir-hd{display:flex;align-items:center;gap:12px;margin:28px 0 12px}
.dir-hd .entry-ic{width:40px;height:40px;border-radius:11px}
.dir-hd h3{font-size:18px}
.dir-hd .cnt{margin-left:auto;font-size:13px;color:var(--text-3)}
.pg{display:flex;align-items:center;gap:12px;padding:12px 16px;background:#fff;border:1px solid #E6EDF4;border-radius:10px;color:var(--text);transition:border-color .15s,box-shadow .15s}
.pg:hover{border-color:var(--primary);box-shadow:var(--shadow-md)}
.pg-no{width:28px;height:28px;border-radius:8px;background:var(--bg);color:var(--text-3);display:grid;place-items:center;font-size:12px;font-weight:600;flex:none}
.pg b{font-size:14px;display:block}
.pg span{font-size:12px;color:var(--text-3);display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pg code{margin-left:auto;font-size:11px;color:var(--primary);background:var(--primary-light);padding:2px 8px;border-radius:4px;white-space:nowrap;font-family:ui-monospace,Menlo,monospace}
.foot{padding:40px 0 60px;text-align:center;color:var(--text-3);font-size:12px}
.foot code{font-family:ui-monospace,Menlo,monospace;background:#fff;border:1px solid var(--line);border-radius:4px;padding:1px 6px}
.flow-scroll{overflow-x:auto;padding-bottom:6px}
.flow{min-width:1120px;display:grid;grid-template-columns:repeat(8,1fr);column-gap:30px;row-gap:14px}
.flow-main{grid-column:1/-1;display:grid;grid-template-columns:repeat(8,1fr);column-gap:30px}
.fn{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;gap:3px;padding:14px 8px 12px;border-radius:12px;background:#fff;border:1.5px solid var(--line);color:var(--text);transition:all .15s}
a.fn:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(48,135,204,.14)}
.flow-main .fn:not(:last-child)::after{content:'';position:absolute;right:-26px;top:50%;width:22px;height:2px;background:var(--blue6)}
.flow-main .fn:not(:last-child)::before{content:'';position:absolute;right:-27px;top:calc(50% - 4px);border:5px solid transparent;border-left:6px solid var(--blue6);border-right:0}
.fn-ic{width:32px;height:32px;border-radius:50%;display:grid;place-items:center;background:var(--primary-light);color:var(--primary);margin-bottom:4px}
.fn b{font-size:14px}
.fn small{font-size:12px;color:var(--text-3)}
.fn-timer{margin-top:6px;display:inline-flex;align-items:center;gap:3px;font-size:11px;color:var(--warn);background:var(--warn-bg);padding:1px 8px;border-radius:10px}
.fn-review{border-color:var(--blue7)}
.fn-start .fn-ic{background:var(--gray-bg);color:var(--text-2)}
.fn-ok{border-color:var(--success-bd);background:var(--success-bg)}
.fn-ok .fn-ic{background:#fff;color:var(--success)}
.fn-pub{border-color:var(--blue7);background:linear-gradient(135deg,#F2F8FD,#E3F1F9)}
.fn-pub .fn-ic{background:var(--primary);color:#fff}
.fn-no{border-color:var(--line);background:var(--gray-bg)}
.fn-no .fn-ic{background:#fff;color:var(--text-3)}
.flow-bypass{grid-column:1/4;grid-row:2;position:relative;height:40px;margin:-14px calc(100% / 6 - 10px) 0;border:1.5px dashed var(--blue6);border-top:0;border-radius:0 0 14px 14px}
.flow-bypass span{position:absolute;left:50%;bottom:-11px;transform:translateX(-50%);background:#fff;padding:0 10px;font-size:12px;color:var(--primary);white-space:nowrap;display:inline-flex;align-items:center;gap:4px}
.flow-vice{grid-column:1/6;grid-row:4;display:flex;align-items:center;gap:14px;margin-top:6px;font-size:12px;color:#9C36B5}
.flow-vice .fn{width:170px;flex:none;border-color:#D8B4E2}
.flow-vice .fn-ic{background:#F3E8F7;color:#9C36B5}
.flow-no{grid-column:6;grid-row:2/4;position:relative;padding-top:22px}
.flow-no::before{content:'不采用';position:absolute;top:0;left:50%;transform:translateX(-50%);font-size:12px;color:var(--text-3);background:#fff;padding:0 4px;z-index:1}
.flow-no::after{content:'';position:absolute;top:-14px;left:50%;height:36px;border-left:1.5px dashed var(--border)}
.flow-back{grid-column:2/6;grid-row:3;margin-top:14px}
.fb-ups{display:grid;grid-template-columns:repeat(4,1fr);column-gap:30px}
.fb-ups i{font-style:normal;justify-self:center;display:inline-flex;align-items:center;gap:3px;font-size:12px;color:var(--danger);border-left:1.5px dashed var(--danger-bd);padding:2px 0 6px 6px}
.fb-bar{display:flex;align-items:center;gap:10px;padding:12px 16px;border-radius:12px;background:var(--danger-bg);border:1.5px dashed var(--danger-bd);color:var(--danger);font-size:13px}
.fb-bar b{white-space:nowrap}
.fb-bar span{color:var(--text-2)}
.fb-bar:hover{border-style:solid}
.rule-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:22px}
.rule{background:#F9FBFD;border:1px solid var(--line);border-radius:12px;padding:16px}
.rule-ic{width:34px;height:34px;border-radius:9px;background:#fff;border:1px solid var(--line);color:var(--primary);display:grid;place-items:center;margin-bottom:10px}
.rule b{font-size:15px}
.rule p{font-size:13px;color:var(--text-2);margin-top:6px;line-height:1.8}
@media (max-width:900px){.g2,.g3,.g4{grid-template-columns:1fr}.rule-grid{grid-template-columns:1fr 1fr}.nums{gap:28px}.nums b{font-size:30px}.hero h1{font-size:24px}}
"""


def build():
    total = len(lib.WRITTEN) + 1
    body = (hero(total) +
            sec('entry', 'grid', '演示入口', '一键进入各角色首页，卡片内为实时页面预览', entries()) +
            sec('scenario', 'flow', '演示剧本', f'{len(SCENARIOS)} 条业务路线贯穿投稿人、指导老师、副书记、副职领导、一审员、二审员、管理员，按编号依次点击即可完整演示闭环', scenarios()) +
            sec('role', 'users', '角色权限', '系统用户角色、数据范围与功能权限矩阵', roles()) +
            sec('feature', 'layers', '功能清单', '核心功能模块，点击卡片查看对应页面', features()) +
            sec('flow', 'trend', '业务流程', '稿件全流程与审核、退回重提、发布跟进三条关键流程，节点可点击查看页面', flows()) +
            sec('audit', 'file-check', '审核流程', '学生稿件 5 级审核、教师稿件 4 级审核、职能部门老师稿件 4 级审核的节点与分支规则，审核时限支持后台配置', audits()) +
            sec('status', 'tag', '状态体系', '流转、线索处置、统计归档三套状态分开记录，统一配色', status_html()) +
            sec('pages', 'list', '页面目录', '按“终端 · 角色”分类存放，每行两个页面入口', directory()) +
            '<footer class="foot">中南大学团委 · 团学组织新闻投稿平台 · 高保真交互原型 · 图片素材来自 Unsplash · 模拟数据仅供演示<br>'
            '页面由 <code>_build/</code> 生成器输出，修改后运行 <code>python3 _build/build.py</code> 重新生成</footer>')
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>团学组织新闻投稿平台 · 原型页面导航</title>
<style>{BASE_CSS}{INDEX_CSS}</style>
</head>
<body>
{body}
<script src="./assets/mock-data.js"></script>
<script src="./assets/app.js"></script>
</body>
</html>
'''
    write('index.html', html)
