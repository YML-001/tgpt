# 页面框架与通用组件
import os
import re
from html import escape
from icons import icon
from styles import PC_CSS, MOBILE_CSS
from data import ROLES, TYPE_ICON

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ROOT = '../../'
WRITTEN = []

TAG_CLASS = {
    '草稿': 'tag-gray', '待指导老师审核': 'tag-warn', '待副书记审核': 'tag-warn', '待一审': 'tag-warn', '待二审': 'tag-warn', '待三审': 'tag-warn',
    '已退回': 'tag-danger', '已终审采用': 'tag-success', '已终审不采用': 'tag-gray', '已发布': 'tag-primary',
    '无需处理': 'tag-gray', '待跟进': 'tag-warn', '已跟进': 'tag-primary', '已转为正式新闻': 'tag-success',
    '计入采用': 'tag-success', '不计入采用': 'tag-gray', '启用': 'tag-success', '停用': 'tag-gray',
    '在任': 'tag-success', '已离任': 'tag-gray', '处理中': 'tag-danger', '已处理': 'tag-gray',
    '通过': 'tag-success', '退回': 'tag-danger', '采用': 'tag-success', '不采用': 'tag-gray',
    '及时': 'tag-success', '超时': 'tag-danger', '高危': 'tag-danger', '低危': 'tag-warn',
}


def write(path, html):
    if '<!--M_NOTES-->' in html:
        from notes import notes_panel
        html = html.replace('<!--M_NOTES-->', notes_panel(path))
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(html)
    WRITTEN.append(path)


# ---------- 通用小组件 ----------
def tag(s, extra=''):
    return f'<span class="tag tag-dot {TAG_CLASS.get(s, "tag-primary")} {extra}">{s}</span>'


def type_tag(t):
    return f'<span class="type-tag">{icon(TYPE_ICON[t], 13)}{t}</span>'


def remain(text, level):
    if level == 'over':
        return f'<span class="overdue-txt">{icon("alert", 13)}{text}</span>'
    if level == 'warn':
        return f'<span class="remain-txt">{text}</span>'
    return f'<span class="ok-txt">{text}</span>'


def stat(ic, color, num, label, sub='', href=None, counter=False, unit=''):
    c = ' data-counter' if counter else ''
    tag_ = 'a' if href else 'div'
    h = f' href="{href}"' if href else ''
    u = f'<small>{unit}</small>' if unit else ''
    sub_html = f'<div class="stat-trend">{sub}</div>' if sub else ''
    return (f'<{tag_} class="card stat"{h}><div class="stat-ic {color}">{icon(ic, 22)}</div>'
            f'<div class="stat-body"><div class="stat-label">{label}</div><div class="stat-num"><span{c}>{num}</span>{u}</div>{sub_html}</div></{tag_}>')


def card(title, body, ic=None, extra='', body_cls='card-body', cls=''):
    head = f'<div class="card-head"><div class="card-title">{title}</div>{extra}</div>' if title else ''
    return f'<div class="card {cls}">{head}<div class="{body_cls}">{body}</div></div>'


def page_head(title, desc='', actions=''):
    d = f'<div class="page-desc">{desc}</div>' if desc else ''
    a = f'<div class="page-actions">{actions}</div>' if actions else ''
    return f'<div class="page-head"><div><h1 class="page-title">{title}</h1>{d}</div>{a}</div>'


def btn(text, cls='', ic=None, attrs=''):
    i = icon(ic, 15) if ic else ''
    return f'<button type="button" class="btn {cls}" {attrs}>{i}{text}</button>'


def a_btn(text, href, cls='', ic=None, attrs=''):
    i = icon(ic, 15) if ic else ''
    return f'<a class="btn {cls}" href="{href}" {attrs}>{i}{text}</a>'


def options(items, placeholder=None, selected=None):
    out = f'<option value="">{placeholder}</option>' if placeholder else ''
    for it in items:
        v, t = (it, it) if isinstance(it, str) else it
        s = ' selected' if selected == v else ''
        out += f'<option value="{v}"{s}>{t}</option>'
    return out


def filter_select(table_id, key, placeholder, items):
    label = placeholder[2:] if placeholder.startswith('全部') else placeholder
    return (f'<label class="f-box"><span class="f-lbl">{label}</span>'
            f'<select class="select" data-filter="{key}" data-for="{table_id}">{options(items, "全部")}</select></label>')


def search_box(table_id, placeholder='搜索稿件标题 / 编号 / 投稿人'):
    ph = placeholder[2:].strip() if placeholder.startswith('搜索') else placeholder
    return (f'<label class="f-box f-search"><span class="f-lbl">关键词</span><input class="input" data-filter="keyword" data-live '
            f'data-for="{table_id}" placeholder="请输入{ph}"></label>')


def date_range(table_id):
    return (f'<div class="f-box f-date"><span class="f-lbl">提交日期</span><input type="date" class="input" data-filter="dateFrom" data-for="{table_id}">'
            f'<span class="f-to">至</span><input type="date" class="input" data-filter="dateTo" data-for="{table_id}"></div>')


def filter_bar(table_id, controls, extra_actions=''):
    query = btn('立即查询', 'btn-primary', 'search', 'data-action="apply-filter" data-for="%s"' % table_id)
    reset = btn('重置', '', 'refresh', 'data-action="reset-filter" data-for="%s"' % table_id)
    return f'<div class="filters">{controls}<div class="f-actions">{query}{reset}{extra_actions}</div></div>'


def table(table_id, headers, rows, page_size=10, pager=True, cls=''):
    ths = ''
    for h in headers:
        if isinstance(h, tuple):
            text, attrs = h
            ths += f'<th {attrs}>{text}</th>'
        else:
            ths += f'<th>{h}</th>'
    p = f'<div class="pager" data-pager-for="{table_id}"></div>' if pager else ''
    return (f'<div class="table-wrap"><table class="tbl {cls}" id="{table_id}" data-table data-page-size="{page_size}">'
            f'<thead><tr>{ths}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>{p}')


def field(label, control, req=False, full=False, hint='', cls=''):
    r = ' req' if req else ''
    f = ' full' if full else ''
    h = f'<div class="hint">{hint}</div>' if hint else ''
    return f'<div class="field{f} {cls}"><label class="lbl{r}">{label}</label>{control}{h}</div>'


def modal(mid, title, body, foot, size='', open_=False):
    o = ' open' if open_ else ''
    return (f'<div class="modal{o}" id="{mid}"><div class="modal-box {size}">'
            f'<div class="modal-head"><span>{title}</span><button class="modal-x" data-close aria-label="关闭">{icon("x", 18)}</button></div>'
            f'<div class="modal-body">{body}</div><div class="modal-foot">{foot}</div></div></div>')


def timeline(items):
    """items: (点颜色, 标题, 标签HTML, 元信息, 意见, 意见样式)"""
    out = ''
    for dot, title, tg, meta, op, opcls in items:
        op_html = f'<div class="tl-opinion {opcls}">{op}</div>' if op else ''
        out += (f'<div class="tl-item"><span class="tl-dot {dot}"></span><div class="tl-head">{title}{tg}</div>'
                f'<div class="tl-meta">{meta}</div>{op_html}</div>')
    return f'<div class="timeline">{out}</div>'


def flow_steps(identity='学生', cur=1, back_at=None):
    """审核进度条：cur 为当前所在节点下标"""
    names = ['提交投稿', '指导老师审核', '副书记审核', '一审', '二审', '三审终审', '采用归档'] if identity == '学生' else \
            ['提交投稿', '副书记审核', '一审', '二审', '三审终审', '采用归档']
    out = ''
    for i, n in enumerate(names):
        cls = 'done' if i < cur else ('cur' if i == cur else '')
        if back_at is not None and i == back_at:
            cls = 'back'
        mark = '✓' if cls == 'done' else ('!' if cls == 'back' else i + 1)
        out += f'<div class="fs {cls}"><i>{mark}</i><b>{n}</b></div>'
    return f'<div class="flow-steps">{out}</div>'


PC_TOOLS = [('undo', 'undo', '撤销'), ('redo', 'redo', '重做'), None, 'block', None,
            ('bold', 'bold', '加粗'), ('italic', 'italic', '斜体'), ('underline', 'underline', '下划线'),
            ('strike', 'strikeThrough', '删除线'), None,
            ('align', 'justifyLeft', '左对齐'), ('align-center', 'justifyCenter', '居中'), ('align-right', 'justifyRight', '右对齐'), None,
            ('list', 'insertUnorderedList', '无序列表'), ('list-ol', 'insertOrderedList', '有序列表'),
            ('outdent', 'outdent', '减少缩进'), ('indent', 'indent', '增加缩进'), None,
            ('quote', 'formatBlock|blockquote', '引用'), ('minus', 'insertHorizontalRule', '分隔线'),
            ('link', '@link', '插入链接'), ('image', '@image', '插入图片'), None,
            ('eraser', 'removeFormat', '清除格式')]
M_TOOLS = [('undo', 'undo', '撤销'), ('redo', 'redo', '重做'), None, ('heading', 'formatBlock|h3', '小标题'),
           ('bold', 'bold', '加粗'), ('italic', 'italic', '斜体'), ('underline', 'underline', '下划线'),
           ('strike', 'strikeThrough', '删除线'), None, ('align-center', 'justifyCenter', '居中'),
           ('list', 'insertUnorderedList', '无序列表'), ('list-ol', 'insertOrderedList', '有序列表'), None,
           ('quote', 'formatBlock|blockquote', '引用'), ('link', '@link', '插入链接'), ('image', '@image', '插入图片'),
           ('eraser', 'removeFormat', '清除格式')]


def editor_tools(tools):
    bar = ''
    for t in tools:
        if t is None:
            bar += '<span class="sep"></span>'
        elif t == 'block':
            items = ''.join(f'<button type="button" class="dm-item ed-{tg}" data-cmd="formatBlock" data-arg="{tg}">{lb}</button>'
                            for tg, lb in (('p', '正文'), ('h2', '标题'), ('h3', '小标题')))
            bar += (f'<div class="dropdown ed-dd"><button type="button" class="ed-dd-btn" data-dropdown title="段落格式">'
                    f'<span class="ed-dd-label">正文</span>{icon("chev-d", 12)}</button><div class="dropdown-menu">{items}</div></div>')
        else:
            ic, cmd, tip = t
            if cmd.startswith('@'):
                bar += f'<button type="button" data-ed="{cmd[1:]}" title="{tip}" aria-label="{tip}">{icon(ic, 16)}</button>'
                continue
            c, _, arg = cmd.partition('|')
            a = f' data-arg="{arg}"' if arg else ''
            bar += f'<button type="button" data-cmd="{c}"{a} title="{tip}" aria-label="{tip}">{icon(ic, 16)}</button>'
    return bar


def editor_pop():
    return ('<div class="ed-pop" hidden><div class="ed-pop-title">插入链接</div>'
            '<input class="input ed-url" placeholder="请输入链接地址，如 https://news.csu.edu.cn">'
            '<input class="input ed-text ed-only-link" placeholder="链接文字（选填，默认使用选中文字）">'
            '<div class="ed-only-image ed-img-src"><label class="ed-local">'
            f'{icon("upload", 14)}选择本地图片<input type="file" accept="image/*" data-ed-file hidden></label>'
            '<button type="button" class="ed-link-btn" data-ed="sample">插入示例图片</button></div>'
            '<div class="ed-pop-foot"><button type="button" class="btn btn-sm" data-ed="cancel">取消</button>'
            '<button type="button" class="btn btn-sm btn-primary" data-ed="ok">确定</button></div></div>')


def editor(eid, content='', placeholder='请输入新闻正文，建议 800—2000 字，可插入图片'):
    bar = editor_tools(PC_TOOLS)
    plain = re.sub(r'<[^>]+>', '', content or '')
    bar += f'<span class="wc">正文字数 <b id="{eid}Count">{len(plain.strip())}</b></span>'
    return (f'<div class="editor-box"><div class="editor-bar">{bar}</div>{editor_pop()}'
            f'<div class="editor" id="{eid}" contenteditable="true" data-required data-min-length="50" data-label="新闻正文" '
            f'data-counter="#{eid}Count" data-placeholder="{placeholder}">{content}</div></div>')


def m_editor(eid, content='', placeholder='请输入新闻正文（不少于 50 字）'):
    plain = re.sub(r'<[^>]+>', '', content or '')
    return (f'<div class="editor-box m-ed-box"><div class="editor-bar m-ed-bar">{editor_tools(M_TOOLS)}</div>{editor_pop()}'
            f'<div class="m-editor" id="{eid}" contenteditable="true" data-required data-min-length="50" data-label="新闻正文" '
            f'data-counter="#{eid}Count" data-placeholder="{placeholder}">{content}</div>'
            f'<div class="m-ed-wc">正文字数 <b id="{eid}Count">{len(plain.strip())}</b></div></div>')


def upload_field(label, kind='img', accept='image/jpeg,image/png', hint='', min_files=1, remark=False,
                 prefill=None, req=True, max_mb=20, full=True):
    r = ' data-remark' if remark else ''
    items = ''
    for src, name, size in (prefill or []):
        extra = '<input placeholder="单张照片备注（选填）">' if remark else ''
        items += (f'<div class="file-item"><img src="{src}" alt="{name}"><button type="button" class="fi-del" aria-label="删除">×</button>'
                  f'<div class="fi-meta"><span class="fi-name">{name}</span><span>{size} · 原图</span></div>{extra}</div>')
    req_attr = f' data-required data-min-files="{min_files}"' if req else ''
    ctrl = (f'<div class="upload-field"><label class="upload">{icon("upload", 26)}<b>点击或拖拽文件到此处上传</b>'
            f'<span class="hint">{hint}</span><input type="file" multiple accept="{accept}" data-upload="{kind}" '
            f'data-max-mb="{max_mb}"{r}{req_attr} data-label="{label}"></label><div class="files">{items}</div>'
            f'<div class="hint mt8">已上传 <b data-file-count>{len(prefill or [])}</b> 个文件</div></div>')
    return field(label, ctrl, req=req, full=full)


def teacher_picker(value='王海峰（计算机学院）', name='teacher'):
    return (f'<div class="teacher-picker"><input class="input" name="{name}" value="{value}" data-required data-in-list '
            f'data-label="指导老师" placeholder="输入姓名 / 工号 / 学院搜索" autocomplete="off"><div class="picker-list"></div></div>')


# ---------- PC 框架 ----------
MENUS = {
    'correspondent': [
        ('投稿管理', [('inbox', '我的投稿', 'my-submissions.html')]),
        ('统计分析', [('chart', '本院投稿统计', 'college-stats.html'), ('trophy', '全校排行榜', 'ranking.html')]),
    ],
    'teacher': [
        ('我的待办', [('inbox', '待办', 'dashboard.html', 5), ('file-check', '已办', 'history.html'),
                  ('bell', '催办/抄送', 'cc.html'), ('layers', '批量审批', 'batch.html')]),
    ],
    'deputy': [
        ('我的待办', [('inbox', '待办', 'todo.html', '{todo}'), ('file-check', '已办', 'history.html'),
                  ('bell', '催办/抄送', 'cc.html'), ('layers', '批量审批', 'batch.html')]),
    ],
    'reviewer': [
        ('我的待办', [('inbox', '待办', 'todo.html', '{todo}'), ('file-check', '已办', 'my-ledger.html'),
                  ('bell', '催办/抄送', 'cc.html'), ('layers', '批量审批', 'batch.html')]),
        ('稿件查询', [('archive', '稿件查询', 'submissions.html')]),
    ],
    'admin': [
        ('统计驾驶舱', [('dashboard', '统计驾驶舱', 'dashboard.html'), ('trophy', '学院排行榜', 'ranking.html')]),
        ('我的待办', [('inbox', '待办', 'final-list.html', 7), ('file-check', '已办', 'final-done.html'),
                  ('bell', '催办/抄送', 'final-cc.html'), ('layers', '批量审批', 'final-batch.html')]),
        ('审核管理', [('bulb', '线索跟进', 'clue-tracking.html'), ('clock', '超时台账', 'timeout-ledger.html')]),
        ('稿件与数据', [('archive', '稿件档案库', 'archive.html'), ('globe', '升华网发布素材', 'publish-export.html')]),
        ('人员与权限', [('users', '一审员名单', 'reviewer1-manage.html'), ('users', '二审员名单', 'reviewer2-manage.html'),
                   ('user', '指导老师名单', 'teacher-manage.html'),
                   ('shield', '角色权限配置', 'role-permission.html')]),
        ('系统配置', [('sliders', '业务参数', 'params.html'), ('message', '审核意见模板', 'opinion-templates.html'),
                  ('alert', '敏感词库', 'sensitive-words.html'), ('terminal', '操作日志', 'operation-logs.html')]),
    ],
}

# 不在侧边栏中的页面，高亮其所属的菜单项
ACTIVE_ALIAS = {
    'submit-news.html': 'my-submissions.html', 'submit-video.html': 'my-submissions.html',
    'submit-photo.html': 'my-submissions.html', 'submit-clue.html': 'my-submissions.html',
    'submit-success.html': 'my-submissions.html', 'resubmit.html': 'my-submissions.html',
    'submission-detail.html': 'my-submissions.html', 'version-history.html': 'my-submissions.html',
}

# 顶栏铃铛弹出的最近消息：（图标, 颜色, 标题, 摘要, 时间, 跳转）
MSG_PREVIEW = {
    'correspondent': [('undo', 'red', '稿件被退回', '《“青春志愿行”社区服务周纪实》被二审退回，请按意见修改', '1 小时前', 'resubmit.html'),
                      ('check-circle', 'green', '稿件终审采用', '《红色经典诵读活动》已终审采用，计入本院采用统计', '昨天 10:30', 'submission-detail.html')],
    'teacher': [('inbox', 'blue', '新的待审稿件', '陈雨桐提交了《科技启航主题团日活动》', '10 分钟前', 'review.html'),
                ('alert', 'red', '审核超时提醒', '《“代码为桥”乡村小学编程支教纪实》已超时 1.5 个工作日', '今天 09:00', 'dashboard.html')],
    'deputy': [('inbox', 'blue', '新的待审稿件', '《计算机学院“网络安全宣传周”系列活动》已通过指导老师审核', '20 分钟前', 'review.html'),
               ('alert', 'red', '审核超时提醒', '《计算机学院“程序设计月”闭幕式》已超时 0.5 个工作日', '今天 09:00', 'todo.html')],
    'reviewer': [('inbox', 'blue', '新的待办稿件', '《科技启航主题团日活动》已到达本环节', '30 分钟前', 'review.html'),
                 ('alert', 'red', '审核超时预警', '有 2 篇稿件已超过审核时限，已记入超时台账', '今天 09:00', 'todo.html'),
                 ('clock', 'orange', '即将超时提醒', '有 2 篇稿件剩余时限不足 1 个工作日', '今天 09:00', 'todo.html')],
    'admin': [('inbox', 'blue', '新的待三审稿件', '《科技启航主题团日活动》已通过二审', '15 分钟前', 'final-review.html'),
              ('alert', 'red', '审核超时预警', '当前有 5 篇稿件超时未处理', '今天 09:00', 'timeout-ledger.html'),
              ('globe', 'blue', '待发布升华网', '有 3 篇已采用新闻尚未标记为已发布', '昨天', 'publish-export.html'),
              ('bulb', 'orange', '新闻线索待跟进', '《校友返校讲述“北斗”研发故事》线索已终审采用', '昨天', 'clue-tracking.html')],
}
MSG_COLORS = {'red': ('var(--danger-bg)', 'var(--danger)'), 'green': ('var(--success-bg)', 'var(--success)'),
              'blue': ('var(--primary-light)', 'var(--primary)'), 'orange': ('var(--warn-bg)', 'var(--warn)')}

def msg_popover(role, count):
    key = 'reviewer' if role.startswith('reviewer') else role
    items = ''
    for i, (ic, color, title, desc, time, href) in enumerate(MSG_PREVIEW[key]):
        bg, fg = MSG_COLORS[color]
        u = ' unread' if i < count else ''
        items += (f'<div class="msg-item{u}" data-href="{href}"><div class="msg-ic" style="background:{bg};color:{fg}">{icon(ic, 18)}</div>'
                  f'<div class="msg-main"><div class="msg-title">{title}</div><div class="msg-desc">{desc}</div><div class="msg-time">{time}</div></div></div>')
    return (f'<div class="dropdown"><button class="icon-btn" data-dropdown aria-label="消息">{icon("bell", 18)}<span class="dot-badge" data-unread-count>{count}</span></button>'
            f'<div class="dropdown-menu msg-pop"><div class="mp-head"><b>消息通知</b><button class="link" data-action="read-all">全部已读</button></div>'
            f'<div class="mp-list">{items}</div><a class="mp-foot" href="messages.html">查看全部消息{icon("chev-r", 14)}</a></div></div>')


def role_rows(cur):
    rows = ''
    for k, r in ROLES.items():
        c = ' cur' if k == cur else ''
        rows += (f'<div class="dm-role{c}"><b>{r["name"]}</b><div class="dm-links">'
                 f'<a href="{ROOT}{r["pc"]}">PC 端</a><a href="{ROOT}{r["mobile"]}">移动端</a></div></div>')
    return rows


def pc_page(role, active, title, body, crumbs=None, css='', modals='', todo_count=None):
    r = ROLES[role]
    menu_key = 'reviewer' if role.startswith('reviewer') else role
    active = ACTIVE_ALIAS.get(active, active)
    groups = MENUS[menu_key]
    cur = next((i for i, (_, items) in enumerate(groups) if any(it[2] == active for it in items)), 0)
    nav = ''
    n_items = sum(len(items) for _, items in groups)
    for gi, (group, items) in enumerate(groups):
        links = ''
        for it in items:
            ic, label, href = it[:3]
            badge = it[3] if len(it) > 3 else None
            if badge == '{todo}':
                badge = todo_count
            b = f'<span class="nav-badge">{badge}</span>' if badge else ''
            on = ' class="active"' if href == active else ''
            links += f'<a href="{href}"{on}><i class="nav-ic">{icon(ic, 12)}</i>{label}{b}</a>'
        cls = ' open cur' if gi == cur else (' open' if n_items <= 12 else '')
        nav += (f'<div class="nav-sec{cls}"><button type="button" class="nav-group" data-action="toggle-nav" aria-expanded="{"true" if "open" in cls else "false"}">'
                f'<span>{group}</span>{icon("chev-d", 14)}</button><div class="nav-items">{links}</div></div>')
    home = r['pc'].split('/')[-1]
    crumbs = crumbs or [title]
    cur_title = crumbs[-1]
    home_tab = '' if active == home and len(crumbs) == 1 else f'<a class="vt" href="{home}">首页</a>'
    links = {it[1]: it[2] for _, items in groups for it in items}
    home_tab += ''.join(f'<a class="vt" href="{links[c]}">{c}</a>' for c in crumbs[:-1] if c in links and links[c] != home)
    close = f'<a class="vt-x" href="{home}" aria-label="关闭当前页签">{icon("x", 12)}</a>' if home_tab else ''
    msg_count = {'correspondent': 2, 'teacher': 2, 'deputy': 2, 'reviewer1': 3, 'reviewer2': 3, 'admin': 4}[role]
    user_menu = (f'<div class="dropdown"><div class="user-chip" data-dropdown role="button" tabindex="0">'
                 f'<img class="avatar" src="{r["avatar"]}" alt="{r["user"]}"><span class="uc-main"><b>{r["user"]}</b><small>{r["name"]}</small></span>{icon("chev-d", 14)}</div>'
                 f'<div class="dropdown-menu"><div class="dm-title">{r["user"]} · {r["dept"]}</div>'
                 f'<a href="{ROOT}{r["mobile"]}">{icon("mobile", 16)}切换到移动端</a>'
                 f'<div class="dm-sep"></div><div class="dm-title">切换演示角色和终端</div>{role_rows(role)}'
                 f'<div class="dm-sep"></div><a href="{ROOT}index.html" data-confirm="确认退出登录？演示环境将返回原型导航页。">{icon("logout", 16)}退出登录</a></div></div>')
    search_ph = '搜索稿件标题 / 编号 / 投稿人' if role != 'correspondent' else '搜索我的稿件标题 / 编号'
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · {r["name"]} · 团学组织新闻投稿平台</title>
<style>{PC_CSS}{css}</style>
<script>(function(){{var d=document.documentElement;function z(){{d.style.zoom=Math.max(innerWidth,1200)/1920}}z();addEventListener('resize',z)}})()</script>
</head>
<body data-user="{r["user"]}">
<header class="top">
  <a class="brand" href="{home}"><span class="brand-emblem">团</span><span class="brand-txt"><b>中南大学团学投稿平台</b><small>知行合一　经世致用</small></span></a>
  <div class="top-bar">
    <div class="top-right">
      {msg_popover(role, msg_count)}
      {user_menu}
      <a class="top-pill" href="{ROOT}index.html">{icon("grid", 14)}原型导航</a>
    </div>
  </div>
</header>
<aside class="side">
  <nav class="nav">{nav}</nav>
</aside>
<div class="main">
  <div class="vtabs">
    <button type="button" class="vt-back" data-action="go-back" data-href="{home}">{icon("chev-l", 14)}返回上一步</button>
    {home_tab}<span class="vt on">{cur_title}{close}</span>
    <div class="dropdown vt-more-wrap"><button type="button" class="vt-more" data-dropdown aria-label="页签操作">{icon("chev-d", 16)}</button>
      <div class="dropdown-menu"><label class="top-search">{icon("search", 14)}<input type="search" placeholder="{search_ph}" data-top-search></label>
        <div class="dm-sep"></div><button type="button" class="dm-item" data-action="reload">{icon("refresh", 16)}刷新当前页</button>
        <a href="{home}">{icon("x", 16)}关闭当前页签</a><button type="button" class="dm-item" data-toast="已关闭其他页签">{icon("x", 16)}关闭其他页签</button></div></div>
  </div>
  <main class="page">
{body}
  </main>
  <footer class="foot">2026 © 中南大学团学组织新闻投稿平台 · 校团委宣传部</footer>
</div>
{modals}
<script src="{ROOT}assets/mock-data.js"></script>
<script src="{ROOT}assets/app.js"></script>
</body>
</html>
'''


# ---------- 移动端框架 ----------
TABBARS = {
    'correspondent': [('home', '首页', 'home.html'), ('inbox', '我的投稿', 'my-submissions.html'),
                      ('plus', '投稿', None), ('bell', '消息', 'messages.html', 2),
                      ('user', '我的', 'profile.html')],
    'teacher': [('inbox', '待办', 'todo.html', 5), ('history', '已办', 'history.html'), ('bell', '消息', 'messages.html', 2)],
    'deputy': [('inbox', '待办', 'todo.html', '{todo}'), ('history', '已办', 'history.html'), ('bell', '消息', 'messages.html', 2)],
    'reviewer': [('inbox', '待办', 'todo.html', '{todo}'), ('list', '台账', 'ledger.html'), ('bell', '消息', 'messages.html', 3)],
    'admin': [('dashboard', '看板', 'home.html'), ('inbox', '终审', 'final-list.html', 6), ('bell', '消息', 'messages.html', 4)],
}


def m_page(role, title, body, tab=None, back=None, right='', foot='', css='', modals='', pc_link=None, todo_count=None):
    r = ROLES[role]
    key = 'reviewer' if role.startswith('reviewer') else role
    tabbar = ''
    if tab:
        items = ''
        for it in TABBARS[key]:
            ic, label, href = it[:3]
            badge = it[3] if len(it) > 3 else None
            if badge == '{todo}':
                badge = todo_count
            on = ' on' if href == tab else ''
            if ic == 'plus':
                items += f'<a href="submit-news.html" class="tb-btn" aria-label="新建投稿"><span class="tb-plus">{icon("plus", 24)}</span></a>'
                continue
            b = f'<span class="tb-badge" data-unread-count>{badge}</span>' if badge and ic == 'bell' else (
                f'<span class="tb-badge">{badge}</span>' if badge else '')
            items += f'<a href="{href}" class="{on.strip()}">{icon(ic, 22)}<span class="tb-txt">{label}</span>{b}</a>'
        tabbar = f'<nav class="tabbar">{items}</nav>'
    back_html = f'<a class="m-back" href="{back}" aria-label="返回">{icon("chev-l", 24)}</a>' if back else ''
    right_html = f'<div class="m-hr">{right}</div>' if right else ''
    foot_html = f'<div class="m-foot">{foot}</div>' if foot else ''
    pc = f'<a class="btn" href="{pc_link}">{icon("monitor", 16)}查看对应 PC 端页面</a>' if pc_link else ''
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{title} · 移动端 · {r["name"]} · 团学组织新闻投稿平台</title>
<style>{MOBILE_CSS}{css}</style>
</head>
<body class="app-stage" data-user="{r["user"]}">
<div class="phone">
  <div class="status-bar"><span>9:41</span><span class="sb-icons">{icon("signal", 17)}{icon("wifi", 17)}{icon("battery", 17)}</span></div>
  <header class="m-header">{back_html}<h1>{title}</h1>{right_html}</header>
  <main class="m-body">
{body}
  </main>
  {foot_html}{tabbar}
  <span class="home-ind"></span>
{modals}
</div>
<aside class="notes">
  <div class="card"><div class="n-role">{r["name"]} · 移动端</div><h3>{title}</h3><!--M_NOTES-->
  {pc}
  <a class="btn" href="{ROOT}index.html">{icon("grid", 16)}返回原型导航</a>
</aside>
<script src="{ROOT}assets/mock-data.js"></script>
<script src="{ROOT}assets/app.js"></script>
</body>
</html>
'''


def m_status(s):
    return tag(s)


__all__ = ['icon', 'escape']
