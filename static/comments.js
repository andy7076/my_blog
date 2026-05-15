// 分页配置
const COMMENTS_PER_PAGE = 10;
let currentPage = 1;
let totalPages = 1;
let currentSlug = '';

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function loadComments(slug, page = 1) {
    currentSlug = slug;
    currentPage = page;
    
    fetch('/api/comments/' + slug + '?page=' + page + '&per_page=' + COMMENTS_PER_PAGE)
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                totalPages = data.total_pages || 1;
                renderComments(data.comments);
                renderPagination();
            }
        })
        .catch(err => console.error('加载评论失败:', err));
}

function renderComments(comments) {
    const container = document.getElementById('commentsList');
    if (!container) return;
    
    const urlParams = new URLSearchParams(window.location.search);
    const isAdmin = urlParams.get('admin') === 'admin123';
    
    if (comments.length === 0) {
        container.innerHTML = '<div class="no-comments">暂无评论，快来抢沙发吧！</div>';
        return;
    }
    
    let html = '<ul class="comment-list">';
    comments.forEach(function(comment) {
        const time = new Date(comment.created_at).toLocaleString('zh-CN');
        let deleteBtn = '';
        if (isAdmin) {
            deleteBtn = '<button class="comment-delete-btn" onclick="deleteComment(' + comment.id + ')">删除</button>';
        }
        html += '<li class="comment-item">' +
            '<div class="comment-header">' +
                '<span class="comment-username">' + escapeHtml(comment.username) + '</span>' +
                '<span class="comment-time">' + time + '</span>' +
                deleteBtn +
            '</div>' +
            '<div class="comment-content">' + escapeHtml(comment.content) + '</div>' +
        '</li>';
    });
    html += '</ul>';
    container.innerHTML = html;
}

function renderPagination() {
    const paginationContainer = document.getElementById('commentsPagination');
    if (!paginationContainer) return;
    
    // 如果只有一页或没有评论，不显示分页控件
    if (totalPages <= 1) {
        paginationContainer.innerHTML = '';
        return;
    }
    
    let html = '<div class="pagination">';
    
    // 上一页按钮
    if (currentPage > 1) {
        html += '<button class="page-btn" onclick="goToPage(' + (currentPage - 1) + ')">← 上一页</button>';
    } else {
        html += '<button class="page-btn" disabled>← 上一页</button>';
    }
    
    // 页码显示
    html += '<span class="page-info">第 ' + currentPage + ' 页 / 共 ' + totalPages + ' 页</span>';
    
    // 下一页按钮
    if (currentPage < totalPages) {
        html += '<button class="page-btn" onclick="goToPage(' + (currentPage + 1) + ')">下一页 →</button>';
    } else {
        html += '<button class="page-btn" disabled>下一页 →</button>';
    }
    
    html += '</div>';
    paginationContainer.innerHTML = html;
}

function goToPage(page) {
    if (page >= 1 && page <= totalPages && page !== currentPage) {
        loadComments(currentSlug, page);
        // 滚动到评论区域顶部
        const commentsSection = document.getElementById('commentsSection');
        if (commentsSection) {
            commentsSection.scrollIntoView({ behavior: 'smooth' });
        }
    }
}

function submitComment() {
    const username = document.getElementById('commentUsername').value.trim();
    const content = document.getElementById('commentContent').value.trim();
    const messageDiv = document.getElementById('commentMessage');
    
    if (!username || !content) {
        messageDiv.innerHTML = '<div class="comment-error">请填写用户名和评论内容</div>';
        return;
    }
    
    fetch('/api/comments/' + currentSlug, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username, content: content })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            messageDiv.innerHTML = '<div class="comment-success">评论提交成功！</div>';
            document.getElementById('commentUsername').value = '';
            document.getElementById('commentContent').value = '';
            // 提交后回到第一页显示最新评论
            loadComments(currentSlug, 1);
            setTimeout(function() { messageDiv.innerHTML = ''; }, 3000);
        } else {
            messageDiv.innerHTML = '<div class="comment-error">' + (data.error || '提交失败') + '</div>';
        }
    })
    .catch(err => {
        messageDiv.innerHTML = '<div class="comment-error">提交失败，请重试</div>';
        console.error(err);
    });
}

function deleteComment(commentId) {
    if (!confirm('确定要删除这条评论吗？')) {
        return;
    }
    
    fetch('/api/comments/delete/' + commentId, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // 删除后重新加载当前页的评论
            loadComments(currentSlug, currentPage);
        } else {
            alert(data.error || '删除失败');
        }
    })
    .catch(err => {
        alert('删除失败，请重试');
        console.error(err);
    });
}

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    // 从 URL 获取 slug
    const pathParts = window.location.pathname.split('/');
    const slug = pathParts[pathParts.length - 1];
    if (slug) {
        currentSlug = slug;
        loadComments(slug, 1);
    }
});