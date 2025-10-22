"""
通用Git仓库自动同步脚本
从原仓库同步最新更新到您的fork仓库
"""

# ==========================================
# 配置参数区域 - 请根据您的仓库修改以下参数
# ==========================================

# 项目名称（用于显示）
PROJECT_NAME = "Yuxi-Know"

# 上游仓库地址（原始仓库的Git URL）
UPSTREAM_REPO_URL = "https://github.com/xerrors/Yuxi-Know.git"

# 主分支名称（通常是 main 或 master）
MAIN_BRANCH = "main"

# 远程仓库名称
UPSTREAM_REMOTE = "upstream"  # 上游仓库的远程名称
ORIGIN_REMOTE = "origin"      # 您的fork仓库的远程名称

# 是否在检测到未提交更改时自动stash（True/False）
AUTO_STASH = False

# 是否自动添加upstream（如果未配置）
AUTO_ADD_UPSTREAM = True

# ==========================================
# 脚本逻辑区域 - 以下代码无需修改
# ==========================================

import subprocess
import sys
import os
from datetime import datetime


def run_command(command, description, silent=False):
    """执行git命令并显示结果"""
    if not silent:
        print(f"[正在执行] {description}...")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
        )

        if result.returncode == 0:
            if result.stdout.strip():
                if not silent:
                    print(f"[成功] {description}")
                    if len(result.stdout.strip()) < 200:  # 只显示较短的输出
                        print(f"   输出: {result.stdout.strip()}")
            else:
                if not silent:
                    print(f"[完成] {description}")
            return True, result.stdout
        else:
            print(f"[失败] {description}")
            print(f"   错误: {result.stderr.strip()}")
            return False, result.stderr

    except Exception as e:
        print(f"[错误] 执行命令时出错: {e}")
        return False, str(e)


def check_is_git_repo():
    """检查当前目录是否是git仓库"""
    success, _ = run_command(
        "git rev-parse --git-dir",
        "检查是否为git仓库",
        silent=True
    )
    
    if not success:
        print("[错误] 当前目录不是git仓库！")
        print("\n请确保：")
        print("  1. 已经fork了目标仓库到你的GitHub账号")
        print("  2. 使用 'git clone https://github.com/你的用户名/仓库名.git' 克隆了你的fork仓库")
        print("  3. 在仓库根目录运行此脚本")
        return False
    
    return True


def verify_origin_remote():
    """验证origin是否指向用户的fork仓库"""
    print("\n[检查] 验证远程仓库配置...")
    
    success, output = run_command(
        f"git remote get-url {ORIGIN_REMOTE}",
        f"获取 {ORIGIN_REMOTE} 仓库地址",
        silent=True
    )
    
    if not success:
        print(f"[错误] 未找到 {ORIGIN_REMOTE} 远程仓库！")
        print("\n这通常意味着你没有正确clone你的fork仓库。")
        print("请检查你是否：")
        print(f"  1. 已经fork了仓库到你的GitHub账号")
        print(f"  2. clone的是你自己的fork仓库（不是原仓库）")
        return False
    
    origin_url = output.strip()
    print(f"[信息] {ORIGIN_REMOTE} 仓库: {origin_url}")
    
    # 警告：如果origin和upstream相同
    if origin_url == UPSTREAM_REPO_URL:
        print("\n" + "!" * 60)
        print("[警告] 检测到 origin 和 upstream 指向同一个仓库！")
        print("!" * 60)
        print("\n这意味着你可能直接clone了原仓库，而不是你的fork。")
        print("\n正确的操作流程应该是：")
        print("  1. 在GitHub上fork原仓库到你的账号")
        print("  2. clone你自己的fork仓库")
        print(f"     git clone https://github.com/你的用户名/{PROJECT_NAME}.git")
        print("\n当前配置下，脚本会尝试推送到原仓库，这可能会失败！")
        
        response = input("\n是否仍要继续？(y/N): ").lower().strip()
        if response != 'y':
            return False
    
    return True


def check_git_status():
    """检查git状态"""
    print("\n[检查] 正在检查工作区状态...")

    success, output = run_command(
        "git status --porcelain",
        "检查工作区状态",
        silent=True
    )

    if not success:
        return False

    if output.strip():
        print("[警告] 检测到未提交的更改:")
        print(output.strip())

        if AUTO_STASH:
            print("\n[自动] 将暂存未提交的更改...")
            return run_command(
                "git stash",
                "暂存未提交的更改"
            )[0]
        else:
            response = input("\n是否继续同步？未提交的更改可能会丢失！(y/N): ").lower().strip()
            if response != 'y':
                print("[取消] 已取消同步操作")
                return False
    else:
        print("[正常] 工作区干净，可以继续")

    return True


def check_and_setup_upstream():
    """检查并设置upstream仓库"""
    print("\n[检查] 正在检查上游仓库配置...")
    
    success, output = run_command(
        "git remote -v",
        "获取远程仓库列表",
        silent=True
    )

    if not success:
        return False

    if UPSTREAM_REMOTE not in output:
        print(f"[提示] 未找到 {UPSTREAM_REMOTE} 仓库")
        
        if AUTO_ADD_UPSTREAM:
            print(f"[自动] 正在添加 {UPSTREAM_REMOTE} 仓库...")
            success, _ = run_command(
                f"git remote add {UPSTREAM_REMOTE} {UPSTREAM_REPO_URL}",
                f"添加 {UPSTREAM_REMOTE} 远程仓库"
            )
            if not success:
                return False
        else:
            print(f"[错误] 请先手动运行:")
            print(f"   git remote add {UPSTREAM_REMOTE} {UPSTREAM_REPO_URL}")
            return False
    
    # 显示当前远程仓库配置
    print(f"\n[信息] 当前远程仓库配置:")
    success, output = run_command("git remote -v", "查看远程仓库", silent=True)
    if success:
        for line in output.strip().split('\n'):
            print(f"   {line}")

    print(f"\n[说明] 同步流程:")
    print(f"   1. 从 {UPSTREAM_REMOTE} 拉取更新（原仓库，只读）")
    print(f"   2. 合并到本地 {MAIN_BRANCH} 分支")
    print(f"   3. 推送到 {ORIGIN_REMOTE}（你的fork仓库）")
    print(f"\n[保证] 你的本地修改只会推送到你自己的仓库，不会影响原仓库！")

    return True


def sync_repository():
    """执行同步流程"""
    print("\n" + "=" * 60)
    print("[开始] 正在执行同步流程...")
    print("=" * 60)

    steps = [
        (f"git fetch {UPSTREAM_REMOTE}", f"从 {UPSTREAM_REMOTE} 仓库获取最新更新"),
        (f"git checkout {MAIN_BRANCH}", f"切换到 {MAIN_BRANCH} 分支"),
        (f"git merge {UPSTREAM_REMOTE}/{MAIN_BRANCH}", f"合并 {UPSTREAM_REMOTE} 更新到本地"),
        (f"git push {ORIGIN_REMOTE} {MAIN_BRANCH}", f"推送更新到 {ORIGIN_REMOTE} 仓库")
    ]

    success_count = 0
    for i, (command, description) in enumerate(steps, 1):
        print(f"\n步骤 {i}/{len(steps)}:")
        if run_command(command, description)[0]:
            success_count += 1
        else:
            print(f"\n[失败] 同步失败在步骤: {description}")
            
            # 特殊提示
            if "push" in command:
                print("\n可能的原因：")
                print("  1. 网络连接问题")
                print("  2. 没有推送权限（请确认origin指向你的fork仓库）")
                print("  3. 需要先设置Git凭据")
            
            return False, success_count, len(steps)

    return True, success_count, len(steps)


def restore_stash():
    """恢复stash的更改"""
    if AUTO_STASH:
        print("\n[恢复] 正在恢复之前暂存的更改...")
        success, output = run_command(
            "git stash list",
            "检查stash列表",
            silent=True
        )
        
        if success and output.strip():
            run_command("git stash pop", "恢复暂存的更改")


def print_help():
    """打印使用帮助"""
    print("\n" + "=" * 60)
    print(" 使用指南")
    print("=" * 60)
    print("\n如果这是第一次使用，请确保：")
    print("\n 1  已经在GitHub上fork了目标仓库")
    print(" 2  clone的是你自己的fork仓库：")
    print(f"   git clone https://github.com/你的用户名/{PROJECT_NAME}.git")
    print("\n 3  修改了脚本开头的配置参数：")
    print(f"   - PROJECT_NAME: 项目名称")
    print(f"   - UPSTREAM_REPO_URL: 原仓库地址")
    print(f"   - MAIN_BRANCH: 主分支名称")
    print("\n 4  在仓库根目录运行脚本：")
    print(f"   python sync_upstream.py")
    print("\n" + "=" * 60)


def main():
    """主函数"""
    print("=" * 60)
    print(f" {PROJECT_NAME} 自动同步工具")
    print(f" 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print(f"\n 配置信息:")
    print(f"   项目名称: {PROJECT_NAME}")
    print(f"   上游仓库: {UPSTREAM_REPO_URL}")
    print(f"   主分支: {MAIN_BRANCH}")
    print(f"   远程配置: {ORIGIN_REMOTE} <- {UPSTREAM_REMOTE}")
    print(f"   自动Stash: {'是' if AUTO_STASH else '否'}")
    print(f"   自动添加Upstream: {'是' if AUTO_ADD_UPSTREAM else '否'}")

    try:
        # 检查是否为git仓库
        if not check_is_git_repo():
            print_help()
            sys.exit(1)

        # 验证origin配置
        if not verify_origin_remote():
            sys.exit(1)

        # 检查git状态
        if not check_git_status():
            sys.exit(1)

        # 检查并设置upstream
        if not check_and_setup_upstream():
            sys.exit(1)

        # 最后确认
        print("\n" + "=" * 60)
        response = input("确认开始同步？(Y/n): ").lower().strip()
        if response == 'n':
            print("[取消] 已取消同步操作")
            sys.exit(0)

        # 执行同步
        success, success_count, total_steps = sync_repository()

        if not success:
            restore_stash()
            sys.exit(1)

        # 恢复stash（如果有）
        restore_stash()

        print("\n" + "=" * 60)
        print(f" [完成] 同步完成！成功执行 {success_count}/{total_steps} 个步骤")
        print(f" [状态] 你的fork仓库现在已是最新版本")
        print("=" * 60)
        print("\n 提示:")
        print("   - 原仓库的更新已同步到你的fork仓库")
        print("   - 你的本地修改不会影响原仓库")
        print("   - 可以继续在本地进行开发")

    except KeyboardInterrupt:
        print("\n\n[中断] 用户取消操作")
        restore_stash()
        sys.exit(1)
    except Exception as e:
        print(f"\n[错误] 发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()