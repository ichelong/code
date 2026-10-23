# -*- coding: utf-8 -*-
"""
密码生成器 - Password Generator
功能：生成指定长度和字符集的随机密码
作者：自动生成工具
"""

import tkinter as tk
import random
from tkinter import messagebox, ttk

# ==================== 初始化配置 ====================

# 定义默认字符集（排除容易混淆的字符）
# 小写字母：排除 i, l（与数字1和字母I容易混淆）
default_lowercase = 'abcdefhjkmnprstuvwxyz'

# 大写字母：排除 I, O（与数字1和0容易混淆）
default_uppercase = 'ABCDEFGHJKMNPQRSTUVWXYZ'

# 数字：排除 0, 1（与字母O和l容易混淆）
default_digits = '23456789'

# 特殊字符集
default_special = '!@#$%&'

# ==================== 全局变量 ====================

# 存储生成的密码列表，用于"复制所有密码"功能
generated_passwords = []

# ==================== 功能函数 ====================

def copy_to_clipboard(password):
    """
    复制单个密码到剪贴板
    
    参数:
        password: 要复制的密码字符串
    """
    # 清空剪贴板
    root.clipboard_clear()
    # 追加密码到剪贴板
    root.clipboard_append(password)
    # 更新状态栏显示复制信息
    status_var.set(f"已复制: {password[:8]}...")
    # 2秒后恢复状态栏为"就绪"
    root.after(2000, lambda: status_var.set("就绪"))


def copy_all_passwords():
    """
    复制所有生成的密码到剪贴板
    所有密码用换行符分隔
    """
    # 检查是否有可复制的密码
    if not generated_passwords:
        status_var.set("没有密码可复制")
        root.after(2000, lambda: status_var.set("就绪"))
        return
    
    # 将所有密码用换行符连接成字符串
    all_passwords = "\n".join(generated_passwords)
    # 清空剪贴板并复制所有密码
    root.clipboard_clear()
    root.clipboard_append(all_passwords)
    # 更新状态栏
    status_var.set(f"已复制 {len(generated_passwords)} 个密码")
    root.after(2000, lambda: status_var.set("就绪"))


def generate_password():
    """
    生成指定长度和字符集的随机密码
    
    流程:
        1. 获取用户输入的密码长度
        2. 获取用户选择的字符集
        3. 验证输入合法性
        4. 从字符池中随机选择字符生成密码
        5. 显示生成的密码并创建复制按钮
    """
    try:
        # 获取输入的密码长度
        length = int(length_entry.get())
        
        # 验证密码长度
        if length <= 0:
            messagebox.showerror("错误", "密码长度必须大于0")
            return
        
        # 获取用户输入的字符集（从输入框获取自定义字符集）
        lowercase = list(lowercase_entry.get())
        uppercase = list(uppercase_entry.get())
        digits = list(digits_entry.get())
        special = list(special_entry.get())
        
        # 验证至少有一个字符集被选中
        if not (lowercase or uppercase or digits or special):
            messagebox.showerror("错误", "至少需要选择一种字符类型")
            return
        
        # 合并所有字符到字符池
        char_pool = lowercase + uppercase + digits + special
        
        # 清除之前的密码显示区域
        for widget in password_frame.winfo_children():
            widget.destroy()
        
        # 清空密码列表，为重新生成做准备
        generated_passwords.clear()
        
        # 生成5个密码并显示
        for i in range(5):
            # 随机从字符池中选择字符生成密码
            password = ''.join(random.choice(char_pool) for _ in range(length))
            generated_passwords.append(password)
            
            # 创建密码序号标签
            password_label = ttk.Label(password_frame, text=f"密码 {i+1}:", width=10)
            password_label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            
            # 创建密码显示文本框（只读状态）
            password_entry = tk.Entry(password_frame, width=30, fg="black", bg="white", relief="sunken")
            password_entry.insert(0, password)
            password_entry.config(state="readonly")
            password_entry.grid(row=i, column=1, padx=5, pady=5)
            
            # 创建单个密码复制按钮
            copy_btn = ttk.Button(password_frame, text="复制", width=8, 
                                 command=lambda p=password: copy_to_clipboard(p))
            copy_btn.grid(row=i, column=2, padx=5, pady=5)
        
        # 添加复制所有密码按钮
        copy_all_btn = ttk.Button(password_frame, text="复制所有密码", width=12, 
                                 command=copy_all_passwords)
        copy_all_btn.grid(row=5, column=0, columnspan=3, padx=5, pady=10, sticky="ew")
            
    except ValueError:
        # 处理用户输入非数字的情况
        messagebox.showerror("错误", "请输入有效的数字")


# ==================== UI界面构建 ====================

# 创建主窗口
root = tk.Tk()
root.title("密码生成器")
root.geometry("500x520")
root.resizable(True, True)

# 设置窗口图标（如果有的话）
try:
    root.iconbitmap()
except:
    pass

# 创建主框架（包含所有UI元素）
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# 创建输入区域框架（包含设置选项）
input_frame = ttk.LabelFrame(main_frame, text="设置", padding="10")
input_frame.pack(fill=tk.X, pady=(0, 10))

# 创建密码长度输入框
ttk.Label(input_frame, text="密码长度:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
length_entry = ttk.Entry(input_frame, width=10)
length_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
length_entry.insert(0, "20")  # 默认长度为20

# 创建字符集输入框

# 小写字母输入框
ttk.Label(input_frame, text="小写字母:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
lowercase_entry = ttk.Entry(input_frame, width=30)
lowercase_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
lowercase_entry.insert(0, default_lowercase)

# 大写字母输入框
ttk.Label(input_frame, text="大写字母:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
uppercase_entry = ttk.Entry(input_frame, width=30)
uppercase_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
uppercase_entry.insert(0, default_uppercase)

# 数字输入框
ttk.Label(input_frame, text="数字:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
digits_entry = ttk.Entry(input_frame, width=30)
digits_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
digits_entry.insert(0, default_digits)

# 特殊字符输入框
ttk.Label(input_frame, text="特殊字符:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
special_entry = ttk.Entry(input_frame, width=30)
special_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
special_entry.insert(0, default_special)

# 创建生成按钮（设置字体加大加粗）
# 创建样式配置
style = ttk.Style()
style.configure("Bold.TButton", font=("Microsoft YaHei", 13))

generate_btn = ttk.Button(input_frame, text="生成密码", command=generate_password, style="Bold.TButton")
generate_btn.grid(row=0, column=2, rowspan=5, padx=10, pady=10, sticky="ns")

# 创建密码显示框架
password_frame = ttk.LabelFrame(main_frame, text="生成的密码", padding="10")
password_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

# 创建状态栏（显示操作提示信息）
status_var = tk.StringVar(value="就绪")
status_bar = ttk.Label(root, textvariable=status_var, relief="sunken", anchor="w")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# 程序启动时只初始化界面，不生成密码
# 用户点击"生成密码"按钮后才会生成密码

# 启动主循环（开始监听用户操作）
root.mainloop()