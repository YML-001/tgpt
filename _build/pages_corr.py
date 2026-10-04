# PC 端 · 投稿人（全校师生）
from lib import (icon, tag, type_tag, stat, card, page_head, btn, a_btn, options, filter_select, search_box,
                 date_range, filter_bar, table, field, modal, flow_steps, editor, upload_field, teacher_picker,
                 pc_page, write)
from data import MY_SUBS, RANKING, IMG, ARCHIVE, TYPE_NAME
from common import (RETURNED, RETURN_OPINIONS, article, gallery, info_kv, returned_timeline, op_log_table,
                    msg_item, messages_page_body, rank_rows, donut, bars, college_detail_modal)

R = 'correspondent'
P = 'pc/correspondent/'

GROUP = {'草稿': '草稿', '待指导老师审核': '审核中', '待一审': '审核中', '待二审': '审核中', '待三审': '审核中',
         '已退回': '已退回', '已终审采用': '已采用', '已发布': '已采用', '已终审不采用': '未采用'}


def page(file, title, body, crumbs=None, modals='', css=''):
    write(P + file, pc_page(R, file, title, body, crumbs=crumbs, modals=modals, css=css))


# ---------- 投稿表单共用区块 ----------
def type_switch(cur):
    items = [('submit-news.html', '新闻投稿'), ('submit-video.html', '视频投稿'),
             ('submit-photo.html', '照片投稿'), ('submit-clue.html', '新闻线索')]
    out = ''
    for href, name in items:
        ck = ' checked' if href == cur else ''
        out += (f'<label class="radio-card"><input type="radio" name="submitType" value="{href}" '
                f'data-nav-radio{ck}>{name}</label>')
    return f'<div class="type-switch"><span class="ts-lbl">投稿类型</span><div class="radio-group">{out}</div></div>'


def identity_section(identity='学生', teacher='王海峰（计算机学院）'):
    s_chk = ' checked' if identity == '学生' else ''
    t_chk = ' checked' if identity == '教师' else ''
    radios = (f'<div class="radio-group"><label class="radio-card"><input type="radio" name="identity" value="学生"{s_chk} required>学生</label>'
              f'<label class="radio-card"><input type="radio" name="identity" value="教师"{t_chk}>教师</label></div>')
    return f'''<div class="form-section"><div class="form-section-title">投稿人信息<span class="hint">所有稿件均记录投稿人、身份、学院与投稿时间</span></div>
<div class="form-grid g3c">
{field('投稿人姓名', '<input class="input" value="陈雨桐" disabled>', hint='取自统一身份认证，不可修改')}
{field('所属学院', '<input class="input" value="计算机学院" disabled>', hint='所属学院取自统一身份认证，稿件计入本院统计')}
{field('投稿人身份', radios, req=True)}
<div class="field full" data-show-when="identity=学生"><label class="lbl req">指导老师</label>{teacher_picker(teacher)}
<div class="hint">默认预填上次选择的指导老师；只能从指导老师名单中选择，可输入姓名 / 工号搜索其他学院老师。学生稿件将先由指导老师审核，通过后进入校团委一审。</div></div>
<div class="field full hidden" data-show-when="identity=教师"><div class="notice notice-info">{icon("info", 15)}<div>教师投稿无需指定指导老师，提交后直接进入<b>校团委一审</b>。</div></div></div>
</div></div>'''


def form_foot(sensitive, type_name):
    confirm = '提交后稿件将进入审核流程（学生投稿先由指导老师审核，教师投稿直接进入校团委一审），审核期间不可修改。确认提交吗？'
    return f'''<div class="form-foot">
<span class="draft-status" data-draft-status>{icon("clock", 14)}&nbsp;每 30 秒自动保存草稿</span>
{a_btn('取消', 'dashboard.html', '', None, 'data-confirm="当前内容已自动保存为草稿，确认离开本页吗？"')}
{btn('保存草稿', '', 'save', 'data-action="save-draft"')}
{btn('提交投稿', 'btn-primary', 'send', f'data-action="submit" data-sensitive="{sensitive}" data-confirm="{confirm}" data-msg="投稿提交成功" data-next="submit-success.html?type={type_name}&identity={{identity}}"')}
</div>'''


DURATION_INPUT = r'<input class="input" name="duration" required placeholder="如 03:25" data-pattern="^\d{1,3}:\d{2}$" data-pattern-msg="请按“分:秒”格式填写，如 03:25">'
PHONE_INPUT = r'<input class="input" name="phone" required placeholder="11 位手机号" data-pattern="^1[3-9]\d{9}$" data-pattern-msg="请填写正确的 11 位手机号">'

SECRET = f'<div class="notice notice-danger mb16">{icon("lock", 15)}<div><b>重要提示：涉密信息请勿上网。</b>稿件提交后将生成永久档案，全部修改与审核记录可追溯。</div></div>'
DEMO_TIP = f'<div class="notice notice-warn mb16">{icon("zap", 15)}<div>演示提示：在标题或正文中输入“翻墙”可体验高危敏感词拦截，输入“最牛”可体验低危词提示；切换“教师 / 学生”身份可查看指导老师字段的联动。</div></div>'


def news_form(prefill=None, sensitive='#newsTitle,#newsIntro,#newsEditor'):
    p = prefill or {}
    content = ''.join(f'<p>{x}</p>' for x in p.get('paras', []))
    return f'''
<div class="form-section"><div class="form-section-title">稿件内容</div>
<div class="form-grid">
{field('新闻标题', f'<input class="input" id="newsTitle" name="title" maxlength="50" required value="{p.get("title", "")}" placeholder="请输入新闻标题，建议 30 字以内" data-counter="#titleCount">', req=True, full=True, hint=f'已输入 <b id="titleCount">{len(p.get("title", ""))}</b> / 50 字')}
{field('撰稿人', f'<input class="input" name="writer" required value="{p.get("writer", "")}" placeholder="多位撰稿人用顿号分隔">', req=True)}
{field('拍摄时间', f'<input type="date" class="input" name="shoot" required value="{p.get("shoot", "")}">', req=True)}
{field('活动简介', f'<textarea class="textarea" id="newsIntro" name="intro" required maxlength="200" placeholder="一句话概括活动时间、地点、主体和亮点（200 字以内）">{p.get("intro", "")}</textarea>', req=True, full=True)}
<div class="field full"><label class="lbl req">新闻正文</label>{editor('newsEditor', content)}</div>
</div></div>
<div class="form-section"><div class="form-section-title">新闻配图<span class="hint">原图存储，不做压缩</span></div>
{upload_field('新闻配图', hint='支持 JPG / PNG，可多选，单张不超过 20MB；建议 3 张以上', prefill=p.get('files'))}
</div>'''


# ---------- 1 工作台 ----------
def dashboard():
    recent = ''
    for sid, title, t, ident, teacher, time, st in MY_SUBS[1:6]:
        recent += (f'<tr><td><a class="t-title" href="submission-detail.html">{title}</a><div class="t-sub">{sid}</div></td>'
                   f'<td>{type_tag(t)}</td><td>{time[5:]}</td><td>{tag(st)}</td></tr>')
    ranks = ''
    for i, (c, s, a, b) in enumerate(RANKING[:5]):
        rc = f' r{i + 1}' if i < 3 else ''
        me = ' <span class="tag tag-primary">本院</span>' if c == '计算机学院' else ''
        ranks += (f'<div class="todo-item"><span class="rank-no{rc}">{i + 1}</span><div class="ti-main"><div class="ti-title">{c}{me}</div>'
                  f'<div class="ti-sub">投稿 {s} · 采用 {a}</div></div><b class="num">{a}</b></div>')
    body = f'''
<div class="welcome">
  <div><h1>下午好，陈雨桐</h1><p>2026—2027 学年你已投稿 12 篇，其中 5 篇被采用；有 1 篇稿件被退回待修改。</p></div>
  <div class="flex gap12">{a_btn('立即投稿', 'submit-news.html', '', 'edit')}{a_btn('我的投稿', 'my-submissions.html', 'btn-ghost-w', 'inbox')}</div>
</div>
<div class="grid g4 mt20">
{stat('file', 'blue', 86, '本院本学年投稿', '<span class="c-success">较上学年同期 +12%</span>', 'college-stats.html')}
{stat('check-circle', 'green', 52, '本院已采用', '采用率 60.5%', 'college-stats.html')}
{stat('clock', 'orange', 14, '本院审核中', '含待指导老师审核 5 篇', 'college-stats.html')}
{stat('undo', 'red', 9, '本院被退回', '已重提 7 篇', 'college-stats.html')}
</div>
<div class="grid g-main mt20">
  <div class="grid">
    {card('我的待办', f"""
      <div class="todo-item"><span class="stat-ic red" style="width:36px;height:36px">{icon('undo', 18)}</span><div class="ti-main"><div class="ti-title">“青春志愿行”社区服务周纪实 · 被二审退回</div><div class="ti-sub">退回意见：第三段引用居民原话未注明姓名与身份……</div></div>{a_btn('去修改', 'resubmit.html', 'btn-sm btn-danger-o')}</div>
      <div class="todo-item"><span class="stat-ic gray" style="width:36px;height:36px">{icon('edit', 18)}</span><div class="ti-main"><div class="ti-title">2026年“青春心向党”国庆主题快闪活动 · 草稿未提交</div><div class="ti-sub">最后保存于今天 09:12</div></div>{a_btn('继续编辑', 'submit-news.html', 'btn-sm')}</div>
      <div class="todo-item"><span class="stat-ic orange" style="width:36px;height:36px">{icon('clock', 18)}</span><div class="ti-main"><div class="ti-title">计算机学院举办2026级新生“科技启航”主题团日活动</div><div class="ti-sub">等待指导老师王海峰审核 · 剩余 0.5 个工作日</div></div>{a_btn('查看进度', 'submission-detail.html', 'btn-sm')}</div>
    """, 'flag', '<a class="link" href="my-submissions.html">全部稿件 ›</a>')}
    {card('最近投稿', table('recentTable', ['稿件', '类型', '投稿时间', '状态'], [recent], pager=False), 'inbox', '<a class="link" href="my-submissions.html">查看全部 ›</a>', 'card-body" style="padding:0')}
  </div>
  <div class="grid" style="align-content:start">
    {card('全校学院排行榜', ranks + '<div class="notice notice-info mt12">' + icon('trophy', 15) + '<div>本院本学年采用 52 篇，全校排名 <b>第 1</b></div></div>', 'trophy', '<a class="link" href="ranking.html">完整榜单 ›</a>')}
    {card('最新消息', '<div style="margin:-20px">' + msg_item('undo', 'red', '稿件被退回', '《“青春志愿行”社区服务周纪实》被二审退回，请查看意见后修改', '1 小时前', 'resubmit.html', True) + msg_item('check-circle', 'green', '稿件终审采用', '《红色经典诵读活动》已终审采用，计入本院采用统计', '昨天', 'submission-detail.html', True) + '</div>', 'bell', '<a class="link" href="messages.html">全部 ›</a>')}
  </div>
</div>'''
    page('dashboard.html', '工作台', body)


# ---------- 2-5 四类投稿 ----------
def submit_news():
    body = page_head('新闻投稿', '适用于学院活动新闻、团学动态新闻稿件；提交后自动生成稿件档案') + type_switch('submit-news.html') + SECRET + DEMO_TIP + \
        f'<form class="form-card" data-autosave novalidate>{identity_section()}{news_form()}{form_foot("#newsTitle,#newsIntro,#newsEditor", "新闻")}</form>'
    page('submit-news.html', '新闻投稿', body, ['我的投稿', '新闻投稿'])


def submit_video():
    usage = options(['新闻报道素材', '宣传片素材', '活动纪实存档', '短视频平台发布', '其他'], '请选择视频用途')
    body = page_head('视频投稿', '适用于活动纪实视频、宣传短片素材') + type_switch('submit-video.html') + SECRET + f'''
<form class="form-card" data-autosave novalidate>{identity_section()}
<div class="form-section"><div class="form-section-title">视频信息</div>
<div class="form-grid">
{field('视频标题', '<input class="input" id="videoTitle" name="title" required maxlength="50" placeholder="请输入视频标题">', req=True, full=True)}
{field('拍摄 / 撰稿人', '<input class="input" name="writer" required placeholder="拍摄或剪辑人员姓名">', req=True)}
{field('视频时长', DURATION_INPUT, req=True)}
{field('视频简介', '<textarea class="textarea" id="videoIntro" name="intro" required placeholder="简要介绍视频内容、拍摄背景"></textarea>', req=True, full=True)}
{field('视频用途', f'<select class="select" name="usage" required>{usage}</select>', req=True)}
{field('用途补充说明', '<input class="input" name="usageNote" placeholder="选填，如希望在国庆专题中使用">')}
</div></div>
<div class="form-section"><div class="form-section-title">视频文件链接</div>
<div class="notice notice-warn mb16">{icon('alert', 15)}<div><b>请提供永久有效的云盘链接。</b>请在百度网盘、夸克网盘等分享时选择“永久有效”，不支持 7 天、30 天等临时分享链接。系统不校验链接有效性，链接失效将导致稿件被退回。</div></div>
<div class="form-grid">
{field('永久云盘链接', '<input class="input" name="link" required placeholder="https://pan.baidu.com/s/……" data-pattern="^https?://" data-pattern-msg="请填写以 http:// 或 https:// 开头的完整链接">', req=True, full=True)}
{field('提取码', '<input class="input" name="code" placeholder="选填，如 8k2d">')}
{field('链接有效期', '<select class="select" name="expire" required><option value="永久有效">永久有效</option></select>', req=True, hint='仅支持永久有效链接')}
</div>
<div class="mt16">{upload_field('视频封面图', hint='选填，JPG / PNG，建议 16:9', req=False)}</div>
</div>
{form_foot('#videoTitle,#videoIntro', '视频')}</form>'''
    page('submit-video.html', '视频投稿', body, ['我的投稿', '视频投稿'])


def submit_photo():
    body = page_head('照片投稿', '适用于活动纪实照片、领导调研、校园风貌素材；支持批量上传原图') + type_switch('submit-photo.html') + SECRET + f'''
<form class="form-card" data-autosave novalidate>{identity_section()}
<div class="form-section"><div class="form-section-title">照片信息</div>
<div class="form-grid">
{field('照片主题', '<input class="input" id="photoTitle" name="title" required maxlength="50" placeholder="如：计算机学院2026级新生开学典礼">', req=True, full=True)}
{field('拍摄人', '<input class="input" name="photographer" required placeholder="拍摄人姓名">', req=True)}
{field('拍摄时间', '<input type="date" class="input" name="shoot" required>', req=True)}
{field('场景简述', '<textarea class="textarea" id="photoDesc" name="desc" required placeholder="简述拍摄场景、活动内容"></textarea>', req=True, full=True)}
{field('涉及重要领导', '<input class="input" name="leader" required placeholder="请填写姓名及职务，无则填“无”">', req=True, full=True, hint='如涉及校领导或上级领导，请准确填写姓名与职务，便于审核核对')}
</div></div>
<div class="form-section"><div class="form-section-title">上传原图<span class="hint">支持批量上传，每张照片可单独添加备注</span></div>
{upload_field('照片原图', hint='支持 JPG / PNG，单张不超过 30MB，原图存储不压缩', remark=True, max_mb=30)}
</div>
{form_foot('#photoTitle,#photoDesc', '照片')}</form>'''
    page('submit-photo.html', '照片投稿', body, ['我的投稿', '照片投稿'])


def submit_clue():
    src = options(['本人亲历', '他人提供', '媒体报道', '网络信息', '其他'], '请选择线索来源')
    body = page_head('新闻线索', '适用于未成文的新闻线索、人物事迹线索，校团委将安排跟进采写') + type_switch('submit-clue.html') + f'''
<div class="notice notice-info mb16">{icon('flow', 15)}<div>线索提交并通过审核后，校团委将进行线索处置跟踪：<b>待跟进 → 已跟进 → 已转为正式新闻</b>，处置进度可在稿件档案中查看。</div></div>
<form class="form-card" data-autosave novalidate>{identity_section()}
<div class="form-section"><div class="form-section-title">线索内容</div>
<div class="form-grid">
{field('线索标题', '<input class="input" id="clueTitle" name="title" required maxlength="50" placeholder="一句话概括线索">', req=True, full=True)}
{field('线索详细描述', '<textarea class="textarea" id="clueDesc" name="desc" required style="min-height:130px" placeholder="请描述人物 / 事件的基本情况、新闻价值与时间节点"></textarea>', req=True, full=True)}
{field('线索来源', f'<select class="select" name="source" required>{src}</select>', req=True)}
<div class="field"><label class="lbl req">是否接受采访</label><div class="radio-group"><label class="radio-card"><input type="radio" name="interview" value="是" required checked>接受采访</label><label class="radio-card"><input type="radio" name="interview" value="否">不接受</label></div></div>
<div class="field full" data-show-when="interview=是"><label class="lbl req">可采访时间段</label><input class="input" name="interviewTime" required placeholder="如：工作日 14:00—17:00，或 10月8日—10月15日"></div>
</div></div>
<div class="form-section"><div class="form-section-title">联系方式</div>
<div class="form-grid">
{field('联系人', '<input class="input" name="contact" required placeholder="联系人姓名">', req=True)}
{field('联系方式', PHONE_INPUT, req=True)}
</div></div>
{form_foot('#clueTitle,#clueDesc', '线索')}</form>'''
    page('submit-clue.html', '新闻线索', body, ['我的投稿', '新闻线索'])


# ---------- 6 提交成功 ----------
def submit_success():
    stu = f'''<div data-when-param-hide="identity=教师">
  <p class="page-desc" style="font-size:14px">稿件已进入 <b class="c-warn">待指导老师审核</b>，指导老师王海峰将在 3 个工作日内处理，审核结果会通过消息通知你。</p>
  <div class="card mt20" style="padding:20px">{flow_steps('学生', 1)}</div>
  <div class="flex gap12 mt24" style="justify-content:center">{a_btn('查看我的投稿', 'my-submissions.html?new=TG2026093005&identity=学生', 'btn-primary btn-lg', 'inbox')}{a_btn('查看稿件档案', 'submission-detail.html', 'btn-lg', 'file')}{a_btn('继续投稿', 'submit-news.html', 'btn-lg', 'plus')}</div>
</div>'''
    tea = f'''<div class="hidden" data-when-param="identity=教师">
  <p class="page-desc" style="font-size:14px">教师投稿无需指导老师审核，稿件已直接进入 <b class="c-warn">待一审</b>，校团委一审员将在 3 个工作日内处理。</p>
  <div class="card mt20" style="padding:20px">{flow_steps('教师', 1)}</div>
  <div class="flex gap12 mt24" style="justify-content:center">{a_btn('查看我的投稿', 'my-submissions.html?new=TG2026093005&identity=教师', 'btn-primary btn-lg', 'inbox')}{a_btn('查看稿件档案', 'submission-detail.html', 'btn-lg', 'file')}{a_btn('继续投稿', 'submit-news.html', 'btn-lg', 'plus')}</div>
</div>'''
    body = f'''<div class="card success-box">
<div class="big-ic">{icon('check', 40)}</div>
<h1 class="page-title" style="justify-content:center">投稿提交成功</h1>
<div class="flex gap12 mt12" style="justify-content:center"><span class="tag tag-primary">稿件编号 TG2026093005</span><span class="tag tag-gray"><span data-param-text="type">新闻</span>投稿</span><span class="tag tag-gray">提交时间 2026-09-30 16:20</span></div>
<div class="mt16">{stu}{tea}</div>
</div>'''
    page('submit-success.html', '提交成功', body, ['我的投稿', '提交成功'])


# ---------- 7 我的投稿 ----------
def my_submissions():
    rows = []
    new_row = (f'<tr class="hidden" data-when-param="new=TG2026093005" data-highlight data-group="审核中" data-type="新闻" data-date="2026-09-30">'
               f'<td><a class="t-title" href="submission-detail.html">【新提交】你刚刚提交的稿件</a><div class="t-sub">TG2026093005</div></td>'
               f'<td>{type_tag("新闻")}</td><td><span data-param-text="identity">学生</span></td><td>—</td><td>2026-09-30 16:20</td>'
               f'<td><span data-when-param-hide="identity=教师">{tag("待指导老师审核")}</span><span class="hidden" data-when-param="identity=教师">{tag("待一审")}</span></td>'
               f'<td><div class="ops"><a class="link" href="submission-detail.html">查看进度</a></div></td></tr>')
    rows.append(new_row)
    for sid, title, t, ident, teacher, time, st in MY_SUBS:
        g = GROUP[st]
        if st == '草稿':
            ops = f'<a class="link" href="submit-news.html">继续编辑</a><button class="link link-danger" data-action="delete-row" data-confirm="确认删除该草稿吗？删除后不可恢复。">删除</button>'
        elif st == '已退回':
            ops = '<a class="link" href="submission-detail.html">查看意见</a><a class="link" href="resubmit.html">修改重提</a>'
        elif g == '审核中':
            ops = '<a class="link" href="submission-detail.html">查看进度</a>'
        else:
            ops = '<a class="link" href="submission-detail.html">稿件档案</a>'
        status = tag(st)
        if sid == 'TG2026092203':
            status = f'<span data-when-param-hide="re=1">{tag(st)}</span><span class="hidden" data-when-param="re=1">{tag("待指导老师审核")}</span>'
        rows.append(f'<tr data-group="{g}" data-type="{t}" data-date="{time[:10]}"><td><a class="t-title" href="submission-detail.html">{title}</a><div class="t-sub">{sid}</div></td>'
                    f'<td>{type_tag(t)}</td><td>{ident}</td><td>{teacher}</td><td>{time}</td><td>{status}</td><td><div class="ops">{ops}</div></td></tr>')
    tabs = [('全部', '', 12), ('草稿', '草稿', 1), ('审核中', '审核中', 4), ('已退回', '已退回', 1), ('已采用', '已采用', 5), ('未采用', '未采用', 1)]
    tab_html = ''.join(f'<button class="tab{" on" if i == 0 else ""}" data-tab="t{i}" data-filter-table="#mySubs" data-filter-key="group" data-filter-value="{v}">{n}<span class="cnt">{c}</span></button>'
                       for i, (n, v, c) in enumerate(tabs))
    ctrls = filter_select('mySubs', 'type', '全部类型', ['新闻', '视频', '照片', '线索']) + date_range('mySubs') + search_box('mySubs')
    body = page_head('我的投稿', '查看本人全部投稿、审核进度与历史审核意见；被退回的稿件可修改后重新提交',
                     btn('导出', '', 'download', 'data-open="exportModal"') + a_btn('新建投稿', 'submit-news.html', 'btn-primary', 'plus')) + \
        f'<div class="card"><div class="tabs" data-tabs>{tab_html}</div>{filter_bar("mySubs", ctrls)}' + \
        table('mySubs', ['稿件标题 / 编号', '类型', '投稿身份', '指导老师', ('投稿时间', 'data-sort'), '当前状态', ('操作', 'class="no-export"')], rows) + '</div>'
    page('my-submissions.html', '我的投稿', body, modals=export_modal())


# ---------- 8 稿件档案 ----------
def submission_detail():
    s = RETURNED
    latest = RETURN_OPINIONS[0]
    versions = f'''<div class="table-wrap"><table class="tbl"><thead><tr><th>版本</th><th>提交时间</th><th>标题</th><th>审核结果</th><th>操作</th></tr></thead><tbody>
<tr><td><span class="tag tag-primary">v2 当前</span></td><td>2026-09-20 11:40</td><td>“青春志愿行”社区服务周纪实</td><td>{tag('已退回')} 二审退回</td><td><a class="link" href="version-history.html">与 v1 对比</a></td></tr>
<tr><td><span class="tag tag-gray">v1</span></td><td>2026-09-18 09:30</td><td>青春志愿行社区服务周活动圆满结束</td><td>{tag('已退回')} 一审退回</td><td><a class="link" href="version-history.html">查看</a></td></tr>
</tbody></table></div><div class="notice notice-info mt16">{icon('info', 15)}<div>每次修改重提都会生成新版本，旧版本与退回意见永久保留、不可覆盖。</div></div>'''
    logs = op_log_table([
        ('2026-09-22 14:18', '周明轩（二审员）', '二审退回，填写退回意见', '10.12.8.66'),
        ('2026-09-21 09:20', '刘子涵（一审员）', '一审通过', '10.12.8.51'),
        ('2026-09-20 16:10', '李晓琳（指导老师）', '指导老师审核通过', '10.12.30.12'),
        ('2026-09-20 11:40', '陈雨桐', '编辑稿件并重新提交，生成 v2', '10.12.34.21'),
        ('2026-09-19 10:05', '刘子涵（一审员）', '一审退回，填写退回意见', '10.12.8.51'),
        ('2026-09-18 09:30', '陈雨桐', '提交投稿，生成 v1', '10.12.34.21'),
        ('2026-09-17 20:12', '陈雨桐', '新建草稿', '10.12.34.21'),
    ])
    body = f'''{page_head(f'{s["title"]} {tag("已退回")}', f'稿件编号 {s["id"]} · 新闻投稿 · 当前版本 v2 · 稿件档案永久保存',
                        a_btn('版本对比', 'version-history.html', '', 'compare') + a_btn('修改后重新提交', 'resubmit.html', 'btn-primary', 'edit'))}
<div class="card" style="padding:20px 24px">{flow_steps('学生', 3, back_at=3)}</div>
<div class="grid g-main mt16">
  <div class="card" data-tabs-scope>
    <div class="tabs" data-tabs><button class="tab on" data-tab="content">稿件内容</button><button class="tab" data-tab="flow">流转记录<span class="cnt">7</span></button><button class="tab" data-tab="ver">修改历史<span class="cnt">2</span></button><button class="tab" data-tab="log">操作日志</button></div>
    <div class="tab-panel on card-body" data-panel="content">{article(s)}<div class="form-section-title mt24">全部配图（3）</div>{gallery(s)}</div>
    <div class="tab-panel card-body" data-panel="flow">{returned_timeline()}</div>
    <div class="tab-panel card-body" data-panel="ver">{versions}</div>
    <div class="tab-panel" data-panel="log">{logs}</div>
  </div>
  <div class="grid" style="align-content:start">
    {card('最新审核意见', f'<div class="notice notice-danger">{icon("undo", 15)}<div><b>{latest[0]} · {latest[1]}</b><br>{latest[4]}<div class="hint mt8">{latest[2]} · 针对 {latest[3]}</div></div></div>' + a_btn('按意见修改并重新提交', 'resubmit.html', 'btn-primary mt16', 'edit', 'style="width:100%"'), 'message')}
    {card('投稿信息', info_kv(s), 'file')}
    {card('统计归档属性', '<div class="flex between"><span class="c-muted">是否计入采用</span>' + tag('不计入采用') + '</div><div class="hint mt8">终审采用后自动计入学院采用统计</div>', 'chart')}
  </div>
</div>'''
    page('submission-detail.html', '稿件档案', body, ['我的投稿', '稿件档案'])


# ---------- 9 版本对比 ----------
def version_history():
    body = f'''{page_head('版本对比', '《“青春志愿行”社区服务周纪实》· 旧版本与退回意见永久保留，不覆盖历史记录', a_btn('返回稿件档案', 'submission-detail.html', '', 'arrow-l') + a_btn('修改后重新提交', 'resubmit.html', 'btn-primary', 'edit'))}
<div class="grid" style="grid-template-columns:280px minmax(0,1fr)">
  <div class="card" style="align-self:start">
    <div class="card-head"><div class="card-title">{icon('history', 18)}版本记录</div></div>
    <div class="card-body">
      <div class="timeline">
        <div class="tl-item"><span class="tl-dot primary"></span><div class="tl-head">v2 · 当前版本</div><div class="tl-meta">2026-09-20 11:40 重新提交</div><div class="tl-opinion danger">二审退回：{RETURN_OPINIONS[0][4]}</div></div>
        <div class="tl-item"><span class="tl-dot"></span><div class="tl-head">v1 · 首次提交</div><div class="tl-meta">2026-09-18 09:30 提交</div><div class="tl-opinion danger">一审退回：{RETURN_OPINIONS[1][4]}</div></div>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="card-head"><div class="card-title">{icon('compare', 18)}v1 → v2 差异</div><div class="legend"><span><i style="background:#FDECEC"></i>删除内容</span><span><i style="background:#E3F8EE"></i>新增内容</span></div></div>
    <div class="card-body">
      <div class="notice notice-warn mb16">{icon('message', 15)}<div>本次修改依据的退回意见（一审 · 刘子涵）：{RETURN_OPINIONS[1][4]}</div></div>
      <table class="tbl"><thead><tr><th style="width:110px">字段</th><th>v1（2026-09-18）</th><th>v2（2026-09-20）</th></tr></thead><tbody>
        <tr><td>新闻标题</td><td><span class="diff-del">青春志愿行社区服务周活动圆满结束</span></td><td><span class="diff-add">“青春志愿行”社区服务周纪实</span></td></tr>
        <tr><td>活动简介</td><td>计算机学院青年志愿者协会开展志愿服务。</td><td>计算机学院青年志愿者协会<span class="diff-add">走进岳麓街道桃花岭社区，开展为期一周的</span>志愿服务。</td></tr>
        <tr><td>正文第 1 段</td><td>近日，计算机学院青年志愿者协会组织志愿者开展“青春志愿行”社区服务周活动。</td><td><span class="diff-add">9月14日至20日，</span>计算机学院青年志愿者协会组织<span class="diff-add">60余名</span>志愿者<span class="diff-add">走进岳麓街道桃花岭社区，</span>开展<span class="diff-add">为期一周的</span>“青春志愿行”社区服务周活动。</td></tr>
        <tr><td>正文第 2 段</td><td>志愿者们教老人使用手机，<span class="diff-del">效果很好</span>。</td><td>志愿者们开设“银龄数字课堂”，手把手教社区老人使用智能手机挂号、缴费和视频通话，<span class="diff-add">累计服务老人200余人次</span>。</td></tr>
        <tr><td>配图</td><td>2 张</td><td>3 张 <span class="diff-add">新增：志愿者合影.jpg</span></td></tr>
        <tr><td>指导老师</td><td>李晓琳（计算机学院）</td><td>李晓琳（计算机学院）</td></tr>
      </tbody></table>
    </div>
  </div>
</div>'''
    page('version-history.html', '版本对比', body, ['我的投稿', '稿件档案', '版本对比'])


# ---------- 10 退回修改 ----------
def resubmit():
    s = dict(RETURNED)
    s['files'] = [(IMG['volunteer'], '志愿者讲解手机使用.jpg', '4.2 MB'), (IMG['students'], '编程启蒙课堂.jpg', '3.8 MB'), (IMG['group'], '志愿者合影.jpg', '5.1 MB')]
    newest = ' <span class="tag tag-danger">最新</span>'
    ops = ''.join(f'<div class="tl-item"><span class="tl-dot danger"></span><div class="tl-head">{n} · {u}{newest if i == 0 else ""}</div><div class="tl-meta">{t} · 针对 {v}</div><div class="tl-opinion danger">{o}</div></div>'
                  for i, (n, u, t, v, o) in enumerate(RETURN_OPINIONS))
    body = f'''{page_head('修改退回稿件', '修改后重新提交将生成 v3 版本，并重新从审核流程起点开始；v1、v2 与历次意见永久保留', a_btn('查看版本对比', 'version-history.html', '', 'compare'))}
<div class="grid g-main-wide">
  <form class="form-card" data-autosave novalidate>
    {identity_section('学生', '李晓琳（计算机学院）')}
    {news_form(s)}
    <div class="form-section"><div class="form-section-title">修改说明</div>{field('本次修改说明', '<textarea class="textarea" name="changeNote" required placeholder="简要说明针对退回意见做了哪些修改，便于审核人员核对"></textarea>', req=True)}</div>
    <div class="form-foot">
      <span class="draft-status" data-draft-status>{icon('clock', 14)}&nbsp;每 30 秒自动保存草稿</span>
      {a_btn('取消', 'submission-detail.html', '', None, 'data-confirm="修改内容已自动保存为草稿，确认离开吗？"')}
      {btn('保存草稿', '', 'save', 'data-action="save-draft"')}
      {btn('重新提交', 'btn-primary', 'send', 'data-action="submit" data-sensitive="#newsTitle,#newsIntro,#newsEditor" data-confirm="重新提交后将生成 v3 版本，并重新进入指导老师审核。确认提交吗？" data-msg="已重新提交，生成 v3 版本" data-next="my-submissions.html?re=1&msg=稿件已重新提交，生成 v3 版本并重新进入审核流程&link=version-history.html&linkText=查看版本记录"')}
    </div>
  </form>
  <div style="align-self:start" class="sticky-actions">
    <div class="card"><div class="card-head"><div class="card-title">{icon('message', 18)}历次退回意见</div><span class="tag tag-danger">2 次</span></div><div class="card-body"><div class="timeline">{ops}</div></div></div>
  </div>
</div>'''
    page('resubmit.html', '修改退回稿件', body, ['我的投稿', '修改重提'])


# ---------- 11 本院统计 ----------
def college_stats():
    own = [r for r in ARCHIVE if r[3] == '计算机学院']
    rows = ''.join(f'<tr data-type="{t}" data-status="{st}"><td><a class="t-title" href="submission-detail.html">{title}</a><div class="t-sub">{sid}</div></td>'
                   f'<td>{type_tag(t)}</td><td>{author}</td><td>{ident}</td><td>{d}</td><td>{tag(st)}</td></tr>'
                   for sid, title, t, c, author, ident, d, st in own)

    def panel(key, total, adopt, reject, back, month, on=''):
        return f'''<div class="tab-panel {on}" data-panel="{key}">
<div class="grid g5">
{stat('file', 'blue', total, '投稿总量')}{stat('check-circle', 'green', adopt, '已采用')}{stat('x-circle', 'gray', reject, '未采用')}{stat('undo', 'red', back, '被退回')}{stat('trend', 'orange', f'{adopt / total * 100:.1f}', '采用率', unit='%')}
</div>
<div class="grid g2 mt16">
{card('月度投稿与采用', bars(month) + '<div class="legend mt12"><span><i style="background:#3087CC"></i>采用</span><span><i style="background:#9CBFDA"></i>未采用 / 审核中</span></div>', 'chart')}
{card('稿件类型分布', donut([('新闻投稿', int(total * .52), '#3087CC'), ('照片投稿', int(total * .24), '#1BB975'), ('视频投稿', int(total * .14), '#F29100'), ('新闻线索', total - int(total * .52) - int(total * .24) - int(total * .14), '#9CBFDA')], center=(str(total), '篇稿件')), 'layers')}
</div></div>'''
    body = f'''{page_head('本院投稿统计', '计算机学院 · 统计本院稿件总量、采用量、未采用量和退回量', btn('导出本院明细', '', 'download', 'data-action="export-csv" data-table="#ownTable" data-filename="计算机学院稿件明细"'))}
<div class="notice notice-info mb16">{icon('lock', 15)}<div><b>数据范围：仅计算机学院。</b>根据校院两级权限隔离规则，投稿人只能查看本院稿件明细，无法查看其他学院稿件详情。</div></div>
<div data-tabs-scope>
  <div class="flex between mb16"><div class="seg" data-tabs><button class="on" data-tab="y26">2026—2027 学年</button><button data-tab="y25">2025—2026 学年</button><button data-tab="s1">本学期</button></div><span class="hint">统计周期由校团委在后台配置</span></div>
  {panel('y26', 86, 52, 12, 9, [('第1周', [12, 8]), ('第2周', [14, 9]), ('第3周', [15, 12]), ('第4周', [11, 5])], 'on')}
  {panel('y25', 214, 131, 38, 27, [('9月', [14, 8]), ('10月', [16, 10]), ('11月', [18, 9]), ('12月', [15, 8]), ('3月', [17, 9]), ('4月', [21, 10]), ('5月', [19, 12]), ('6月', [11, 7])])}
  {panel('s1', 86, 52, 12, 9, [('9月', [52, 34]), ('10月', [0, 0]), ('11月', [0, 0]), ('12月', [0, 0])])}
</div>
<div class="card mt16"><div class="card-head"><div class="card-title">{icon('list', 18)}本院稿件明细</div><div class="flex gap8">{filter_select('ownTable', 'type', '全部类型', ['新闻', '视频', '照片', '线索'])}{filter_select('ownTable', 'status', '全部状态', ['待指导老师审核', '待一审', '待二审', '待三审', '已退回', '已终审采用', '已终审不采用', '已发布'])}</div></div>
{table('ownTable', ['稿件', '类型', '投稿人', '身份', ('投稿日期', 'data-sort'), '状态'], [rows])}</div>'''
    page('college-stats.html', '本院投稿统计', body)


# ---------- 12 全校排行榜 ----------
def ranking():
    own = '计算机学院'
    link = lambda c: (f'<button type="button" class="t-title link-btn" data-open="ownDetailModal">{c}</button>' if c == own
                      else f'<a class="t-title" href="no-permission.html">{c}</a>')
    act = lambda c: (btn('查看本院明细', 'btn-sm btn-primary', 'list', 'data-open="ownDetailModal"') if c == own
                     else '<span class="c-muted">仅本院可查看</span>')
    sem = [(c, int(s * .45), int(a * .42), int(b * .5)) for c, s, a, b in RANKING]
    podium = ''
    for i, (c, s, a, b) in enumerate(sorted(RANKING, key=lambda r: -r[2])[:3]):
        colors = ['linear-gradient(135deg,#FFE9A8,#FFD066)', 'linear-gradient(135deg,#EEF1F5,#D7DEE8)', 'linear-gradient(135deg,#FBE3CF,#F3C39B)']
        podium += f'<div class="card" style="padding:20px;background:{colors[i]};border:none"><div class="flex between"><span class="rank-no r{i + 1}" style="width:32px;height:32px;font-size:15px">{i + 1}</span>{icon("award", 26)}</div><div class="fw mt12" style="font-size:17px">{c}</div><div class="hint" style="color:#5A6270">采用 <b style="font-size:22px;color:var(--text)">{a}</b> 篇 · 投稿 {s} 篇</div></div>'
    heads = [('排名', 'data-sort'), '学院', ('投稿量', 'data-sort'), ('采用量', 'data-sort'), ('退回量', 'data-sort'), ('采用率', 'data-sort'), '操作']
    body = f'''{page_head('全校学院排行榜', '公开榜单 · 按终审采用数量排序；本院可在当前页查看稿件明细，他院明细不对投稿人开放',
                          btn('查看本院明细', 'btn-primary', 'list', 'data-open="ownDetailModal"') + btn('导出排行榜', '', 'download', 'data-action="export-csv" data-table="#rankY" data-filename="全校学院排行榜"'))}
<div class="grid g3 mb16">{podium}</div>
<div class="card" data-tabs-scope>
  <div class="card-head"><div class="seg" data-tabs><button class="on" data-tab="year">2026—2027 学年</button><button data-tab="sem">2026 秋季学期</button><button data-tab="last">2025—2026 学年</button></div><span class="hint">数据更新于 2026-09-30 16:00 · 统计周期后台可配置</span></div>
  <div class="tab-panel on" data-panel="year">{table('rankY', heads, rank_rows(link, action=act), page_size=20)}</div>
  <div class="tab-panel" data-panel="sem">{table('rankS', heads, rank_rows(link, data=sem, action=act), page_size=20)}</div>
  <div class="tab-panel" data-panel="last">{table('rankL', heads, rank_rows(link, data=[(c, s * 2 + 7, a * 2 + 3, b * 2) for c, s, a, b in RANKING], action=act), page_size=20)}</div>
</div>'''
    stat = next(r[1:] for r in RANKING if r[0] == own)
    page('ranking.html', '全校排行榜', body, modals=college_detail_modal('ownDetailModal', own, stat))


# ---------- 13 消息 ----------
def messages():
    items = [
        ('undo', 'red', '稿件被退回', '《“青春志愿行”社区服务周纪实》被二审员周明轩退回：第三段引用居民原话未注明姓名与身份……点击查看并修改', '1 小时前', 'resubmit.html', True),
        ('check-circle', 'green', '稿件终审采用', '《计算机学院学生党支部开展“红色经典诵读”活动》已终审采用，计入本院采用统计', '昨天 10:30', 'submission-detail.html', True),
        ('check', 'blue', '指导老师审核通过', '《学院“算法之星”编程挑战赛精彩瞬间》已由王海峰老师审核通过，进入校团委一审', '09-28 16:35', 'submission-detail.html'),
        ('x-circle', 'orange', '稿件终审未采用', '《新学期“书香计院”读书分享会》终审未采用：同类题材近期已有报道', '09-12 09:10', 'submission-detail.html'),
        ('trophy', 'blue', '排行榜已更新', '9 月学院投稿排行榜已更新，计算机学院以 52 篇采用量位列第 1', '09-30 08:00', 'ranking.html'),
        ('bell', 'blue', '系统通知', '国庆假期（10月1日—7日）不计入审核工作日，节后审核时效顺延', '09-26 17:00', 'messages.html'),
    ]
    page('messages.html', '消息通知', messages_page_body(items))


# ---------- 本院稿件导出弹窗（我的投稿页“导出”按钮） ----------
def export_modal():
    own = [r for r in ARCHIVE if r[3] == '计算机学院']
    csv = '\\n'.join(['稿件编号,标题,类型,投稿人,身份,投稿日期,状态'] + [','.join((sid, title, t, author, ident, d, st)) for sid, title, t, c, author, ident, d, st in own])
    scope = ('<div class="radio-group" style="flex-direction:column;align-items:stretch">'
             '<label class="radio-card"><input type="radio" name="expScope" value="cur" checked>我的投稿（按当前列表筛选结果，<b data-total-for="mySubs">0</b> 条）</label>'
             f'<label class="radio-card"><input type="radio" name="expScope" value="all">本院全部稿件（计算机学院，{len(own)} 条）</label></div>')
    period = f'<select class="select">{options(["2026—2027 学年", "2026 秋季学期", "2025—2026 学年"])}</select>'
    body = f'''<div class="notice notice-warn mb16">{icon('lock', 15)}<div>投稿人<b>仅可导出本院（计算机学院）稿件数据</b>，导出行为将记入操作日志。</div></div>
<div class="grid" style="gap:16px">{field('导出范围', scope)}{field('统计周期', period)}
<div class="field"><label class="lbl">最近导出</label><div class="hint">2026-09-26 10:12 · 本院 2026—2027 学年稿件明细 · Excel · 82 条<br>2026-09-01 15:40 · 本院 2025—2026 学年稿件明细 · CSV · 214 条</div></div></div>'''
    cur = 'data-action="export-csv" data-table="#mySubs" data-filename="我的投稿列表" data-show-when="expScope=cur"'
    all_ = f'data-action="export-csv" data-csv="{csv}" data-filename="计算机学院稿件明细" data-show-when="expScope=all"'
    foot = ('<button class="btn" data-close>取消</button>' +
            btn('导出 CSV', '', 'download', cur) + btn('导出 Excel', 'btn-primary', 'download', cur + ' data-format="Excel"') +
            btn('导出 CSV', 'hidden', 'download', all_) + btn('导出 Excel', 'btn-primary hidden', 'download', all_ + ' data-format="Excel"'))
    return modal('exportModal', '导出稿件', body, foot, 'modal-sm')


# ---------- 15 无权查看 ----------
def no_permission():
    body = f'''<div class="card forbid" style="padding:48px 40px">
<div class="big-ic">{icon('lock', 40)}</div>
<h1 class="page-title" style="justify-content:center">无权查看该学院稿件明细</h1>
<p class="page-desc" style="font-size:14px;margin-top:10px">你当前的角色是 <b>投稿人（计算机学院 · 学生）</b>。根据校院两级数据隔离规则，投稿人只能查看本院稿件明细和全校公开排行榜，无法查看其他学院的稿件详情。</p>
<div class="notice notice-info mt20" style="text-align:left">{icon('info', 15)}<div>如需跨学院协作，请联系校团委宣传部（电话 0731-88830000）。本次越权访问尝试已记入操作日志。</div></div>
<div class="flex gap12 mt24" style="justify-content:center">{a_btn('返回排行榜', 'ranking.html', '', 'arrow-l')}{a_btn('查看本院统计', 'college-stats.html', 'btn-primary', 'chart')}</div>
</div>'''
    page('no-permission.html', '无权查看', body, ['全校排行榜', '无权查看'])


def build():
    dashboard(); submit_news(); submit_video(); submit_photo(); submit_clue(); submit_success()
    my_submissions(); submission_detail(); version_history(); resubmit(); college_stats(); ranking()
    messages(); no_permission()
