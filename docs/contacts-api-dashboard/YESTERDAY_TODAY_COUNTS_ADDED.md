# Dashboard Enhancement - Yesterday & Today Counts

**Date:** 2026-02-10 13:25 UTC
**Status:** ✅ IMPLEMENTED

---

## 🎯 **What Was Added**

Enhanced the dashboard to show **daily breakdown** of new persons:
- ✅ Existing: "+59,747 this week"
- ✅ NEW: "+10,022 yesterday"
- ✅ NEW: "+143 today" (only shows if > 0)

---

## 📝 **Changes Made**

### 1. Backend API (`/opt/contacts_api/app/main.py`)

**Added queries to count persons by day:**

```python
# Get yesterday's count
yesterday_counts = await conn.fetchrow("""
    SELECT COUNT(*) as count
    FROM core.person
    WHERE DATE(created_at) = CURRENT_DATE - INTERVAL '1 day'
""")

# Get today's count
today_counts = await conn.fetchrow("""
    SELECT COUNT(*) as count
    FROM core.person
    WHERE DATE(created_at) = CURRENT_DATE
""")
```

**Added to API response:**
```python
return {
    ...
    "persons_yesterday": yesterday_counts["count"],
    "persons_today": today_counts["count"]
}
```

### 2. Frontend Display (`/opt/contacts_api/static/admin-dashboard.html`)

**Updated JavaScript to show breakdown:**

```javascript
let personsGrowth = `+${formatNumber(overview.persons_last_7_days)} this week`;
if (overview.persons_yesterday > 0) {
    personsGrowth += `<br>+${formatNumber(overview.persons_yesterday)} yesterday`;
}
if (overview.persons_today > 0) {
    personsGrowth += `<br>+${formatNumber(overview.persons_today)} today`;
}
document.getElementById('persons-growth').innerHTML = personsGrowth;
```

---

## 📊 **Current Data**

**Database Verification:**
- Yesterday (Feb 9): **10,022 persons**
- Today (Feb 10 so far): **143 persons**
- This week: **59,747 persons**

---

## 🎨 **Expected Display**

**Before:**
```
Total Persons
1,983,444
+59,747 this week
```

**After:**
```
Total Persons
1,983,444
+59,747 this week
+10,022 yesterday
+143 today
```

---

## 🔄 **Service Status**

```
● contacts-api.service - Active (running)
   Started: Tue 2026-02-10 13:24:41 UTC
   Status: Application startup complete
```

---

## 🧪 **Testing Instructions**

1. **Refresh dashboard:** `Ctrl+Shift+R` (hard refresh)
2. **URL:** https://leadsdatabase.cc/static/admin-dashboard.html
3. **Look for:** "Total Persons" card
4. **Should see:** Three lines showing week, yesterday, and today counts

**Note:** "today" will only show if count > 0

---

## 📂 **Files Modified**

1. `/opt/contacts_api/app/main.py`
   - Added `yesterday_counts` and `today_counts` queries
   - Added `persons_yesterday` and `persons_today` to response

2. `/opt/contacts_api/static/admin-dashboard.html`
   - Updated `persons-growth` display logic
   - Changed from `textContent` to `innerHTML` to support line breaks

---

## ✅ **Backups Created**

- `/opt/contacts_api/app/main.py.backup_before_yesterday_today_20260210_132425`
- `/opt/contacts_api/static/admin-dashboard.html.backup_before_yesterday_today_20260210_132433`

---

**Please refresh your dashboard and verify the yesterday/today counts appear!** 🚀
