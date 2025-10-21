"""
自动同步上游仓库脚本
从原仓库同步最新更新到您的fork仓库
"""

import subprocess
import sys
import os
from datetime import datetime

def run_command(command, description):
    """执行git命令并显示结果"""
    print(f"[正在执行] {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__)
        )

        if result.returncode == 0:
            if result.stdout.strip():
                print(f"[成功] {description}")
                print(f"   输出: {result.stdout.strip()}")
            else:
                print(f"[完成] {description}")
        else:
            print(f"[失败] {description}")
            print(f"   错误: {result.stderr.strip()}")
            return False
        return True

    except Exception as e:
        print(f"[错误] 执行命令时出错: {e}")
        return False

def check_git_status():
    """检查git状态"""
    print("[检查] 正在检查git状态...")

    # 检查是否有未提交的更改
    result = subprocess.run(
        "git status --porcelain",
        shell=True,
        capture_output=True,
        text=True,
        cwd=os.path.dirname(__file__)
    )

    if result.stdout.strip():
        print("[警告] 检测到未提交的更改:")
        print(result.stdout.strip())

        response = input("是否继续同步？(y/N): ").lower().strip()
        if response != 'y':
            print("[取消] 已取消同步操作")
            return False
    else:
        print("[正常] 工作区干净，可以继续")

    return True

def main():
    """主函数"""
    print("=" * 60)
    print("Yuxi-Know 自动同步工具")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 检查git状态
    if not check_git_status():
        sys.exit(1)

    # 检查upstream是否已配置
    print("\n[检查] 正在检查远程仓库配置...")
    result = subprocess.run(
        "git remote -v",
        shell=True,
        capture_output=True,
        text=True,
        cwd=os.path.dirname(__file__)
    )

    if "upstream" not in result.stdout:
        print("[错误] 未找到upstream仓库，请先运行:")
        print("   git remote add upstream https://github.com/xerrors/Yuxi-Know.git")
        sys.exit(1)

    print("[成功] 远程仓库配置正确")

    # 执行同步步骤
    print("\n[开始] 正在执行同步流程...")

    steps = [
        ("git fetch upstream", "从上游仓库获取最新更新"),
        ("git checkout main", "切换到main分支"),
        ("git merge upstream/main", "合并上游更新到本地"),
        ("git push origin main", "推送更新到您的fork仓库")
    ]

    success_count = 0
    for command, description in steps:
        if run_command(command, description):
            success_count += 1
        else:
            print(f"\n[失败] 同步失败在步骤: {description}")
            sys.exit(1)

    print("\n" + "=" * 60)
    print(f"[完成] 同步完成！成功执行 {success_count}/{len(steps)} 个步骤")
    print("[状态] 您的仓库现在已是最新版本")
    print("=" * 60)

if __name__ == "__main__":
    main()