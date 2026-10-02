# راهنمای انتخاب رشته ۱۴۰۵ — داده‌محور

سامانه‌ای استاتیک برای کمک به بررسی رشته و دانشگاه با اتصال دو منبع:
- راهنمای انتخاب رشته جاب‌ویژن ۱۴۰۵
- داده‌های انتخاب رشته سازمان سنجش ۱۴۰۴ از پروژه مرجع Sanjesh1404

## اصل کلیدی
هیچ داده ساختگی، تخمینی یا پرکننده در خروجی مجاز نیست.

## اجرای کامل
```bash
pip install -r requirements-data.txt
make build
make validate
```

برای کنترل بصری PDF:
```bash
make review
```

پس از build:
```bash
python3 -m http.server 8000 --directory site
```

## Vercel
Build Command:
`python3 scripts/build_vercel.py`

Output Directory:
`_site`

## ساختار
- `/` درگاه اصلی
- `/dashboard/` داشبورد
- `/compare/` مقایسه
- `/atlas/` اطلس
- `/about/` منابع و روش‌شناسی

## وضعیت داده
فایل‌های `data/raw` در Git ذخیره نمی‌شوند؛ build آنها را مستقیماً از URLهای اصلی دریافت می‌کند. این کار از ثبت نسخه‌ای قدیمی یا داده دستکاری‌شده جلوگیری می‌کند.
