# -*- coding: utf-8 -*-
import requests
import json
import os
import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog

class NovelCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("AI小说创作工具")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2d2d2d')
        
        # 加载配置
        self.config = self.load_config()
        self.current_project = None
        
        # 创建界面
        self.create_widgets()
        
    def load_config(self):
        """加载配置文件"""
        config_path = "novel_creator_config.json"
        default_config = {
            "api_providers": {
                "OpenAI": {
                    "api_key": "",
                    "endpoint": "https://api.openai.com/v1/chat/completions"
                },
                "Claude": {
                    "api_key": "",
                    "endpoint": "https://api.anthropic.com/v1/messages"
                },
                "Gemini": {
                    "api_key": "",
                    "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
                }
            },
            "current_provider": "OpenAI",
            "projects": []
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    return json.load(f)
            except:
                return default_config
        return default_config
    
    def save_config(self):
        """保存配置文件"""
        with open("novel_creator_config.json", "w") as f:
            json.dump(self.config, f, indent=2)
    
    def create_widgets(self):
        # 创建选项卡
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建各个选项卡
        self.create_api_tab()
        self.create_prompt_tab()
        self.create_project_tab()
        self.create_generate_tab()
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, 
                                 bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                 bg='#3d3d3d', fg='white')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_status("就绪")
    
    def update_status(self, message):
        """更新状态栏"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.status_var.set(f"[{timestamp}] {message}")
    
    def create_api_tab(self):
        """创建API设置选项卡"""
        api_tab = ttk.Frame(self.notebook)
        self.notebook.add(api_tab, text="API设置")
        
        # 标题
        tk.Label(api_tab, text="API配置", font=("Arial", 14, "bold"), 
                bg='#2d2d2d', fg='white').pack(pady=10)
        
        # 提供商选择
        frame = tk.Frame(api_tab, bg='#2d2d2d')
        frame.pack(fill=tk.X, padx=20, pady=5)
        tk.Label(frame, text="选择API提供商:", bg='#2d2d2d', fg='white').pack(side=tk.LEFT)
        
        providers = list(self.config["api_providers"].keys())
        self.provider_var = tk.StringVar(value=self.config["current_provider"])
        provider_combo = ttk.Combobox(frame, textvariable=self.provider_var, values=providers)
        provider_combo.pack(side=tk.LEFT, padx=10)
        provider_combo.bind("<<ComboboxSelected>>", self.provider_changed)
        
        # API密钥输入框
        frame = tk.Frame(api_tab, bg='#2d2d2d')
        frame.pack(fill=tk.X, padx=20, pady=5)
        tk.Label(frame, text="API密钥:", bg='#2d2d2d', fg='white').pack(side=tk.LEFT)
        self.api_key_var = tk.StringVar()
        api_key_entry = tk.Entry(frame, textvariable=self.api_key_var, width=50, show="*")
        api_key_entry.pack(side=tk.LEFT, padx=10)
        
        # 测试按钮
        test_btn = tk.Button(api_tab, text="测试连接", command=self.test_api_connection,
                            bg='#4a6fa5', fg='white', relief=tk.FLAT)
        test_btn.pack(pady=10)
        
        # 加载当前选择的API密钥
        self.provider_changed()
    
    def provider_changed(self, event=None):
        """当API提供商改变时更新密钥显示"""
        provider = self.provider_var.get()
        api_key = self.config["api_providers"][provider]["api_key"]
        self.api_key_var.set(api_key)
        self.config["current_provider"] = provider
    
    def test_api_connection(self):
        """测试API连接"""
        provider = self.provider_var.get()
        api_key = self.api_key_var.get()
        
        # 保存密钥
        self.config["api_providers"][provider]["api_key"] = api_key
        self.save_config()
        
        # 测试连接
        self.update_status(f"测试 {provider} 连接...")
        
        # 模拟测试 - 在实际应用中应发送真实请求
        self.root.after(1500, lambda: self.update_status(f"{provider} 连接成功!"))

    def create_prompt_tab(self):
        """创建提示词生成选项卡"""
        prompt_tab = ttk.Frame(self.notebook)
        self.notebook.add(prompt_tab, text="提示词生成")
        
        # 标题
        tk.Label(prompt_tab, text="生成小说创作提示词", font=("Arial", 14, "bold"), 
                bg='#2d2d2d', fg='white').pack(pady=10)
        
        # 提示词输入
        frame = tk.Frame(prompt_tab, bg='#2d2d2d')
        frame.pack(fill=tk.X, padx=20, pady=5)
        tk.Label(frame, text="主题/关键词:", bg='#2d2d2d', fg='white').pack(side=tk.LEFT)
        self.prompt_input_var = tk.StringVar()
        prompt_entry = tk.Entry(frame, textvariable=self.prompt_input_var, width=50)
        prompt_entry.pack(side=tk.LEFT, padx=10)
        
        # 提示词类型
        frame = tk.Frame(prompt_tab, bg='#2d2d2d')
        frame.pack(fill=tk.X, padx=20, pady=5)
        tk.Label(frame, text="提示类型:", bg='#2d2d2d', fg='white').pack(side=tk.LEFT)
        prompt_types = ["角色设定", "世界观设定", "情节大纲", "完整故事"]
        self.prompt_type_var = tk.StringVar(value=prompt_types[0])
        prompt_type_combo = ttk.Combobox(frame, textvariable=self.prompt_type_var, values=prompt_types)
        prompt_type_combo.pack(side=tk.LEFT, padx=10)
        
        # 生成按钮
        generate_btn = tk.Button(prompt_tab, text="生成提示词", command=self.generate_prompt,
                                bg='#4a6fa5', fg='white', relief=tk.FLAT)
        generate_btn.pack(pady=10)
        
        # 结果展示
        self.prompt_result = scrolledtext.ScrolledText(prompt_tab, height=15, 
                                                      bg='#1e1e1e', fg='white',
                                                      insertbackground='white')
        self.prompt_result.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.prompt_result.config(state=tk.DISABLED)
        
        # 保存按钮
        save_btn = tk.Button(prompt_tab, text="保存到剪贴板", command=self.copy_prompt,
                           bg='#5a7d9c', fg='white', relief=tk.FLAT)
        save_btn.pack(pady=5)

    def generate_prompt(self):
        """生成提示词"""
        theme = self.prompt_input_var.get()
        prompt_type = self.prompt_type_var.get()
        
        if not theme:
            messagebox.showerror("错误", "请输入主题或关键词")
            return
        
        self.update_status(f"正在生成 {prompt_type} 提示词...")
        
        # 模拟不同提示词生成
        prompt_results = {
            "角色设定": [
                f"角色名称：林风\n年龄：28岁\n职业：私家侦探\n特点：聪明但愤世嫉俗，右腿因一次任务受伤而微跛，有酗酒倾向\n背景故事：曾是警队精英，因不满体制腐败而辞职，开了一家小型侦探社\n动机：寻找三年前杀害搭档的真凶",
                f"角色名称：艾莉亚\n年龄：17岁\n身份：魔法学院学生\n特点：拥有罕见的时空魔法天赋，但难以控制，左眼因魔法事故变为银色\n背景故事：孤儿，在教会孤儿院长大，被魔法学院院长发掘\n动机：寻找关于自己身世的秘密，控制体内强大的魔法力量"
            ],
            "世界观设定": [
                f"世界名称：埃瑟兰\n纪元：第三魔法纪元\n主要特征：\n- 魔法与蒸汽科技共存\n- 空中浮岛与地下城并存\n- 六大魔法家族掌控政治经济\n- 魔法能源危机日益严重\n独特设定：\n'灵魂共鸣'系统 - 每个人在16岁时会觉醒一个灵魂共鸣体，可以是动物、植物或器物，决定个人的魔法属性与能力上限",
                f"世界名称：新长安\n时代：赛博朋克唐朝\n主要特征：\n- 传统唐风建筑与霓虹全息投影结合\n- 机械义肢与古武术并存\n- 四大公司控制城市命脉\n- 底层人民生活在充满蒸汽管道的'地下唐城'\n独特设定：\n'经脉芯片' - 将武学经脉系统数字化，通过植入芯片可快速习得武功，但过度使用会导致'经脉过载'"
            ],
            "情节大纲": [
                f"标题：《星尘挽歌》\n\n第一章：陨落之星\n- 主角在垃圾星发现神秘水晶\n- 被帝国士兵追捕，意外激活水晶\n- 获得星尘之力，逃离垃圾星\n\n第二章：星尘学院\n- 进入培养星尘能力者的学院\n- 结识同伴与对手\n- 发现水晶与古代文明的联系\n\n第三章：暗流涌动\n- 学院内部派系斗争\n- 帝国势力渗透学院\n- 主角小队发现院长秘密\n\n最终章：星尘觉醒\n- 古代文明真相揭露\n- 最终决战：学院 vs 帝国舰队\n- 主角牺牲自我重启星尘网络，带来和平新时代",
                f"标题：《长安夜行录》\n\n第一章：夜雨客\n- 雨夜，神秘女子将婴儿托付给退休捕快\n- 婴儿身上有奇异莲花印记\n- 当晚女子被黑衣人追杀身亡\n\n第二章：十年之后\n- 婴儿长大成为街头混混\n- 莲花印记觉醒，吸引各方势力\n- 退休捕快为保护养子被杀\n\n第三章：身世之谜\n- 主角寻找生母线索\n- 发现与消失的'莲花教'有关\n- 结识前朝遗孤与神秘剑客\n\n最终章：长安决战\n- 揭穿当朝宰相的阴谋\n- 莲花教真相：守护前朝龙脉\n- 主角抉择：复兴前朝还是守护当下长安"
            ],
            "完整故事": [
                f"标题：《时间修补匠》\n\n故事：在时间管理局最底层的维修部，老张是个不起眼的'时间修补匠'，负责修复微小的时间裂缝。一次例行维修中，他发现一个裂缝正在不断扩大。调查后得知，这是有人故意制造'时间炸弹'，目的是让整个时间线崩溃。老张只有72小时，他必须利用自己对时间裂缝的了解和一台老旧的时光穿梭机，穿越到不同历史节点收集'时间锚点'。在维多利亚时代的伦敦，他结识了女发明家艾达；在二战时期的诺曼底，他救下年轻士兵托马斯；在23世纪的月球基地，他获得未来科学家的帮助。最终他揭露了幕后黑手——未来的自己。原来为了拯救患绝症的女儿，未来的他试图重置时间线。老张面临抉择：拯救女儿还是守护时间线。最终他选择后者，但将自己的记忆封存在时间裂缝中，给女儿留下线索..."
            ]
        }
        
        # 随机选择一个结果
        import random
        result = random.choice(prompt_results[prompt_type])
        
        # 显示结果
        self.prompt_result.config(state=tk.NORMAL)
        self.prompt_result.delete(1.0, tk.END)
        self.prompt_result.insert(tk.END, result)
        self.prompt_result.config(state=tk.DISABLED)
        
        self.update_status(f"{prompt_type}提示词生成完成")
    
    def copy_prompt(self):
        """复制提示词到剪贴板"""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.prompt_result.get(1.0, tk.END))
        self.update_status("提示词已复制到剪贴板")
    
    def create_project_tab(self):
        """创建小说项目管理选项卡"""
        project_tab = ttk.Frame(self.notebook)
        self.notebook.add(project_tab, text="小说项目")
        
        # 左侧项目列表
        list_frame = tk.Frame(project_tab, bg='#3d3d3d')
        list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 5), pady=10)
        
        tk.Label(list_frame, text="小说项目", font=("Arial", 12), 
                bg='#3d3d3d', fg='white').pack(pady=5)
        
        self.project_list = tk.Listbox(list_frame, width=25, height=20, 
                                     bg='#1e1e1e', fg='white', selectbackground='#4a6fa5')
        self.project_list.pack(fill=tk.BOTH, expand=True)
        self.project_list.bind("<<ListboxSelect>>", self.load_project)
        
        # 加载项目到列表
        self.refresh_project_list()
        
        # 项目操作按钮
        btn_frame = tk.Frame(list_frame, bg='#3d3d3d')
        btn_frame.pack(fill=tk.X, pady=5)
        
        new_btn = tk.Button(btn_frame, text="新建", command=self.new_project,
                          bg='#5a7d9c', fg='white', relief=tk.FLAT, width=8)
        new_btn.pack(side=tk.LEFT, padx=2)
        
        delete_btn = tk.Button(btn_frame, text="删除", command=self.delete_project,
                             bg='#a55a5a', fg='white', relief=tk.FLAT, width=8)
        delete_btn.pack(side=tk.LEFT, padx=2)
        
        # 右侧项目编辑器
        edit_frame = tk.Frame(project_tab, bg='#2d2d2d')
        edit_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=10)
        
        # 项目元数据
        meta_frame = tk.LabelFrame(edit_frame, text="项目信息", bg='#2d2d2d', fg='white')
        meta_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(meta_frame, text="标题:", bg='#2d2d2d', fg='white').grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.title_var = tk.StringVar()
        tk.Entry(meta_frame, textvariable=self.title_var, width=40).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        tk.Label(meta_frame, text="作者:", bg='#2d2d2d', fg='white').grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.author_var = tk.StringVar()
        tk.Entry(meta_frame, textvariable=self.author_var, width=40).grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        tk.Label(meta_frame, text="类型:", bg='#2d2d2d', fg='white').grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.genre_var = tk.StringVar()
        genres = ["科幻", "奇幻", "悬疑", "爱情", "历史", "武侠", "都市", "其他"]
        ttk.Combobox(meta_frame, textvariable=self.genre_var, values=genres, width=37).grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        # 项目内容
        notebook = ttk.Notebook(edit_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 大纲选项卡
        outline_frame = ttk.Frame(notebook)
        notebook.add(outline_frame, text="大纲")
        self.outline_text = scrolledtext.ScrolledText(outline_frame, height=10, 
                                                   bg='#1e1e1e', fg='white',
                                                   insertbackground='white')
        self.outline_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 角色选项卡
        character_frame = ttk.Frame(notebook)
        notebook.add(character_frame, text="角色")
        self.character_text = scrolledtext.ScrolledText(character_frame, height=10, 
                                                      bg='#1e1e1e', fg='white',
                                                      insertbackground='white')
        self.character_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 设定选项卡
        setting_frame = ttk.Frame(notebook)
        notebook.add(setting_frame, text="世界观")
        self.setting_text = scrolledtext.ScrolledText(setting_frame, height=10, 
                                                    bg='#1e1e1e', fg='white',
                                                    insertbackground='white')
        self.setting_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 保存按钮
        save_btn = tk.Button(edit_frame, text="保存项目", command=self.save_project,
                           bg='#4a6fa5', fg='white', relief=tk.FLAT)
        save_btn.pack(pady=10)
    
    def refresh_project_list(self):
        """刷新项目列表"""
        self.project_list.delete(0, tk.END)
        for project in self.config["projects"]:
            self.project_list.insert(tk.END, project["title"])
    
    def new_project(self):
        """创建新项目"""
        self.title_var.set("")
        self.author_var.set("")
        self.genre_var.set("")
        self.outline_text.delete(1.0, tk.END)
        self.character_text.delete(1.0, tk.END)
        self.setting_text.delete(1.0, tk.END)
        self.current_project = None
        self.update_status("已创建新项目")
    
    def load_project(self, event):
        """加载选中的项目"""
        if not self.project_list.curselection():
            return
        
        index = self.project_list.curselection()[0]
        project = self.config["projects"][index]
        self.current_project = index
        
        self.title_var.set(project["title"])
        self.author_var.set(project["author"])
        self.genre_var.set(project["genre"])
        self.outline_text.delete(1.0, tk.END)
        self.outline_text.insert(tk.END, project["outline"])
        self.character_text.delete(1.0, tk.END)
        self.character_text.insert(tk.END, project["characters"])
        self.setting_text.delete(1.0, tk.END)
        self.setting_text.insert(tk.END, project["setting"])
        
        self.update_status(f"已加载项目: {project['title']}")
    
    def save_project(self):
        """保存当前项目"""
        title = self.title_var.get()
        if not title:
            messagebox.showerror("错误", "请输入项目标题")
            return
        
        project_data = {
            "title": title,
            "author": self.author_var.get(),
            "genre": self.genre_var.get(),
            "outline": self.outline_text.get(1.0, tk.END).strip(),
            "characters": self.character_text.get(1.0, tk.END).strip(),
            "setting": self.setting_text.get(1.0, tk.END).strip(),
            "chapters": []  # 章节内容
        }
        
        if self.current_project is None:
            # 新项目
            self.config["projects"].append(project_data)
            self.current_project = len(self.config["projects"]) - 1
        else:
            # 更新现有项目
            self.config["projects"][self.current_project] = project_data
        
        self.save_config()
        self.refresh_project_list()
        self.update_status(f"项目已保存: {title}")
    
    def delete_project(self):
        """删除当前选中的项目"""
        if not self.project_list.curselection():
            return
        
        index = self.project_list.curselection()[0]
        title = self.config["projects"][index]["title"]
        
        if messagebox.askyesno("确认删除", f"确定要删除项目 '{title}' 吗？"):
            del self.config["projects"][index]
            self.save_config()
            self.refresh_project_list()
            self.new_project()
            self.update_status(f"已删除项目: {title}")
    
    def create_generate_tab(self):
        """创建小说生成选项卡"""
        generate_tab = ttk.Frame(self.notebook)
        self.notebook.add(generate_tab, text="生成小说")
        
        # 生成设置
        settings_frame = tk.Frame(generate_tab, bg='#2d2d2d')
        settings_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 项目选择
        tk.Label(settings_frame, text="选择项目:", bg='#2d2d2d', fg='white').grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.project_names = [p["title"] for p in self.config["projects"]]
        self.generate_project_var = tk.StringVar()
        project_combo = ttk.Combobox(settings_frame, textvariable=self.generate_project_var, values=self.project_names, width=40)
        project_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # 生成类型
        tk.Label(settings_frame, text="生成类型:", bg='#2d2d2d', fg='white').grid(row=1, column=0, sticky="e", padx=5, pady=5)
        generate_types = ["完整章节", "段落续写", "场景描述", "对话生成"]
        self.generate_type_var = tk.StringVar(value=generate_types[0])
        type_combo = ttk.Combobox(settings_frame, textvariable=self.generate_type_var, values=generate_types, width=15)
        type_combo.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # 风格控制
        tk.Label(settings_frame, text="写作风格:", bg='#2d2d2d', fg='white').grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.style_var = tk.StringVar(value="文学性")
        style_combo = ttk.Combobox(settings_frame, textvariable=self.style_var, 
                                  values=["简洁", "详细", "文学性", "诗意", "幽默", "悬疑"], width=15)
        style_combo.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # 生成长度
        tk.Label(settings_frame, text="生成长度:", bg='#2d2d2d', fg='white').grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.length_var = tk.StringVar(value="中等")
        length_combo = ttk.Combobox(settings_frame, textvariable=self.length_var, 
                                   values=["短", "中等", "长", "超长"], width=15)
        length_combo.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # 提示词输入
        prompt_frame = tk.LabelFrame(generate_tab, text="自定义提示词（可选）", bg='#2d2d2d', fg='white')
        prompt_frame.pack(fill=tk.X, padx=20, pady=5)
        self.custom_prompt_var = tk.StringVar()
        custom_prompt_entry = tk.Entry(prompt_frame, textvariable=self.custom_prompt_var, width=80)
        custom_prompt_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # 生成按钮
        generate_frame = tk.Frame(generate_tab, bg='#2d2d2d')
        generate_frame.pack(fill=tk.X, padx=20, pady=10)
        
        generate_btn = tk.Button(generate_frame, text="生成小说内容", command=self.generate_novel,
                               bg='#4a6fa5', fg='white', relief=tk.FLAT, font=("Arial", 10, "bold"))
        generate_btn.pack(side=tk.LEFT, padx=10)
        
        # 结果展示
        result_frame = tk.Frame(generate_tab, bg='#2d2d2d')
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.generated_text = scrolledtext.ScrolledText(result_frame, height=15, 
                                                      bg='#1e1e1e', fg='white',
                                                      insertbackground='white')
        self.generated_text.pack(fill=tk.BOTH, expand=True)
        self.generated_text.config(state=tk.DISABLED)
        
        # 操作按钮
        btn_frame = tk.Frame(result_frame, bg='#2d2d2d')
        btn_frame.pack(fill=tk.X, pady=5)
        
        copy_btn = tk.Button(btn_frame, text="复制内容", command=self.copy_generated,
                           bg='#5a7d9c', fg='white', relief=tk.FLAT)
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = tk.Button(btn_frame, text="保存到文件", command=self.save_generated,
                           bg='#5a7d9c', fg='white', relief=tk.FLAT)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        insert_btn = tk.Button(btn_frame, text="插入到项目", command=self.insert_to_project,
                             bg='#5a7d9c', fg='white', relief=tk.FLAT)
        insert_btn.pack(side=tk.LEFT, padx=5)
    
    def generate_novel(self):
        """生成小说内容"""
        project_name = self.generate_project_var.get()
        if not project_name:
            messagebox.showerror("错误", "请选择一个项目")
            return
        
        # 查找项目
        project = None
        for p in self.config["projects"]:
            if p["title"] == project_name:
                project = p
                break
        
        if not project:
            messagebox.showerror("错误", "项目不存在")
            return
        
        # 模拟生成不同内容
        content_types = {
            "完整章节": [
                "第一章 星尘觉醒\n\n林风推开吱呀作响的木门，雨水顺着他的旧皮衣滴落在斑驳的地板上。'老张，有新案子了？'他朝昏暗的屋内喊道。角落的阴影里，一个佝偻的身影动了动，烟斗的火光在黑暗中明灭。'这次不一样，'沙哑的声音响起，'有人出高价，找一块会发光的石头。'林风嗤笑一声，'又是寻宝？你知道我不接这种——'话未说完，一张泛黄的照片被推到桌上。照片上是一块菱形的蓝色水晶，内部仿佛有星河流动。林风的手指微微颤抖，这块水晶...和他三年前在搭档尸体旁见到的一模一样。",
                "第二章 魔法学院的秘密\n\n艾莉亚屏住呼吸，藏在图书馆的巨大书架后。月光透过彩色玻璃窗，在古老的书卷上投下诡异的光影。她听到脚步声越来越近——是院长和那个黑袍人。'仪式必须在下个满月完成，'院长低沉的声音中带着一丝急切，'那个女孩的力量比我们想象的还要强大。'黑袍人发出沙哑的笑声，'银眼少女...终于找到了。艾莉亚感到一阵寒意，她下意识地碰了碰自己的左眼，那里在黑暗中正发出微弱的银光。"
            ],
            "段落续写": [
                "林风握紧照片，冰冷的触感从指尖蔓延至心脏。三年来，这个画面无数次在他噩梦中出现——搭档李明倒在血泊中，右手紧握着这样一块发光的石头，眼神里满是未说出口的警告。雨水敲打窗户的声音将他拉回现实。'雇主是谁？'他声音沙哑。老张摇摇头，'匿名。但定金足够你买下半个街区。'林风盯着照片，蓝色水晶仿佛有生命般微微脉动。突然，他注意到照片角落有个模糊的标记——一只展开翅膀的鹰，那是李氏家族的徽章。李明从未提起过自己的家族背景。",
                "艾莉亚悄悄后退，却不小心碰倒了一摞古籍。巨大的声响在寂静的图书馆回荡。'谁在那里？'院长的声音陡然变得凌厉。艾莉亚转身就跑，耳边风声呼啸。突然，一道魔法屏障在她面前升起，她猝不及防撞了上去。黑袍人缓步走来，兜帽下露出苍白的下巴，'意外的收获。'他的手指在空中划出复杂的符号，艾莉亚感到全身魔力被禁锢。就在这时，她胸前的吊坠突然发热——这是孤儿院院长临终前给她的遗物，从未有过任何反应。"
            ],
            "场景描述": [
                "废弃的教堂里，彩色玻璃早已破碎，月光从空洞的窗口倾泻而下，照亮空气中漂浮的尘埃。墙角蛛网密布，倒下的长椅像巨兽的骸骨。祭坛上方，巨大的管风琴只剩扭曲的骨架，琴键上停着一只乌鸦，血红的眼睛注视着闯入者。林风的手电光束扫过墙壁，突然定格——那里刻着与照片上一模一样的鹰形徽章，下方用拉丁文写着：'光生于暗'。徽章中央有个水晶形状的凹槽，大小与他手中的照片完全吻合。",
                "魔法学院的星象塔顶，艾莉亚站在环形露台边缘。脚下是翻滚的云海，头顶是触手可及的璀璨星河。七座悬浮的岛屿环绕着主塔，由发光的虹桥相连。东岛是植物园，发光的藤蔓缠绕成塔；西岛是炼金工坊，蒸汽与魔法火焰交织升腾；南岛图书馆的穹顶是巨大的水晶球，映照着银河的投影；北岛训练场上，学徒们骑着扫帚在空中划出银色轨迹。中央的主塔尖顶射出一道蓝色光柱，直通云霄——那是维持浮岛魔力的能量源，也是院长禁止任何人接近的禁地。"
            ],
            "对话生成": [
                "'你早知道李明的身份，是不是？'林风猛地转身，枪口对准老张。老人叹了口气，烟斗在黑暗中明灭，'三年前我警告过你，别查那个案子。''他是你什么人？'林风的手指扣在扳机上。'我儿子，'老张的声音突然苍老了十岁，'他加入李氏家族是为了查清他们用星石做的勾当。'枪口微微下垂，'那为什么现在告诉我？''因为昨晚，'老张掀开外套，腹部缠着渗血的绷带，'他们找到了我。这块石头...'他掏出一块蓝色水晶，'是唯一能阻止他们的关键。拿着它，去找一个叫'星尘之子'的组织...'话未说完，窗外传来玻璃破碎声，一道红光射入，正中老张胸口。",
                "'你到底是什么人？'艾莉亚紧握发烫的吊坠，盯着黑袍人。对方低笑，'我是影法师，被学院驱逐的第一任院长。'他掀开兜帽，露出一张布满符文刺青的脸，'现在的院长是我曾经的学徒，他背叛了我，偷走了控制浮岛的核心咒语。'艾莉亚皱眉，'这和我有什么关系？''因为你是星之女，'影法师指着她的左眼，'只有你的银眼能看穿虹桥的魔法路径，进入中央塔顶。'吊坠突然漂浮起来，投射出一幅星图，'这吊坠里有你母亲留下的信息。她不是抛弃你，而是为了保护你逃离院长的追捕。'"
            ]
        }
        
        # 获取生成类型
        gen_type = self.generate_type_var.get()
        
        # 模拟生成过程
        self.update_status(f"正在生成 {gen_type}...")
        self.generated_text.config(state=tk.NORMAL)
        self.generated_text.delete(1.0, tk.END)
        
        # 显示"正在生成"动画
        self.generated_text.insert(tk.END, f"正在生成{gen_type}内容，请稍候...")
        self.root.update()
        
        # 模拟延迟
        import random
        self.root.after(2000, lambda: self.finish_generation(content_types, gen_type))
    
    def finish_generation(self, content_types, gen_type):
        """完成生成并显示结果"""
        # 随机选择一个内容
        content = random.choice(content_types[gen_type])
        
        self.generated_text.delete(1.0, tk.END)
        self.generated_text.insert(tk.END, content)
        self.generated_text.config(state=tk.DISABLED)
        self.update_status(f"{gen_type}生成完成")
    
    def copy_generated(self):
        """复制生成的内容"""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.generated_text.get(1.0, tk.END))
        self.update_status("内容已复制到剪贴板")
    
    def save_generated(self):
        """保存生成的内容到文件"""
        content = self.generated_text.get(1.0, tk.END)
        if not content.strip():
            messagebox.showinfo("提示", "没有内容可保存")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.update_status(f"内容已保存到: {file_path}")
    
    def insert_to_project(self):
        """将生成的内容插入到当前项目"""
        if self.current_project is None:
            messagebox.showerror("错误", "没有打开的项目")
            return
        
        content = self.generated_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showinfo("提示", "没有内容可插入")
            return
        
        # 添加到项目的章节中
        self.config["projects"][self.current_project]["chapters"].append(content)
        self.save_config()
        self.update_status("内容已添加到当前项目")

if __name__ == "__main__":
    root = tk.Tk()
    app = NovelCreator(root)
    root.mainloop()