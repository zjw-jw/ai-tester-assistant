"""独立初始化知识库脚本（思路 A）
在启动 Streamlit 之前，先在这里把知识库建好，避免启动时卡死。
"""
from __future__ import annotations

import sys
from pathlib import Path

# 确保能 import 到项目模块（在根目录运行时通常不需要，保险起见）
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import config as app_config
from rag.knowledge_base import KnowledgeBaseManager


def main() -> None:
    print("=" * 60)
    print("AI 测试员助手平台 · 知识库初始化")
    print("=" * 60)

    app_config.ensure_dirs()
    app_config.setup_logging()

    manager = KnowledgeBaseManager(on_log=print)

    print("\n[1/3] 读取知识库状态 ...")
    statuses = manager.statuses()
    for s in statuses:
        icon = "🟢" if s.ready else "⚪"
        print(f"  {icon} {s.name}: {s.count} 个片段")

    print("\n[2/3] 检查并构建空知识库 ...")
    pending = [s for s in statuses if s.count == 0]
    if not pending:
        print("  所有知识库已就绪，无需构建。")
    else:
        for s in pending:
            print(f"  → 正在构建「{s.name}」...")
            result = manager.rebuild(s.key)
            print(f"    ✅ 完成：{result.get('files', 0)} 个文件 / {result.get('chunks', 0)} 个片段")

    print("\n[3/3] 检查向量模型一致性 ...")
    info = manager.embedding_info
    print(f"  当前向量模型：{info.quality_hint}（kind={info.kind}, dim={info.dim}）")

    stale = manager.stale_domains()
    if not stale:
        print("  所有知识库向量模型一致，无需重建。")
    else:
        for s in stale:
            print(f"  → 正在用「{info.kind}」重建「{s.name}」...")
            result = manager.rebuild(s.key)
            print(f"    ✅ 完成：{result.get('chunks', 0)} 个片段")

    print("\n" + "=" * 60)
    print("✅ 知识库初始化完成，现在可以启动 Streamlit 了：")
    print("   streamlit run app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()