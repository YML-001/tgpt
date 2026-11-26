# 多个角色共用的业务区块：稿件正文、投稿信息、流转记录、消息、排行榜等
from lib import icon, tag, type_tag, timeline, card, table, modal, filter_select, btn
from data import FEATURED, ADOPTED, IMG, RANKING, ARCHIVE, deputy_of, vice_of

RETURNED = dict(
    id='TG2026092203', title='“青春志愿行”社区服务周纪实', type='新闻', college='计算机学院',
    author='陈雨桐', identity='学生', teacher='李晓琳（计算机学院）', time='2026-09-20 11:40', shoot='2026-09-16',
    writer='陈雨桐', intro='计算机学院青年志愿者协会走进岳麓街道桃花岭社区，开展为期一周的志愿服务。',
    paras=[
        '9月14日至20日，计算机学院青年志愿者协会组织60余名志愿者走进岳麓街道桃花岭社区，开展为期一周的“青春志愿行”社区服务周活动。',
        '活动期间，志愿者们开设“银龄数字课堂”，手把手教社区老人使用智能手机挂号、缴费和视频通话，累计服务老人200余人次。',
        '“以前挂号要跑医院排队，现在孩子们教会了我在手机上操作。”社区居民说。志愿者们还为社区儿童开设了编程启蒙课，激发孩子们对科技的兴趣。',
    ],
    images=[IMG['volunteer'], IMG['students'], IMG['group']],
    captions=['志愿者为老人讲解手机使用', '编程启蒙课堂', '志愿者合影'],
    files=[('居民访谈记录.docx', '64 KB')],
)

RETURN_OPINIONS = [
    ('二审退回', '周明轩', '2026-09-22 14:18', 'v2',
     '第三段引用居民原话未注明姓名与身份，请补充；图 3 中有未成年人正脸，请替换或做打码处理后重新提交。'),
    ('一审退回', '刘子涵', '2026-09-19 10:05', 'v1',
     '标题缺乏新闻点，建议突出“社区服务周”；正文缺少活动时间、地点和参与人数等要素；配图仅 2 张，请补充至 3 张以上。'),
]


def article(sub, with_images=True):
    body = ''
    for i, p in enumerate(sub['paras']):
        body += f'<p>{p}</p>'
        if with_images and i < len(sub['images']) and i in (0, 2):
            k = 0 if i == 0 else 1
            body += (f'<figure><img src="{sub["images"][k]}" alt="{sub["captions"][k]}">'
                     f'<figcaption>图{k + 1}：{sub["captions"][k]}</figcaption></figure>')
    return (f'<article class="article"><h2>{sub["title"]}</h2><div class="article-meta">'
            f'<span>{icon("user", 13)} 撰稿：{sub["writer"]}</span><span>{icon("calendar", 13)} 拍摄时间：{sub["shoot"]}</span>'
            f'<span>{icon("map", 13)} {sub["college"]}</span><span>正文约 {sum(len(p) for p in sub["paras"])} 字</span></div>'
            f'<div class="notice notice-info mb16">{icon("info", 15)}<div><b>活动简介：</b>{sub["intro"]}</div></div>'
            f'<div class="article-body">{body}</div></article>')


def gallery(sub):
    items = ''.join(f'<figure><img src="{s}" alt="{c}"><figcaption>图片{i + 1}.jpg · {c}</figcaption></figure>'
                    for i, (s, c) in enumerate(zip(sub['images'], sub['captions'])))
    return f'<div class="gallery">{items}</div>'


def info_kv(sub, extra=None):
    if sub['identity'] == '职能部门老师':
        rows = [('稿件编号', sub['id']), ('稿件类型', type_tag(sub['type'])), ('所属部门', sub['college']), ('投稿人', sub['author']),
                ('投稿人身份', '职能部门老师'), ('副职领导', vice_of(sub['college'])), ('投稿时间', sub['time']), ('撰稿人', sub.get('writer', '—'))]
        return '<dl class="kv c2">' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows + (extra or [])) + '</dl>'
    rows = [('稿件编号', sub['id']), ('稿件类型', type_tag(sub['type'])), ('所属学院', sub['college']),
            ('投稿人', sub['author']), ('投稿人身份', sub['identity']),
            ('指导老师', sub['teacher'] if sub['identity'] == '学生' else '—（教师投稿无需指定）'),
            ('副书记', f'{deputy_of(sub["college"])} · 学工系统'), ('投稿时间', sub['time']), ('撰稿人', sub['writer']), ('拍摄时间', sub['shoot'])]
    rows += extra or []
    return '<dl class="kv c2">' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows) + '</dl>'


def featured_flow_timeline(upto='teacher'):
    """重点稿件当前的流转记录；upto 表示当前待处理的节点"""
    from detail import flow_records
    return flow_records(FEATURED, upto)


def returned_timeline():
    return timeline([
        ('danger', '二审退回', tag('已退回'), '周明轩（二审员）· 2026-09-22 14:18', RETURN_OPINIONS[0][4], 'danger'),
        ('ok', '一审通过', '', '刘子涵（一审员）· 2026-09-21 09:20', '修改到位，同意报送二审。', ''),
        ('ok', '副书记审核通过', '', f'{deputy_of("计算机学院")} · 2026-09-20 17:30', '内容导向正确，同意报送校团委一审。', ''),
        ('ok', '指导老师审核通过', '', '李晓琳（指导老师）· 2026-09-20 16:10', '已按意见修改，同意报送。', ''),
        ('primary', '修改后重新提交（v2）', '', '陈雨桐 · 2026-09-20 11:40 · 重新进入审核流程', '', ''),
        ('danger', '一审退回', '', '刘子涵（一审员）· 2026-09-19 10:05', RETURN_OPINIONS[1][4], 'danger'),
        ('ok', '副书记审核通过', '', f'{deputy_of("计算机学院")} · 2026-09-18 17:05', '同意报送校团委一审。', ''),
        ('ok', '指导老师审核通过', '', '李晓琳（指导老师）· 2026-09-18 15:20', '同意报送。', ''),
        ('ok', '提交投稿（v1）', '', '陈雨桐（学生 · 计算机学院）· 2026-09-18 09:30', '', ''),
    ])


def adopted_timeline():
    from detail import flow_records
    return flow_records(ADOPTED, 'adopted')


def op_log_table(rows, table_id='logTable'):
    trs = ''.join(f'<tr><td>{t}</td><td>{u}</td><td>{a}</td><td>{ip}</td></tr>' for t, u, a, ip in rows)
    return (f'<div class="table-wrap"><table class="tbl" id="{table_id}"><thead><tr><th>操作时间</th><th>操作人</th>'
            f'<th>操作行为</th><th>IP 地址</th></tr></thead><tbody>{trs}</tbody></table></div>')


def sensitive_card(t='新闻'):
    if t != '新闻':
        scope = {'视频': '视频标题、简介、用途说明', '照片': '照片主题、场景简述、单张备注', '线索': '线索标题、线索内容'}[t]
        return (f'<div class="sens-card"><div class="flex between"><b class="flex gap8">{icon("shield", 16)}敏感词检测结果</b>'
                f'<span class="tag tag-success">未命中</span></div>'
                f'<div class="hint mt8">检测模式：语义匹配 · 检测范围：{scope} · 高危词 <b class="c-success">0</b> 个 · 低危词 <b class="c-success">0</b> 个</div></div>')
    return (f'<div class="sens-card"><div class="flex between"><b class="flex gap8">{icon("shield", 16)}敏感词检测结果</b>'
            f'<span class="tag tag-warn">低危 1 处</span></div>'
            f'<div class="hint mt8">检测模式：语义匹配 · 高危词 <b class="c-success">0</b> 个 · 低危词 <b class="c-warn">1</b> 个</div>'
            f'<div class="mt8" style="font-size:13px;line-height:1.8">第 2 段：“……是学院<mark class="low">最牛</mark>的科研平台……”'
            f'<div class="hint">建议修改为客观表述，低危词不拦截提交</div></div></div>')


def msg_item(ic, color, title, desc, time, href, unread=False, tg=''):
    u = ' unread' if unread else ''
    colors = {'red': ('var(--danger-bg)', 'var(--danger)'), 'green': ('var(--success-bg)', 'var(--success)'),
              'blue': ('var(--primary-light)', 'var(--primary)'), 'orange': ('var(--warn-bg)', 'var(--warn)')}
    bg, fg = colors[color]
    return (f'<div class="msg-item{u}" data-href="{href}"><div class="msg-ic" style="background:{bg};color:{fg}">{icon(ic, 20)}</div>'
            f'<div class="msg-main"><div class="msg-title">{title}{tg}</div><div class="msg-desc">{desc}</div></div>'
            f'<div class="msg-time">{time}</div></div>')


def messages_page_body(items, desc='稿件审核结果、待办提醒与系统通知，PC 端与移动端实时同步'):
    from lib import page_head, btn
    n = sum(1 for i in items if len(i) > 6 and i[6])
    html = ''.join(msg_item(*i[:6], unread=(len(i) > 6 and i[6])) for i in items)
    return page_head('消息通知', desc, btn('全部标为已读', '', 'check', 'data-action="read-all"')) + \
        f'<div class="card"><div class="tabs" data-tabs><button class="tab on" data-tab="all" data-filter-list=".msg-list">全部消息<span class="cnt">{len(items)}</span></button>' \
        f'<button class="tab" data-tab="unread" data-filter-list=".msg-list">未读<span class="cnt" data-unread-count>{n}</span></button></div>' \
        f'<div class="msg-list">{html}</div></div>'


DETAIL_TPL = [('“青春心向党”主题团日活动纪实', '新闻', '已终审采用'), ('迎新晚会精彩瞬间', '照片', '已发布'),
              ('青年志愿服务队走进社区', '新闻', '待二审'), ('学生科研团队获省级竞赛一等奖', '新闻', '已终审采用'),
              ('“三下乡”社会实践纪实短片', '视频', '已终审不采用'), ('优秀毕业生返校分享成长故事', '线索', '待一审'),
              ('学风建设月系列活动', '新闻', '已退回')]
DETAIL_AUTHORS = [('李明', '学生'), ('王悦', '学生'), ('赵晨', '教师'), ('周宁', '学生'), ('孙浩', '学生'), ('吴静', '教师'), ('郑可', '学生')]
COUNTED = ('已终审采用', '已发布')


def counted(st):
    return '<span class="c-success fw">是</span>' if st in COUNTED else '<span class="c-muted">否</span>'


def college_subs(college, n=7):
    """某学院本统计周期的稿件明细（稿件档案中的真实示例 + 补足的演示数据）"""
    rows = [r for r in ARCHIVE if r[3] == college]
    seed = sum(map(ord, college))
    i = 0
    while len(rows) < n:
        title, t, st = DETAIL_TPL[(seed + i) % len(DETAIL_TPL)]
        author, ident = DETAIL_AUTHORS[(seed + i * 3) % len(DETAIL_AUTHORS)]
        day = 28 - (seed + i * 4) % 27
        rows.append((f'TG202609{day:02d}{80 + i:02d}', title, t, college, author, ident, f'2026-09-{day:02d}', st))
        i += 1
    return sorted(rows, key=lambda r: r[6], reverse=True)


def college_detail_modal(mid, college, stat):
    """排行榜内“查看本院明细”弹窗：不离开排行榜菜单"""
    tid = mid + 'Table'
    subs = college_subs(college)
    trs = ''.join(f'<tr data-type="{t}" data-status="{st}"><td><div class="fw">{title}</div><div class="t-sub">{sid}</div></td>'
                  f'<td>{type_tag(t)}</td><td>{author}<div class="t-sub">{ident}</div></td><td>{d}</td><td>{tag(st)}</td>'
                  f'<td>{counted(st)}</td></tr>'
                  for sid, title, t, _, author, ident, d, st in subs)
    sub, adopt, back = stat
    kv = ''.join(f'<div><b>{v}</b><span>{k}</span></div>' for k, v in
                 (('投稿量', sub), ('采用量', adopt), ('退回量', back), ('采用率', f'{adopt / sub * 100:.1f}%')))
    heads = ['稿件标题 / 编号', '类型', '投稿人', ('投稿时间', 'data-sort'), '当前状态', '是否计入采用']
    body = (f'<div class="rk-sum">{kv}</div>'
            f'<div class="flex between mb12"><span class="hint">统计周期：2026—2027 学年 · 共 {len(subs)} 篇最近稿件</span>'
            f'<div class="flex gap8">{filter_select(tid, "type", "全部类型", ["新闻", "视频", "照片", "线索"])}'
            f'{filter_select(tid, "status", "全部状态", ["待一审", "待二审", "已退回", "已终审采用", "已终审不采用", "已发布"])}</div></div>'
            + table(tid, heads, [trs], page_size=7))
    foot = ('<button class="btn" data-close>关闭</button>'
            f'<button type="button" class="btn btn-primary" data-action="export-csv" data-table="#{tid}" data-filename="{college}稿件明细">'
            f'{icon("download", 15)}导出明细</button>')
    return modal(mid, f'{college} · 稿件明细', body, foot, 'modal-xl')


def m_college_detail_modal(mid, college, stat):
    subs = college_subs(college)
    items = ''.join(f'<div class="rk-item"><div class="flex between"><b>{title}</b>{tag(st)}</div>'
                    f'<div class="hint">{sid} · {t} · {author}（{ident}） · {d}</div>'
                    f'<div class="hint">计入采用：{counted(st)}</div></div>'
                    for sid, title, t, _, author, ident, d, st in subs)
    sub, adopt, back = stat
    kv = ''.join(f'<div><b>{v}</b><span>{k}</span></div>' for k, v in
                 (('投稿', sub), ('采用', adopt), ('退回', back), ('采用率', f'{adopt / sub * 100:.1f}%')))
    return modal(mid, f'{college} · 稿件明细', f'<div class="rk-sum">{kv}</div><div class="hint mb8">统计周期：2026—2027 学年</div>{items}',
                 '<button class="btn btn-primary" data-close>我知道了</button>')


def rank_rows(college_link=None, own='计算机学院', data=None, key='ranking', action=None):
    rows = []
    data = data or RANKING
    top = max(r[2] for r in data)
    for i, (c, sub, adopt, back) in enumerate(sorted(data, key=lambda r: -r[2])):
        no = i + 1
        rc = f' r{no}' if no <= 3 else ''
        rate = f'{adopt / sub * 100:.1f}%'
        name = c
        if college_link:
            name = college_link(c)
        me = ' style="background:#F2F9FE"' if c == own else ''
        me_tag = ' <span class="tag tag-primary">本院</span>' if c == own else ''
        rows.append(f'<tr{me}><td data-value="{no}"><span class="rank-no{rc}">{no}</span></td><td><div class="flex gap8">{name}{me_tag}</div></td>'
                    f'<td class="num">{sub}</td><td class="num fw" style="color:var(--text)">{adopt}</td><td class="num">{back}</td>'
                    f'<td data-value="{adopt / sub:.3f}"><div class="flex gap8"><div class="progress" style="width:90px"><i style="width:{adopt / top * 100:.0f}%"></i></div>{rate}</div></td>'
                    + (f'<td>{action(c)}</td>' if action else '') + '</tr>')
    return rows


def donut(parts, size=140, stroke=22, center=('', '')):
    total = sum(v for _, v, _ in parts)
    r = (size - stroke) / 2
    circ = 2 * 3.14159 * r
    off = 0
    segs = ''
    for _, v, color in parts:
        ln = v / total * circ
        segs += (f'<circle cx="{size / 2}" cy="{size / 2}" r="{r}" fill="none" stroke="{color}" stroke-width="{stroke}" '
                 f'stroke-dasharray="{ln:.1f} {circ - ln:.1f}" stroke-dashoffset="{-off:.1f}" transform="rotate(-90 {size / 2} {size / 2})"/>')
        off += ln
    legend = ''.join(f'<div><i style="background:{c}"></i>{n}<b>{v}</b><span class="c-muted" style="width:44px;text-align:right">{v / total * 100:.0f}%</span></div>'
                     for n, v, c in parts)
    return (f'<div class="donut-wrap"><svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">{segs}'
            f'<text x="50%" y="46%" text-anchor="middle" font-size="22" font-weight="700" fill="#3C444F">{center[0]}</text>'
            f'<text x="50%" y="62%" text-anchor="middle" font-size="11" fill="#9096A2">{center[1]}</text></svg>'
            f'<div class="donut-legend">{legend}</div></div>')


def bars(data, colors=('#3087CC', '#9CBFDA'), height=200):
    """data: [(标签, [数值...])]，堆叠柱状图"""
    top = max(sum(v) for _, v in data)
    cols = ''
    for label, vals in data:
        segs = ''.join(f'<i style="height:{v / top * (height - 50):.0f}px;background:{colors[j]}"></i>' for j, v in enumerate(vals))
        cols += f'<div class="bar-col"><em>{sum(vals)}</em><div class="bar-stack">{segs}</div><span>{label}</span></div>'
    return f'<div class="bars" style="height:{height}px">{cols}</div>'


# 投稿、修改重提每次打开都先确认。不写入本地存储，标题栏不提供关闭。
def standard_ack_modal():
    info = '欢迎使用新升华网投稿系统！存在技术问题请联系校团委网络信息部（升华工作室）。'
    note1 = '此标准暂行，若有投递不符合内容要求或格式要求的稿件审核处将不再修改直接打回。有不同意见者请通过各二级学院网络信息部提出问题和反馈。经讨论后酌情进行调整。'
    note2 = '请严格按照以下「升华网稿件审核标准」投稿，审核人员将在两个工作日内完成审核，审核结果将发送至预留邮箱，如有任何问题请联系团委宣传部（0731-88836525）。'
    intro = '为了帮助通讯员更好地把握稿件质量，提高稿件的通过率，切实提升中南大学升华网的整体稿件质量，现将审核标准（暂行）公布如下，请广大通讯员参照标准执行。'
    ending = '此标准暂行，若有投递不符合内容要求或格式要求的稿件审核处将不再修改直接打回。有不同意见者请通过各二级学院网络信息部提出问题和反馈。经讨论后酌情进行调整。如存在技术问题，请联系校团委宣传部。'
    content_items = [
        '1、通讯员应确保其所提供稿件的原创性及合法性，严禁抄袭，一经发现查实，立即取消通讯员资格并通报批评；对于侵犯他人之合法权益（包括但不限于著作权）的，由稿件提供者承担相应法律责任。',
        '2、请根据稿件的性质，按照栏目设定投递到最适合的栏目中。各学院投稿以学院层面团学工作新闻（各学院团委和学生会所组织的学生活动、会议等）、班级团日活动为主要稿件来源，投送板块为团学资讯板块。',
        '3、稿件篇幅为400-800字之间，综合性稿件篇幅为400-1000字之间。要提高新闻报道的专业性，新闻6要素（时间、地点、人物、事件的起因、经过、结果）要齐全，最好配发1-2幅图片，以提高稿件通过率。',
        '4、稿件涉及学生生活、校园活动、团学活动等方面的，要写出活动的精彩之处，突出活动的主题、意义，并配发照片。',
        '5、稿件流水账、套路化、语句不通、词不达意、情节晦涩难懂、错别字多，内容言之无物，缺乏可读性，版式凌乱，段落参差，乱用标点，大量空行的，一律做退稿处理。',
    ]
    format_items = [
        '1、文章末尾请用括号注明作者的学院和姓名，需另起一行。作者栏请标注为撰稿，照片拍摄者栏请标注为摄影，审核老师栏请标注为审核。',
        '2、正文字体为宋体、3号字（21px）、字体颜色为黑色（000000）、2倍行间距，正文首行缩进，文字部分为两端对齐，图片为居中对齐，图片宽度设置为500px。投稿时需按此标准设定。',
        '3、「完整标题」长度不限，「标题」要短，否则后面部分的文字会不显示，影响阅读。',
        '4、文章正文中不需要再次写入标题。',
        '5、正文和标题均应体现投稿人所在单位（学院），正文第一段中所在单位（学院）请写全称。',
        '6、文字稿要求配有图片。要将图片大小控制在150KB 以内，较长的边控制在500像素为宜。如果只有一张或两张图片，要优先插入正文中（正文中）。图片居中放置。图片需能够看清人物主体或想突出的内容。',
        '7、切勿重复投稿，包括任何形式的重复。',
        '8、若有需要上传图片附件或文件附件的情况，请事先检查所附链接是否能打开，否则审核处无法对其进行操作。',
        '9、如遇图片不能插入的问题，可尝试从其他文件和网页将图片复制入投稿内容区域，或尝试调整浏览器，如360浏览器等。',
        '10、若图片及文字排版存在问题，建议在Word文档中先行排版，完成之后统一复制。',
    ]
    def paras(items):
        return ''.join('<p>' + item + '</p>' for item in items)
    body = (
        '<div class="notice notice-info"><span class="std-kicker">信息</span><div>' + info + '</div></div>'
        + '<div class="notice notice-warn"><span class="std-kicker">注意</span><div>' + note1 + '</div></div>'
        + '<div class="notice notice-warn"><span class="std-kicker">注意</span><div>' + note2 + '</div></div>'
        + '<article class="std-doc"><h2>升华网稿件审核标准</h2><p>' + intro + '</p>'
        + '<h3>一、内容要求</h3>' + paras(content_items)
        + '<h3>二、格式要求</h3>' + paras(format_items)
        + '<p>' + ending + '</p></article>'
    )
    foot = btn('我已知晓', 'btn-primary btn-lg', None, 'id="stdAckBtn" data-action="ack-standard"')
    return ('<div class="modal std-ack open" id="stdAck" data-static="1" role="dialog" aria-modal="true" aria-labelledby="stdAckTitle">'
            '<div class="modal-box"><div class="modal-head"><span id="stdAckTitle">升华网稿件审核标准</span></div>'
            '<div class="modal-body">' + body + '</div><div class="modal-foot">' + foot + '</div></div></div>')


def hbars(data, colors=('#3087CC', '#B0CEE4')):
    """data: [(名称, 主值, 总值)]"""
    top = max(t for _, _, t in data)
    out = ''
    for name, a, t in data:
        out += (f'<div class="hbar"><span class="hb-name" title="{name}">{name}</span><div class="hb-track">'
                f'<i style="width:{a / top * 100:.0f}%;background:{colors[0]}"></i><i style="width:{(t - a) / top * 100:.0f}%;background:{colors[1]}"></i></div>'
                f'<span class="hb-val">{a} / {t}</span></div>')
    return out
