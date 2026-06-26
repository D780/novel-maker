// 主应用逻辑
class NovelMakerApp {
    constructor() {
        this.currentView = 'overview';
        this.prompts = {
            'btn-new-chapter': '请帮我新建一个章节。我需要你：\n1. 基于当前大纲，为我创建下一章的章节文件\n2. 填写章节标题、大纲要点、预计字数\n3. 在 chapters/ 目录下生成对应的章节文件\n\n请先确认当前进度，然后创建新章节。',
            'btn-import': '请帮我导入一个已有项目。我需要你：\n1. 扫描当前目录下的小说文件（markdown/txt 格式）\n2. 解析章节结构、角色信息、世界观设定\n3. 生成项目配置文件（.novel-maker/）\n4. 更新大纲和角色档案\n\n请先列出当前目录下可导入的文件。',
            'btn-export': '请帮我导出项目数据。我需要你：\n1. 收集所有章节内容、角色档案、大纲\n2. 生成完整的项目快照\n3. 输出为可分享的格式（markdown 或 json）\n\n请先确认要导出的内容范围。'
        };
        this.init();
    }

    init() {
        this.bindEvents();
        this.bindQuickActions();
        this.loadProject();
    }

    bindEvents() {
        // 导航切换 - 顶部导航栏
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const view = link.dataset.view;
                this.switchView(view);
            });
        });
    }

    bindQuickActions() {
        Object.keys(this.prompts).forEach(id => {
            const btn = document.getElementById(id);
            if (btn) {
                btn.addEventListener('click', () => {
                    this.copyPrompt(id);
                });
            }
        });
    }

    async copyPrompt(btnId) {
        const prompt = this.prompts[btnId];
        if (!prompt) return;

        try {
            await navigator.clipboard.writeText(prompt);
            this.showToast('已复制提示词，请粘贴到 Trae 聊天框');
        } catch {
            // fallback for non-secure contexts
            const textarea = document.createElement('textarea');
            textarea.value = prompt;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            this.showToast('已复制提示词，请粘贴到 Trae 聊天框');
        }
    }

    showToast(message) {
        const existing = document.querySelector('.toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        document.body.appendChild(toast);

        requestAnimationFrame(() => {
            toast.classList.add('toast-visible');
        });

        setTimeout(() => {
            toast.classList.remove('toast-visible');
            setTimeout(() => toast.remove(), 300);
        }, 2500);
    }

    switchView(viewName) {
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.classList.toggle('active', link.dataset.view === viewName);
        });

        document.querySelectorAll('.view').forEach(view => {
            view.classList.toggle('active', view.id === viewName);
        });

        this.currentView = viewName;
    }

    async loadProject() {
        console.log('Loading project...');
    }
}

const app = new NovelMakerApp();
