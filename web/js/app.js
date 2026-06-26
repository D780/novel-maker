// 主应用逻辑
class NovelMakerApp {
    constructor() {
        this.currentView = 'overview';
        this.init();
    }

    init() {
        this.bindEvents();
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

    switchView(viewName) {
        // 更新导航状态
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.classList.toggle('active', link.dataset.view === viewName);
        });

        // 更新视图显示
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
