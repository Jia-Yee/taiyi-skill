#!/usr/bin/env python3
"""
Taiyi - 虚拟人物人格管理脚本
用于创建、存储和管理虚拟人物人格
"""

import os
import json
import sys
from pathlib import Path

# 数据存储目录
TAIYI_DIR = Path.home() / ".qclaw" / "taiyi"
TAIYI_DIR.mkdir(parents=True, exist_ok=True)

def create_persona(name: str, info: dict = None) -> dict:
    """创建新人物人格"""
    persona_dir = TAIYI_DIR / name
    persona_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建人格文件
    persona = {
        "name": name,
        "info": info or {"created": "unknown"},
        "works": [],
        "knowledge": {},
        "persona": {
            "style": "scholarly",
            "traits": [],
            "thinking_mode": ""
        }
    }
    
    # 写入信息文件
    with open(persona_dir / "info.json", "w", encoding="utf-8") as f:
        json.dump(persona, f, ensure_ascii=False, indent=2)
    
    return persona

def get_persona(name: str) -> dict:
    """获取人物人格信息"""
    persona_file = TAIYI_DIR / name / "info.json"
    if not persona_file.exists():
        return None
    
    with open(persona_file, encoding="utf-8") as f:
        return json.load(f)

def list_personas() -> list:
    """列出所有已创建的人物人格"""
    if not TAIYI_DIR.exists():
        return []
    return [d.name for d in TAIYI_DIR.iterdir() if d.is_dir()]

def update_persona(name: str, data: dict) -> bool:
    """更新人物人格信息"""
    persona_dir = TAIYI_DIR / name
    if not persona_dir.exists():
        return False
    
    persona_file = persona_dir / "info.json"
    with open(persona_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True

def delete_persona(name: str) -> bool:
    """删除人物人格"""
    import shutil
    persona_dir = TAIYI_DIR / name
    if not persona_dir.exists():
        return False
    
    shutil.rmtree(persona_dir)
    return True

if __name__ == "__main__":
    # 简单命令行接口
    if len(sys.argv) < 2:
        print("Usage: python taiyi.py <command> [args]")
        print("Commands:")
        print("  list                    - 列出所有人物")
        print("  create <name>           - 创建人物")
        print("  get <name>              - 获取人物信息")
        print("  delete <name>           - 删除人物")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        print("已创建的人物人格:")
        for p in list_personas():
            print(f"  - {p}")
    elif cmd == "create" and len(sys.argv) > 2:
        name = sys.argv[2]
        create_persona(name)
        print(f"已创建人物: {name}")
    elif cmd == "get" and len(sys.argv) > 2:
        name = sys.argv[2]
        persona = get_persona(name)
        if persona:
            print(json.dumps(persona, ensure_ascii=False, indent=2))
        else:
            print(f"未找到人物: {name}")
    elif cmd == "delete" and len(sys.argv) > 2:
        name = sys.argv[2]
        if delete_persona(name):
            print(f"已删除人物: {name}")
        else:
            print(f"未找到人物: {name}")
    else:
        print("Unknown command")
        sys.exit(1)