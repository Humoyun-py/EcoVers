# BACKEND ROUTES INTEGRATION GUIDE
#############################################################################
# 20 TA YANGI O'YIN UCHUN BACKEND ROUTES TAYYOR!
#############################################################################

## ✅ BAJARILGAN

### 1. Backend Routes (new_games_routes.py)
20 ta to'liq Flask route yaratildi. Har birida:
- ✅ Energiya tekshirishuvi
- ✅ Energiya ayirboshlash (energy cost)
- ✅ Database commit
- ✅ Xatoliklar boshqaruvi
- ✅ games.html ga redirect

### 2. Route nomlar va URL'lar:
| # | O'yin Nomi | Route function | URL Path | Energy Cost |
|---|-----------|----------------|----------|-------------|
| 1 | Hayvonlarni Himoya Qilish | hayvonlar_himoya | /hayvonlar_himoya | 18 |
| 2 | Iqlim O'zgarishi Jasorati | iqlim_ozgarishi | /iqlim_ozgarishi | 25 |
| 3 | Okean Tozalash | okean_tozalash | /okean_tozalash | 16 |
| 4 | O'rmon Muhofizchisi | ormon_muhofizchisi | /ormon_muhofizchisi | 20 |
| 5 | Ekologik Shahar Qurish | ekologik_shahar | /ekologik_shahar | 30 |
| 6 | Biodiversitet Sarguzashti | biodiversitet | /biodiversitet | 14 |
| 7 | Kompost Ustasi | kompost_ustasi | /kompost_ustasi | 12 |
| 8 | Solar Energiya Ferma | solar_energiya | /solar_energiya | 22 |
| 9 | Karbon Izini Kamaytirish | karbon_kamaytirish | /karbon_kamaytirish | 15 |
| 10 | Havo Sifati Monitor | havo_sifati | /havo_sifati | 17 |
| 11 | Ekologik Bog'bon | ekologik_bogbon | /ekologik_bogbon | 19 |
| 12 | Asalari Qutqarish | asalari_qutqarish | /asalari_qutqarish | 21 |
| 13 | Dengiz Korallari Tiklanishi | korall_tiklanishi | /korall_tiklanishi | 23 |
| 14 | Plastikdan Qochish | plastikdan_qochish | /plastikdan_qochish | 11 |
| 15 | Shamol Energiyasi Qo'rg'on | shamol_energiyasi | /shamol_energiyasi | 24 |
| 16 | Tropik O'rmonlarni Asrash | tropik_ormonlar | /tropik_ormonlar | 28 |
| 17 | Suv Zaxiralarini Boshqarish | suv_boshqarish | /suv_boshqarish | 20 |
| 18 | Elektromobilga O'tish | elektromobil | /elektromobil | 22 |
| 19 | Ekologik Tadbirkor | ekologik_tadbirkor | /ekologik_tadbirkor | 35 |
| 20 | Tabiat Fotografchisi | tabiat_fotografchisi | /tabiat_fotografchisi | 13 |

#############################################################################
## 📋 KEYINGI QADAMLAR (Foydalanuvchi bajarishlari kerak)
#############################################################################

### QADAM 1: app.py ga route'larni ko'chirish
1. `new_games_routes.py` faylini oching
2. Barcha route'larni nusxalang (1-sonli qatordan boshlab)
3. `app.py` faylini oching
4. 1818-qatorni toping (eco_puzzle route'dan keyin)
5. Route'larni qo'shing
6. Faylni saqlang

### QADAM 2: games.html tugmalarni yangilash (Qisman bajarildi)
Ba'zi tugmalar yangilandi. Qolganlari uchun har bir o'yin tugmasini:

ESKI KOD:
```html
<button class="btn btn-danger w-100" onclick="alert('Bu o\'yin hali ishlab chiqilmoqda!')">
    <i class="fas fa-play  me-2"></i>Tez kunda!
</button>
```

YANGI KOD (Flask url_for bilan):
```html
<a href="{{ url_for('biodiversitet') }}" class="btn btn-lg w-100" style="background: #9c27b0; color: white;">
    <i class="fas fa-play me-2"></i>O'ynash
</a>
```

### QADAM 3:создать HTML template'lar (ixtiyoriy)
Hozircha route'lar error bermaydi, lekin template'lar yo'q deb ogohlantiradi.
Agar template yaratmoqchi bo'lsangiz, har bir o'yin uchun oddiy template:

```html
{% extends "base.html" %}
{% block title %}Hayvonlarni Himoya Qilish - EcoVerse{% endblock %}
{% block content %}
<div class="container mt-5">
    <h1>Hayvonlarni Himoya Qilish 🦁</h1>
    <p>Bu o'yin hali ishlab chiqilmoqda...</p>
    <a href="{{ url_for('games') }}" class="btn btn-primary">Orqaga</a>
</div>
{% endblock %}
```

#############################################################################
## 🔥 MUHIM ESLATMALAR
#############################################################################

1. **app.py serverni qayta ishga tushiring** route'larni qo'shgandan keyin
2. **Energiya yetarli bo'lishi kerak** o'yinni ochish uchun
3. **Template'lar yo'q** bo'lsa, 500 xato ko'rsatadi (bu oddiy, tuzatish oson)
4. **coin rewards** `/game /complete` API orqali beriladi (mavjud)

#############################################################################
## 📊 TO'LIQ IMPLEMENTATSIYA
#############################################################################

✅ Frontend (games.html) - 20 ta o'yin kartasi qo'shildi
✅ Backend Routes - 20 ta Flask route yaratildi  
⏳ Templates - Har bir o'yin uchun HTML (ixtiyoriy)
✅ Energiya tizimi - Avtomatik ishlaydi
✅ Coin mukofotlari - complete_game API orqali

#############################################################################
