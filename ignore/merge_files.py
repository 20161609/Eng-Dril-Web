import os

# 무시할 디렉토리 목록
IGNORE_DIRS = {".venv", "venv", "__pycache__"}

# 포함할 확장자 및 파일명
INCLUDE_EXTS = {".py", ".txt", ".env", ".md", ".yaml"}
INCLUDE_FILENAMES = {"Dockerfile", ".dockerignore", ".gitignore"}

OUTPUT_FILE = "merged_text.txt"

def should_include(file):
    if file in INCLUDE_FILENAMES:
        return True
    _, ext = os.path.splitext(file)
    return ext in INCLUDE_EXTS

def build_tree(base_dir):
    """디렉토리 트리 문자열 생성"""
    lines = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        level = root.replace(base_dir, "").count(os.sep)
        indent = "│   " * level
        lines.append(f"{indent}├── {os.path.basename(root) or '.'}")
        for f in files:
            if should_include(f):
                lines.append(f"{indent}│   ├── {f}")
    return "\n".join(lines)

def merge_files(base_dir):
    result = []
    result.append("# === Directory Structure ===\n")
    result.append(build_tree(base_dir))
    result.append("\n\n# === File Contents ===\n")

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if not should_include(file):
                continue
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                relative_path = os.path.relpath(path, base_dir)
                result.append(f'"""\n{content}\n"""({relative_path})\n')
            except Exception as e:
                print(f"[WARN] {file} 읽기 실패: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("\n".join(result))

    print(f"✅ 완료: {OUTPUT_FILE} 생성됨")

if __name__ == "__main__":
    base_dir = os.getcwd()
    merge_files(base_dir)
