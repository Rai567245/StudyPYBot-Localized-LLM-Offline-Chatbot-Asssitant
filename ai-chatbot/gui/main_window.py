import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import re

class StudyPYGUI:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("StudyPyBot")
        self.root.geometry("1000x800")
        
        # --- THEME & STATE ---
        self.dark_mode = True
        self.sidebar_expanded = True
        self.current_nav = "New Chat" 
        self.is_running = False  
        
        self.themes = {
            "dark": {
                "bg": "#0f0f0f",      
                "side": "#1a1a1c",    
                "txt": "#e3e3e3", 
                "entry": "#1e1f20", 
                "acc": "#3c4043",     
                "hover": "#2d2d30",
                "active": "#8ab4f8",  
                "label_u": "#8ab4f8", 
                "label_b": "#c4eed0",
                "code_bg": "#282c34"  
            },
            "light": {
                "bg": "#ffffff", 
                "side": "#f8f9fa", 
                "txt": "#1f1f1f", 
                "entry": "#f1f3f4", 
                "acc": "#dee2e6", 
                "hover": "#e8eaed",
                "active": "#1a73e8", 
                "label_u": "#1a73e8", 
                "label_b": "#188038",
                "code_bg": "#f0f0f0"
            }
        }

        self.root.configure(bg=self.themes["dark"]["bg"])

        # --- LAYOUT STRUCTURE ---
        self.sidebar = tk.Frame(self.root, bg=self.themes["dark"]["side"], width=260)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.main_container = tk.Frame(self.root, bg=self.themes["dark"]["bg"])
        self.main_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Initialize UI Components
        self.setup_sidebar()
        self.setup_main_chat()
        self.update_recent_topics()

    # --- SIDEBAR LOGIC ---
    def setup_sidebar(self):
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        t = self.themes["dark"] if self.dark_mode else self.themes["light"]
        
        self.burger_btn = tk.Button(
            self.sidebar, text="☰", font=("Arial", 16),
            bg=t["side"], fg=t["txt"], bd=0, relief="flat",
            cursor="hand2", command=self.toggle_sidebar, padx=20,
            activebackground=t["side"], activeforeground=t["active"]
        )
        self.burger_btn.pack(anchor="nw", pady=(10, 20))

        nav_items = [
            ("＋", "New Chat", self.new_chat),
            ("📁", "Load History", self.load_history_to_chat),
            ("💾", "Export History", self.controller.export_history),
            ("◐", "Toggle Theme", self.toggle_theme)
        ]

        for icon, label, cmd in nav_items:
            btn_frame = tk.Frame(self.sidebar, bg=t["side"])
            btn_frame.pack(fill=tk.X, pady=2)
            
            is_active = self.current_nav == label
            indicator = tk.Frame(btn_frame, width=4, bg=t["active"] if is_active else t["side"])
            indicator.pack(side=tk.LEFT, fill=tk.Y)

            icn_lbl = tk.Label(btn_frame, text=icon, font=("Arial", 14), bg=t["side"], 
                               fg=t["active"] if is_active else t["txt"], width=4)
            icn_lbl.pack(side=tk.LEFT, padx=(5, 0), pady=10)
            
            if self.sidebar_expanded:
                txt_lbl = tk.Label(btn_frame, text=label, font=("Arial", 11, "bold" if is_active else "normal"), 
                                   bg=t["side"], fg=t["txt"])
                txt_lbl.pack(side=tk.LEFT, padx=10)
                widgets = (btn_frame, icn_lbl, txt_lbl)
            else:
                widgets = (btn_frame, icn_lbl)

            def make_cmd(c=cmd, l=label):
                self.current_nav = l
                c()
                self.setup_sidebar()

            for w in widgets:
                w.bind("<Enter>", lambda e, f=btn_frame: self._on_hover(f, True))
                w.bind("<Leave>", lambda e, f=btn_frame: self._on_hover(f, False))
                w.bind("<Button-1>", lambda e, c=make_cmd: c())

        if self.sidebar_expanded:
            tk.Frame(self.sidebar, bg=t["acc"], height=1).pack(fill=tk.X, padx=20, pady=20)
            
            search_frame = tk.Frame(self.sidebar, bg=t["hover"], padx=10, pady=5)
            search_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
            self.history_search = tk.Entry(search_frame, bg=t["hover"], fg=t["txt"], bd=0, 
                                            font=("Arial", 9), insertbackground=t["txt"])
            self.history_search.insert(0, "Search history...")
            self.history_search.pack(fill=tk.X)
            self.history_search.bind("<KeyRelease>", lambda e: self.update_recent_topics())
            self.history_search.bind("<FocusIn>", lambda e: self.history_search.delete(0, tk.END) if self.history_search.get() == "Search history..." else None)

            tk.Label(self.sidebar, text="RECENT", fg="#9aa0a6", bg=t["side"], font=("Arial", 8, "bold")).pack(anchor="w", padx=25)
            self.history_list = tk.Frame(self.sidebar, bg=t["side"])
            self.history_list.pack(fill=tk.BOTH, expand=True)

        # --- SIDEBAR FOOTER ---
        footer_frame = tk.Frame(self.sidebar, bg=t["side"])
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        line = tk.Frame(footer_frame, bg=t["acc"], height=1)
        line.pack(fill=tk.X, padx=20, pady=(0, 15))

        profile_frame = tk.Frame(footer_frame, bg=t["side"])
        profile_frame.pack(fill=tk.X, padx=20)

        avatar = tk.Label(profile_frame, text="👤", font=("Arial", 14), bg=t["side"], fg=t["txt"])
        avatar.pack(side=tk.LEFT)

        if self.sidebar_expanded:
            user_name = tk.Label(profile_frame, text="Study Guest", font=("Arial", 10, "bold"), 
                                 bg=t["side"], fg=t["txt"])
            user_name.pack(side=tk.LEFT, padx=10)
            
            help_btn = tk.Label(profile_frame, text="⚙", font=("Arial", 12), 
                                bg=t["side"], fg="#9aa0a6", cursor="hand2")
            help_btn.pack(side=tk.RIGHT)

    def toggle_sidebar(self):
        self.sidebar_expanded = not self.sidebar_expanded
        self.sidebar.config(width=260 if self.sidebar_expanded else 64)
        self.setup_sidebar()
        if self.sidebar_expanded: self.update_recent_topics()

    def _on_hover(self, frame, is_hover):
        t = self.themes["dark"] if self.dark_mode else self.themes["light"]
        color = t["hover"] if is_hover else t["side"]
        frame.config(bg=color)
        for child in frame.winfo_children():
            if child.winfo_width() != 4: 
                child.config(bg=color)

    # --- MAIN CHAT UI ---
    def setup_main_chat(self):
        t = self.themes["dark"] if self.dark_mode else self.themes["light"]

        if not hasattr(self, 'chat_area'):
            self.header = tk.Frame(self.main_container, bg=t["bg"])
            self.header.pack(fill=tk.X, padx=20, pady=(15, 0))
            self.header_lbl = tk.Label(self.header, text="StudyPYBot - Local Transformer", fg=t["txt"], bg=t["bg"], font=("Arial", 10, "italic"))
            self.header_lbl.pack(expand=True)

            self.chat_area = scrolledtext.ScrolledText(
                self.main_container, state='disabled', wrap='word', font=("Arial", 11), 
                bg=t["bg"], fg=t["txt"], bd=0, highlightthickness=0, padx=40, pady=20,
                insertbackground=t["txt"]
            )
            self.chat_area.pack(fill=tk.BOTH, expand=True)

            self.input_wrapper = tk.Frame(self.main_container, bg=t["bg"])
            self.input_wrapper.pack(fill=tk.X, side=tk.BOTTOM, padx=60, pady=(0, 40))

            self.input_container = tk.Frame(self.input_wrapper, bg=t["entry"], highlightthickness=1, highlightbackground=t["acc"])
            self.input_container.pack(fill=tk.X)

            self.attach_btn = tk.Label(self.input_container, text="📎", bg=t["entry"], fg="#9aa0a6", font=("Arial", 12), cursor="hand2")
            self.attach_btn.pack(side=tk.LEFT, padx=(15, 0))

            self.placeholder = "Ask StudyPYBot..."
            self.user_input = tk.Entry(
                self.input_container, font=("Arial", 11), bg=t["entry"], 
                fg="#9aa0a6", bd=0, highlightthickness=0, insertbackground=t["txt"]
            )
            self.user_input.insert(0, self.placeholder)
            self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12, padx=15)
            
            self.user_input.bind("<FocusIn>", self.clear_placeholder)
            self.user_input.bind("<FocusOut>", self.restore_placeholder)
            self.user_input.bind("<Return>", self.send_message)

            self.send_btn = tk.Button(
                self.input_container, text="✦", command=self.send_message, 
                bg=t["entry"], fg="#8ab4f8", font=("Arial", 18), relief="flat", bd=0, cursor="hand2",
                activebackground=t["entry"]
            )
            self.send_btn.pack(side=tk.RIGHT, padx=15)
        
        self.apply_theme_styles()

    def apply_theme_styles(self):
        t = self.themes["dark"] if self.dark_mode else self.themes["light"]
        
        self.header.config(bg=t["bg"])
        self.header_lbl.config(fg=t["txt"], bg=t["bg"])
        self.chat_area.config(bg=t["bg"], fg=t["txt"], insertbackground=t["txt"])
        self.input_wrapper.config(bg=t["bg"])
        self.input_container.config(bg=t["entry"], highlightbackground=t["acc"])
        self.attach_btn.config(bg=t["entry"])
        self.user_input.config(bg=t["entry"], insertbackground=t["txt"])
        
        btn_color = "#ea4335" if self.is_running else "#8ab4f8"
        btn_text = "■" if self.is_running else "✦"
        self.send_btn.config(bg=t["entry"], fg=btn_color, text=btn_text, activebackground=t["entry"])

        if self.user_input.get() != self.placeholder:
            self.user_input.config(fg=t["txt"])
        
        self.chat_area.tag_configure("bold", font=("Arial", 11, "bold"))
        self.chat_area.tag_configure("code", font=("Courier New", 10), background=t["code_bg"], foreground="#dcdce4" if self.dark_mode else "#333333")
        self.chat_area.tag_configure("user_label", font=("Arial", 11, "bold"), foreground=t["label_u"])
        self.chat_area.tag_configure("bot_label", font=("Arial", 11, "bold"), foreground=t["label_b"])
        self.chat_area.tag_configure("typing_status", font=("Arial", 11, "italic"), foreground="#9aa0a6")

    # --- CORE LOGIC ---
    def stop_generation(self):
        self.is_running = False
        self.reset_send_button()

    def animate_thinking(self, count=0):
        if not self.is_running: return 
        tag_ranges = self.chat_area.tag_ranges("typing_status")
        if not tag_ranges: return
        dots = "." * (count % 4)
        self.chat_area.config(state='normal')
        self.chat_area.delete(tag_ranges[0], tag_ranges[1])
        self.chat_area.insert(tag_ranges[0], f"StudyPYBot is thinking{dots}", "typing_status")
        self.chat_area.config(state='disabled')
        self.root.after(400, lambda: self.animate_thinking(count + 1))

    def append_formatted_text(self, text):
        self.chat_area.config(state='normal')
        parts = re.split(r'(\*\*.*?\*\*|`.*?`)', text)
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                self.chat_area.insert(tk.END, part[2:-2], "bold")
            elif part.startswith('`') and part.endswith('`'):
                self.chat_area.insert(tk.END, f" {part[1:-1]} ", "code")
            else: 
                self.chat_area.insert(tk.END, part)
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def send_message(self, event=None):
        msg = self.user_input.get().strip()
        if not msg or msg == self.placeholder: return
        
        t = self.themes["dark"] if self.dark_mode else self.themes["light"]
        self.is_running = True
        
        self.send_btn.config(text="■", command=self.stop_generation, fg="#ea4335", bg=t["entry"]) 
        
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, "\n\nYou: ", "user_label")
        self.chat_area.insert(tk.END, f"{msg}\n")
        self.chat_area.insert(tk.END, "\nStudyPYBot: ", "bot_label")
        self.chat_area.insert(tk.END, "StudyPYBot is thinking", "typing_status")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)
        
        self.user_input.delete(0, tk.END)
        self.animate_thinking()
        
        threading.Thread(target=self.run_ai, args=(msg,), daemon=True).start()

    def run_ai(self, msg):
        removed_status = False
        try:
            for chunk in self.controller.get_streaming_response(msg):
                if not self.is_running:
                    break 
                
                if not removed_status:
                    self.chat_area.config(state='normal')
                    tag_ranges = self.chat_area.tag_ranges("typing_status")
                    if tag_ranges: self.chat_area.delete(tag_ranges[0], tag_ranges[1])
                    self.chat_area.config(state='disabled')
                    removed_status = True
                
                self.root.after(0, lambda c=chunk: self.append_formatted_text(c))
        except Exception as e:
            print(f"Error: {e}")
        
        self.is_running = False
        self.root.after(0, self.reset_send_button)

    def reset_send_button(self):
        t = self.themes["dark"] if self.dark_mode else self.themes["light"]
        self.send_btn.config(text="✦", command=self.send_message, fg="#8ab4f8", bg=t["entry"])
        self.update_recent_topics()

    def update_recent_topics(self):
        if not self.sidebar_expanded or not hasattr(self, 'history_list'): return
        for widget in self.history_list.winfo_children(): widget.destroy()
        
        t = self.themes["dark"] if self.dark_mode else self.themes["light"]
        search_q = self.history_search.get().lower() if self.history_search.get() != "Search history..." else ""

        history = self.controller.storage.load_history()
        unique_topics = []
        for entry in reversed(history):
            topic = entry['user'].strip()
            if search_q in topic.lower():
                if topic not in unique_topics and topic != self.placeholder:
                    unique_topics.append(topic)
            if len(unique_topics) >= 7: break

        for topic in unique_topics:
            item_frame = tk.Frame(self.history_list, bg=t["side"])
            item_frame.pack(fill=tk.X)

            display_text = (topic[:18] + '..') if len(topic) > 18 else topic
            
            lbl = tk.Label(item_frame, text=f"•  {display_text}", 
                           fg="#9aa0a6", bg=t["side"], font=("Arial", 9), 
                           anchor="w", padx=30, pady=8, cursor="hand2")
            lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            del_btn = tk.Label(item_frame, text="✕", fg="#9aa0a6", bg=t["side"], 
                               font=("Arial", 8), padx=15, cursor="hand2")
            del_btn.pack(side=tk.RIGHT)

            lbl.bind("<Button-1>", lambda e, t=topic: self.auto_ask(t))
            del_btn.bind("<Button-1>", lambda e, t=topic: self.delete_topic(t))

            # Hover logic for the whole row
            def on_enter(e, f=item_frame, l=lbl, d=del_btn):
                f.config(bg=t["hover"])
                l.config(bg=t["hover"], fg=t["txt"])
                d.config(bg=t["hover"], fg="#ea4335")

            def on_leave(e, f=item_frame, l=lbl, d=del_btn):
                f.config(bg=t["side"])
                l.config(bg=t["side"], fg="#9aa0a6")
                d.config(bg=t["side"], fg="#9aa0a6")

            for w in (lbl, del_btn):
                w.bind("<Enter>", on_enter)
                w.bind("<Leave>", on_leave)

    def delete_topic(self, topic_text):
        if messagebox.askyesno("Delete Topic", f"Delete history for: '{topic_text[:20]}...'?"):
            history = self.controller.storage.load_history()
            # Remove all entries with this prompt
            new_history = [entry for entry in history if entry['user'].strip() != topic_text]
            self.controller.storage.save_history(new_history) 
            self.update_recent_topics()

    def load_history_to_chat(self):
        if messagebox.askyesno("Load History", "Load all saved history? This will clear current chat."):
            history = self.controller.storage.load_history()
            self.chat_area.config(state='normal')
            self.chat_area.delete('1.0', tk.END)
            
            for entry in history:
                # 1. Insert User Message with Spacing and Tag
                self.chat_area.insert(tk.END, "\n\nYou: ", "user_label")
                self.chat_area.insert(tk.END, f"{entry['user']}\n")
                
                # 2. Insert Bot Label with Spacing
                self.chat_area.insert(tk.END, "\nStudyPYBot: ", "bot_label")
                
                # 3. Process the bot's text through the formatter for Bold/Code support
                bot_text = entry['bot']
                if not bot_text.endswith('\n'):
                    bot_text += '\n'
                self.append_formatted_text(bot_text)
                
            self.chat_area.config(state='disabled')
            self.chat_area.yview(tk.END)

    # --- THEME & UTILS ---
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        t = self.themes["dark"] if self.dark_mode else self.themes["light"]
        self.root.config(bg=t["bg"])
        self.main_container.config(bg=t["bg"])
        self.sidebar.config(bg=t["side"])
        self.setup_sidebar()
        self.apply_theme_styles()
        self.update_recent_topics()

    def auto_ask(self, text):
        self.user_input.delete(0, tk.END)
        t = self.themes["dark"] if self.dark_mode else self.themes["light"]
        self.user_input.config(fg=t["txt"])
        self.user_input.insert(0, text)
        self.send_message()

    def clear_placeholder(self, e):
        t = self.themes["dark"] if self.dark_mode else self.themes["light"]
        if self.user_input.get() == self.placeholder:
            self.user_input.delete(0, tk.END)
            self.user_input.config(fg=t["txt"])

    def restore_placeholder(self, e):
        if not self.user_input.get():
            self.user_input.insert(0, self.placeholder)
            self.user_input.config(fg="#9aa0a6")

    def new_chat(self):
        if messagebox.askyesno("New Chat", "Clear current session?"):
            self.chat_area.config(state='normal')
            self.chat_area.delete('1.0', tk.END)
            self.chat_area.config(state='disabled')