# PC 端 · 副书记（学院副书记，学工系统固定角色，按投稿人所在学院自动路由，无需配置）
from lib import card, btn, a_btn, pc_page, write
from data import DEPUTY_TODO, FEATURED
from common import featured_flow_timeline, messages_page_body
from workflow import norm, todo_body, done_body, cc_body, batch_body, detail_body, node_chart, flow_name
from review import review_body, reject_modal, q, type_review_pages, type_done_pages
from detail import sub_content

R = 'deputy'
P = 'pc/deputy/'
SID = FEATURED['id']
ROWS = norm(DEPUTY_TODO, 'deputy')
TPL_DEPUTY = ['稿件政治导向需进一步把关，请修改相关表述后重新提交。', '涉及学院重要活动的表述与学院通稿不一致，请核对后修改。',
              '活动信息需与学院官方发布保持一致，请补充核实来源。']
PASS_MSG = '副书记审核通过，稿件已报送校团委一审'
PASS_NEXT = q('todo.html', done=SID, msg=PASS_MSG, link=q('history.html', new=SID, act='pass'), linkText='查看已办')
REJECT_NEXT = q('todo.html', done=SID, type='warn', msg='已退回稿件，系统已通知投稿学生陈雨桐', link=q('history.html', new=SID, act='reject'), linkText='查看已办')
SCOPE = card('副书记审核说明', f'<div style="font-size:13px;line-height:1.9;color:var(--text-2)">· 副书记为投稿人所在学院的副书记，<b>取自学工系统，无需配置</b>。<br>'
                         '· 学生稿件在指导老师通过后到达；教师稿件提交后直接到达。<br>· 通过后报送校团委一审；退回须填写意见，稿件回到投稿人修改。</div>', 'shield')
NEW_ROWS = []


def page(file, title, body, crumbs=None, modals='', active=None):
    write(P + file, pc_page(R, active or file, title, body, crumbs=crumbs, modals=modals, todo_count=len(ROWS)))


def todo():
    page('todo.html', '待办', todo_body('dTodo', ROWS, '副书记审核', 'review.html'), ['待办'])


def review_actions():
    return (btn('通过，报送一审', 'btn-success btn-lg', 'check', f'data-action="pass" data-opinion="optional" data-tpl="deputy" data-title="副书记审核通过" data-ok="确认通过" data-msg="{PASS_MSG}" data-next="{PASS_NEXT}"') +
            a_btn('退回修改', 'review-reject.html', 'btn-danger-o btn-lg', 'undo'))


def review(reject=False):
    d = ROWS[[r['sid'] for r in ROWS].index(SID)]
    body = review_body(FEATURED, '待副书记审核', '副书记审核', 2, (d['rem'], d['lv']), featured_flow_timeline('deputy'), review_actions(), 'todo.html',
                       start=FEATURED['time'], arrive=d['arrive'], extra_right=SCOPE)
    modals = reject_modal('rejectBox', '退回稿件', '退回意见', TPL_DEPUTY, REJECT_NEXT) if reject else ''
    page('review-reject.html' if reject else 'review.html', '办理', body, ['待办', '新闻投稿审核'], modals, active='todo.html')


def typed_pages():
    global NEW_ROWS
    made = type_review_pages(page, ROWS, '副书记审核', 'deputy', 'todo.html', 'history.html', 'deputy', '通过，报送一审', PASS_MSG, '待办',
                             extra_right=SCOPE)
    NEW_ROWS = [(sid, title, t, author, col, '2026-09-30 16:40') for sid, title, t, author, col in made.values()]
    type_done_pages(page, '副书记审核', 'history.html')


def history():
    base = [
        ('TG2026092702', '学院“算法之星”编程挑战赛精彩瞬间', '照片', '陈雨桐', '学生', '2026-09-27 15:02', '已通过', '0.3 个工作日', '及时', '同意报送校团委一审。'),
        ('TG2026092606', '计算机学院教工“三全育人”工作坊', '新闻', '李晓琳', '教师', '2026-09-27 10:40', '已通过', '0.6 个工作日', '及时', '内容导向正确，同意报送。'),
        ('TG2026092504', '计算机学院学生会换届大会', '新闻', '周子墨', '学生', '2026-09-26 16:20', '已退回', '1.1 个工作日', '及时', '活动信息需与学院官方发布保持一致，请补充核实来源。'),
        ('TG2026092503', '新生军训风采纪实短片《淬炼》', '视频', '李晓琳', '教师', '2026-09-25 15:30', '已通过', '0.2 个工作日', '及时', '同意报送。'),
        ('TG2026092004', '校友返校讲述“北斗”研发故事', '线索', '陈雨桐', '学生', '2026-09-21 15:10', '已通过', '0.4 个工作日', '及时', '线索价值较高，同意报送。'),
        ('TG2026091805', '计算机学院学生党支部开展“红色经典诵读”活动', '新闻', '陈雨桐', '学生', '2026-09-19 17:00', '已通过', '0.5 个工作日', '及时', '同意报送。'),
        ('TG2026091206', '学院开学典礼现场图集', '照片', '李晓琳', '教师', '2026-09-12 16:30', '已通过', '3.2 个工作日', '超时', '同意报送。'),
    ]
    rows = [(sid, title, t, author, '计算机学院', st, op, time, cost, ok) for sid, title, t, author, ident, time, st, cost, ok, op in base]
    body = done_body('dHis', rows, '副书记审核', 'done-detail.html', ('已通过', '已退回'),
                     [(SID, FEATURED['title'], '新闻', '陈雨桐', '计算机学院', '2026-09-30 16:40')] + NEW_ROWS, '副书记已办记录')
    page('history.html', '已办', body, ['已办'])


def cc():
    urges = [(flow_name('新闻', '计算机学院“程序设计月”闭幕式'), '副书记审核', '系统（超时自动催办）', '2026-09-24 15:00', '2026-09-29 09:00'),
             (flow_name('新闻', '计算机学院“网络安全宣传周”系列活动'), '副书记审核', '张静（校团委管理员）', '2026-09-29 15:40', '2026-09-30 09:30')]
    copies = [(flow_name('新闻', '计算机学院学生党支部开展“红色经典诵读”活动'), '三审终审', '张静（校团委管理员）', '2026-09-19 10:30', '已读'),
              (flow_name('视频', '新生军训风采纪实短片《淬炼》'), '二审', '周明轩（二审员）', '2026-09-27 09:20', '未读')]
    page('cc.html', '催办/抄送', cc_body(urges, copies, 'review.html', 'done-detail.html'), ['催办/抄送'])


def batch():
    page('batch.html', '批量审批', batch_body(ROWS, '副书记审核', 'review.html', 'deputy'), ['批量审批'])


def done_detail():
    body = detail_body(FEATURED, '已通过', 'tag-solid-ok', node_chart('学生', 3), featured_flow_timeline('r1'), 'history.html',
                       FEATURED['time'], FEATURED['times']['teacher'], sub_content(FEATURED))
    page('done-detail.html', '已办详情', body, ['已办', '新闻投稿审核'], active='history.html')


def messages():
    items = [
        ('inbox', 'blue', '新的待审稿件', '《计算机学院“网络安全宣传周”系列活动》已通过指导老师审核，请在 3 个工作日内审核', '20 分钟前', 'review.html', True),
        ('inbox', 'blue', '教师投稿待审', '李晓琳老师提交了《计算机学院教工党支部“书香润初心”读书会》，教师稿件提交后直接到达副书记审核', '1 小时前', 'review-photo.html', True),
        ('alert', 'red', '审核超时提醒', '《计算机学院“程序设计月”闭幕式》已超过审核时限 0.5 个工作日，已记入超时台账', '今天 09:00', 'todo.html'),
        ('check-circle', 'green', '您审核的稿件已终审采用', '《计算机学院学生党支部开展“红色经典诵读”活动》已由校团委终审采用', '09-19 10:30', 'history.html'),
    ]
    page('messages.html', '消息通知', messages_page_body(items))


def build():
    todo(); review(); review(True); typed_pages(); history(); cc(); batch(); done_detail(); messages()
