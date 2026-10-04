# 移动端（H5 / 小程序，手机框展示）：全部角色
from lib import icon, tag, type_tag, btn, a_btn, options, field, m_page, write, teacher_picker, m_editor
from data import MY_SUBS, RANKING, FEATURED, ADOPTED, IMG, R1_TODO, R2_TODO, R3_TODO, TEACHER_TODO, TYPE_ICON
from common import RETURNED, RETURN_OPINIONS, returned_timeline, featured_flow_timeline, msg_item, m_college_detail_modal
from review import q
from pages_corr import type_switch

SID = FEATURED['id']
GROUP = {'草稿': '草稿', '待指导老师审核': '审核中', '待一审': '审核中', '待二审': '审核中', '待三审': '审核中',
         '已退回': '已退回', '已终审采用': '已采用', '已发布': '已采用', '已终审不采用': '未采用'}
DURATION_INPUT = r'<input class="input" name="duration" required placeholder="如 03:25" data-pattern="^\d{1,3}:\d{2}$" data-pattern-msg="请按“分:秒”格式填写">'
PHONE_INPUT = r'<input class="input" name="phone" type="tel" inputmode="tel" required placeholder="11 位手机号" data-pattern="^1[3-9]\d{9}$" data-pattern-msg="请填写正确的 11 位手机号">'


def remain_m(text, lv):
    c = {'over': 'c-danger', 'warn': 'c-warn', 'ok': 'c-success'}[lv]
    i = icon('alert', 12) if lv == 'over' else icon('clock', 12)
    return f'<span class="{c} flex" style="gap:3px">{i}{text}</span>'


def seg(items, target, key='group'):
    return '<div class="m-seg" data-tabs>' + ''.join(
        f'<button class="{"on" if i == 0 else ""}" data-tab="s{i}" data-filter-items="{target}" data-filter-key="{key}" data-filter-value="{v}">{n}</button>'
        for i, (n, v) in enumerate(items)) + '</div>'


def m_article(sub):
    body = ''
    for i, p in enumerate(sub['paras']):
        body += f'<p>{p}</p>'
        if i == 0:
            body += f'<img src="{sub["images"][0]}" alt="{sub["captions"][0]}">'
    return (f'<div class="m-card m-article"><h2>{sub["title"]}</h2><div class="m-item-meta" style="margin:0 0 10px">'
            f'<span>撰稿：{sub["writer"]}</span><span>{sub["college"]}</span><span>拍摄：{sub["shoot"]}</span></div>'
            f'<div class="notice notice-info" style="margin-bottom:10px">{icon("info", 14)}<div>{sub["intro"]}</div></div>{body}'
            f'<div class="files" style="margin-top:6px">' + ''.join(f'<div class="file-item"><img src="{s}" alt="{c}"><div class="fi-meta"><span class="fi-name">{c}</span></div></div>' for s, c in zip(sub['images'], sub['captions'])) + '</div></div>')


def m_kv(rows):
    return '<dl class="m-kv">' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows) + '</dl>'


# =============== 投稿人 ===============
C = 'correspondent'
CP = 'mobile/correspondent/'


def cw(file, title, body, **kw):
    write(CP + file, m_page(C, title, body, **kw))


def identity_block(identity='学生', teacher='王海峰（计算机学院）'):
    s = ' checked' if identity == '学生' else ''
    t = ' checked' if identity == '教师' else ''
    return f'''<div class="m-form-title">投稿人信息</div><div class="m-form">
<div class="field"><label class="lbl">投稿人</label><div>陈雨桐 · 计算机学院</div></div>
<div class="field"><label class="lbl req">投稿人身份</label><div class="radio-group"><label class="radio-card"><input type="radio" name="identity" value="学生"{s} required>学生</label><label class="radio-card"><input type="radio" name="identity" value="教师"{t}>教师</label></div></div>
<div class="field" data-show-when="identity=学生"><label class="lbl req">指导老师</label>{teacher_picker(teacher)}<div class="hint">默认预填上次选择的指导老师，可搜索其他学院；学生稿件先由指导老师审核</div></div>
<div class="field hidden" data-show-when="identity=教师"><div class="notice notice-info">{icon('info', 14)}<div>教师投稿无需指导老师，提交后直接进入校团委一审</div></div></div>
</div>'''


def submit_foot(sensitive, type_name):
    return (f'<span class="hidden" data-draft-status></span>' +
            btn('存草稿', 'w-auto', 'save', 'data-action="save-draft"') +
            btn('提交投稿', 'btn-primary', 'send', f'data-action="submit" data-form="#mForm" data-sensitive="{sensitive}" data-confirm="提交后将进入审核流程，审核期间不可修改。确认提交吗？" data-msg="投稿提交成功" data-next="submit-success.html?type={type_name}&identity={{identity}}"'))


def m_upload(label, remark=False, req=True, hint='支持 JPG / PNG，原图上传', files=None):
    r = ' data-remark' if remark else ''
    rq = ' data-required data-min-files="1"' if req else ''
    items = ''.join(f'<div class="file-item"><img src="{s}" alt="{n}"><button type="button" class="fi-del" aria-label="删除">×</button><div class="fi-meta"><span class="fi-name">{n}</span><span>原图</span></div></div>' for s, n in (files or []))
    return (f'<div class="field"><label class="lbl{" req" if req else ""}">{label}</label><div class="upload-field"><label class="upload">{icon("camera", 22)}<span>拍照或从相册选择</span><span class="hint">{hint}</span>'
            f'<input type="file" multiple accept="image/*" data-upload="img" data-max-mb="30"{r}{rq} data-label="{label}"></label><div class="files">{items}</div>'
            f'<div class="hint mt8">已上传 <b data-file-count>{len(files or [])}</b> 张</div></div></div>')


def c_home():
    recent = ''
    for sid, title, t, ident, teacher, time, st in MY_SUBS[1:4]:
        recent += (f'<a class="m-item" href="detail.html"><div class="m-item-top"><div class="m-item-title">{title}</div></div>'
                   f'<div class="m-item-foot"><span class="c-muted">{t} · {time[5:]}</span>{tag(st)}</div></a>')
    ranks = ''.join(f'<div class="rank-row{" me" if c == "计算机学院" else ""}"><span class="rank-no r{i + 1}">{i + 1}</span><span class="rr-name">{c}</span><span class="rr-bar"><i style="width:{a / 52 * 100:.0f}%"></i></span><b>{a}</b></div>'
                    for i, (c, s, a, b) in enumerate(RANKING[:3]))
    grid = [('submit-news.html', 'file', '新闻投稿', '文字 + 图片', 'blue'), ('submit-video.html', 'video', '视频投稿', '云盘链接', 'purple'),
            ('submit-photo.html', 'image', '照片投稿', '批量原图', 'green'), ('submit-clue.html', 'bulb', '新闻线索', '未成文线索', 'orange')]
    g = ''.join(f'<a class="svc {c}" href="{h}"><b>{n}<i>{icon("chev-r", 12)}</i></b><small>{d}</small><span class="svc-ic">{icon(i, 26)}</span></a>'
                for h, i, n, d, c in grid)
    body = f'''<div class="m-hero"><h2>下午好，陈雨桐</h2><p>计算机学院 · 学生</p>
<div class="m-stats"><div><b>12</b><span>本学年投稿</span></div><div><b>5</b><span>已采用</span></div><div><b>4</b><span>审核中</span></div><div><b>1</b><span>被退回</span></div></div></div>
<div class="svc-grid">{g}</div>
<a class="m-item" href="resubmit.html" style="box-shadow:inset 3px 0 0 var(--danger),var(--shadow-sm)"><div class="m-item-top"><div class="m-item-title">稿件被退回，待修改</div>{tag('已退回')}</div>
<div class="m-item-meta"><span>《“青春志愿行”社区服务周纪实》</span></div><div class="msg-desc">二审意见：第三段引用居民原话未注明姓名与身份……</div></a>
<div class="m-section"><span>最近投稿</span><a href="my-submissions.html">全部 ›</a></div>{recent}
<div class="m-card"><div class="m-card-title">全校学院排行榜<a href="ranking.html">完整榜单 ›</a></div>{ranks}</div>'''
    cw('home.html', '团学投稿', body, tab='home.html', pc_link='../../pc/correspondent/dashboard.html')


def c_forms():
    secret = f'<div class="notice notice-danger" style="margin-bottom:4px">{icon("lock", 14)}<div>涉密信息请勿上网 · 内容每 30 秒自动保存</div></div>'
    news = type_switch('submit-news.html') + f'''<form id="mForm" data-autosave novalidate>{secret}{identity_block()}
<div class="m-form-title">稿件内容</div><div class="m-form">
{field('新闻标题', '<input class="input" id="mTitle" name="title" required maxlength="50" placeholder="建议 30 字以内">', req=True)}
{field('撰稿人', '<input class="input" name="writer" required placeholder="多人用顿号分隔">', req=True)}
{field('拍摄时间', '<input type="date" class="input" name="shoot" required>', req=True)}
{field('活动简介', '<textarea class="textarea" id="mIntro" name="intro" required placeholder="一句话概括活动"></textarea>', req=True)}
<div class="field"><label class="lbl req">新闻正文</label>{m_editor('mEditor')}</div>
</div>
<div class="m-form-title">新闻配图</div><div class="m-form">{m_upload('新闻配图')}</div></form>'''
    cw('submit-news.html', '新闻投稿', news, back='home.html', foot=submit_foot('#mTitle,#mIntro,#mEditor', '新闻'), pc_link='../../pc/correspondent/submit-news.html')

    usage = options(['新闻报道素材', '宣传片素材', '活动纪实存档', '短视频平台发布', '其他'], '请选择')
    video = type_switch('submit-video.html') + f'''<form id="mForm" data-autosave novalidate>{secret}{identity_block()}
<div class="m-form-title">视频信息</div><div class="m-form">
{field('视频标题', '<input class="input" id="mTitle" name="title" required placeholder="请输入视频标题">', req=True)}
{field('视频简介', '<textarea class="textarea" id="mIntro" name="intro" required placeholder="简要介绍视频内容"></textarea>', req=True)}
{field('拍摄 / 撰稿人', '<input class="input" name="writer" required>', req=True)}
{field('视频时长', DURATION_INPUT, req=True)}
{field('视频用途', f'<select class="select" name="usage" required>{usage}</select>', req=True)}
</div>
<div class="m-form-title">永久云盘链接</div>
<div class="notice notice-warn" style="margin-bottom:10px">{icon('alert', 14)}<div>请提供<b>永久有效</b>的云盘链接，不支持 7 天等临时分享链接；链接失效将被退回。</div></div>
<div class="m-form">{field('云盘链接', '<input class="input" name="link" required placeholder="https://pan.baidu.com/s/……" data-pattern="^https?://" data-pattern-msg="请填写完整链接">', req=True)}{field('提取码', '<input class="input" name="code" placeholder="选填">')}</div></form>'''
    cw('submit-video.html', '视频投稿', video, back='home.html', foot=submit_foot('#mTitle,#mIntro', '视频'), pc_link='../../pc/correspondent/submit-video.html')

    photo = type_switch('submit-photo.html') + f'''<form id="mForm" data-autosave novalidate>{secret}{identity_block()}
<div class="m-form-title">照片信息</div><div class="m-form">
{field('照片主题', '<input class="input" id="mTitle" name="title" required placeholder="如：新生开学典礼">', req=True)}
{field('拍摄人', '<input class="input" name="photographer" required>', req=True)}
{field('拍摄时间', '<input type="date" class="input" name="shoot" required>', req=True)}
{field('场景简述', '<textarea class="textarea" id="mIntro" name="desc" required placeholder="简述拍摄场景"></textarea>', req=True)}
{field('涉及重要领导', '<input class="input" name="leader" required placeholder="无则填“无”">', req=True)}
</div>
<div class="m-form-title">上传原图（可为每张添加备注）</div><div class="m-form">{m_upload('照片原图', remark=True, hint='支持批量选择，单张不超过 30MB')}</div></form>'''
    cw('submit-photo.html', '照片投稿', photo, back='home.html', foot=submit_foot('#mTitle,#mIntro', '照片'), pc_link='../../pc/correspondent/submit-photo.html')

    src = options(['本人亲历', '他人提供', '媒体报道', '网络信息', '其他'], '请选择')
    clue = type_switch('submit-clue.html') + f'''<form id="mForm" data-autosave novalidate>{identity_block()}
<div class="m-form-title">线索内容</div><div class="m-form">
{field('线索标题', '<input class="input" id="mTitle" name="title" required placeholder="一句话概括线索">', req=True)}
{field('详细描述', '<textarea class="textarea" id="mIntro" name="desc" required placeholder="人物 / 事件情况与新闻价值"></textarea>', req=True)}
{field('线索来源', f'<select class="select" name="source" required>{src}</select>', req=True)}
<div class="field"><label class="lbl req">是否接受采访</label><div class="radio-group"><label class="radio-card"><input type="radio" name="interview" value="是" checked required>接受</label><label class="radio-card"><input type="radio" name="interview" value="否">不接受</label></div></div>
<div class="field" data-show-when="interview=是"><label class="lbl req">可采访时间段</label><input class="input" name="interviewTime" required placeholder="如：工作日 14:00—17:00"></div>
</div>
<div class="m-form-title">联系方式</div><div class="m-form">{field('联系人', '<input class="input" name="contact" required>', req=True)}{field('联系方式', PHONE_INPUT, req=True)}</div></form>'''
    cw('submit-clue.html', '新闻线索', clue, back='home.html', foot=submit_foot('#mTitle,#mIntro', '线索'), pc_link='../../pc/correspondent/submit-clue.html')


def c_success():
    def steps(names, cur):
        return '<div class="m-steps">' + ''.join(f'<div class="{"done" if i < cur else "cur" if i == cur else ""}"><i></i>{n}</div>' for i, n in enumerate(names)) + '</div>'
    body = f'''<div class="m-result"><div class="big-ic">{icon('check', 38)}</div><h2>投稿提交成功</h2><p>稿件编号 TG2026093005 · <span data-param-text="type">新闻</span>投稿</p></div>
<div class="m-card" data-when-param-hide="identity=教师"><b>已进入【待指导老师审核】</b><div class="msg-desc">指导老师王海峰将在 3 个工作日内处理</div>{steps(['提交', '指导老师', '一审', '二审', '终审'], 1)}</div>
<div class="m-card hidden" data-when-param="identity=教师"><b>已进入【待一审】</b><div class="msg-desc">教师投稿无需指导老师审核，校团委一审员将在 3 个工作日内处理</div>{steps(['提交', '一审', '二审', '终审'], 1)}</div>
<a class="btn btn-primary btn-block" href="my-submissions.html?new=TG2026093005">查看我的投稿</a>
<a class="btn btn-block mt12" href="submit-news.html">继续投稿</a>
<a class="btn btn-block mt12" href="home.html">返回首页</a>'''
    cw('submit-success.html', '提交成功', body, pc_link='../../pc/correspondent/submit-success.html')


def c_my():
    items = (f'<a class="m-item hidden" href="detail.html" data-when-param="new=TG2026093005" data-highlight data-group="审核中"><div class="m-item-top"><div class="m-item-title">【新提交】你刚刚提交的稿件</div></div>'
             f'<div class="m-item-foot"><span class="c-muted">TG2026093005 · 刚刚</span>{tag("待指导老师审核")}</div></a>')
    for sid, title, t, ident, teacher, time, st in MY_SUBS:
        href = 'resubmit.html' if st == '已退回' else ('submit-news.html' if st == '草稿' else 'detail.html')
        status = tag(st)
        if sid == 'TG2026092203':
            status = f'<span data-when-param-hide="re=1">{tag(st)}</span><span class="hidden" data-when-param="re=1">{tag("待指导老师审核")}</span>'
        extra = '<div class="msg-desc c-danger">二审退回：第三段引用居民原话未注明姓名与身份……</div>' if st == '已退回' else ''
        items += (f'<a class="m-item" href="{href}" data-group="{GROUP[st]}"><div class="m-item-top"><div class="m-item-title">{title}</div></div>{extra}'
                  f'<div class="m-item-foot"><span class="c-muted flex gap8">{icon(TYPE_ICON[t], 13)}{t} · {time[5:]}</span>{status}</div></a>')
    body = seg([('全部', ''), ('草稿', '草稿'), ('审核中', '审核中'), ('已退回', '已退回'), ('已采用', '已采用'), ('未采用', '未采用')], '#myList') + \
        f'<div id="myList">{items}</div><div class="m-empty hidden">暂无该状态的稿件</div>'
    cw('my-submissions.html', '我的投稿', body, tab='my-submissions.html', pc_link='../../pc/correspondent/my-submissions.html')


def c_detail():
    s = RETURNED
    op = RETURN_OPINIONS[0]
    body = f'''<div class="m-card" style="box-shadow:inset 3px 0 0 var(--danger),var(--shadow-sm)"><div class="m-item-top"><div class="m-item-title">{s["title"]}</div>{tag('已退回')}</div>
<div class="notice notice-danger mt12">{icon('undo', 14)}<div><b>{op[0]} · {op[1]}</b><br>{op[4]}<div class="hint">{op[2]}</div></div></div></div>
<div class="m-tabs" data-tabs><button class="on" data-tab="c">稿件内容</button><button data-tab="f">流转记录</button><button data-tab="i">投稿信息</button></div>
<div data-tabs-scope style="margin-top:-12px;padding-top:12px">
<div class="tab-panel on" data-panel="c">{m_article(s)}</div>
<div class="tab-panel" data-panel="f"><div class="m-card">{returned_timeline()}</div></div>
<div class="tab-panel" data-panel="i"><div class="m-card">{m_kv([('稿件编号', s['id']), ('类型', '新闻投稿'), ('所属学院', s['college']), ('投稿人', '陈雨桐（学生）'), ('指导老师', s['teacher']), ('当前版本', 'v2（共 2 个版本）'), ('投稿时间', s['time'])])}</div></div>
</div>'''
    cw('detail.html', '稿件档案', body, back='my-submissions.html', foot=a_btn('按意见修改并重新提交', 'resubmit.html', 'btn-primary', 'edit'), pc_link='../../pc/correspondent/submission-detail.html')


def c_resubmit():
    s = RETURNED
    ops = ''.join(f'<div class="notice notice-danger" style="margin-bottom:8px">{icon("undo", 14)}<div><b>{n} · {u}</b>（{t[5:]}）<br>{o}</div></div>' for n, u, t, v, o in RETURN_OPINIONS)
    content = ''.join(f'<p>{p}</p>' for p in s['paras'])
    files = [(IMG['volunteer'], '志愿者讲解.jpg'), (IMG['students'], '编程启蒙.jpg'), (IMG['group'], '志愿者合影.jpg')]
    body = f'''<div class="m-form-title">历次退回意见（2 次）</div>{ops}
<form id="mForm" data-autosave novalidate>{identity_block('学生', '李晓琳（计算机学院）')}
<div class="m-form-title">修改稿件（将生成 v3）</div><div class="m-form">
{field('新闻标题', f'<input class="input" id="mTitle" name="title" required value="{s["title"]}">', req=True)}
{field('活动简介', f'<textarea class="textarea" id="mIntro" name="intro" required>{s["intro"]}</textarea>', req=True)}
<div class="field"><label class="lbl req">新闻正文</label>{m_editor('mEditor', content)}</div>
{m_upload('新闻配图', files=files)}
{field('修改说明', '<textarea class="textarea" name="note" required placeholder="说明针对退回意见做了哪些修改"></textarea>', req=True)}
</div></form>'''
    foot = btn('存草稿', 'w-auto', 'save', 'data-action="save-draft"') + btn('重新提交', 'btn-primary', 'send', 'data-action="submit" data-form="#mForm" data-sensitive="#mTitle,#mIntro,#mEditor" data-confirm="重新提交后生成 v3 版本，并重新进入指导老师审核。确认提交吗？" data-msg="已重新提交" data-next="my-submissions.html?re=1&msg=已重新提交，生成 v3 版本并重新进入审核"')
    cw('resubmit.html', '修改重提', body + '<span class="hidden" data-draft-status></span>', back='detail.html', foot=foot, pc_link='../../pc/correspondent/resubmit.html')


def c_ranking():
    def rows(data):
        top = max(r[2] for r in data)
        out = ''
        for i, (c, s, a, b) in enumerate(sorted(data, key=lambda r: -r[2])):
            me = c == '计算机学院'
            act = 'data-open="ownDetailModal"' if me else 'data-toast="根据数据隔离规则，投稿人仅可查看本院稿件明细" data-toast-type="warn"'
            rc = f' r{i + 1}' if i < 3 else ''
            out += f'<div class="rank-row{" me" if me else ""}" {act} style="cursor:pointer"><span class="rank-no{rc}">{i + 1}</span><span class="rr-name">{c}</span><span class="rr-bar"><i style="width:{a / top * 100:.0f}%"></i></span><b>{a}</b></div>'
        return out
    sem = [(c, int(s * .45), int(a * .42), int(b * .5)) for c, s, a, b in RANKING]
    body = f'''<div class="m-hero" style="padding:14px 16px"><h2>计算机学院 · 第 1 名</h2><p>本学年采用 52 篇 · 投稿 86 篇 · 采用率 60.5%</p></div>
<div data-tabs-scope><div class="m-seg" data-tabs><button class="on" data-tab="y">2026—2027 学年</button><button data-tab="s">秋季学期</button></div>
<div class="tab-panel on" data-panel="y"><div class="m-card"><div class="m-card-title">按采用数排序<span class="hint">采用篇数</span></div>{rows(RANKING)}</div></div>
<div class="tab-panel" data-panel="s"><div class="m-card"><div class="m-card-title">按采用数排序<span class="hint">采用篇数</span></div>{rows(sem)}</div></div></div>'''
    stat = next(r[1:] for r in RANKING if r[0] == '计算机学院')
    body = body.replace('<p>本学年采用 52 篇 · 投稿 86 篇 · 采用率 60.5%</p>',
                        f'<p>本学年采用 52 篇 · 投稿 86 篇 · 采用率 60.5%</p><button type="button" class="m-hero-btn" data-open="ownDetailModal">{icon("list", 14)}查看本院明细</button>')
    cw('ranking.html', '全校排行榜', body, back='home.html', pc_link='../../pc/correspondent/ranking.html',
       modals=m_college_detail_modal('ownDetailModal', '计算机学院', stat))


def c_messages():
    items = [msg_item('undo', 'red', '稿件被退回', '《“青春志愿行”社区服务周纪实》被二审退回，点击查看意见并修改', '1 小时前', 'resubmit.html', True),
             msg_item('check-circle', 'green', '稿件终审采用', '《红色经典诵读活动》已终审采用，计入本院采用统计', '昨天', 'detail.html', True),
             msg_item('check', 'blue', '指导老师审核通过', '《“算法之星”编程挑战赛精彩瞬间》已进入校团委一审', '09-28', 'my-submissions.html'),
             msg_item('trophy', 'blue', '排行榜已更新', '计算机学院以 52 篇采用量位列第 1', '09-30', 'ranking.html')]
    right = '<button class="link" data-action="read-all">全部已读</button>'
    cw('messages.html', '消息', ''.join(items), tab='messages.html', right=right, pc_link='../../pc/correspondent/messages.html')


def c_profile():
    from data import AVATAR
    body = f'''<div class="m-profile"><img src="{AVATAR['corr']}" alt="陈雨桐"><div><b>陈雨桐</b><span>计算机学院 · 学生 · 学号 8209230118</span></div></div>
<div class="m-section"><span>本院本学年投稿情况（仅本院）</span></div>
<div class="m-mini-stats"><div><b>86</b><span>投稿总量</span></div><div><b class="c-success">52</b><span>已采用</span></div><div><b class="c-danger">9</b><span>被退回</span></div></div>
<div class="m-card mt12">
<a class="m-list-link" href="my-submissions.html"><span class="ll-ic">{icon('inbox', 17)}</span>我的投稿{icon('chev-r', 16)}</a>
<a class="m-list-link" href="ranking.html"><span class="ll-ic">{icon('trophy', 17)}</span>全校排行榜{icon('chev-r', 16)}</a>
<a class="m-list-link" href="messages.html"><span class="ll-ic">{icon('bell', 17)}</span>消息通知{icon('chev-r', 16)}</a>
<button type="button" class="m-list-link" data-open="ruleSheet"><span class="ll-ic">{icon('book', 17)}</span>投稿须知{icon('chev-r', 16)}</button>
<a class="m-list-link" href="../../pc/correspondent/dashboard.html"><span class="ll-ic">{icon('monitor', 17)}</span>切换到 PC 端{icon('chev-r', 16)}</a>
</div>
<a class="btn btn-block btn-danger-o" href="../../index.html" data-confirm="确认退出登录？演示环境将返回原型导航页。">退出登录</a>'''
    rules = f'''<div class="modal" id="ruleSheet"><div class="modal-box"><div class="modal-head"><span>投稿须知</span><button class="modal-x" data-close aria-label="关闭">{icon('x', 18)}</button></div>
<div class="modal-body" style="font-size:14px;line-height:1.9;color:var(--text-2)">1. 涉密信息请勿上网。<br>2. 学生投稿必须指定指导老师，先由指导老师审核；教师投稿直接进入一审。<br>3. 稿件依次经过一审、二审、三审终审，每个环节 3 个工作日内处理。<br>4. 被退回的稿件可修改后重新提交，历史版本与意见永久保留。<br>5. 视频请提供永久有效的云盘链接。</div>
<div class="modal-foot"><button class="btn btn-primary" data-close>我知道了</button></div></div></div>'''
    cw('profile.html', '我的', body, tab='profile.html', modals=rules, pc_link='../../pc/correspondent/dashboard.html')


# =============== 审核类角色通用 ===============
def review_list(rows, href='review.html'):
    out = ''
    for sid, title, t, col, ident, time, rem, lv in rows:
        ov = ' overdue' if lv == 'over' else ''
        out += (f'<a class="m-item{ov}" href="{href}" data-row-id="{sid}" data-level="{lv}"><div class="m-item-top"><div class="m-item-title">{title}</div></div>'
                f'<div class="m-item-meta"><span>{icon(TYPE_ICON[t], 12)} {t}</span><span>{col}</span><span>{ident}投稿</span></div>'
                f'<div class="m-item-foot"><span class="c-muted">到达 {time[5:]}</span>{remain_m(rem, lv)}</div></a>')
    return out


def review_page(role, folder, node, status, upto, timer, pass_next, reject_next, tpl, pass_text, reject_text, back, pc_link, todo_count=None, reject_title='退回稿件', reject_label='退回意见', file='review.html'):
    lv_cls = ' danger' if timer[1] == 'over' else ''
    body = f'''<div class="m-timer{lv_cls}">{icon('clock', 20)}<div>当前节点：{node} · 时限 3 个工作日<br><b>{timer[0]}</b></div></div>
<div class="m-tabs" data-tabs><button class="on" data-tab="c">稿件内容</button><button data-tab="f">流转记录</button><button data-tab="i">投稿信息</button></div>
<div data-tabs-scope style="margin-top:-12px;padding-top:12px">
<div class="tab-panel on" data-panel="c">
<div class="sens-card" style="margin-bottom:12px"><b class="c-warn">{icon('shield', 14)} 敏感词检测：低危 1 处</b><div class="hint">第 2 段“最牛”，建议改为客观表述（不拦截）</div></div>
{m_article(FEATURED)}</div>
<div class="tab-panel" data-panel="f"><div class="m-card">{featured_flow_timeline(upto)}</div></div>
<div class="tab-panel" data-panel="i"><div class="m-card">{m_kv([('稿件编号', SID), ('类型', '新闻投稿'), ('学院', '计算机学院'), ('投稿人', '陈雨桐（学生）'), ('指导老师', FEATURED['teacher']), ('投稿时间', FEATURED['time']), ('当前状态', tag(status))])}</div></div>
</div>'''
    foot = (btn(reject_text, 'btn-danger-o', 'undo', f'data-action="reject" data-tpl="{tpl}" data-title="{reject_title}" data-label="{reject_label}" data-ok="确认" data-next="{reject_next}"') +
            btn(pass_text, 'btn-success', 'check', f'data-action="pass" data-opinion="optional" data-tpl="{tpl}" data-title="{pass_text}" data-ok="确认" data-next="{pass_next}"'))
    write(f'mobile/{folder}/{file}', m_page(role, '审核稿件', body, back=back, foot=foot, pc_link=pc_link, todo_count=todo_count))


def ledger_page(role, folder, title, rows, pc_link, tab, todo_count=None):
    new = (f'<div class="m-item hidden" data-when-param="new={SID}" data-highlight><div class="m-item-title">{FEATURED["title"]}</div>'
           f'<div class="m-item-foot"><span class="c-muted">刚刚 · 用时 0.3 个工作日</span><span><span data-when-param="act=pass">{tag("通过")}</span><span data-when-param="act=reject">{tag("退回")}</span></span></div></div>')
    items = ''.join(f'<div class="m-item" data-result="{r}"><div class="m-item-title">{t}</div><div class="m-item-foot"><span class="c-muted">{tm} · 用时 {cost}</span><span class="flex gap8">{tag(ok)}{tag(r)}</span></div></div>'
                    for t, tm, r, cost, ok in rows)
    body = f'''<div class="m-mini-stats"><div><b>186</b><span>累计审核</span></div><div><b class="c-success">96.2%</b><span>及时率</span></div><div><b class="c-danger">7</b><span>超时</span></div></div>
<div class="mt12">{seg([('全部', ''), ('通过', '通过'), ('退回', '退回')], '#ledgerList', 'result')}</div><div id="ledgerList">{new}{items}</div><div class="m-empty hidden">暂无记录</div>'''
    write(f'mobile/{folder}/{tab}', m_page(role, title, body, tab=tab, pc_link=pc_link, todo_count=todo_count))


LEDGER_ROWS = [('学院“算法之星”编程挑战赛精彩瞬间', '09-29 15:20', '通过', '0.6 天', '及时'), ('湘雅医学院新生开学第一课', '09-29 10:05', '退回', '1.1 天', '及时'),
               ('新生军训风采纪实短片《淬炼》', '09-26 17:30', '通过', '0.4 天', '及时'), ('湘雅医学院“医路同行”义诊进社区', '09-26 09:10', '通过', '3.5 天', '超时'),
               ('“青春志愿行”社区服务周纪实', '09-21 09:20', '通过', '0.7 天', '及时')]


def messages_page(role, folder, items, pc_link, todo_count=None):
    right = '<button class="link" data-action="read-all">全部已读</button>'
    write(f'mobile/{folder}/messages.html', m_page(role, '消息', ''.join(msg_item(*i[:6], unread=len(i) > 6 and i[6]) for i in items), tab='messages.html', right=right, pc_link=pc_link, todo_count=todo_count))


def todo_page(role, folder, title, rows, pc_link, desc, todo_count=None, file='todo.html', review='review.html'):
    n_over = sum(1 for r in rows if r[7] == 'over')
    n_warn = sum(1 for r in rows if r[7] == 'warn')
    body = f'''<div class="m-mini-stats"><div><b data-counter>{len(rows)}</b><span>待处理</span></div><div><b class="c-danger">{n_over}</b><span>已超时</span></div><div><b class="c-warn">{n_warn}</b><span>即将超时</span></div></div>
<div class="notice notice-info mt12" style="margin-bottom:10px">{icon('info', 14)}<div>{desc}</div></div>
{seg([('全部', ''), ('已超时', 'over'), ('即将超时', 'warn'), ('正常', 'ok')], '#todoList', 'level')}
<div id="todoList">{review_list(rows, review)}</div><div class="m-empty hidden">暂无该类稿件</div>'''
    write(f'mobile/{folder}/{file}', m_page(role, title, body, tab=file, pc_link=pc_link, todo_count=todo_count))


def sort_rows(rows):
    order = {'over': 0, 'warn': 1, 'ok': 2}
    return sorted(rows, key=lambda r: (order[r[7]], r[5]))


# =============== 指导老师 ===============
def teacher():
    rows = sort_rows([(sid, title, t, '计算机学院', author, time, rem, lv) for sid, title, t, author, time, rem, lv in TEACHER_TODO])
    rows = [(r[0], r[1], r[2], r[4], '学生', r[5], r[6], r[7]) for r in rows]
    todo_page('teacher', 'teacher', '待审稿件', rows, '../../pc/teacher/dashboard.html', '仅显示指定您为指导老师的学生稿件，审核通过后进入校团委一审')
    review_page('teacher', 'teacher', '指导老师审核', '待指导老师审核', 'teacher', ('剩余 0.5 个工作日', 'warn'),
                q('todo.html', done=SID, msg='已通过，稿件已报送校团委一审', link=q('history.html', new=SID, act='pass'), linkText='审核记录'),
                q('todo.html', done=SID, type='warn', msg='已退回，已通知投稿学生', link=q('history.html', new=SID, act='reject'), linkText='审核记录'),
                'teacher', '通过，报送一审', '退回', 'todo.html', '../../pc/teacher/review.html')
    ledger_page('teacher', 'teacher', '审核记录', LEDGER_ROWS[:3] + [('“挑战杯”校赛备赛动员会', '09-18 17:40', '通过', '3.5 天', '超时')], '../../pc/teacher/history.html', 'history.html')
    messages_page('teacher', 'teacher', [
        ('inbox', 'blue', '新的待审稿件', f'陈雨桐提交了《{FEATURED["title"]}》', '10 分钟前', 'review.html', True),
        ('alert', 'red', '审核超时提醒', '《“代码为桥”乡村小学编程支教纪实》已超时 1.5 个工作日', '今天 09:00', 'todo.html', True),
        ('check-circle', 'green', '您审核的稿件已终审采用', '《红色经典诵读活动》已终审采用', '09-19', 'history.html')], '../../pc/teacher/messages.html')


# =============== 一审员 / 二审员 ===============
def reviewers():
    for role, rows, node, status, upto, nxt in [('reviewer1', R1_TODO, '一审', '待一审', 'r1', '二审'), ('reviewer2', R2_TODO, '二审', '待二审', 'r2', '三审终审')]:
        allrows = sort_rows([(SID, FEATURED['title'], '新闻', '计算机学院', '学生', '2026-09-28 16:35' if role == 'reviewer1' else '2026-09-29 11:20', '剩余 2.5 个工作日', 'ok')] + rows)
        n = len(allrows)
        pc = f'../../pc/{role}/'
        todo_page(role, role, f'待{node}', allrows, pc + 'todo.html', f'只展示分配给您（{node}环节）的稿件，超时优先排序', n)
        review_page(role, role, node, status, upto, ('剩余 2.5 个工作日', 'ok'),
                    q('todo.html', done=SID, msg=f'{node}通过，已流转至{nxt}', link=q('ledger.html', new=SID, act='pass'), linkText='审核台账'),
                    q('todo.html', done=SID, type='warn', msg='已退回，已通知投稿人', link=q('ledger.html', new=SID, act='reject'), linkText='审核台账'),
                    'review', f'{node}通过', '退回', 'todo.html', pc + 'review.html', n)
        ledger_page(role, role, '审核台账', LEDGER_ROWS, pc + 'my-ledger.html', 'ledger.html', n)
        messages_page(role, role, [
            ('inbox', 'blue', f'新的待{node}稿件', f'《{FEATURED["title"]}》已到达{node}环节', '30 分钟前', 'review.html', True),
            ('alert', 'red', '审核超时预警', '有稿件已超过审核时限，已记入超时台账', '今天 09:00', 'todo.html', True),
            ('clock', 'orange', '即将超时提醒', '有稿件剩余时限不足 1 个工作日', '今天 09:00', 'todo.html', True),
            ('check-circle', 'green', '您审核的稿件已终审采用', f'《{ADOPTED["title"]}》', '09-19', 'ledger.html')], pc + 'messages.html', n)


# =============== 管理员 ===============
def admin():
    pc = '../../pc/admin/'
    rows = sort_rows([(SID, FEATURED['title'], '新闻', '计算机学院', '学生', '2026-09-30 09:00', '剩余 3 个工作日', 'ok')] + R3_TODO)
    body = f'''<div class="m-hero"><h2>统计看板</h2><p>2026—2027 学年 · 数据更新于 16:00</p>
<div class="m-stats"><div><b>1024</b><span>投稿总量</span></div><div><b>562</b><span>终审采用</span></div><div><b>131</b><span>退回</span></div><div><b>94.8%</b><span>及时率</span></div></div></div>
<div class="m-mini-stats"><div data-href="final-list.html" style="cursor:pointer"><b class="c-warn">{len(rows)}</b><span>待三审</span></div><div data-href="final-list.html" style="cursor:pointer"><b class="c-danger">5</b><span>超时未处理</span></div><div data-toast="升华网素材导出请在 PC 端操作" data-toast-type="info" style="cursor:pointer"><b class="c-primary">3</b><span>待发布升华网</span></div></div>
<div class="m-card mt12"><div class="m-card-title">稿件类型</div>
{''.join(f'<div class="rank-row"><span class="rr-name">{n}</span><span class="rr-bar" style="width:140px"><i style="width:{v / 532 * 100:.0f}%;background:{c}"></i></span><b style="width:40px">{v}</b></div>' for n, v, c in [('新闻投稿', 532, '#3087CC'), ('照片投稿', 248, '#1BB975'), ('视频投稿', 146, '#F29100'), ('新闻线索', 98, '#9CBFDA')])}</div>
<div class="m-card"><div class="m-card-title">学院采用排行<a href="{pc}ranking.html">完整榜单 ›</a></div>
{''.join(f'<div class="rank-row"><span class="rank-no r{i + 1}">{i + 1}</span><span class="rr-name">{c}</span><span class="rr-bar"><i style="width:{a / 52 * 100:.0f}%"></i></span><b>{a}</b></div>' for i, (c, s, a, b) in enumerate(RANKING[:3]))}</div>
<a class="btn btn-primary btn-block" href="final-list.html">{icon('inbox', 16)}处理待三审稿件</a>
<a class="btn btn-block mt12" href="{pc}dashboard.html">{icon('monitor', 16)}在 PC 端查看完整驾驶舱</a>'''
    write('mobile/admin/home.html', m_page('admin', '看板', body, tab='home.html', pc_link=pc + 'dashboard.html'))
    todo_page('admin', 'admin', '待三审', rows, pc + 'final-list.html', '二审通过的稿件，终审二选一：采用 / 不采用', file='final-list.html', review='final-review.html')
    review_page('admin', 'admin', '三审终审', '待三审', 'r3', ('剩余 3 个工作日', 'ok'),
                q('final-list.html', done=SID, msg='已终审采用，计入学院采用统计'),
                q('final-list.html', done=SID, type='warn', msg='已终审不采用，不计入采用统计'),
                'final', '终审采用', '不采用', 'final-list.html', pc + 'final-review.html', reject_title='终审不采用', reject_label='终审意见', file='final-review.html')
    messages_page('admin', 'admin', [
        ('inbox', 'blue', '新的待三审稿件', f'《{FEATURED["title"]}》已通过二审', '15 分钟前', 'final-review.html', True),
        ('alert', 'red', '审核超时预警', '当前有 5 篇稿件超时未处理', '今天 09:00', 'final-list.html', True),
        ('globe', 'blue', '待发布升华网', '有 3 篇已采用新闻尚未标记为已发布', '昨天', 'home.html')], pc + 'messages.html')


def build():
    c_home(); c_forms(); c_success(); c_my(); c_detail(); c_resubmit(); c_ranking(); c_messages(); c_profile()
    teacher(); reviewers(); admin()
