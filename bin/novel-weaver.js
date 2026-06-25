#!/usr/bin/env node

import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync, copyFileSync, lstatSync, realpathSync, rmSync } from 'fs';
import { resolve, dirname, join } from 'path';
import { fileURLToPath } from 'url';
import readline from 'readline';

// 递归复制目录
function copyDirSync(src, dest) {
  let realSrc = src;
  try { realSrc = realpathSync(src); } catch {}
  mkdirSync(dest, { recursive: true });
  const entries = readdirSync(realSrc, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name === '.DS_Store') continue;
    const srcPath = join(realSrc, entry.name);
    const destPath = join(dest, entry.name);
    let stat;
    try { stat = lstatSync(srcPath); } catch { continue; }
    if (stat.isSymbolicLink()) {
      try {
        const real = realpathSync(srcPath);
        const realStat = lstatSync(real);
        if (realStat.isDirectory()) copyDirSync(real, destPath);
        else copyFileSync(real, destPath);
      } catch {}
    } else if (stat.isDirectory()) {
      copyDirSync(srcPath, destPath);
    } else if (stat.isFile()) {
      copyFileSync(srcPath, destPath);
    }
  }
}

const __dirname = dirname(fileURLToPath(import.meta.url));
const PKG = JSON.parse(readFileSync(resolve(__dirname, '..', 'package.json'), 'utf8'));
const SKILLS_SRC = resolve(__dirname, '..', 'skill');
const PROJECT_DIR = process.cwd();

// 支持的 IDE 列表
const TARGETS = [
  { name: 'Claude Code',   dir: '.claude/skills/novel-weaver',  detect: '.claude' },
  { name: 'Cursor',        dir: '.cursor/rules/novel-weaver',   detect: ['.cursor', '.cursorrules'] },
  { name: 'Codex CLI',     dir: '.codex/skills/novel-weaver',   detect: '.codex' },
  { name: 'Kiro',          dir: '.kiro/steering/novel-weaver',  detect: '.kiro' },
  { name: 'DeerFlow',      dir: 'skills/custom/novel-weaver',   detect: 'deer_flow' },
  { name: 'Trae',          dir: '.trae/skills/novel-weaver',    detect: '.trae' },
  { name: 'Antigravity',   dir: '.agents/skills/novel-weaver',  detect: '.agents' },
  { name: 'VS Code',       dir: '.github/superpowers/novel-weaver', detect: '.github/copilot-instructions.md' },
  { name: 'OpenClaw',      dir: 'skills/novel-weaver',          detect: '.openclaw' },
  { name: 'Windsurf',      dir: '.windsurf/skills/novel-weaver', detect: '.windsurf' },
  { name: 'Gemini CLI',    dir: '.gemini/skills/novel-weaver',  detect: 'GEMINI.md' },
  { name: 'Aider',         dir: '.aider/skills/novel-weaver',   detect: '.aider' },
  { name: 'OpenCode',      dir: '.opencode/skills/novel-weaver', detect: '.opencode' },
  { name: 'Qwen Code',     dir: '.qwen/skills/novel-weaver',    detect: '.qwen' },
  { name: 'Hermes Agent',  dir: '.hermes/skills/novel-weaver',  detect: ['.hermes', 'HERMES.md', '.hermes.md'] },
  { name: 'Claw Code',     dir: '.claw/skills/novel-weaver',    detect: ['.claw', 'CLAW.md'] },
  { name: 'Qoder',         dir: '.qoder/skills/novel-weaver',   detect: '.qoder' },
  { name: 'Copilot CLI',   dir: '.claude/skills/novel-weaver',  detect: '.claude' },
];

// 工具名称别名映射
const TOOL_ALIASES = {
  'claude': 'Claude Code',
  'claude-code': 'Claude Code',
  'cursor': 'Cursor',
  'codex': 'Codex CLI',
  'kiro': 'Kiro',
  'deerflow': 'DeerFlow',
  'trae': 'Trae',
  'antigravity': 'Antigravity',
  'vscode': 'VS Code',
  'vs-code': 'VS Code',
  'openclaw': 'OpenClaw',
  'windsurf': 'Windsurf',
  'gemini': 'Gemini CLI',
  'gemini-cli': 'Gemini CLI',
  'aider': 'Aider',
  'opencode': 'OpenCode',
  'qwen': 'Qwen Code',
  'qwen-code': 'Qwen Code',
  'hermes': 'Hermes Agent',
  'hermes-agent': 'Hermes Agent',
  'claw': 'Claw Code',
  'claw-code': 'Claw Code',
  'qoder': 'Qoder',
  'copilot': 'Copilot CLI',
  'copilot-cli': 'Copilot CLI',
};

function detectIDEs() {
  const detected = [];
  for (const target of TARGETS) {
    const detect = Array.isArray(target.detect) ? target.detect : [target.detect];
    for (const d of detect) {
      if (existsSync(resolve(PROJECT_DIR, d))) {
        detected.push(target);
        break;
      }
    }
  }
  return detected;
}

function installSkill(target) {
  const destDir = resolve(PROJECT_DIR, target.dir);
  console.log(`  安装到 ${target.name}: ${target.dir}`);
  copyDirSync(SKILLS_SRC, destDir);
  console.log(`  ✅ ${target.name} 安装成功`);
}

function uninstallSkill() {
  console.log('🗑️  卸载 NovelWeaver...\n');
  console.log('⚠️  警告：此操作将删除以下目录及其所有内容：\n');
  for (const target of TARGETS) {
    const destDir = resolve(PROJECT_DIR, target.dir);
    if (existsSync(destDir)) {
      console.log(`  - ${target.name}: ${target.dir}`);
    }
  }
  console.log('\n如果目录中包含自定义文件，它们将被永久删除。');
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  rl.question('\n确认卸载？(y/N): ', (answer) => {
    rl.close();
    if (answer.toLowerCase() !== 'y' && answer.toLowerCase() !== 'yes') {
      console.log('❌ 卸载已取消');
      return;
    }
    for (const target of TARGETS) {
      const destDir = resolve(PROJECT_DIR, target.dir);
      if (existsSync(destDir)) {
        rmSync(destDir, { recursive: true, force: true });
        console.log(`  ✅ ${target.name} 已卸载`);
      }
    }
    console.log('\n✅ 卸载完成');
  });
}

function showHelp() {
  console.log(`
novel-weaver v${PKG.version} - 全能网文写作助手

用法：
  npx novel-weaver                   自动检测 IDE 并安装
  npx novel-weaver --tool trae       指定 IDE 安装
  npx novel-weaver --uninstall       卸载
  npx novel-weaver --help            显示帮助

支持的 IDE：
  ${[...new Set(Object.values(TOOL_ALIASES))].join(', ')}
`);
}

function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    showHelp();
    return;
  }
  
  if (args.includes('--uninstall')) {
    uninstallSkill();
    return;
  }
  
  // 解析 --tool 参数
  let toolArg = null;
  const toolIdx = args.indexOf('--tool');
  if (toolIdx !== -1 && args[toolIdx + 1]) {
    toolArg = args[toolIdx + 1].toLowerCase();
  }
  
  console.log(`
  NovelWeaver v${PKG.version} - 全能网文写作助手
  6角色协作架构，用说话的方式写小说
  `);
  
  let targets;
  
  if (toolArg) {
    const toolName = TOOL_ALIASES[toolArg];
    if (!toolName) {
      console.log(`❌ 未知的工具: ${toolArg}`);
      console.log(`支持的: ${[...new Set(Object.values(TOOL_ALIASES))].join(', ')}`);
      process.exit(1);
    }
    targets = TARGETS.filter(t => t.name === toolName);
  } else {
    targets = detectIDEs();
  }
  
  if (targets.length === 0) {
    console.log('❌ 未检测到 IDE，请使用 --tool 参数指定');
    console.log(`支持的: ${[...new Set(Object.values(TOOL_ALIASES))].join(', ')}`);
    process.exit(1);
  }
  
  console.log(`检测到 ${targets.length} 个 IDE:\n`);
  for (const t of targets) {
    console.log(`  - ${t.name}`);
  }
  console.log();
  
  // 去重
  const uniqueTargets = [];
  const seenDirs = new Set();
  for (const t of targets) {
    if (!seenDirs.has(t.dir)) {
      seenDirs.add(t.dir);
      uniqueTargets.push(t);
    }
  }
  
  for (const target of uniqueTargets) {
    installSkill(target);
  }
  
  console.log(`
✅ 安装完成！

在 IDE 聊天框输入以下指令开始创作：
  /novel-weaver init 开始写小说
  /novel-weaver help 查看帮助
`);
}

main();
