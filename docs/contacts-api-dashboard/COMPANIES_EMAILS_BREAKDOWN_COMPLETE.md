# Companies & Emails Daily Breakdown - Complete

**Date:** 2026-02-10 13:35 UTC
**Status:** ✅ IMPLEMENTED

---

## 🎯 **What Was Added**

Extended yesterday/today counts to **all three metrics**:
- ✅ **Persons** (already had it)
- ✅ **Companies** (NEW)
- ✅ **Emails** (NEW)

---

## 📊 **Current Data**

**Yesterday (Feb 9):**
- Persons: 10,022
- Companies: 5,770
- Emails: 10,008

**Today (Feb 10 so far):**
- Persons: 143
- Companies: 694
- Emails: 1,369

---

## 🔧 **Changes Made**

### 1. Database Indexes Created

```sql
-- Index on company.created_at
CREATE INDEX company_created_at_idx ON core.company (created_at DESC);

-- Index on email.first_seen_at
CREATE INDEX email_first_seen_at_idx ON core.email (first_seen_at DESC);
```

### 2. Backend API (`/opt/contacts_api/app/main.py`)

**Added queries for companies:**
```python
companies_yesterday = await conn.fetchrow("""
    SELECT COUNT(*) as count
    FROM core.company
    WHERE created_at >= date_trunc('day', CURRENT_DATE - INTERVAL '1 day')
      AND created_at < date_trunc('day', CURRENT_DATE)
""")

companies_today = await conn.fetchrow("""
    SELECT COUNT(*) as count
    FROM core.company
    WHERE created_at >= date_trunc('day', CURRENT_DATE)
      AND created_at < date_trunc('day', CURRENT_DATE + INTERVAL '1 day')
""")
```

**Added queries for emails (using `first_seen_at`):**
```python
emails_yesterday = await conn.fetchrow("""
    SELECT COUNT(*) as count
    FROM core.email
    WHERE first_seen_at >= date_trunc('day', CURRENT_DATE - INTERVAL '1 day')
      AND first_seen_at < date_trunc('day', CURRENT_DATE)
""")

emails_today = await conn.fetchrow("""
    SELECT COUNT(*) as count
    FROM core.email
    WHERE first_seen_at >= date_trunc('day', CURRENT_DATE)
      AND first_seen_at < date_trunc('day', CURRENT_DATE + INTERVAL '1 day')
""")
```

**Added to API response:**
```python
return {
    ...
    "companies_yesterday": companies_yesterday["count"],
    "companies_today": companies_today["count"],
    "emails_yesterday": emails_yesterday["count"],
    "emails_today": emails_today["count"]
}
```

### 3. Frontend Display (`/opt/contacts_api/static/admin-dashboard.html`)

**Updated to show breakdown for all three metrics:**
```javascript
// Companies
let companiesGrowth = `+${formatNumber(overview.companies_last_7_days)} this week`;
if (overview.companies_yesterday > 0) {
    companiesGrowth += `<br>+${formatNumber(overview.companies_yesterday)} yesterday`;
}
if (overview.companies_today > 0) {
    companiesGrowth += `<br>+${formatNumber(overview.companies_today)} today`;
}
document.getElementById('companies-growth').innerHTML = companiesGrowth;

// Emails (similar pattern)
let emailsGrowth = `+${formatNumber(overview.emails_last_7_days)} this week`;
if (overview.emails_yesterday > 0) {
    emailsGrowth += `<br>+${formatNumber(overview.emails_yesterday)} yesterday`;
}
if (overview.emails_today > 0) {
    emailsGrowth += `<br>+${formatNumber(overview.emails_today)} today`;
}
document.getElementById('emails-growth').innerHTML = emailsGrowth;
```

---

## ⚡ **Performance**

All queries use **index-only scans** and are very fast:

| Query | Time | Index Used |
|-------|------|------------|
| Persons (yesterday) | 18ms | `person_created_at_idx` |
| Companies (yesterday) | 5.8ms | `company_created_at_idx` |
| Emails (yesterday) | 7.4ms | `email_first_seen_at_idx` |
| **Total for 6 queries** | **~62ms** | **All indexed** |

**Page load:** Still instant despite 6 queries!

---

## 🎨 **Expected Display**

### **Total Persons Card:**
```
1,983,444
+59,747 this week
+10,022 yesterday
+143 today
```

### **Total Companies Card:**
```
680,798
+26,625 this week
+5,770 yesterday
+694 today
```

### **Total Emails Card:**
```
1,607,338
+59,733 this week
+10,008 yesterday
+1,369 today
```

---

## 📂 **Files Modified**

1. `/opt/contacts_api/app/main.py`
   - Added company and email count queries
   - Added 4 new fields to response

2. `/opt/contacts_api/static/admin-dashboard.html`
   - Updated companies and emails display logic
   - Changed from `textContent` to `innerHTML` for line breaks

3. **Database:**
   - Created `company_created_at_idx` on `core.company`
   - Created `email_first_seen_at_idx` on `core.email`

---

## ✅ **Backups Created**

- `/opt/contacts_api/app/main.py.backup_before_companies_emails_20260210_133419`
- `/opt/contacts_api/static/admin-dashboard.html.backup_before_companies_emails_20260210_133437`

---

## 🧪 **Testing Instructions**

1. **Refresh dashboard:** `Ctrl+Shift+R`
2. **URL:** https://leadsdatabase.cc/static/admin-dashboard.html
3. **Look for:** All three cards (Persons, Companies, Emails) should show 3-line breakdown

**Expected:**
- ✅ Week count (always shown)
- ✅ Yesterday count (if > 0)
- ✅ Today count (if > 0)

---

## 💡 **Key Implementation Notes**

1. **Emails use `first_seen_at`** instead of `created_at` (more accurate for when email was discovered)
2. **All queries use date ranges** instead of `DATE()` function (index-friendly)
3. **All timestamp columns indexed** for fast queries
4. **Counts only show if > 0** (today might be 0 early in the day)
5. **Performance maintained** despite 6 queries (~62ms total)

---

**Refresh your dashboard to see the full breakdown for all metrics!** 🚀
