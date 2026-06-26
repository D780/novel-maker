// Markdown 渲染
class MarkdownRenderer {
    constructor() {
        if (typeof marked !== 'undefined') {
            marked.setOptions({
                breaks: true,
                gfm: true
            });
        }
    }

    render(content) {
        if (typeof marked !== 'undefined') {
            return marked.parse(content);
        }
        // 简单的 Markdown 渲染
        return content
            .replace(/^### (.*$)/gm, '<h3>$1</h3>')
            .replace(/^## (.*$)/gm, '<h2>$1</h2>')
            .replace(/^# (.*$)/gm, '<h1>$1</h1>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }
}

window.markdownRenderer = new MarkdownRenderer();
