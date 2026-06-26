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
        // 导航切换
        document.querySelectorAll('.sidebar nav li').forEach(item => {
            item.addEventListener('click', () => {
                const view = item.dataset.view;
                this.switchView(view);
            });
        });
    }

    switchView(viewName) {
        // 更新导航状态
        document.querySelectorAll('.sidebar nav li').forEach(item => {
            item.classList.toggle('active', item.dataset.view === viewName);
        });

        // 更新视图显示
        document.querySelectorAll('.view').forEach(view => {
            view.classList.toggle('active', view.id === viewName);
        });

        this.currentView = viewName;
    }

    async loadProject() {
        // 加载项目数据
        // 实际实现需要通过 File API 读取本地文件
        console.log('Loading project...');
    }
}

// 初始化应用
const app = new NovelMakerApp();
