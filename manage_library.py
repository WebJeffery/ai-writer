import os
import sys

BASE_DIR = "私有知识库"
CATEGORIES = ["文风样本", "故事库", "领域知识"]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def list_files(category=None):
    files = []
    search_dirs = [category] if category else CATEGORIES
    
    print(f"\n--- 📂 知识库文件列表 ---")
    for cat in search_dirs:
        dir_path = os.path.join(BASE_DIR, cat)
        if os.path.exists(dir_path):
            cat_files = [f for f in os.listdir(dir_path) if not f.startswith('.')]
            if cat_files:
                print(f"\n[{cat}]")
                for f in cat_files:
                    print(f"  - {f}")
                    files.append((cat, f))
            else:
                print(f"\n[{cat}] (空)")
        else:
            print(f"\n[{cat}] (目录不存在)")
    print("\n-------------------------")
    return files

def get_file_content(category, filename):
    path = os.path.join(BASE_DIR, category, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"读取失败: {e}"

def build_prompt():
    print("\n🚀 开始构建爆款写作 Prompt...")
    
    # 1. 选择文风
    print("\n1️⃣  选择文风样本 (输入文件名，留空跳过):")
    list_files("文风样本")
    style_file = input("文件名 > ").strip()
    style_content = ""
    if style_file:
        style_content = get_file_content("文风样本", style_file)
    
    # 2. 选择故事
    print("\n2️⃣  选择个人故事 (输入文件名，留空跳过):")
    list_files("故事库")
    story_file = input("文件名 > ").strip()
    story_content = ""
    if story_file:
        story_content = get_file_content("故事库", story_file)

    # 3. 输入选题
    topic = input("\n3️⃣  输入文章选题/主题 > ").strip()
    
    # 4. 生成 Prompt
    print("\n" + "="*50)
    print("✨ 生成的 Prompt (可直接复制到 AI):")
    print("="*50)
    
    prompt = "你是一个专业的自媒体爆款文章写手。\n\n"
    
    if style_content:
        prompt += f"【文风参考】\n请严格模仿以下文章的语言风格、句式结构和情感基调：\n{style_content[:500]}...\n(略)\n\n"
        
    if story_content:
        prompt += f"【个人故事素材】\n请在文章中自然地融入以下个人经历，以增加真实感：\n{story_content}\n\n"
        
    prompt += f"【写作任务】\n请基于以上要求，写一篇关于“{topic}”的文章。\n"
    prompt += "要求：\n1. 标题要有吸引力（爆款标题）。\n2. 开头即高潮，吸引读者注意力。\n3. 金句频出，引发共鸣。"
    
    print(prompt)
    print("="*50)

def main():
    while True:
        print("\n=== 🧠 AI 写作私有知识库管家 ===")
        print("1. 查看所有文件")
        print("2. 构建写作 Prompt")
        print("3. 退出")
        
        choice = input("\n请选择功能 (1-3): ").strip()
        
        if choice == '1':
            list_files()
        elif choice == '2':
            build_prompt()
        elif choice == '3':
            print("👋 再见！")
            break
        else:
            print("❌ 无效输入")

if __name__ == "__main__":
    # 确保目录存在
    for cat in CATEGORIES:
        os.makedirs(os.path.join(BASE_DIR, cat), exist_ok=True)
        
    main()
