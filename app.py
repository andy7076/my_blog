import os
import sqlite3
from datetime import datetime
from functools import wraps

import markdown
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    send_from_directory,
)

app = Flask(__name__)
app.config["POSTS_DIR"] = os.path.join(os.path.dirname(__file__), "posts")
app.config["DATABASE"] = os.path.join(os.path.dirname(__file__), "comments.db")

# 百度统计代码
BAIDU_TONGJI_CODE = """
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?YOUR_TONGJI_ID";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>
"""


def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库"""
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT NOT NULL,
            username TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


def parse_post(filename):
    """解析 Markdown 文章"""
    import re
    
    filepath = os.path.join(app.config["POSTS_DIR"], filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 解析 YAML front matter
    parts = content.split("---", 2)
    if len(parts) >= 3:
        front_matter = parts[1].strip()
        body = parts[2].strip()
    else:
        front_matter = ""
        body = content.strip()

    # 解析 front matter 字段
    meta = {}
    for line in front_matter.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()

    # 转换 Markdown 为 HTML
    html_body = markdown.markdown(
        body, extensions=["tables", "fenced_code", "codehilite"]
    )
    
    # 从渲染后的 HTML 中提取纯文本摘要
    # 1. 移除 HTML 标签
    text_only = re.sub(r'<[^>]+>', '', html_body)
    # 2. 移除代码块和多余空白
    text_only = re.sub(r'\s+', ' ', text_only).strip()
    # 3. 截取前 200 字符
    excerpt = text_only[:200] + ('...' if len(text_only) > 200 else '')

    return {
        "slug": filename.replace(".md", ""),
        "title": meta.get("title", filename.replace(".md", "").replace("-", " ")),
        "date": meta.get("date", "未知日期"),
        "tags": meta.get("tags", ""),
        "body": body,
        "html_body": html_body,
        "excerpt": excerpt,
    }


def get_all_posts():
    """获取所有文章列表"""
    posts = []
    posts_dir = app.config["POSTS_DIR"]
    if not os.path.exists(posts_dir):
        return posts

    for filename in os.listdir(posts_dir):
        if filename.endswith(".md"):
            try:
                post = parse_post(filename)
                posts.append(post)
            except Exception as e:
                print(f"解析文章失败 {filename}: {e}")

    # 按日期倒序排列（最新的在前）
    def parse_date(date_str):
        """解析日期字符串，支持多种格式"""
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"):
            try:
                return datetime.strptime(date_str, fmt)
            except (ValueError, TypeError):
                continue
        return datetime.min  # 无法解析的日期排在最后

    posts.sort(key=lambda p: parse_date(p.get("date", "")), reverse=True)
    return posts


# ==================== 路由 ====================


@app.route("/")
def index():
    """首页 - 显示所有文章列表"""
    page = request.args.get("page", 1, type=int)
    per_page = 20
    all_posts = get_all_posts()
    total = len(all_posts)
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    posts = all_posts[start:start + per_page]
    active_tab = request.args.get("tab", "tools")
    if active_tab not in ("tools", "posts", "about"):
        active_tab = "tools"
    return render_template(
        "index.html",
        posts=posts,
        page=page,
        total_pages=total_pages,
        total=total,
        baidu_tongji=BAIDU_TONGJI_CODE,
        active_tab=active_tab,
    )


@app.route("/post/<slug>")
def post(slug):
    """显示单篇文章"""
    filename = f"{slug}.md"
    filepath = os.path.join(app.config["POSTS_DIR"], filename)

    if not os.path.exists(filepath):
        return "文章不存在", 404

    post = parse_post(filename)
    return render_template(
        "post.html", post=post, baidu_tongji=BAIDU_TONGJI_CODE, active_tab="posts"
    )


@app.route("/ads.txt")
def ads_txt():
    """提供 ads.txt 文件访问"""
    return send_from_directory(
        os.path.join(os.path.dirname(__file__), "static"),
        "ads.txt",
        mimetype="text/plain",
    )


# ==================== 评论 API ====================


@app.route("/api/comments/<slug>")
def get_comments(slug):
    """获取文章的评论（带分页）"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    conn = get_db()
    total = conn.execute(
        "SELECT COUNT(*) FROM comments WHERE slug = ?", (slug,)
    ).fetchone()[0]

    offset = (page - 1) * per_page
    comments = conn.execute(
        "SELECT * FROM comments WHERE slug = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (slug, per_page, offset),
    ).fetchall()
    conn.close()

    total_pages = (total + per_page - 1) // per_page if total > 0 else 1

    # 将 UTC 时间转换为北京时间（UTC+8）
    from datetime import datetime, timedelta
    def to_beijing_time(dt_str):
        if not dt_str:
            return dt_str
        try:
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            beijing_dt = dt + timedelta(hours=8)
            return beijing_dt.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            return dt_str

    comments_data = []
    for c in comments:
        c_dict = dict(c)
        c_dict["created_at"] = to_beijing_time(c_dict.get("created_at"))
        comments_data.append(c_dict)

    return jsonify(
        {
            "success": True,
            "comments": comments_data,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
        }
    )


@app.route("/api/comments/<slug>", methods=["POST"])
def add_comment(slug):
    """添加评论"""
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "无效的数据"}), 400

    username = data.get("username", "").strip()
    content = data.get("content", "").strip()

    if not username or not content:
        return jsonify({"success": False, "error": "用户名和评论内容不能为空"}), 400

    if len(username) > 50:
        return jsonify({"success": False, "error": "用户名不能超过50个字符"}), 400

    if len(content) > 1000:
        return jsonify({"success": False, "error": "评论内容不能超过1000个字符"}), 400

    conn = get_db()
    conn.execute(
        "INSERT INTO comments (slug, username, content) VALUES (?, ?, ?)",
        (slug, username, content),
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "评论提交成功"})


@app.route("/api/comments/delete/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    """删除评论"""
    conn = get_db()
    conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "评论删除成功"})


# ==================== 模板 ====================


@app.template_filter("nl2br")
def nl2br(text):
    """将换行符转换为 <br> 标签"""
    import markupsafe

    return markupsafe.Markup(text.replace("\n", "<br>\n"))


# ==================== 启动 ====================

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=8081)
