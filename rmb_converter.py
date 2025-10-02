import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import re

class RMBConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("人民币大写转换器")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        # 设置样式
        self.setup_style()
        
        # 创建界面
        self.create_widgets()
    
    def setup_style(self):
        """设置界面样式"""
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('微软雅黑', 10))
        style.configure('TButton', font=('微软雅黑', 9))
        style.configure('Title.TLabel', font=('微软雅黑', 12, 'bold'))
    
    def create_widgets(self):
        """创建界面组件"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="人民币大写转换器", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # 输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, text="输入金额:").pack(side=tk.LEFT)
        
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(input_frame, textvariable=self.amount_var, 
                                     font=('微软雅黑', 11), width=20)
        self.amount_entry.pack(side=tk.LEFT, padx=10)
        self.amount_entry.bind('<KeyRelease>', self.on_amount_change)
        
        # 转换按钮
        convert_btn = ttk.Button(input_frame, text="转换", command=self.convert_amount)
        convert_btn.pack(side=tk.LEFT, padx=5)
        
        # 结果显示区域
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(result_frame, text="中文大写:").pack(anchor=tk.W)
        
        result_input_frame = ttk.Frame(result_frame)
        result_input_frame.pack(fill=tk.X, pady=5)
        
        self.result_var = tk.StringVar()
        self.result_entry = ttk.Entry(result_input_frame, textvariable=self.result_var,
                                     font=('微软雅黑', 11), width=30, state='readonly')
        self.result_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 复制按钮
        copy_btn = ttk.Button(result_input_frame, text="复制", command=self.copy_to_clipboard)
        copy_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, pady=20)
        
        about_btn = ttk.Button(button_frame, text="关于", command=self.show_about)
        about_btn.pack(side=tk.LEFT, padx=10)
        
        exit_btn = ttk.Button(button_frame, text="退出", command=self.root.quit)
        exit_btn.pack(side=tk.RIGHT, padx=10)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("请输入金额进行转换")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                relief=tk.SUNKEN, style='TLabel')
        status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
    
    def on_amount_change(self, event):
        """实时验证输入"""
        amount = self.amount_var.get()
        if amount and not self.validate_amount(amount):
            self.status_var.set("请输入有效的金额格式")
        else:
            self.status_var.set("")
    
    def validate_amount(self, amount):
        """验证金额格式"""
        pattern = r'^\d{1,12}(\.\d{0,2})?$'
        return re.match(pattern, amount) is not None
    
    def convert_amount(self):
        """转换金额为中文大写"""
        amount_str = self.amount_var.get().strip()
        
        if not amount_str:
            messagebox.showwarning("输入错误", "请输入金额")
            return
        
        if not self.validate_amount(amount_str):
            messagebox.showerror("输入错误", "请输入有效的金额格式（最多两位小数）")
            return
        
        try:
            # 转换为数字
            amount = float(amount_str)
            if amount >= 1000000000000:  # 万亿
                messagebox.showerror("输入错误", "金额过大，最大支持9999亿")
                return
            
            # 转换为中文大写
            result = self.to_chinese_upper(amount)
            self.result_var.set(result)
            self.status_var.set("转换成功")
            
        except Exception as e:
            messagebox.showerror("转换错误", f"转换过程中发生错误: {str(e)}")
    
    def to_chinese_upper(self, amount):
        """将数字金额转换为中文大写"""
        # 定义数字和单位
        numbers = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
        units = ['', '拾', '佰', '仟']
        big_units = ['', '万', '亿']
        
        # 分离整数和小数部分
        integer_part = int(amount)
        decimal_part = round(amount - integer_part, 2)
        
        # 处理整数部分
        if integer_part == 0:
            result = "零"
        else:
            # 将整数部分分组（每4位一组）
            integer_str = str(integer_part)
            groups = []
            while integer_str:
                groups.append(integer_str[-4:])
                integer_str = integer_str[:-4] if len(integer_str) > 4 else ''
            groups.reverse()
            
            result_parts = []
            for i, group in enumerate(groups):
                group_result = []
                zero_flag = False  # 零标志
                
                for j, digit in enumerate(group):
                    digit_int = int(digit)
                    unit_index = len(group) - j - 1
                    
                    if digit_int == 0:
                        zero_flag = True
                    else:
                        if zero_flag:
                            group_result.append('零')
                            zero_flag = False
                        group_result.append(numbers[digit_int] + units[unit_index])
                
                if group_result:  # 如果该组有数字
                    group_str = ''.join(group_result)
                    big_unit_index = len(groups) - i - 1
                    group_str += big_units[big_unit_index]
                    result_parts.append(group_str)
                elif i == len(groups) - 1 and not result_parts:  # 全是零的情况
                    result_parts.append('零')
            
            result = ''.join(result_parts)
        
        result += "元"
        
        # 处理小数部分
        if decimal_part == 0:
            result += "整"
        else:
            # 角和分
            jiao = int(decimal_part * 10)
            fen = int(round(decimal_part * 100)) % 10
            
            if jiao > 0:
                result += numbers[jiao] + "角"
            if fen > 0:
                result += numbers[fen] + "分"
        
        return result
    
    def copy_to_clipboard(self):
        """复制到剪贴板"""
        result = self.result_var.get()
        if result:
            try:
                pyperclip.copy(result)
                self.status_var.set("已复制到剪贴板")
            except Exception as e:
                messagebox.showerror("复制错误", f"无法复制到剪贴板: {str(e)}")
        else:
            messagebox.showwarning("复制错误", "没有内容可复制")
    
    def show_about(self):
        """显示关于信息"""
        about_text = """人民币大写转换器
        
版本: 1.0
开发者: Lu Wentao
邮箱: luwentao@gmail.com

功能:
• 将阿拉伯数字金额转换为中文大写
• 支持复制到剪贴板
• 实时输入验证"""
        
        messagebox.showinfo("关于", about_text)

def main():
    root = tk.Tk()
    app = RMBConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()