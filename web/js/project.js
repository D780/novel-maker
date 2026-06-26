/**
 * NovelMaker - 项目管理模块
 * 处理项目的增删改查和切换
 */

// 项目管理类
class ProjectManager {
    constructor() {
        this.projects = [];
        this.activeProject = null;
        this.loadProjects();
    }
    
    // 加载项目列表
    loadProjects() {
        const saved = localStorage.getItem('novel-maker-projects');
        if (saved) {
            this.projects = JSON.parse(saved);
            
            // 找到活跃项目
            const activeId = localStorage.getItem('novel-maker-active-project');
            if (activeId) {
                this.activeProject = this.projects.find(p => p.id === activeId);
            }
            
            // 如果没有活跃项目，使用第一个
            if (!this.activeProject && this.projects.length > 0) {
                this.activeProject = this.projects[0];
            }
        }
    }
    
    // 保存项目列表
    saveProjects() {
        localStorage.setItem('novel-maker-projects', JSON.stringify(this.projects));
        if (this.activeProject) {
            localStorage.setItem('novel-maker-active-project', this.activeProject.id);
        }
    }
    
    // 添加项目
    addProject(name, path = '') {
        const project = {
            id: this.generateId(),
            name: name,
            path: path,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            chapters: 0,
            words: 0
        };
        
        this.projects.push(project);
        
        // 如果是第一个项目，设为活跃
        if (this.projects.length === 1) {
            this.activeProject = project;
        }
        
        this.saveProjects();
        return project;
    }
    
    // 删除项目
    deleteProject(projectId) {
        const index = this.projects.findIndex(p => p.id === projectId);
        if (index !== -1) {
            this.projects.splice(index, 1);
            
            // 如果删除的是活跃项目，切换到第一个
            if (this.activeProject && this.activeProject.id === projectId) {
                this.activeProject = this.projects.length > 0 ? this.projects[0] : null;
            }
            
            this.saveProjects();
            return true;
        }
        return false;
    }
    
    // 切换项目
    switchProject(projectId) {
        const project = this.projects.find(p => p.id === projectId);
        if (project) {
            this.activeProject = project;
            this.saveProjects();
            return true;
        }
        return false;
    }
    
    // 更新项目信息
    updateProject(projectId, updates) {
        const project = this.projects.find(p => p.id === projectId);
        if (project) {
            Object.assign(project, updates, { updatedAt: new Date().toISOString() });
            this.saveProjects();
            return true;
        }
        return false;
    }
    
    // 获取活跃项目
    getActiveProject() {
        return this.activeProject;
    }
    
    // 获取所有项目
    getAllProjects() {
        return this.projects;
    }
    
    // 生成唯一 ID
    generateId() {
        return 'project_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
}

// 全局项目管理器实例
const projectManager = new ProjectManager();

// 渲染项目列表
function loadProjectList() {
    const container = document.getElementById('project-list');
    if (!container) return;
    
    const projects = projectManager.getAllProjects();
    const activeProject = projectManager.getActiveProject();
    
    container.innerHTML = '';
    
    if (projects.length === 0) {
        container.innerHTML = '<li class="project-item"><em>暂无项目，请添加一个项目。</em></li>';
        return;
    }
    
    projects.forEach(project => {
        const li = document.createElement('li');
        li.className = `project-item ${activeProject && activeProject.id === project.id ? 'active' : ''}`;
        
        li.innerHTML = `
            <div>
                <strong>${project.name}</strong>
                <br>
                <small>章节数：${project.chapters || 0} | 字数：${project.words || 0}</small>
                <br>
                <small>最后更新：${new Date(project.updatedAt).toLocaleString()}</small>
            </div>
            <div class="project-actions">
                <button class="btn btn-primary" onclick="switchToProject('${project.id}')">
                    ${activeProject && activeProject.id === project.id ? '当前' : '切换'}
                </button>
                <button class="btn btn-danger" onclick="deleteProject('${project.id}')">删除</button>
            </div>
        `;
        
        container.appendChild(li);
    });
}

// 添加项目
function addProject() {
    const name = prompt('请输入项目名称：');
    if (name) {
        const path = prompt('请输入项目路径（可选）：') || '';
        projectManager.addProject(name, path);
        loadProjectList();
        alert('项目添加成功');
    }
}

// 删除项目
function deleteProject(projectId) {
    if (confirm('确定要删除这个项目吗？')) {
        projectManager.deleteProject(projectId);
        loadProjectList();
        alert('项目已删除');
    }
}

// 切换到项目
function switchToProject(projectId) {
    if (projectManager.switchProject(projectId)) {
        loadProjectList();
        alert('已切换到项目');
    }
}

// 导入项目
function importProject() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = function(e) {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                const projectData = JSON.parse(e.target.result);
                
                if (projectData.name) {
                    projectManager.addProject(projectData.name, projectData.path || '');
                    loadProjectList();
                    alert('项目导入成功');
                } else {
                    alert('项目文件格式错误');
                }
            } catch (error) {
                alert('项目文件格式错误');
            }
        };
        reader.readAsText(file);
    };
    input.click();
}

// 导出项目
function exportProject(projectId) {
    const project = projectManager.getAllProjects().find(p => p.id === projectId);
    if (project) {
        const blob = new Blob([JSON.stringify(project, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${project.name}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }
}
