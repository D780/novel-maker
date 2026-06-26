// 编辑器功能
class Editor {
    constructor() {
        this.content = '';
        this.init();
    }

    init() {
        const textarea = document.getElementById('editor-content');
        const preview = document.getElementById('editor-preview');

        if (textarea && preview) {
            textarea.addEventListener('input', () => {
                this.content = textarea.value;
                preview.innerHTML = window.markdownRenderer.render(this.content);
            });
        }
    }

    setContent(content) {
        this.content = content;
        const textarea = document.getElementById('editor-content');
        const preview = document.getElementById('editor-preview');

        if (textarea) {
            textarea.value = content;
        }
        if (preview) {
            preview.innerHTML = window.markdownRenderer.render(content);
        }
    }

    getContent() {
        return this.content;
    }

    async save() {
        // 保存文件
        console.log('Saving...');
    }
}

window.editor = new Editor();
