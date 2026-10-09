# 稿件详情：审核流转记录、四类稿件的完整字段展示、PC / 移动端详情布局（各角色共用）
from datetime import datetime, timedelta
from lib import icon, tag, type_tag, timeline, card, flow_steps
from data import TYPE_NAME, deputy_of
from common import counted, op_log_table

NODE = {'teacher': '指导老师审核', 'deputy': '副书记审核', 'r1': '一审', 'r2': '二审', 'r3': '三审终审'}
STATUS = {'teacher': '待指导老师审核', 'deputy': '待副书记审核', 'r1': '待一审', 'r2': '待二审', 'r3': '待三审'}
REVIEWER = {'r1': '刘子涵（一审员）', 'r2': '周明轩（二审员）', 'r3': '张静（校团委管理员）'}
PASS_OP = {'teacher': '内容基本符合要求，同意报送。', 'deputy': '内容导向正确，同意报送校团委一审。', 'r1': '要素齐全，同意流转二审。',
           'r2': '内容扎实，同意报送终审。'}
STEP_HOURS = {'teacher': 3.75, 'deputy': 2.4, 'r1': 18.75, 'r2': 6.3, 'r3': 20.5}


def stages(identity):
    """学生：指导老师 → 副书记 → 一审 → 二审 → 三审；教师：副书记 → 一审 → 二审 → 三审"""
    return (['teacher'] if identity == '学生' else []) + ['deputy', 'r1', 'r2', 'r3']


def who(sub, st):
    if st == 'teacher':
        return f'{sub["teacher"].split("（")[0]}（指导老师）'
    if st == 'deputy':
        return deputy_of(sub['college'])
    return REVIEWER[st]


def pass_times(sub):
    """各节点通过时间：可由 sub['times'] 指定，否则按提交时间顺延"""
    t = datetime.strptime(sub['time'], '%Y-%m-%d %H:%M')
    out = {}
    for st in stages(sub['identity']):
        t += timedelta(hours=STEP_HOURS[st])
        out[st] = (sub.get('times') or {}).get(st) or t.strftime('%Y-%m-%d %H:%M')
        t = datetime.strptime(out[st], '%Y-%m-%d %H:%M')
    return out


def arrive_time(sub, stage):
    sts = stages(sub['identity'])
    i = sts.index(stage)
    return sub['time'] if i == 0 else pass_times(sub)[sts[i - 1]]


def flow_records(sub, stage):
    """stage：当前待处理的节点（teacher / deputy / r1 / r2 / r3），或 adopted / rejected（终审结束）"""
    sts = stages(sub['identity'])
    times = pass_times(sub)
    done = sts if stage in ('adopted', 'rejected') else sts[:sts.index(stage)]
    items = []
    if stage == 'adopted':
        items.append(('ok', '三审终审：采用', tag('已终审采用'), f'{REVIEWER["r3"]} · {times["r3"]} · 计入采用统计', '内容质量较高，予以采用，计入学院采用统计。', ''))
    elif stage == 'rejected':
        items.append(('', '三审终审：不采用', tag('已终审不采用'), f'{REVIEWER["r3"]} · {times["r3"]} · 不计入采用', '同类题材近期已有报道，不予采用。', ''))
    else:
        items.append(('primary', f'到达{NODE[stage]}', tag(STATUS[stage]), f'{arrive_time(sub, stage)} · 系统 · 计时开始（3 个工作日）', '', ''))
    for st in reversed([x for x in done if x != 'r3']):
        items.append(('ok', f'{NODE[st]}通过', '', f'{who(sub, st)} · {times[st]}', PASS_OP[st], ''))
    items.append(('ok', '提交投稿（v1）', '', f'{sub["author"]}（{sub["identity"]} · {sub["college"]}）· {sub["time"]}', '', ''))
    return timeline(items)


def chart_cur(identity, stage):
    """节点流程图中当前节点的下标（0 为“开始”）"""
    sts = stages(identity)
    return len(sts) + 1 if stage in ('adopted', 'rejected') else sts.index(stage) + 1


def step_cur(identity, stage):
    """投稿人进度条（flow_steps）中当前节点的下标"""
    return chart_cur(identity, stage)


def default_logs(sub, stage):
    sts = stages(sub['identity'])
    times = pass_times(sub)
    done = sts if stage in ('adopted', 'rejected') else sts[:sts.index(stage)]
    rows = []
    if stage in ('adopted', 'rejected'):
        rows.append((times['r3'], REVIEWER['r3'], '三审终审：' + ('采用，统计归档改为“计入采用”' if stage == 'adopted' else '不采用'), '10.12.8.10'))
    ips = {'teacher': '10.12.30.8', 'deputy': '10.12.30.2', 'r1': '10.12.8.51', 'r2': '10.12.8.66'}
    for st in reversed([x for x in done if x != 'r3']):
        rows.append((times[st], who(sub, st), f'{NODE[st]}通过', ips[st]))
    rows.append((sub['time'], f'{sub["author"]}（投稿人）', '提交投稿，生成 v1', '10.12.34.21'))
    return rows


# ---------- 稿件内容：按类型展示投稿表单中的全部字段 ----------
EXT_COLOR = {'PDF': '#DF2027', 'DOC': '#2A8DC7', 'DOCX': '#2A8DC7', 'XLS': '#1BB975', 'XLSX': '#1BB975', 'ZIP': '#F29100', 'PPT': '#E8590C', 'PPTX': '#E8590C'}


def files_list(files, empty='未上传附件'):
    if not files:
        return f'<div class="att-empty">{empty}</div>'
    out = ''
    for name, size in files:
        ext = name.rsplit('.', 1)[-1].upper()
        out += (f'<div class="att"><span class="att-ic" style="background:{EXT_COLOR.get(ext, "#6B7785")}">{ext}</span>'
                f'<div class="att-main"><b title="{name}">{name}</b><span>{size}</span></div>'
                f'<button type="button" class="link" data-toast="已开始下载「{name}」，下载行为已记入操作日志">下载</button></div>')
    return f'<div class="att-list">{out}</div>'


def kv(rows, cls='c2'):
    return f'<dl class="kv {cls}">' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows) + '</dl>'


def sub_title(t):
    return f'<div class="form-section-title mt24">{t}</div>'


def news_content(sub):
    body = ''
    for i, p in enumerate(sub['paras']):
        body += f'<p>{p}</p>'
        if i < len(sub['images']) and i in (0, 2):
            k = 0 if i == 0 else 1
            body += f'<figure><img src="{sub["images"][k]}" alt="{sub["captions"][k]}"><figcaption>图{k + 1}：{sub["captions"][k]}</figcaption></figure>'
    intro = sub.get('intro') or '<span class="c-muted">未填写（选填）</span>'
    pics = ''.join(f'<figure><img src="{s}" alt="{c}"><figcaption>图片{i + 1}.jpg · {c}</figcaption></figure>'
                   for i, (s, c) in enumerate(zip(sub['images'], sub['captions'])))
    files = sub.get('files', [])
    return (f'<article class="article"><h2>{sub["title"]}</h2><div class="article-meta">'
            f'<span>{icon("user", 13)} 撰稿：{sub["writer"]}</span><span>{icon("calendar", 13)} 拍摄时间：{sub["shoot"]}</span>'
            f'<span>{icon("map", 13)} {sub["college"]}</span><span>正文约 {sum(len(p) for p in sub["paras"])} 字</span></div>'
            f'<div class="notice notice-info mb16">{icon("info", 15)}<div><b>活动简介：</b>{intro}</div></div>'
            f'<div class="article-body">{body}</div></article>'
            + sub_title(f'新闻配图（{len(sub["images"])}）') + (f'<div class="gallery">{pics}</div>' if pics else '<div class="att-empty">未上传配图（选填）</div>')
            + sub_title(f'附件（{len(files)}）') + files_list(files))


def video_content(sub):
    link = f'<a class="link" href="{sub["link"]}" target="_blank" rel="noopener">{sub["link"]}</a>'
    copy = f'<button type="button" class="link" data-action="copy" data-text="{sub["link"]} 提取码 {sub["code"]}">复制链接</button>'
    rows = [('视频标题', sub['title']), ('拍摄 / 撰稿人', sub['writer']), ('视频时长', sub['duration']), ('视频用途', sub['usage']),
            ('用途补充说明', sub.get('usage_note') or '—'), ('链接有效期', f'<span class="tag tag-success">{sub["expire"]}</span>'),
            ('永久云盘链接', f'{link}{copy}'), ('提取码', f'<b style="color:var(--text)">{sub["code"]}</b>')]
    files = sub.get('files', [])
    return (f'<div class="type-head">{icon("video", 18)}<b>{sub["title"]}</b><span class="hint">时长 {sub["duration"]} · {sub["usage"]}</span></div>'
            + kv(rows)
            + '<div class="grid mt16" style="grid-template-columns:320px minmax(0,1fr);gap:16px">'
            + f'<figure class="cover"><img src="{sub["cover"]}" alt="视频封面"><figcaption>{icon("play", 12)} 视频封面图</figcaption></figure>'
            + f'<div class="intro-box"><b>视频简介</b><p>{sub["intro"]}</p><div class="notice notice-warn mt12">{icon("alert", 15)}<div>视频文件存放于云盘，平台不校验链接有效性；审核时请打开链接确认可正常播放。</div></div></div></div>'
            + sub_title(f'附件（{len(files)}）') + files_list(files))


def photo_content(sub):
    rows = [('照片主题', sub['title']), ('拍摄人', sub['photographer']), ('拍摄时间', sub['shoot']), ('照片数量', f'{len(sub["photos"])} 张（原图存储）'),
            ('涉及重要领导', sub['leader'])]
    pics = ''.join(f'<figure><img src="{s}" alt="{n}"><figcaption><b>{n}</b><span>{size} · 原图</span><em>备注：{r}</em></figcaption></figure>'
                   for s, n, size, r in sub['photos'])
    return (f'<div class="type-head">{icon("image", 18)}<b>{sub["title"]}</b><span class="hint">{sub["photographer"]} 拍摄 · {sub["shoot"]}</span></div>'
            + kv(rows) + f'<div class="intro-box mt16"><b>场景简述</b><p>{sub["desc"]}</p></div>'
            + sub_title(f'照片原图与单张备注（{len(sub["photos"])}）') + f'<div class="gallery photo-gallery">{pics}</div>')


def clue_content(sub):
    rows = [('线索标题', sub['title']), ('线索类型', sub['clue_type']), ('线索来源', sub['source']), ('事件时间地点', sub['when_where']),
            ('是否接受采访', '接受采访' if sub['interview'] == '是' else '不接受采访'),
            ('可采访时间段', sub['interview_time'] if sub['interview'] == '是' else '—'),
            ('联系人', sub['contact']), ('联系方式', sub['phone']), ('处置状态', f'<span class="tag tag-warn">{sub["follow"]}</span>')]
    return (f'<div class="type-head">{icon("bulb", 18)}<b>{sub["title"]}</b><span class="hint">{sub["clue_type"]} · {sub["source"]}</span></div>'
            + kv(rows) + f'<div class="intro-box mt16"><b>线索内容</b><p>{sub["desc"]}</p></div>'
            + f'<div class="notice notice-info mt16">{icon("flow", 15)}<div>新闻线索终审采用后进入线索跟进：<b>待跟进 → 已跟进 → 已转为正式新闻</b>，由校团委安排采写。</div></div>')


def sub_content(sub):
    return {'新闻': news_content, '视频': video_content, '照片': photo_content, '线索': clue_content}[sub['type']](sub)


def base_rows(sub, status):
    teacher = sub['teacher'] if sub['identity'] == '学生' else '—（教师投稿无需指定）'
    return [('稿件编号', sub['id']), ('稿件类型', type_tag(sub['type'])), ('投稿人', sub['author']), ('投稿身份', sub['identity']),
            ('所属学院', sub['college']), ('指导老师', teacher), ('副书记', f'{deputy_of(sub["college"])}<span class="hint">学工系统</span>'),
            ('投稿时间', sub['time']), ('当前状态', tag(status)), ('是否计入采用', counted(status))]


# ---------- 稿件详情（投稿人稿件档案、审核人员稿件查询、管理员档案库） ----------
def full_detail(sub, status, stage, logs=None, versions=None, side='', head_extra=''):
    sts = [('content', '稿件内容'), ('chart', '审核流程'), ('flow', '审批记录')] + ([('ver', '修改历史')] if versions else []) + [('log', '操作日志')]
    tabs = ''.join(f'<button class="tab{" on" if i == 0 else ""}" data-tab="{k}">{n}</button>' for i, (k, n) in enumerate(sts))
    from workflow import node_chart
    panels = (f'<div class="tab-panel on card-body" data-panel="content">{sub_content(sub)}</div>'
              f'<div class="tab-panel card-body" data-panel="chart"><div class="wf-flow-panel">{node_chart(sub["identity"], chart_cur(sub["identity"], stage))}</div>'
              f'<div class="hint mt12">{"学生稿件：指导老师 → 副书记 → 一审 → 二审 → 三审终审" if sub["identity"] == "学生" else "教师稿件：副书记 → 一审 → 二审 → 三审终审"}；副书记为投稿人所在学院副书记，取自学工系统。</div></div>'
              f'<div class="tab-panel card-body" data-panel="flow">{flow_records(sub, stage)}</div>'
              + (f'<div class="tab-panel card-body" data-panel="ver">{versions}</div>' if versions else '')
              + f'<div class="tab-panel" data-panel="log">{op_log_table(logs or default_logs(sub, stage))}</div>')
    info = '<dl class="kv c1">' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in base_rows(sub, status)) + '</dl>'
    return f'''<div class="card" style="padding:20px 24px">{flow_steps(sub['identity'], step_cur(sub['identity'], stage))}</div>
<div class="grid g-main mt16">
  <div class="card" data-tabs-scope><div class="tabs" data-tabs>{tabs}</div>{panels}</div>
  <div class="grid" style="align-content:start">{side}{card('基础信息', info, 'file')}</div>
</div>'''


# ---------- 移动端 ----------
def m_kv(rows):
    return '<dl class="m-kv">' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows) + '</dl>'


def m_files(files):
    if not files:
        return '<div class="hint">未上传附件</div>'
    return ''.join(f'<div class="m-att"><span class="att-ic" style="background:{EXT_COLOR.get(n.rsplit(".", 1)[-1].upper(), "#6B7785")}">{n.rsplit(".", 1)[-1].upper()}</span>'
                   f'<div class="att-main"><b>{n}</b><span>{s}</span></div></div>' for n, s in files)


def m_content(sub):
    t = sub['type']
    if t == '新闻':
        body = ''
        for i, p in enumerate(sub['paras']):
            body += f'<p>{p}</p>'
            if i == 0 and sub['images']:
                body += f'<img src="{sub["images"][0]}" alt="{sub["captions"][0]}">'
        intro = sub.get('intro') or '未填写（选填）'
        pics = ''.join(f'<div class="file-item"><img src="{s}" alt="{c}"><div class="fi-meta"><span class="fi-name">{c}</span></div></div>' for s, c in zip(sub['images'], sub['captions']))
        return (f'<div class="m-card m-article"><h2>{sub["title"]}</h2><div class="m-item-meta" style="margin:0 0 10px">'
                f'<span>撰稿：{sub["writer"]}</span><span>{sub["college"]}</span><span>拍摄：{sub["shoot"]}</span></div>'
                f'<div class="notice notice-info" style="margin-bottom:10px">{icon("info", 14)}<div>{intro}</div></div>{body}'
                f'<div class="m-sub-t">新闻配图（{len(sub["images"])}）</div><div class="files">{pics}</div>'
                f'<div class="m-sub-t">附件（{len(sub.get("files", []))}）</div>{m_files(sub.get("files", []))}</div>')
    if t == '视频':
        return (f'<div class="m-card"><div class="m-item-title">{sub["title"]}</div><img class="m-cover" src="{sub["cover"]}" alt="视频封面">'
                + m_kv([('拍摄 / 撰稿人', sub['writer']), ('视频时长', sub['duration']), ('视频用途', sub['usage']), ('用途说明', sub.get('usage_note') or '—'),
                        ('云盘链接', f'<span style="word-break:break-all">{sub["link"]}</span>'), ('提取码', sub['code']), ('链接有效期', sub['expire'])])
                + f'<div class="m-sub-t">视频简介</div><div class="msg-desc">{sub["intro"]}</div>'
                + f'<div class="m-sub-t">附件（{len(sub.get("files", []))}）</div>{m_files(sub.get("files", []))}</div>')
    if t == '照片':
        pics = ''.join(f'<div class="m-photo"><img src="{s}" alt="{n}"><div><b>{n}</b><span>{size} · 原图</span><em>备注：{r}</em></div></div>' for s, n, size, r in sub['photos'])
        return (f'<div class="m-card"><div class="m-item-title">{sub["title"]}</div>'
                + m_kv([('拍摄人', sub['photographer']), ('拍摄时间', sub['shoot']), ('涉及重要领导', sub['leader']), ('照片数量', f'{len(sub["photos"])} 张')])
                + f'<div class="m-sub-t">场景简述</div><div class="msg-desc">{sub["desc"]}</div><div class="m-sub-t">照片与单张备注</div>{pics}</div>')
    return (f'<div class="m-card"><div class="m-item-title">{sub["title"]}</div>'
            + m_kv([('线索类型', sub['clue_type']), ('线索来源', sub['source']), ('事件时间地点', sub['when_where']),
                    ('接受采访', '是' if sub['interview'] == '是' else '否'), ('可采访时间', sub['interview_time'] if sub['interview'] == '是' else '—'),
                    ('联系人', sub['contact']), ('联系方式', sub['phone']), ('处置状态', sub['follow'])])
            + f'<div class="m-sub-t">线索内容</div><div class="msg-desc">{sub["desc"]}</div></div>')


def m_base(sub, status):
    teacher = sub['teacher'] if sub['identity'] == '学生' else '—（教师投稿无需指定）'
    return m_kv([('稿件编号', sub['id']), ('类型', TYPE_NAME[sub['type']]), ('学院', sub['college']), ('投稿人', f'{sub["author"]}（{sub["identity"]}）'),
                 ('指导老师', teacher), ('副书记', deputy_of(sub['college'])), ('投稿时间', sub['time']), ('当前状态', tag(status)), ('计入采用', counted(status))])


# ---------- 各角色列表行 → 对应类型的演示稿件 ----------
def sample_for(t, row=None):
    """以该类型的演示稿件为模板，套用列表行的编号、标题、投稿人、学院、身份、时间"""
    from data import FEATURED, VIDEO, PHOTO, CLUE
    base = dict({'新闻': FEATURED, '视频': VIDEO, '照片': PHOTO, '线索': CLUE}[t])
    if row:
        base.update({k: v for k, v in row.items() if v})
        base.pop('times', None)
        if base['identity'] == '教师':
            base['teacher'] = '—'
    return base
