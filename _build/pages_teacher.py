# PC 端 · 指导老师
from lib import icon, tag, type_tag, remain, stat, card, page_head, btn, a_btn, filter_select, search_box, \
    filter_bar, table, pc_page, write
from data import TEACHER_TODO, TEACHER_REVIEWED, FEATURED
from query import query_pages
from common import featured_flow_timeline, messages_page_body
from detail import sub_content
from workflow import norm, todo_body, done_body, cc_body, batch_body, detail_body, node_chart, flow_name
from review import review_body, reject_modal, q, type_review_pages, type_done_pages

R = 'teacher'
P = 'pc/teacher/'
SID = FEATURED['id']
NEW_ROWS = []
TPL_TEACHER = ['稿件导语不够精炼，请突出活动核心亮点后重新提交。', '配图数量不足或清晰度不够，请补充 3 张以上高清原图。',
               '活动时间、地点等要素缺失，请补全新闻五要素。']

PASS_NEXT = q('dashboard.html', done=SID, msg='已审核通过，稿件已提交学院副书记审核', link=q('history.html', new=SID, act='pass'), linkText='查看已办')
REJECT_NEXT = q('dashboard.html', done=SID, type='warn', msg='已退回稿件，系统已通知投稿学生陈雨桐', link=q('history.html', new=SID, act='reject'), linkText='查看已办')


def page(file, title, body, crumbs=None, modals='', active=None):
    write(P + file, pc_page(R, active or file, title, body, crumbs=crumbs, modals=modals))


def dashboard():
    rows = norm(TEACHER_TODO, 'teacher')
    page('dashboard.html', '待办', todo_body('tTodo', rows, '指导老师审核', 'review.html'), ['待办'])


def review_actions():
    return (btn('通过，提交副书记审核', 'btn-success btn-lg', 'check', f'data-action="pass" data-opinion="optional" data-tpl="teacher" data-title="通过，提交副书记审核" data-ok="确认通过" data-msg="审核通过，稿件已提交学院副书记审核" data-next="{PASS_NEXT}"') +
            a_btn('退回修改', 'review-reject.html', 'btn-danger-o btn-lg', 'undo'))


def review(reject=False):
    body = review_body(FEATURED, '待指导老师审核', '指导老师审核', 1, ('剩余 0.5 个工作日', 'warn'),
                       featured_flow_timeline('teacher'), review_actions(), 'dashboard.html', arrive=FEATURED['time'])
    modals = reject_modal('rejectBox', '退回稿件', '退回意见', TPL_TEACHER, REJECT_NEXT) if reject else ''
    file = 'review-reject.html' if reject else 'review.html'
    page(file, '办理', body, ['待办', '新闻投稿审核'], modals, active='dashboard.html')


def typed_pages():
    global NEW_ROWS
    made = type_review_pages(page, norm(TEACHER_TODO, 'teacher'), '指导老师审核', 'teacher', 'dashboard.html', 'history.html', 'teacher',
                             '通过，提交副书记审核', '审核通过，稿件已提交学院副书记审核', '待办')
    NEW_ROWS = [(sid, title, t, author, col, '2026-09-30 16:30') for sid, title, t, author, col in made.values()]
    type_done_pages(page, '指导老师审核', 'history.html')


def history():
    base = [
        ('TG2026092702', '学院“算法之星”编程挑战赛精彩瞬间', '照片', '陈雨桐', '2026-09-27 11:20', '已通过', '0.8 个工作日', '及时', '内容基本符合要求，同意报送校团委。'),
        ('TG2026092601', '计算机学院“程序设计月”启动仪式', '新闻', '周子墨', '2026-09-27 10:20', '已退回', '1.2 个工作日', '及时', '活动时间、地点等要素缺失，请补全新闻五要素。'),
        ('TG2026092004', '校友返校讲述“北斗”研发故事', '线索', '陈雨桐', '2026-09-21 09:00', '已通过', '0.5 个工作日', '及时', '线索价值较高，建议校团委安排采访。'),
        ('TG2026091805', '学生党支部开展“红色经典诵读”活动', '新闻', '陈雨桐', '2026-09-18 20:10', '已通过', '1 个工作日', '及时', '同意报送。'),
        ('TG2026091510', '“挑战杯”校赛备赛动员会', '新闻', '林嘉懿', '2026-09-18 17:40', '已通过', '3.5 个工作日', '超时', '同意报送。'),
        ('TG2026090807', '新学期“书香计院”读书分享会', '新闻', '陈雨桐', '2026-09-09 11:10', '已通过', '0.6 个工作日', '及时', '同意报送。'),
        ('TG2026090508', '“智能+”暑期社会实践成果展示', '视频', '陈雨桐', '2026-09-06 15:20', '已通过', '0.9 个工作日', '及时', '视频链接已确认为永久有效。'),
    ]
    rows = [(sid, title, t, author, '计算机学院', st, op, time, cost, ok) for sid, title, t, author, time, st, cost, ok, op in base]
    body = done_body('tHis', rows, '指导老师审核', 'done-detail.html', ('已通过', '已退回'),
                     [(SID, FEATURED['title'], '新闻', '陈雨桐', '计算机学院', '2026-09-30 16:30')] + NEW_ROWS, '指导老师已办记录')
    page('history.html', '已办', body, ['已办'])


def cc():
    urges = [(flow_name('新闻', '“代码为桥”乡村小学编程支教纪实'), '指导老师审核', '系统（超时自动催办）', '2026-09-24 09:40', '2026-09-29 09:00'),
             (flow_name('新闻', FEATURED['title']), '指导老师审核', '张静（校团委管理员）', '2026-09-28 10:24', '2026-09-30 09:00')]
    copies = [(flow_name('新闻', '学生党支部开展“红色经典诵读”活动'), '三审终审', '张静（校团委管理员）', '2026-09-19 10:30', '已读'),
              (flow_name('照片', '学院“算法之星”编程挑战赛精彩瞬间'), '一审', '刘子涵（一审员）', '2026-09-29 15:20', '未读')]
    page('cc.html', '催办/抄送', cc_body(urges, copies, 'review.html', 'done-detail.html'), ['催办/抄送'])


def batch():
    page('batch.html', '批量审批', batch_body(norm(TEACHER_TODO, 'teacher'), '指导老师审核', 'review.html', 'teacher'), ['批量审批'])


def done_detail():
    body = detail_body(FEATURED, '已通过', 'tag-solid-ok', node_chart('学生', 2), featured_flow_timeline('deputy'), 'history.html',
                       FEATURED['time'], FEATURED['time'], sub_content(FEATURED))
    page('done-detail.html', '已办详情', body, ['已办', '新闻投稿审核'], active='history.html')


def messages():
    items = [
        ('inbox', 'blue', '新的待审稿件', '陈雨桐提交了《计算机学院举办2026级新生“科技启航”主题团日活动》，请在 3 个工作日内审核', '10 分钟前', 'review.html', True),
        ('alert', 'red', '审核超时提醒', '《“代码为桥”乡村小学编程支教纪实》已超过审核时限 1.5 个工作日，已记入超时台账', '今天 09:00', 'dashboard.html', True),
        ('check-circle', 'green', '您审核的稿件已终审采用', '《学生党支部开展“红色经典诵读”活动》已由校团委终审采用', '09-19 10:30', 'history.html'),
        ('bell', 'blue', '系统通知', '国庆假期（10月1日—7日）不计入审核工作日，节后审核时效顺延', '09-26 17:00', 'messages.html'),
    ]
    page('messages.html', '消息通知', messages_page_body(items))


def build():
    dashboard(); review(); review(True); typed_pages(); history()
    query_pages(page, '指导老师审核', TEACHER_REVIEWED, '只显示指定您为指导老师、且您已审核过的学生稿件（含跨学院选择您的学生）；')
    cc(); batch(); done_detail(); messages()
