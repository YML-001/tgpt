# 升华网发布素材：清洗后的正文、ZIP 包结构、复制与导出按钮（审核人员、管理员共用）
from lib import icon, btn
from data import ADOPTED


def clean_text(sub=ADOPTED):
    lines = [sub['title'], '', f'撰稿：{sub["writer"]}　所属学院：{sub["college"]}　拍摄时间：{sub["shoot"]}', f'活动简介：{sub["intro"]}', '']
    for i, p in enumerate(sub['paras']):
        lines.append(p)
        if i < len(sub['captions']):
            lines.append(f'【此处插入图片{i + 1}：图片{i + 1}.jpg（{sub["captions"][i]}）】')
        lines.append('')
    return '\n'.join(lines).strip()


def clean_text_html(sub=ADOPTED):
    import re
    txt = clean_text(sub)
    return re.sub(r'(【此处插入图片[^】]+】)', r'<span class="ph">\1</span>', txt)


def zip_tree(sub=ADOPTED):
    folder = f'{sub["title"][:14]}…_{sub["id"]}'
    imgs = ''.join(f'<div>    ├─ 图片{i + 1}.jpg <span class="c">#{c}（原图）</span></div>' for i, c in enumerate(sub['captions']))
    return (f'<div class="zip-tree"><div class="d">{folder}/</div><div>├─ 新闻正文.txt <span class="c"># 纯文本正文 + 撰稿人、学院、拍摄时间、活动简介</span></div>'
            f'<div class="d">└─ images/ <span class="c"># 全部原始图片，不压缩画质</span></div>{imgs}</div>')


def export_buttons(sub=ADOPTED, size=''):
    images = '|'.join(sub['images'])
    folder = f'{sub["title"][:14]}_{sub["id"]}'
    return (btn('复制升华网可用正文', f'btn-outline {size}', 'copy', f'data-action="copy" data-target="#cleanText" data-log="复制升华网可用正文（{sub["id"]}）" data-msg="已复制清洗后的正文，请到升华网编辑器粘贴；图片需按占位提示单独上传"') +
            btn('导出升华网素材包', f'btn-primary {size}', 'package', f'data-action="export-zip" data-target="#cleanText" data-images="{images}" data-folder="{folder}" data-log="导出升华网素材包（{sub["id"]}）"'))


def publish_panel(sub=ADOPTED):
    return f'''<div class="notice notice-info mb16">{icon('info', 15)}<div><b>仅【已终审采用】的新闻投稿显示本功能。</b>视频、照片、线索类稿件及未终审稿件不提供升华网素材导出。受浏览器限制，复制时图片无法随文字一起粘贴，请按占位提示单独上传原图。</div></div>
<div class="grid g2">
  <div><div class="flex between mb16"><b>清洗后的正文预览</b><span class="hint">已去除本系统样式、自定义标签与多余换行</span></div><div class="clean-text" id="cleanText">{clean_text_html(sub)}</div></div>
  <div><div class="flex between mb16"><b>素材包目录结构</b><span class="hint">ZIP 格式</span></div>{zip_tree(sub)}
    <div class="notice notice-warn mt16">{icon('flow', 15)}<div>发布步骤：① 复制正文粘贴到升华网编辑器 → ② 按占位提示上传 images 中的原图 → ③ 补全撰稿人等元信息并发布 → ④ 由管理员在本平台将稿件标记为【已发布】。</div></div>
    <div class="flex gap8 mt16">{export_buttons(sub)}</div>
  </div>
</div>'''
