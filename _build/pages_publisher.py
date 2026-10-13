# PC 与移动端 · 升华网管理员（只协助把三审完毕的稿件复制进升华网）
from lib import icon, tag, btn, m_page, pc_page, write
from pages_admin import PUBLISH_QUEUE, publish_queue_body
from common import msg_item, messages_page_body


def build():
    write('pc/publisher/publish.html', pc_page(
        'publisher', 'publish.html', '升华网发布素材', publish_queue_body(), crumbs=['升华网发布素材']))
    notes = [
        ('globe', 'blue', '待升华网发布', '《中南学子在第十二届“挑战杯”湖南省大学生创业计划竞赛中获佳绩》待复制进升华网', '20 分钟前', 'publish.html', True),
        ('check-circle', 'green', '稿件已发布', '《冶金学院新生入学教育》已标记为已发布', '昨天', 'publish.html'),
    ]
    write('pc/publisher/messages.html', pc_page(
        'publisher', 'publish.html', '消息通知', messages_page_body(notes, '待升华网发布与已发布提醒'), crumbs=['消息通知']))
    items = ''
    for sid, title, t, col, d, st, copyable in PUBLISH_QUEUE:
        tip = '可复制进升华网' if copyable and st == '待升华网发布' else ('已发布' if st == '已发布' else '不可复制')
        items += (f'<div class="m-item"><div class="m-item-top"><div class="m-item-title">{title}</div>{tag(st)}</div>'
                  f'<div class="m-item-meta"><span>{t}</span><span>{col}</span><span>{tip}</span></div>'
                  f'<div class="m-item-foot"><span class="c-muted">{sid} · 终审 {d[5:]}</span></div></div>')
    mark = btn('标记当前新闻为已发布', 'btn-success btn-block', 'check',
               'data-action="set-status" data-target=".js-row-pub" data-value="已发布" data-hide="#mMark" '
               'data-title="标记为已发布" data-confirm="请确认已在升华网完成该新闻的发布。" data-msg="已标记为已发布"')
    body = f'''<div class="notice notice-info">{icon("globe", 14)}<div>这里列出三审完毕的稿件。只有【待升华网发布】的新闻可以复制正文；不采用、视频、照片和线索只备查。</div></div>
<div class="m-card" style="margin-top:10px"><b>当前待发布</b><div class="msg-desc">《中南学子在第十二届“挑战杯”湖南省大学生创业计划竞赛中获佳绩》 · <span class="js-row-pub">待升华网发布</span></div>
<div id="mMark" class="mt12">{mark}</div></div>
<div id="pubList">{items}</div>'''
    write('mobile/publisher/publish.html', m_page(
        'publisher', '升华网发布', body, tab='publish.html', pc_link='../../pc/publisher/publish.html'))
    msgs = notes
    write('mobile/publisher/messages.html', m_page(
        'publisher', '消息', ''.join(msg_item(*i[:6], unread=len(i) > 6 and i[6]) for i in msgs),
        tab='messages.html', right='<button class="link" data-action="read-all">全部已读</button>',
        pc_link='../../pc/publisher/publish.html'))
