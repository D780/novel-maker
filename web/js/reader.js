// 文件读取功能
class FileReader {
    constructor() {
        this.projectPath = null;
    }

    async selectProject() {
        // 使用 File API 选择项目目录
        if ('showDirectoryPicker' in window) {
            const dirHandle = await window.showDirectoryPicker();
            this.projectPath = dirHandle;
            return true;
        }
        return false;
    }

    async readFile(path) {
        // 读取文件内容
        if (this.projectPath) {
            try {
                const fileHandle = await this.projectPath.getFileHandle(path);
                const file = await fileHandle.getFile();
                return await file.text();
            } catch (e) {
                console.error('Error reading file:', e);
                return null;
            }
        }
        return null;
    }

    async listChapters() {
        // 列出所有章节
        const chapters = [];
        if (this.projectPath) {
            try {
                const novelsDir = await this.projectPath.getDirectoryHandle('novels');
                for await (const entry of novelsDir.values()) {
                    if (entry.kind === 'directory' && entry.name.startsWith('volume')) {
                        const chaptersDir = await entry.getDirectoryHandle('chapters');
                        for await (const chapter of chaptersDir.values()) {
                            if (chapter.name.endsWith('.md')) {
                                chapters.push(`${entry.name}/chapters/${chapter.name}`);
                            }
                        }
                    }
                }
            } catch (e) {
                console.error('Error listing chapters:', e);
            }
        }
        return chapters.sort();
    }
}

window.fileReader = new FileReader();
