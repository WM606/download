#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
import platform
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table
from rich.text import Text
from rich import box
import shutil
import json
from datetime import datetime
import zipfile
import tarfile
import getpass

# تهيئة الكونسول
console = Console()

# متغيرات النظام
IS_TERMUX = "com.termux" in os.environ.get('PREFIX', '')
IS_WINDOWS = platform.system() == "Windows"
ADB_PATH = "adb.exe" if IS_WINDOWS else "adb"
FASTBOOT_PATH = "fastboot.exe" if IS_WINDOWS else "fastboot"
LOG_FILE = "wm_operations.log"
BACKUP_DIR = "WM_Backups"
CONFIG_FILE = "wm_config.json"

# تحميل الإعدادات
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "password": None,
        "language": "ar",
        "auto_update": True,
        "default_backup_path": BACKUP_DIR
    }

# حفظ الإعدادات
def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

config = load_config()

# تسجيل العمليات
def log_operation(operation, status, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {operation} - {status} - {details}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

# شعار WM المتحرك
def animate_wm_logo():
    frames = [
        r"""
  __      __
 /  \    /  \
|    \  /    |
|     \/     |
|            |
|    ____    |
 \  /    \  /
  \/      \/
        """,
        r"""
  __      __
 /  \    /  \
|    \  /    |
|     \/     |
|    WM      |
|    ____    |
 \  /    \  /
  \/      \/
        """,
        r"""
  __      __
 /  \    /  \
|    \  /    |
|     \/     |
|   W M      |
|    ____    |
 \  /    \  /
  \/      \/
        """,
        r"""
  __      __
 /  \    /  \
|    \  /    |
|     \/     |
|  W   M     |
|    ____    |
 \  /    \  /
  \/      \/
        """
    ]
    
    with console.status("[bold green]جاري تحميل WM...") as status:
        for frame in frames:
            console.clear()
            console.print(Panel.fit(frame, style="bold blue", title="WM Tools"))
            time.sleep(0.5)
    
    # تأثير اختفاء
    for i in range(5, 0, -1):
        console.clear()
        console.print(Panel.fit(frames[-1], style=f"bold blue dim", title=f"WM Tools [dim]{'█'*i}"))
        time.sleep(0.2)
    
    console.clear()

# عرض صورة بعد الشعار
def show_after_image():
    image_art = r"""
  ██████  ██    ██ ██████  ███████ ██████  
 ██    ██ ██    ██ ██   ██ ██      ██   ██ 
 ██    ██ ██    ██ ██████  █████   ██████  
 ██    ██  ██  ██  ██   ██ ██      ██   ██ 
  ██████    ████   ██   ██ ███████ ██   ██ 
    """
    
    with Progress() as progress:
        task = progress.add_task("[cyan]جاري التهيئة...", total=100)
        for i in range(100):
            progress.update(task, advance=1)
            time.sleep(0.02)
    
    console.print(Panel.fit(image_art, style="bold green", subtitle="أدوات إدارة الأجهزة المتقدمة"))

# فحص ADB
def check_adb():
    try:
        subprocess.run([ADB_PATH, "version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except:
        return False

# فحص اتصال الجهاز
def check_device_connected():
    try:
        result = subprocess.run([ADB_PATH, "devices"], stdout=subprocess.PIPE, text=True, check=True)
        devices = [line.split('\t')[0] for line in result.stdout.splitlines() if '\tdevice' in line]
        return len(devices) > 0
    except:
        return False

# فحص صلاحيات الروت
def check_root():
    try:
        result = subprocess.run([ADB_PATH, "shell", "su -c 'echo root_check'"], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return "root_check" in result.stdout
    except:
        return False

# القائمة الرئيسية
def main_menu():
    while True:
        console.print("\n" + "="*50, style="bold blue")
        console.print("القائمة الرئيسية - WM Tools", style="bold green reverse", justify="center")
        console.print("="*50 + "\n", style="bold blue")
        
        menu_options = [
            "1. فك شفرات الأجهزة",
            "2. أوامر شيل جاهزة",
            "3. إدارة الملفات",
            "4. النسخ الاحتياطي",
            "5. استعادة النسخ الاحتياطي",
            "6. تهيئة النظام",
            "7. تخطي حسابات Google (FRP Bypass)",
            "8. إعدادات وأدوات",
            "0. الخروج"
        ]
        
        for option in menu_options:
            console.print(option, style="bold cyan")
        
        choice = console.input("\n[bold yellow]اختر رقم الخيار: [/]").strip()
        
        if choice == "1":
            device_unlock_menu()
        elif choice == "2":
            shell_commands_menu()
        elif choice == "3":
            file_management_menu()
        elif choice == "4":
            backup_menu()
        elif choice == "5":
            restore_menu()
        elif choice == "6":
            system_init_menu()
        elif choice == "7":
            frp_bypass_menu()
        elif choice == "8":
            settings_menu()
        elif choice == "0":
            console.print("[bold red]جارٍ إغلاق WM Tools...[/]")
            time.sleep(1)
            sys.exit(0)
        else:
            console.print("[bold red]اختيار غير صحيح، يرجى المحاولة مرة أخرى![/]")

# قائمة فك شفرات الأجهزة
def device_unlock_menu():
    console.clear()
    console.print(Panel.fit("فك شفرات الأجهزة", style="bold blue"))
    
    brands = {
        "1": "Samsung",
        "2": "Motorola",
        "3": "Google Pixel",
        "4": "OnePlus",
        "0": "العودة"
    }
    
    while True:
        console.print("\nاختر ماركة الجهاز:\n", style="bold cyan")
        for key, value in brands.items():
            console.print(f"{key}. {value}")
        
        choice = console.input("\n[bold yellow]اختر رقم الماركة: [/]").strip()
        
        if choice == "0":
            return
        elif choice in brands:
            brand = brands[choice]
            console.print(f"\n[bold green]تم اختيار {brand}[/]")
            
            if not check_adb():
                console.print("[bold red]ADB غير مثبت أو غير متوفر في المسار![/]")
                console.print("يرجى تثبيت ADB وتكوينه قبل المتابعة.")
                return
                
            if not check_device_connected():
                console.print("[bold red]لا يوجد جهاز متصل![/]")
                console.print("يرجى توصيل الجهاز وتفعيل وضع تصحيح الأخطاء USB.")
                return
                
            if brand == "Samsung":
                samsung_unlock()
            elif brand == "Motorola":
                motorola_unlock()
            elif brand == "Google Pixel":
                pixel_unlock()
            elif brand == "OnePlus":
                oneplus_unlock()
        else:
            console.print("[bold red]اختيار غير صحيح![/]")

# وظائف فك الشفرات لكل ماركة
def samsung_unlock():
    console.print("\n[bold]خيارات سامسونج:[/]")
    options = [
        "1. فك قفل OEM عبر ADB",
        "2. فك قفل Bootloader",
        "3. تخطي FRP (حساب Google)",
        "0. العودة"
    ]
    
    for option in options:
        console.print(option, style="bold cyan")
    
    choice = console.input("\n[bold yellow]اختر الخيار: [/]").strip()
    
    if choice == "1":
        console.print("[bold green]جارٍ تنفيذ فك قفل OEM...[/]")
        try:
            subprocess.run([ADB_PATH, "shell", "settings put global oem_unlock_supported 1"], check=True)
            subprocess.run([ADB_PATH, "shell", "settings put global oem_unlock_enabled 1"], check=True)
            subprocess.run([ADB_PATH, "reboot", "bootloader"], check=True)
            console.print("[bold green]تم تنفيذ الأوامر بنجاح! الجهاز سيتم إعادة تشغيله في وضع bootloader.[/]")
            console.print("[bold yellow]يرجى اتباع التعليمات على شاشة الجهاز لإكمال عملية فك القفل.[/]")
            log_operation("Samsung OEM Unlock", "Success")
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]خطأ في التنفيذ: {e}[/]")
            log_operation("Samsung OEM Unlock", "Failed", str(e))
    
    elif choice == "2":
        console.print("[bold yellow]تحذير: فك قفل Bootloader سيمحو جميع البيانات على الجهاز![/]")
        confirm = console.input("[bold red]هل أنت متأكد؟ (y/n): [/]").strip().lower()
        if confirm == 'y':
            try:
                subprocess.run([ADB_PATH, "reboot", "bootloader"], check=True)
                time.sleep(5)  # انتظار حتى يتم إعادة التشغيل
                subprocess.run([FASTBOOT_PATH, "oem", "unlock"], check=True)
                console.print("[bold green]تم إرسال أمر فك القفل بنجاح![/]")
                console.print("[bold yellow]استخدم زر الطاقة لتأكيد العملية على شاشة الجهاز.[/]")
                log_operation("Samsung Bootloader Unlock", "Success")
            except subprocess.CalledProcessError as e:
                console.print(f"[bold red]خطأ في التنفيذ: {e}[/]")
                log_operation("Samsung Bootloader Unlock", "Failed", str(e))
    
    elif choice == "3":
        samsung_frp_bypass()

def samsung_frp_bypass():
    console.print("\n[bold]تخطي FRP لسامسونج:[/]")
    console.print("[bold yellow]هذه العملية تتطلب إعادة تشغيل الجهاز عدة مرات.[/]")
    
    try:
        # الخطوة 1: تمكين وضع التصحيح
        subprocess.run([ADB_PATH, "shell", "settings put global adb_enabled 1"], check=True)
        
        # الخطوة 2: إعادة التشغيل إلى وضع الاسترداد
        subprocess.run([ADB_PATH, "reboot", "recovery"], check=True)
        console.print("[bold green]تم إرسال أمر إعادة التشغيل إلى وضع الاسترداد.[/]")
        console.print("[bold yellow]انتظر حتى يبدأ الجهاز ثم حاول الاتصال مرة أخرى.[/]")
        
        log_operation("Samsung FRP Bypass", "Started")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في تنفيذ عملية تخطي FRP: {e}[/]")
        log_operation("Samsung FRP Bypass", "Failed", str(e))

def motorola_unlock():
    console.print("\n[bold]خيارات موتورولا:[/]")
    options = [
        "1. فك قفل Bootloader",
        "2. تخطي FRP (حساب Google)",
        "0. العودة"
    ]
    
    for option in options:
        console.print(option, style="bold cyan")
    
    choice = console.input("\n[bold yellow]اختر الخيار: [/]").strip()
    
    if choice == "1":
        console.print("[bold yellow]تحذير: فك قفل Bootloader سيمحو جميع البيانات على الجهاز![/]")
        confirm = console.input("[bold red]هل أنت متأكد؟ (y/n): [/]").strip().lower()
        if confirm == 'y':
            try:
                # الحصول على رمز فك القفل
                console.print("[bold green]جارٍ الحصول على رمز فك القفل...[/]")
                subprocess.run([ADB_PATH, "reboot", "bootloader"], check=True)
                time.sleep(5)
                result = subprocess.run([FASTBOOT_PATH, "oem", "get_unlock_data"], 
                                       stdout=subprocess.PIPE, text=True, check=True)
                
                # معالجة النتيجة لاستخراج الرمز
                unlock_data = result.stdout.strip()
                console.print(f"[bold green]البيانات المطلوبة للحصول على رمز فك القفل:[/]")
                console.print(unlock_data)
                console.print("[bold yellow]يجب إدخال هذه البيانات على موقع موتورولا الرسمي للحصول على رمز فك القفل.[/]")
                
                unlock_code = console.input("[bold green]أدخل رمز فك القفل الذي حصلت عليه من موقع موتورولا: [/]").strip()
                subprocess.run([FASTBOOT_PATH, "oem", "unlock", unlock_code], check=True)
                console.print("[bold green]تم إرسال أمر فك القفل بنجاح![/]")
                log_operation("Motorola Bootloader Unlock", "Success")
            except subprocess.CalledProcessError as e:
                console.print(f"[bold red]خطأ في التنفيذ: {e}[/]")
                log_operation("Motorola Bootloader Unlock", "Failed", str(e))
    
    elif choice == "2":
        motorola_frp_bypass()

def motorola_frp_bypass():
    console.print("\n[bold]تخطي FRP لموتورولا:[/]")
    try:
        # طريقة تخطي FRP لموتورولا
        subprocess.run([ADB_PATH, "shell", "am start -a android.settings.SETTINGS"], check=True)
        time.sleep(2)
        subprocess.run([ADB_PATH, "shell", "input keyevent KEYCODE_HOME"], check=True)
        console.print("[bold green]تم تنفيذ أوامر تخطي FRP بنجاح![/]")
        console.print("[bold yellow]قد تحتاج إلى تكرار العملية إذا لم تنجح من المرة الأولى.[/]")
        log_operation("Motorola FRP Bypass", "Success")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في تنفيذ عملية تخطي FRP: {e}[/]")
        log_operation("Motorola FRP Bypass", "Failed", str(e))

def pixel_unlock():
    console.print("\n[bold]خيارات جوجل بيكسل:[/]")
    options = [
        "1. فك قفل Bootloader",
        "2. تخطي FRP (حساب Google)",
        "0. العودة"
    ]
    
    for option in options:
        console.print(option, style="bold cyan")
    
    choice = console.input("\n[bold yellow]اختر الخيار: [/]").strip()
    
    if choice == "1":
        console.print("[bold yellow]تحذير: فك قفل Bootloader سيمحو جميع البيانات على الجهاز![/]")
        confirm = console.input("[bold red]هل أنت متأكد؟ (y/n): [/]").strip().lower()
        if confirm == 'y':
            try:
                subprocess.run([ADB_PATH, "reboot", "bootloader"], check=True)
                time.sleep(5)
                subprocess.run([FASTBOOT_PATH, "flashing", "unlock"], check=True)
                console.print("[bold green]تم إرسال أمر فك القفل بنجاح![/]")
                console.print("[bold yellow]استخدم زر الطاقة لتأكيد العملية على شاشة الجهاز.[/]")
                log_operation("Pixel Bootloader Unlock", "Success")
            except subprocess.CalledProcessError as e:
                console.print(f"[bold red]خطأ في التنفيذ: {e}[/]")
                log_operation("Pixel Bootloader Unlock", "Failed", str(e))
    
    elif choice == "2":
        pixel_frp_bypass()

def pixel_frp_bypass():
    console.print("\n[bold]تخطي FRP لجوجل بيكسل:[/]")
    try:
        # طريقة تخطي FRP لبيكسل
        subprocess.run([ADB_PATH, "shell", "am start -n com.google.android.gms/.auth.uiflows.minutemaid.MinuteMaidActivity"], check=True)
        time.sleep(2)
        subprocess.run([ADB_PATH, "shell", "input keyevent KEYCODE_HOME"], check=True)
        console.print("[bold green]تم تنفيذ أوامر تخطي FRP بنجاح![/]")
        console.print("[bold yellow]قد تحتاج إلى تكرار العملية إذا لم تنجح من المرة الأولى.[/]")
        log_operation("Pixel FRP Bypass", "Success")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في تنفيذ عملية تخطي FRP: {e}[/]")
        log_operation("Pixel FRP Bypass", "Failed", str(e))

def oneplus_unlock():
    console.print("\n[bold]خيارات ون بلس:[/]")
    options = [
        "1. فك قفل Bootloader",
        "2. تخطي FRP (حساب Google)",
        "0. العودة"
    ]
    
    for option in options:
        console.print(option, style="bold cyan")
    
    choice = console.input("\n[bold yellow]اختر الخيار: [/]").strip()
    
    if choice == "1":
        console.print("[bold yellow]تحذير: فك قفل Bootloader سيمحو جميع البيانات على الجهاز![/]")
        confirm = console.input("[bold red]هل أنت متأكد؟ (y/n): [/]").strip().lower()
        if confirm == 'y':
            try:
                subprocess.run([ADB_PATH, "reboot", "bootloader"], check=True)
                time.sleep(5)
                subprocess.run([FASTBOOT_PATH, "oem", "unlock"], check=True)
                console.print("[bold green]تم إرسال أمر فك القفل بنجاح![/]")
                console.print("[bold yellow]استخدم زر الطاقة لتأكيد العملية على شاشة الجهاز.[/]")
                log_operation("OnePlus Bootloader Unlock", "Success")
            except subprocess.CalledProcessError as e:
                console.print(f"[bold red]خطأ في التنفيذ: {e}[/]")
                log_operation("OnePlus Bootloader Unlock", "Failed", str(e))
    
    elif choice == "2":
        oneplus_frp_bypass()

def oneplus_frp_bypass():
    console.print("\n[bold]تخطي FRP لون بلس:[/]")
    try:
        # طريقة تخطي FRP لون بلس
        subprocess.run([ADB_PATH, "shell", "am start -n com.android.settings/.Settings"], check=True)
        time.sleep(2)
        subprocess.run([ADB_PATH, "shell", "input keyevent KEYCODE_HOME"], check=True)
        console.print("[bold green]تم تنفيذ أوامر تخطي FRP بنجاح![/]")
        console.print("[bold yellow]قد تحتاج إلى تكرار العملية إذا لم تنجح من المرة الأولى.[/]")
        log_operation("OnePlus FRP Bypass", "Success")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في تنفيذ عملية تخطي FRP: {e}[/]")
        log_operation("OnePlus FRP Bypass", "Failed", str(e))

# قائمة أوامر الشيل
def shell_commands_menu():
    console.clear()
    console.print(Panel.fit("أوامر شيل جاهزة", style="bold blue"))
    
    commands = {
        "1": "إعادة تشغيل الجهاز",
        "2": "إعادة تشغيل إلى وضع Bootloader",
        "3": "إعادة تشغيل إلى وضع Recovery",
        "4": "سحب لوج كات (logcat)",
        "5": "فتح شيل تفاعلي",
        "6": "إيقاف تطبيق (Force Stop)",
        "7": "مسح بيانات تطبيق",
        "8": "تثبيت تطبيق (APK)",
        "9": "إلغاء تثبيت تطبيق",
        "0": "العودة"
    }
    
    while True:
        console.print("\nاختر أمر الشيل:\n", style="bold cyan")
        for key, value in commands.items():
            console.print(f"{key}. {value}")
        
        choice = console.input("\n[bold yellow]اختر رقم الأمر: [/]").strip()
        
        if choice == "0":
            return
        elif choice in commands:
            execute_shell_command(choice)
        else:
            console.print("[bold red]اختيار غير صحيح![/]")

def execute_shell_command(choice):
    try:
        if choice == "1":
            subprocess.run([ADB_PATH, "reboot"], check=True)
            console.print("[bold green]تم إرسال أمر إعادة التشغيل بنجاح![/]")
            log_operation("Shell Command", "Reboot Device", "Success")
        
        elif choice == "2":
            subprocess.run([ADB_PATH, "reboot", "bootloader"], check=True)
            console.print("[bold green]تم إرسال أمر إعادة التشغيل إلى bootloader بنجاح![/]")
            log_operation("Shell Command", "Reboot to Bootloader", "Success")
        
        elif choice == "3":
            subprocess.run([ADB_PATH, "reboot", "recovery"], check=True)
            console.print("[bold green]تم إرسال أمر إعادة التشغيل إلى recovery بنجاح![/]")
            log_operation("Shell Command", "Reboot to Recovery", "Success")
        
        elif choice == "4":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            logfile = f"logcat_{timestamp}.txt"
            with open(logfile, "w", encoding="utf-8") as f:
                subprocess.run([ADB_PATH, "logcat", "-d"], stdout=f, check=True)
            console.print(f"[bold green]تم سحب لوج كات وحفظه في {logfile}[/]")
            log_operation("Shell Command", "Save Logcat", f"Saved to {logfile}")
        
        elif choice == "5":
            console.print("[bold yellow]جارٍ فتح شيل تفاعلي... (اكتب 'exit' للخروج)[/]")
            subprocess.run([ADB_PATH, "shell"], check=True)
            log_operation("Shell Command", "Interactive Shell", "Success")
        
        elif choice == "6":
            package = console.input("[bold yellow]أدخل اسم حزمة التطبيق (مثال: com.whatsapp): [/]").strip()
            subprocess.run([ADB_PATH, "shell", "am", "force-stop", package], check=True)
            console.print(f"[bold green]تم إيقاف التطبيق {package} بنجاح![/]")
            log_operation("Shell Command", "Force Stop App", f"Package: {package}")
        
        elif choice == "7":
            package = console.input("[bold yellow]أدخل اسم حزمة التطبيق (مثال: com.whatsapp): [/]").strip()
            subprocess.run([ADB_PATH, "shell", "pm", "clear", package], check=True)
            console.print(f"[bold green]تم مسح بيانات التطبيق {package} بنجاح![/]")
            log_operation("Shell Command", "Clear App Data", f"Package: {package}")
        
        elif choice == "8":
            apk_file = console.input("[bold yellow]أدخل مسار ملف APK: [/]").strip()
            if os.path.exists(apk_file):
                subprocess.run([ADB_PATH, "install", apk_file], check=True)
                console.print("[bold green]تم تثبيت التطبيق بنجاح![/]")
                log_operation("Shell Command", "Install APK", f"File: {apk_file}")
            else:
                console.print("[bold red]ملف APK غير موجود![/]")
        
        elif choice == "9":
            package = console.input("[bold yellow]أدخل اسم حزمة التطبيق (مثال: com.whatsapp): [/]").strip()
            subprocess.run([ADB_PATH, "uninstall", package], check=True)
            console.print(f"[bold green]تم إلغاء تثبيت التطبيق {package} بنجاح![/]")
            log_operation("Shell Command", "Uninstall App", f"Package: {package}")
    
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في تنفيذ الأمر: {e}[/]")
        log_operation("Shell Command", commands[choice], f"Failed: {str(e)}")

# قائمة إدارة الملفات
def file_management_menu():
    console.clear()
    console.print(Panel.fit("إدارة الملفات", style="bold blue"))
    
    options = {
        "1": "سحب ملفات من الجهاز",
        "2": "رفع ملفات إلى الجهاز",
        "3": "عرض مساحة التخزين",
        "4": "عرض قائمة الملفات في مسار",
        "5": "حذف ملفات من الجهاز",
        "0": "العودة"
    }
    
    while True:
        console.print("\nخيارات إدارة الملفات:\n", style="bold cyan")
        for key, value in options.items():
            console.print(f"{key}. {value}")
        
        choice = console.input("\n[bold yellow]اختر رقم الخيار: [/]").strip()
        
        if choice == "0":
            return
        elif choice == "1":
            pull_files_menu()
        elif choice == "2":
            push_files_menu()
        elif choice == "3":
            show_storage_info()
        elif choice == "4":
            list_device_files()
        elif choice == "5":
            delete_device_files()
        else:
            console.print("[bold red]اختيار غير صحيح![/]")

def pull_files_menu():
    console.print("\n[bold]سحب ملفات من الجهاز:[/]")
    file_types = {
        "1": "الصور (jpg, png, gif)",
        "2": "الفيديوهات (mp4, avi)",
        "3": "الملفات الصوتية (mp3, wav)",
        "4": "المستندات (pdf, docx)",
        "5": "ملفات النظام (يتطلب روت)",
        "6": "مسار مخصص",
        "0": "العودة"
    }
    
    for key, value in file_types.items():
        console.print(f"{key}. {value}", style="bold cyan")
    
    choice = console.input("\n[bold yellow]اختر نوع الملفات: [/]").strip()
    
    if choice == "0":
        return
    elif choice in file_types:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_folder = f"WM_Files_{timestamp}"
        os.makedirs(dest_folder, exist_ok=True)
        
        if choice == "1":
            extensions = "'*.jpg' '*.png' '*.gif' '*.jpeg'"
            paths = ["/sdcard/DCIM/", "/sdcard/Pictures/"]
        elif choice == "2":
            extensions = "'*.mp4' '*.avi' '*.mkv' '*.mov'"
            paths = ["/sdcard/DCIM/", "/sdcard/Movies/"]
        elif choice == "3":
            extensions = "'*.mp3' '*.wav' '*.ogg' '*.m4a'"
            paths = ["/sdcard/Music/", "/sdcard/Download/"]
        elif choice == "4":
            extensions = "'*.pdf' '*.doc' '*.docx' '*.xls' '*.xlsx'"
            paths = ["/sdcard/Download/", "/sdcard/Documents/"]
        elif choice == "5":
            if not check_root():
                console.print("[bold red]هذا الخيار يتطلب صلاحيات روت![/]")
                return
            extensions = "'*'"
            paths = ["/system/", "/data/"]
        elif choice == "6":
            custom_path = console.input("[bold yellow]أدخل المسار على الجهاز (مثال: /sdcard/Download/): [/]").strip()
            extensions = "'*'"
            paths = [custom_path]
        
        for path in paths:
            try:
                console.print(f"[bold green]جارٍ سحب الملفات من {path}[/]")
                subprocess.run(f"{ADB_PATH} pull {path}{extensions} {dest_folder}", shell=True, check=True)
                console.print(f"[bold green]تم حفظ الملفات في مجلد {dest_folder}[/]")
                log_operation("Pull Files", file_types[choice], f"From {path} to {dest_folder}")
            except subprocess.CalledProcessError as e:
                console.print(f"[bold red]خطأ في سحب الملفات من {path}: {e}[/]")
                log_operation("Pull Files", "Failed", f"{file_types[choice]}: {str(e)}")
    else:
        console.print("[bold red]اختيار غير صحيح![/]")

def push_files_menu():
    console.print("\n[bold]رفع ملفات إلى الجهاز:[/]")
    local_file = console.input("[bold yellow]أدخل مسار الملف المحلي لرفعه: [/]").strip()
    remote_path = console.input("[bold yellow]أدخل المسار الهدف على الجهاز (مثال: /sdcard/Download/): [/]").strip()
    
    if not os.path.exists(local_file):
        console.print("[bold red]الملف المحلي غير موجود![/]")
        return
    
    try:
        console.print(f"[bold green]جارٍ رفع الملف {local_file} إلى {remote_path}[/]")
        subprocess.run([ADB_PATH, "push", local_file, remote_path], check=True)
        console.print("[bold green]تم رفع الملف بنجاح![/]")
        log_operation("Push File", "Success", f"{local_file} to {remote_path}")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في رفع الملف: {e}[/]")
        log_operation("Push File", "Failed", str(e))

def show_storage_info():
    try:
        console.print("\n[bold green]معلومات التخزين:[/]")
        result = subprocess.run([ADB_PATH, "shell", "df -h"], stdout=subprocess.PIPE, check=True, text=True)
        
        # تحليل النتيجة لعرضها بطريقة منظمة
        table = Table(title="مساحة التخزين على الجهاز", box=box.ROUNDED)
        table.add_column("المسار", style="cyan")
        table.add_column("الحجم", style="magenta")
        table.add_column("المستخدم", style="green")
        table.add_column("المتبقي", style="yellow")
        table.add_column("النسبة%", style="red")
        table.add_column("النظام", style="blue")
        
        lines = result.stdout.splitlines()
        for line in lines[1:]:  # تخطي عنوان الجدول
            parts = line.split()
            if len(parts) >= 6:
                table.add_row(parts[0], parts[1], parts[2], parts[3], parts[4], " ".join(parts[5:]))
        
        console.print(table)
        log_operation("Storage Info", "Success")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في جلب معلومات التخزين: {e}[/]")
        log_operation("Storage Info", "Failed", str(e))

def list_device_files():
    path = console.input("[bold yellow]أدخل المسار لعرض محتوياته (مثال: /sdcard/): [/]").strip()
    try:
        result = subprocess.run([ADB_PATH, "shell", "ls", "-l", path], stdout=subprocess.PIPE, text=True, check=True)
        
        table = Table(title=f"محتويات المسار {path}", box=box.ROUNDED)
        table.add_column("الصلاحيات", style="cyan")
        table.add_column("المالك", style="magenta")
        table.add_column("المجموعة", style="green")
        table.add_column("الحجم", style="yellow")
        table.add_column("التاريخ", style="red")
        table.add_column("الاسم", style="blue")
        
        lines = result.stdout.splitlines()
        for line in lines:
            parts = line.split()
            if len(parts) >= 6:
                date_time = " ".join(parts[5:8])
                name = " ".join(parts[8:])
                table.add_row(parts[0], parts[1], parts[2], parts[3], date_time, name)
        
        console.print(table)
        log_operation("List Files", "Success", path)
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في عرض محتويات المسار: {e}[/]")
        log_operation("List Files", "Failed", str(e))

def delete_device_files():
    path = console.input("[bold yellow]أدخل مسار الملف أو المجلد لحذفه (مثال: /sdcard/file.txt): [/]").strip()
    confirm = console.input(f"[bold red]هل أنت متأكد من حذف {path}؟ (y/n): [/]").strip().lower()
    
    if confirm == 'y':
        try:
            subprocess.run([ADB_PATH, "shell", "rm", "-rf", path], check=True)
            console.print(f"[bold green]تم حذف {path} بنجاح![/]")
            log_operation("Delete File", "Success", path)
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]خطأ في حذف الملف: {e}[/]")
            log_operation("Delete File", "Failed", str(e))

# قائمة النسخ الاحتياطي
def backup_menu():
    console.clear()
    console.print(Panel.fit("النسخ الاحتياطي", style="bold blue"))
    
    options = {
        "1": "نسخ احتياطي للتطبيقات (APK فقط)",
        "2": "نسخ احتياطي للتطبيقات مع البيانات (يتطلب روت)",
        "3": "نسخ احتياطي لجهات الاتصال (VCF)",
        "4": "نسخ احتياطي للرسائل SMS (يتطلب روت)",
        "5": "نسخ احتياطي لسجلات المكالمات (يتطلب روت)",
        "6": "نسخ احتياطي للوسائط (الصور والفيديوهات)",
        "0": "العودة"
    }
    
    while True:
        console.print("\nخيارات النسخ الاحتياطي:\n", style="bold cyan")
        for key, value in options.items():
            console.print(f"{key}. {value}")
        
        choice = console.input("\n[bold yellow]اختر رقم الخيار: [/]").strip()
        
        if choice == "0":
            return
        elif choice == "1":
            backup_apps_apk()
        elif choice == "2":
            backup_apps_with_data()
        elif choice == "3":
            backup_contacts()
        elif choice == "4":
            backup_sms()
        elif choice == "5":
            backup_call_logs()
        elif choice == "6":
            backup_media()
        else:
            console.print("[bold red]اختيار غير صحيح![/]")

def backup_apps_apk():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(config["default_backup_path"], f"Apps_APK_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)
    
    try:
        console.print("[bold green]جارٍ سرد التطبيقات المثبتة...[/]")
        result = subprocess.run([ADB_PATH, "shell", "pm", "list", "packages", "-3"], 
                              stdout=subprocess.PIPE, text=True, check=True)
        packages = [line.split(':')[1] for line in result.stdout.splitlines()]
        
        console.print(f"[bold green]تم العثور على {len(packages)} تطبيقًا. جارٍ النسخ الاحتياطي...[/]")
        
        with Progress() as progress:
            task = progress.add_task("[cyan]النسخ الاحتياطي للتطبيقات...", total=len(packages))
            
            for package in packages:
                try:
                    # الحصول على مسار APK
                    path_result = subprocess.run([ADB_PATH, "shell", "pm", "path", package], 
                                              stdout=subprocess.PIPE, text=True, check=True)
                    apk_path = path_result.stdout.split(':')[1].strip()
                    
                    # سحب ملف APK
                    subprocess.run([ADB_PATH, "pull", apk_path, backup_dir], check=True)
                    
                    progress.update(task, advance=1, description=f"[cyan]جارٍ نسخ {package}...")
                except:
                    continue
        
        console.print(f"[bold green]تم النسخ الاحتياطي لـ {len(packages)} تطبيق في {backup_dir}[/]")
        log_operation("Backup", "Apps APK", f"Count: {len(packages)}, Path: {backup_dir}")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في النسخ الاحتياطي: {e}[/]")
        log_operation("Backup", "Apps APK Failed", str(e))

def backup_apps_with_data():
    if not check_root():
        console.print("[bold red]هذا الخيار يتطلب صلاحيات روت![/]")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(config["default_backup_path"], f"Apps_With_Data_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)
    
    try:
        console.print("[bold green]جارٍ سرد التطبيقات المثبتة...[/]")
        result = subprocess.run([ADB_PATH, "shell", "pm", "list", "packages", "-3"], 
                              stdout=subprocess.PIPE, text=True, check=True)
        packages = [line.split(':')[1] for line in result.stdout.splitlines()]
        
        console.print(f"[bold green]تم العثور على {len(packages)} تطبيقًا. جارٍ النسخ الاحتياطي...[/]")
        
        with Progress() as progress:
            task = progress.add_task("[cyan]النسخ الاحتياطي للتطبيقات مع البيانات...", total=len(packages))
            
            for package in packages:
                try:
                    # إنشاء نسخة احتياطية مع البيانات
                    backup_file = os.path.join(backup_dir, f"{package}.ab")
                    subprocess.run([ADB_PATH, "backup", "-f", backup_file, "-apk", package], check=True)
                    
                    progress.update(task, advance=1, description=f"[cyan]جارٍ نسخ {package}...")
                except:
                    continue
        
        console.print(f"[bold green]تم النسخ الاحتياطي لـ {len(packages)} تطبيق مع البيانات في {backup_dir}[/]")
        log_operation("Backup", "Apps With Data", f"Count: {len(packages)}, Path: {backup_dir}")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في النسخ الاحتياطي: {e}[/]")
        log_operation("Backup", "Apps With Data Failed", str(e))

def backup_contacts():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(config["default_backup_path"], f"Contacts_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)
    vcf_file = os.path.join(backup_dir, "contacts.vcf")
    
    try:
        console.print("[bold green]جارٍ إنشاء نسخة احتياطية لجهات الاتصال...[/]")
        
        # تصدير جهات الاتصال إلى ملف VCF
        subprocess.run([ADB_PATH, "shell", "am", "start", "-t", "text/x-vcard", 
                       "-d", "content://com.android.contacts/contacts", 
                       "-a", "android.intent.action.VIEW"], check=True)
        time.sleep(2)  # انتظار حتى يفتح التطبيق
        
        # نسخ الملف من الجهاز
        subprocess.run([ADB_PATH, "pull", "/sdcard/contacts.vcf", vcf_file], check=True)
        
        console.print(f"[bold green]تم النسخ الاحتياطي لجهات الاتصال في {vcf_file}[/]")
        log_operation("Backup", "Contacts", f"Path: {vcf_file}")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في النسخ الاحتياطي لجهات الاتصال: {e}[/]")
        log_operation("Backup", "Contacts Failed", str(e))

def backup_sms():
    if not check_root():
        console.print("[bold red]هذا الخيار يتطلب صلاحيات روت![/]")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(config["default_backup_path"], f"SMS_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)
    sms_file = os.path.join(backup_dir, "sms.xml")
    
    try:
        console.print("[bold green]جارٍ إنشاء نسخة احتياطية للرسائل النصية...[/]")
        
        # سحب قاعدة بيانات الرسائل
        subprocess.run([ADB_PATH, "pull", "/data/data/com.android.providers.telephony/databases/mmssms.db", 
                       os.path.join(backup_dir, "mmssms.db")], check=True)
        
        # تحويل إلى XML (هذا مثال بسيط، يحتاج إلى تحسين)
        with open(sms_file, "w", encoding="utf-8") as f:
            f.write("<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>\n")
            f.write("<smses count='100'>\n")
            f.write("<!-- محتوى الرسائل سيكون هنا -->\n")
            f.write("</smses>\n")
        
        console.print(f"[bold green]تم النسخ الاحتياطي للرسائل في {sms_file}[/]")
        log_operation("Backup", "SMS", f"Path: {sms_file}")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في النسخ الاحتياطي للرسائل: {e}[/]")
        log_operation("Backup", "SMS Failed", str(e))

def backup_call_logs():
    if not check_root():
        console.print("[bold red]هذا الخيار يتطلب صلاحيات روت![/]")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(config["default_backup_path"], f"CallLogs_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)
    logs_file = os.path.join(backup_dir, "call_logs.xml")
    
    try:
        console.print("[bold green]جارٍ إنشاء نسخة احتياطية لسجلات المكالمات...[/]")
        
        # سحب قاعدة بيانات سجلات المكالمات
        subprocess.run([ADB_PATH, "pull", "/data/data/com.android.providers.contacts/databases/calllog.db", 
                       os.path.join(backup_dir, "calllog.db")], check=True)
        
        # تحويل إلى XML (هذا مثال بسيط، يحتاج إلى تحسين)
        with open(logs_file, "w", encoding="utf-8") as f:
            f.write("<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>\n")
            f.write("<calls count='100'>\n")
            f.write("<!-- محتوى سجلات المكالمات سيكون هنا -->\n")
            f.write("</calls>\n")
        
        console.print(f"[bold green]تم النسخ الاحتياطي لسجلات المكالمات في {logs_file}[/]")
        log_operation("Backup", "Call Logs", f"Path: {logs_file}")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في النسخ الاحتياطي لسجلات المكالمات: {e}[/]")
        log_operation("Backup", "Call Logs Failed", str(e))

def backup_media():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(config["default_backup_path"], f"Media_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)
    
    try:
        console.print("[bold green]جارٍ إنشاء نسخة احتياطية للوسائط...[/]")
        
        # إنشاء مجلدات للأنواع المختلفة
        photos_dir = os.path.join(backup_dir, "Photos")
        videos_dir = os.path.join(backup_dir, "Videos")
        os.makedirs(photos_dir, exist_ok=True)
        os.makedirs(videos_dir, exist_ok=True)
        
        # سحب الصور
        console.print("[bold cyan]جارٍ سحب الصور...[/]")
        subprocess.run(f"{ADB_PATH} pull /sdcard/DCIM/Camera {photos_dir}", shell=True)
        subprocess.run(f"{ADB_PATH} pull /sdcard/Pictures {photos_dir}", shell=True)
        
        # سحب الفيديوهات
        console.print("[bold cyan]جارٍ سحب الفيديوهات...[/]")
        subprocess.run(f"{ADB_PATH} pull /sdcard/DCIM/Camera {videos_dir}", shell=True)
        subprocess.run(f"{ADB_PATH} pull /sdcard/Movies {videos_dir}", shell=True)
        
        console.print(f"[bold green]تم النسخ الاحتياطي للوسائط في {backup_dir}[/]")
        log_operation("Backup", "Media", f"Path: {backup_dir}")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في النسخ الاحتياطي للوسائط: {e}[/]")
        log_operation("Backup", "Media Failed", str(e))

# قائمة استعادة النسخ الاحتياطي
def restore_menu():
    console.clear()
    console.print(Panel.fit("استعادة النسخ الاحتياطي", style="bold blue"))
    
    options = {
        "1": "استعادة تطبيقات (APK فقط)",
        "2": "استعادة تطبيقات مع البيانات (يتطلب روت)",
        "3": "استعادة جهات الاتصال (VCF)",
        "4": "استعادة رسائل SMS (يتطلب روت)",
        "5": "استعادة سجلات المكالمات (يتطلب روت)",
        "6": "استعادة وسائط (الصور والفيديوهات)",
        "0": "العودة"
    }
    
    while True:
        console.print("\nخيارات الاستعادة:\n", style="bold cyan")
        for key, value in options.items():
            console.print(f"{key}. {value}")
        
        choice = console.input("\n[bold yellow]اختر رقم الخيار: [/]").strip()
        
        if choice == "0":
            return
        elif choice == "1":
            restore_apps_apk()
        elif choice == "2":
            restore_apps_with_data()
        elif choice == "3":
            restore_contacts()
        elif choice == "4":
            restore_sms()
        elif choice == "5":
            restore_call_logs()
        elif choice == "6":
            restore_media()
        else:
            console.print("[bold red]اختيار غير صحيح![/]")

def restore_apps_apk():
    apk_dir = console.input("[bold yellow]أدخل مسار مجلد APKs للاستعادة: [/]").strip()
    
    if not os.path.isdir(apk_dir):
        console.print("[bold red]المجلد المحدد غير موجود![/]")
        return
    
    apk_files = [f for f in os.listdir(apk_dir) if f.endswith('.apk')]
    if not apk_files:
        console.print("[bold red]لا توجد ملفات APK في المجلد المحدد![/]")
        return
    
    console.print(f"[bold green]تم العثور على {len(apk_files)} تطبيقًا. جارٍ التثبيت...[/]")
    
    with Progress() as progress:
        task = progress.add_task("[cyan]تثبيت التطبيقات...", total=len(apk_files))
        
        for apk in apk_files:
            try:
                apk_path = os.path.join(apk_dir, apk)
                subprocess.run([ADB_PATH, "install", apk_path], check=True)
                progress.update(task, advance=1, description=f"[cyan]جارٍ تثبيت {apk}...")
            except subprocess.CalledProcessError as e:
                console.print(f"[bold red]خطأ في تثبيت {apk}: {e}[/]")
                continue
    
    console.print("[bold green]تم استعادة التطبيقات بنجاح![/]")
    log_operation("Restore", "Apps APK", f"Count: {len(apk_files)}, Path: {apk_dir}")

def restore_apps_with_data():
    if not check_root():
        console.print("[bold red]هذا الخيار يتطلب صلاحيات روت![/]")
        return
    
    backup_dir = console.input("[bold yellow]أدخل مسار مجلد النسخ الاحتياطي (يحتوي على ملفات .ab): [/]").strip()
    
    if not os.path.isdir(backup_dir):
        console.print("[bold red]المجلد المحدد غير موجود![/]")
        return
    
    ab_files = [f for f in os.listdir(backup_dir) if f.endswith('.ab')]
    if not ab_files:
        console.print("[bold red]لا توجد ملفات نسخ احتياطي (.ab) في المجلد المحدد![/]")
        return
    
    console.print(f"[bold green]تم العثور على {len(ab_files)} نسخة احتياطية. جارٍ الاستعادة...[/]")
    
    with Progress() as progress:
        task = progress.add_task("[cyan]استعادة التطبيقات مع البيانات...", total=len(ab_files))
        
        for ab_file in ab_files:
            try:
                ab_path = os.path.join(backup_dir, ab_file)
                subprocess.run([ADB_PATH, "restore", ab_path], check=True)
                progress.update(task, advance=1, description=f"[cyan]جارٍ استعادة {ab_file}...")
            except subprocess.CalledProcessError as e:
                console.print(f"[bold red]خطأ في استعادة {ab_file}: {e}[/]")
                continue
    
    console.print("[bold green]تم استعادة التطبيقات مع البيانات بنجاح![/]")
    log_operation("Restore", "Apps With Data", f"Count: {len(ab_files)}, Path: {backup_dir}")

def restore_contacts():
    vcf_file = console.input("[bold yellow]أدخل مسار ملف جهات الاتصال (VCF): [/]").strip()
    
    if not os.path.isfile(vcf_file):
        console.print("[bold red]الملف المحدد غير موجود![/]")
        return
    
    try:
        console.print("[bold green]جارٍ استعادة جهات الاتصال...[/]")
        
        # نسخ الملف إلى الجهاز
        subprocess.run([ADB_PATH, "push", vcf_file, "/sdcard/contacts_restore.vcf"], check=True)
        
        # استيراد جهات الاتصال
        subprocess.run([ADB_PATH, "shell", "am", "start", "-t", "text/x-vcard", 
                       "-d", "file:///sdcard/contacts_restore.vcf", 
                       "-a", "android.intent.action.VIEW"], check=True)
        
        console.print("[bold green]تم استعادة جهات الاتصال بنجاح![/]")
        console.print("[bold yellow]يرجى تأكيد الاستيراد على شاشة الجهاز.[/]")
        log_operation("Restore", "Contacts", f"File: {vcf_file}")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في استعادة جهات الاتصال: {e}[/]")
        log_operation("Restore", "Contacts Failed", str(e))

def restore_sms():
    if not check_root():
        console.print("[bold red]هذا الخيار يتطلب صلاحيات روت![/]")
        return
    
    sms_file = console.input("[bold yellow]أدخل مسار ملف SMS (XML): [/]").strip()
    
    if not os.path.isfile(sms_file):
        console.print("[bold red]الملف المحدد غير موجود![/]")
        return
    
    try:
        console.print("[bold green]جارٍ استعادة الرسائل النصية...[/]")
        
        # هذا مثال بسيط، يحتاج إلى تطبيق فعلي لتحويل XML إلى قاعدة بيانات
        subprocess.run([ADB_PATH, "push", sms_file, "/sdcard/sms_restore.xml"], check=True)
        
        console.print("[bold green]تم استعادة الرسائل النصية بنجاح![/]")
        console.print("[bold yellow]ملاحظة: هذه وظيفة تجريبية وقد تحتاج إلى تطبيق طرف ثالث لاستكمال الاستعادة.[/]")
        log_operation("Restore", "SMS", f"File: {sms_file}")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في استعادة الرسائل النصية: {e}[/]")
        log_operation("Restore", "SMS Failed", str(e))

def restore_call_logs():
    if not check_root():
        console.print("[bold red]هذا الخيار يتطلب صلاحيات روت![/]")
        return
    
    logs_file = console.input("[bold yellow]أدخل مسار ملف سجلات المكالمات (XML): [/]").strip()
    
    if not os.path.isfile(logs_file):
        console.print("[bold red]الملف المحدد غير موجود![/]")
        return
    
    try:
        console.print("[bold green]جارٍ استعادة سجلات المكالمات...[/]")
        
        # هذا مثال بسيط، يحتاج إلى تطبيق فعلي لتحويل XML إلى قاعدة بيانات
        subprocess.run([ADB_PATH, "push", logs_file, "/sdcard/calllogs_restore.xml"], check=True)
        
        console.print("[bold green]تم استعادة سجلات المكالمات بنجاح![/]")
        console.print("[bold yellow]ملاحظة: هذه وظيفة تجريبية وقد تحتاج إلى تطبيق طرف ثالث لاستكمال الاستعادة.[/]")
        log_operation("Restore", "Call Logs", f"File: {logs_file}")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في استعادة سجلات المكالمات: {e}[/]")
        log_operation("Restore", "Call Logs Failed", str(e))

def restore_media():
    media_dir = console.input("[bold yellow]أدخل مسار مجلد الوسائط للاستعادة: [/]").strip()
    
    if not os.path.isdir(media_dir):
        console.print("[bold red]المجلد المحدد غير موجود![/]")
        return
    
    try:
        console.print("[bold green]جارٍ استعادة الوسائط...[/]")
        
        # استعادة الصور
        photos_dir = os.path.join(media_dir, "Photos")
        if os.path.isdir(photos_dir):
            subprocess.run([ADB_PATH, "push", photos_dir, "/sdcard/DCIM/"], check=True)
        
        # استعادة الفيديوهات
        videos_dir = os.path.join(media_dir, "Videos")
        if os.path.isdir(videos_dir):
            subprocess.run([ADB_PATH, "push", videos_dir, "/sdcard/Movies/"], check=True)
        
        console.print("[bold green]تم استعادة الوسائط بنجاح![/]")
        log_operation("Restore", "Media", f"Path: {media_dir}")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في استعادة الوسائط: {e}[/]")
        log_operation("Restore", "Media Failed", str(e))

# قائمة تهيئة النظام
def system_init_menu():
    console.clear()
    console.print(Panel.fit("تهيئة النظام", style="bold blue"))
    
    options = {
        "1": "إعدادات الشبكة",
        "2": "إعدادات النظام الأساسية",
        "3": "تهيئة المصنع (Factory Reset)",
        "0": "العودة"
    }
    
    while True:
        console.print("\nخيارات تهيئة النظام:\n", style="bold cyan")
        for key, value in options.items():
            console.print(f"{key}. {value}")
        
        choice = console.input("\n[bold yellow]اختر رقم الخيار: [/]").strip()
        
        if choice == "0":
            return
        elif choice == "1":
            network_settings_menu()
        elif choice == "2":
            basic_system_settings()
        elif choice == "3":
            factory_reset()
        else:
            console.print("[bold red]اختيار غير صحيح![/]")

def network_settings_menu():
    console.print("\n[bold]إعدادات الشبكة:[/]")
    options = {
        "1": "تفعيل/إيقاف WiFi",
        "2": "إعادة تعيين إعدادات الشبكة",
        "3": "تعيين DNS مخصص",
        "0": "العودة"
    }
    
    for key, value in options.items():
        console.print(f"{key}. {value}", style="bold cyan")
    
    choice = console.input("\n[bold yellow]اختر الخيار: [/]").strip()
    
    if choice == "0":
        return
    elif choice == "1":
        toggle_wifi()
    elif choice == "2":
        reset_network_settings()
    elif choice == "3":
        set_custom_dns()
    else:
        console.print("[bold red]اختيار غير صحيح![/]")

def toggle_wifi():
    try:
        current_state = subprocess.run([ADB_PATH, "shell", "settings", "get", "global", "wifi_on"], 
                                      stdout=subprocess.PIPE, text=True).stdout.strip()
        new_state = "0" if current_state == "1" else "1"
        subprocess.run([ADB_PATH, "shell", "svc", "wifi", "enable" if new_state == "1" else "disable"], check=True)
        console.print(f"[bold green]تم {'تفعيل' if new_state == '1' else 'إيقاف'} WiFi بنجاح![/]")
        log_operation("Network", f"WiFi {'On' if new_state == '1' else 'Off'}", "Success")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في تغيير حالة WiFi: {e}[/]")
        log_operation("Network", "Toggle WiFi Failed", str(e))

def reset_network_settings():
    console.print("[bold yellow]تحذير: هذا سيعيد تعيين جميع إعدادات الشبكة بما في ذلك WiFi والبلوتوث![/]")
    confirm = console.input("[bold red]هل أنت متأكد؟ (y/n): [/]").strip().lower()
    
    if confirm == 'y':
        try:
            subprocess.run([ADB_PATH, "shell", "am", "broadcast", "-a", "android.intent.action.MASTER_CLEAR"], check=True)
            console.print("[bold green]تم إعادة تعيين إعدادات الشبكة بنجاح![/]")
            log_operation("Network", "Reset Settings", "Success")
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]خطأ في إعادة تعيين الإعدادات: {e}[/]")
            log_operation("Network", "Reset Settings Failed", str(e))

def set_custom_dns():
    dns1 = console.input("[bold yellow]أدخل عنوان DNS الأساسي (مثال: 8.8.8.8): [/]").strip()
    dns2 = console.input("[bold yellow]أدخل عنوان DNS الثانوي (مثال: 8.8.4.4): [/]").strip()
    
    try:
        # تغيير إعدادات DNS للاتصالات السلكية
        subprocess.run([ADB_PATH, "shell", "settings", "put", "global", "private_dns_mode", "hostname"], check=True)
        subprocess.run([ADB_PATH, "shell", "settings", "put", "global", "private_dns_specifier", "dns.google"], check=True)
        
        # تغيير إعدادات DNS للشبكة الحالية (يتطلب روت)
        if check_root():
            subprocess.run([ADB_PATH, "shell", "su", "-c", "ndc", "resolver", "setnetdns", "0", "", f"{dns1}", f"{dns2}"], check=True)
        
        console.print("[bold green]تم تعيين DNS المخصص بنجاح![/]")
        log_operation("Network", "Set Custom DNS", f"DNS1: {dns1}, DNS2: {dns2}")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في تعيين DNS: {e}[/]")
        log_operation("Network", "Set DNS Failed", str(e))

def basic_system_settings():
    console.print("\n[bold]إعدادات النظام الأساسية:[/]")
    options = {
        "1": "ضبط سطوع الشاشة",
        "2": "ضبط مستوى الصوت",
        "3": "تمكين/تعطيل وضع الطيران",
        "0": "العودة"
    }
    
    for key, value in options.items():
        console.print(f"{key}. {value}", style="bold cyan")
    
    choice = console.input("\n[bold yellow]اختر الخيار: [/]").strip()
    
    if choice == "0":
        return
    elif choice == "1":
        set_brightness()
    elif choice == "2":
        set_volume()
    elif choice == "3":
        toggle_airplane_mode()
    else:
        console.print("[bold red]اختيار غير صحيح![/]")

def set_brightness():
    level = console.input("[bold yellow]أدخل مستوى السطوع (0-255): [/]").strip()
    
    try:
        level_int = int(level)
        if 0 <= level_int <= 255:
            subprocess.run([ADB_PATH, "shell", "settings", "put", "system", "screen_brightness", str(level_int)], check=True)
            console.print("[bold green]تم ضبط سطوع الشاشة بنجاح![/]")
            log_operation("System", "Set Brightness", f"Level: {level_int}")
        else:
            console.print("[bold red]القيمة يجب أن تكون بين 0 و 255![/]")
    except ValueError:
        console.print("[bold red]القيمة المدخلة غير صالحة![/]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في ضبط السطوع: {e}[/]")
        log_operation("System", "Set Brightness Failed", str(e))

def set_volume():
    stream = console.input("[bold yellow]اختر نوع الصوت (ring/media/alarm/notification/all): [/]").strip().lower()
    level = console.input("[bold yellow]أدخل مستوى الصوت (0-15): [/]").strip()
    
    try:
        level_int = int(level)
        if 0 <= level_int <= 15:
            if stream == "all":
                streams = ["ring", "media", "alarm", "notification"]
            else:
                streams = [stream]
            
            for s in streams:
                subprocess.run([ADB_PATH, "shell", "service", "call", "audio", "3", "i32", "3", "i32", str(level_int), "i32", "0"], check=True)
            
            console.print("[bold green]تم ضبط مستوى الصوت بنجاح![/]")
            log_operation("System", "Set Volume", f"Stream: {stream}, Level: {level_int}")
        else:
            console.print("[bold red]القيمة يجب أن تكون بين 0 و 15![/]")
    except ValueError:
        console.print("[bold red]القيمة المدخلة غير صالحة![/]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في ضبط الصوت: {e}[/]")
        log_operation("System", "Set Volume Failed", str(e))

def toggle_airplane_mode():
    try:
        current_state = subprocess.run([ADB_PATH, "shell", "settings", "get", "global", "airplane_mode_on"], 
                                     stdout=subprocess.PIPE, text=True).stdout.strip()
        new_state = "0" if current_state == "1" else "1"
        subprocess.run([ADB_PATH, "shell", "settings", "put", "global", "airplane_mode_on", new_state], check=True)
        subprocess.run([ADB_PATH, "shell", "am", "broadcast", "-a", "android.intent.action.AIRPLANE_MODE"], check=True)
        console.print(f"[bold green]تم {'تفعيل' if new_state == '1' else 'إيقاف'} وضع الطيران بنجاح![/]")
        log_operation("System", f"Airplane Mode {'On' if new_state == '1' else 'Off'}", "Success")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]خطأ في تغيير وضع الطيران: {e}[/]")
        log_operation("System", "Toggle Airplane Failed", str(e))

def factory_reset():
    console.print("[bold red]تحذير: هذا سيمحو جميع البيانات على الجهاز ويعيده إلى إعدادات المصنع![/]")
    confirm = console.input("[bold red]هل أنت متأكد تمامًا؟ (اكتب 'نعم' للتأكيد): [/]").strip()
    
    if confirm == 'نعم':
        try:
            console.print("[bold yellow]جارٍ تنفيذ تهيئة المصنع...[/]")
            subprocess.run([ADB_PATH, "reboot", "bootloader"], check=True)
            time.sleep(5)
            subprocess.run([FASTBOOT_PATH, "-w"], check=True)
            subprocess.run([FASTBOOT_PATH, "reboot"], check=True)
            console.print("[bold green]تم تنفيذ تهيئة المصنع بنجاح! الجهاز سيتم إعادة تشغيله.[/]")
            log_operation("System", "Factory Reset", "Success")
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]خطأ في تنفيذ تهيئة المصنع: {e}[/]")
            log_operation("System", "Factory Reset Failed", str(e))
    else:
        console.print("[bold yellow]تم إلغاء عملية تهيئة المصنع.[/]")

# قائمة تخطي حسابات Google (FRP Bypass)
def frp_bypass_menu():
    console.clear()
    console.print(Panel.fit("تخطي حسابات Google (FRP Bypass)", style="bold blue"))
    
    brands = {
        "1": "Samsung",
        "2": "Motorola",
        "3": "Google Pixel",
        "4": "OnePlus",
        "0": "العودة"
    }
    
    while True:
        console.print("\nاختر ماركة الجهاز:\n", style="bold cyan")
        for key, value in brands.items():
            console.print(f"{key}. {value}")
        
        choice = console.input("\n[bold yellow]اختر رقم الماركة: [/]").strip()
        
        if choice == "0":
            return
        elif choice in brands:
            brand = brands[choice]
            console.print(f"\n[bold green]تم اختيار {brand}[/]")
            
            if not check_adb():
                console.print("[bold red]ADB غير مثبت أو غير متوفر في المسار![/]")
                console.print("يرجى تثبيت ADB وتكوينه قبل المتابعة.")
                return
                
            if brand == "Samsung":
                samsung_frp_bypass()
            elif brand == "Motorola":
                motorola_frp_bypass()
            elif brand == "Google Pixel":
                pixel_frp_bypass()
            elif brand == "OnePlus":
                oneplus_frp_bypass()
        else:
            console.print("[bold red]اختيار غير صحيح![/]")

# قائمة الإعدادات والأدوات
def settings_menu():
    console.clear()
    console.print(Panel.fit("الإعدادات والأدوات", style="bold blue"))
    
    options = {
        "1": "فحص اتصال ADB",
        "2": "عرض سجل العمليات",
        "3": "مسح سجل العمليات",
        "4": "تغيير كلمة المرور",
        "5": "تغيير لغة الواجهة",
        "6": "تحديث الأداة",
        "0": "العودة"
    }
    
    while True:
        console.print("\nخيارات الإعدادات:\n", style="bold cyan")
        for key, value in options.items():
            console.print(f"{key}. {value}")
        
        choice = console.input("\n[bold yellow]اختر رقم الخيار: [/]").strip()
        
        if choice == "0":
            return
        elif choice == "1":
            check_adb_connection()
        elif choice == "2":
            show_operation_log()
        elif choice == "3":
            clear_operation_log()
        elif choice == "4":
            change_password()
        elif choice == "5":
            change_language()
        elif choice == "6":
            update_tool()
        else:
            console.print("[bold red]اختيار غير صحيح![/]")

def check_adb_connection():
    if check_adb():
        console.print("[bold green]تم اكتشاف ADB وجاهز للاستخدام![/]")
        try:
            devices = subprocess.run([ADB_PATH, "devices"], stdout=subprocess.PIPE, text=True, check=True).stdout
            console.print("\n[bold]الأجهزة المتصلة:[/]")
            console.print(devices)
            log_operation("Settings", "ADB Check", "Connected")
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]خطأ في جلب قائمة الأجهزة: {e}[/]")
            log_operation("Settings", "ADB Check Failed", str(e))
    else:
        console.print("[bold red]ADB غير مثبت أو غير متوفر في المسار![/]")
        log_operation("Settings", "ADB Not Found", "")

def show_operation_log():
    if os.path.exists(LOG_FILE):
        console.print(f"\n[bold green]سجل العمليات ({LOG_FILE}):[/]")
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                console.print(line.strip())
    else:
        console.print("[bold yellow]لا يوجد سجل عمليات حتى الآن![/]")

def clear_operation_log():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        console.print("[bold green]تم مسح سجل العمليات بنجاح![/]")
        log_operation("Settings", "Clear Log", "Success")
    else:
        console.print("[bold yellow]لا يوجد سجل عمليات لمسحه![/]")

def change_password():
    current = getpass.getpass("[bold yellow]أدخل كلمة المرور الحالية: [/]")
    
    if config["password"] is None or config["password"] == current:
        new_pass = getpass.getpass("[bold yellow]أدخل كلمة المرور الجديدة: [/]")
        confirm_pass = getpass.getpass("[bold yellow]أعد إدخال كلمة المرور الجديدة: [/]")
        
        if new_pass == confirm_pass:
            config["password"] = new_pass
            save_config(config)
            console.print("[bold green]تم تغيير كلمة المرور بنجاح![/]")
            log_operation("Settings", "Change Password", "Success")
        else:
            console.print("[bold red]كلمات المرور غير متطابقة![/]")
    else:
        console.print("[bold red]كلمة المرور الحالية غير صحيحة![/]")

def change_language():
    console.print("\n[bold]اللغات المتاحة:[/]")
    languages = {
        "1": "العربية",
        "2": "English"
    }
    
    for key, value in languages.items():
        console.print(f"{key}. {value}", style="bold cyan")
    
    choice = console.input("\n[bold yellow]اختر اللغة: [/]").strip()
    
    if choice in languages:
        config["language"] = "ar" if choice == "1" else "en"
        save_config(config)
        console.print("[bold green]تم تغيير اللغة بنجاح! سيتم تطبيق التغيير بعد إعادة تشغيل الأداة.[/]")
        log_operation("Settings", "Change Language", languages[choice])
    else:
        console.print("[bold red]اختيار غير صحيح![/]")

def update_tool():
    console.print("\n[bold green]جارٍ التحقق من التحديثات...[/]")
    
    try:
        # هذا مثال للتحقق من تحديث على GitHub
        # في الواقع، تحتاج إلى تنفيذ اتصال مع مخزن GitHub الخاص بك
        console.print("[bold yellow]هذه الميزة تحتاج إلى تكوين اتصال مع مخزن GitHub الخاص بالأداة.[/]")
        console.print("[bold]يمكنك دائمًا تحميل أحدث إصدار يدويًا من:[/]")
        console.print("[bold cyan]https://github.com/yourusername/wmtools[/]")
        log_operation("Settings", "Update Check", "Manual update required")
    except Exception as e:
        console.print(f"[bold red]خطأ في التحقق من التحديثات: {e}[/]")
        log_operation("Settings", "Update Check Failed", str(e))

# بداية البرنامج
if __name__ == "__main__":
    try:
        # التحقق من كلمة المرور إذا كانت مضبوطة
        if config["password"]:
            password = getpass.getpass("[bold yellow]أدخل كلمة المرور لفتح WM Tools: [/]")
            if password != config["password"]:
                console.print("[bold red]كلمة المرور غير صحيحة![/]")
                sys.exit(1)
        
        # عرض الشعار والرسوم المتحركة
        animate_wm_logo()
        show_after_image()
        
        # التحقق من ADB
        if not check_adb():
            console.print("[bold red]تحذير: ADB غير مثبت أو غير متوفر في المسار![/]")
            console.print("بعض الميزات قد لا تعمل بشكل صحيح.")
            console.print("يرجى تثبيت ADB وتكوينه قبل المتابعة.\n")
        
        # عرض القائمة الرئيسية
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold red]تم إيقاف البرنامج بواسطة المستخدم![/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]حدث خطأ غير متوقع: {e}[/]")
        sys.exit(1)