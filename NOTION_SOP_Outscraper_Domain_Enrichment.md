# Outscraper Domain Enrichment SOP

**Created by:** Claude Code

### **Creation Date:** 02/04/2026

### **Updated Date:** 02/04/2026

---

### **Overview**

- **WHAT**

    This SOP explains how to enrich business domains with email addresses and contact information using our internal Outscraper database (3M+ businesses) via Clay’s HTTP API integration.

- **WHY**

    Quickly find verified business emails without manual research. Pull contact data, phone numbers, and social media links for outreach campaigns.

- **WHEN**

    Use when you have a list of company domains and need to find business emails, contact names, or company details. Run before launching outreach campaigns.


---

### **Video**

---

### **Resources Needed**

- Clay workspace access
- Table containing **domains** you want to enrich (e.g., `example.com`, not `https://example.com`)
- Internet connection

---

### **General Guidelines**

- Use clean domain names only (e.g., `example.com`, not `https://www.example.com/`)
- If your table has more than 1,000 rows, split into smaller batches
- Always check the `count` field before accessing business data
- Domains without emails will return `count: 0` (this is expected)
- No authentication or API key required

---

### **Step-by-Step Instructions**

### **1. Open the Target Table**

- In Clay, open the table containing **domains** you want to enrich.
- Ensure you have a column with clean domain values (e.g., `themoonnoho.com`, `google.com`).

---

### **2. Add a New Enrichment Column**

- Click **"+ Add Column"**.
- Search for **"HTTP API"**.
- Select **"HTTP API"** from the options.

---

### **3. Configure the HTTP API**

- Click **"Configure"** at the top of the enrichment setup panel.

![HTTP API Configure](https://via.placeholder.com/400x200?text=Configure+Button)

---

### **4. Set Up the Inputs**

- Under **Method**, choose **GET**.

### **Choose your endpoint based on data needed:**

---

### **Option A: Get Emails Only** ⭐ **RECOMMENDED**

**Best for:** Email validation, quick email lookup

**Endpoint:**
```
https://data.eagleinfoservice.com/api/v1/outscraper/business/domain/emails-only
```

**Query Parameters:**
- **Key:** `domain`
- **Value:** Select your **Domain** column

![Query Parameters](https://via.placeholder.com/600x150?text=Query+Parameters)

**Expected Output:**
```json
{
  "count": 1,
  "businesses": [{
    "name": "The Moon Café",
    "email_1": "themoonnoho@gmail.com",
    "email_1_full_name": "John Doe",
    "email_1_title": "Manager"
  }]
}
```

**Features:**
- Returns ONLY email fields that have values (no empty/null fields)
- Returns up to 3 emails per business with contact details
- Lightest response (88% less data than full endpoint)

---

### **Option B: Get Contact Info**

**Best for:** Basic outreach with phone numbers

**Endpoint:**
```
https://data.eagleinfoservice.com/api/v1/outscraper/business/domain/contact-info
```

**Query Parameters:**
- **Key:** `domain`
- **Value:** Select your **Domain** column

**Expected Output:**
```json
{
  "count": 1,
  "businesses": [{
    "name": "The Moon Café",
    "email_1": "themoonnoho@gmail.com",
    "phone": "+1234567890",
    "city": "Los Angeles",
    "state": "CA",
    "category": "Coffee Shop"
  }]
}
```

**Includes:**
- All email fields
- All phone numbers
- Location data (city, state, address)
- Business category

---

### **Option C: Get Full Profile**

**Best for:** Complete outreach with social media

**Endpoint:**
```
https://data.eagleinfoservice.com/api/v1/outscraper/business/domain/full-profile
```

**Query Parameters:**
- **Key:** `domain`
- **Value:** Select your **Domain** column

**Expected Output:**
```json
{
  "count": 1,
  "businesses": [{
    "name": "The Moon Café",
    "email_1": "themoonnoho@gmail.com",
    "phone": "+1234567890",
    "linkedin": "linkedin.com/in/themooncafe",
    "facebook": "facebook.com/themooncafe",
    "description": "Artisan coffee shop",
    "rating": 4.7,
    "reviews": 342
  }]
}
```

**Includes:**
- All contact info
- Social media links (LinkedIn, Facebook, Instagram, Twitter)
- Business details (description, rating, reviews)
- Full address information

---

### **5. Save and Run Enrichment**

- Click **Save** to confirm configuration.
- Run enrichment for all rows.
- Expect **Status Code: 200** for successful requests.

---

### **6. Working With Output**

- Click on any **output cell** in the HTTP API column.
- On the right-hand panel, you'll see the returned JSON structure.

**To extract specific fields:**
- Find the field you want (e.g., `email_1`, `name`, `phone`).
- Click **"Add as column"** next to it.
- Clay will create a new column with that value populated.

![Add as Column](https://via.placeholder.com/400x200?text=Add+as+Column)

**Available Fields (Option A - Emails Only):**
```
count                  → Number of businesses found
businesses[0].name     → Company name
businesses[0].email_1  → Primary email
businesses[0].email_2  → Secondary email (if exists)
businesses[0].email_3  → Tertiary email (if exists)
businesses[0].site     → Website
```

**Available Fields (Option B - Contact Info):**
```
businesses[0].phone        → Main phone number
businesses[0].city         → City
businesses[0].state        → State
businesses[0].full_address → Full address
businesses[0].category     → Business category
```

**Available Fields (Option C - Full Profile):**
```
businesses[0].linkedin    → LinkedIn URL
businesses[0].facebook    → Facebook URL
businesses[0].instagram   → Instagram URL
businesses[0].twitter     → Twitter URL
businesses[0].rating     → Google rating
businesses[0].reviews     → Number of reviews
businesses[0].description → Business description
```

---

### **7. Handle No Results**

**When `count` is 0:**
- This means no emails were found for that domain
- The `businesses` array will be empty: `[]`
- This is **not an error** - it's expected behavior

**In Clay:**
- Use conditional logic: `IF count > 0`
- Skip rows where no data is available
- Do not attempt to access `businesses[0]` when count is 0

---

### **8. Handle Multiple Businesses**

- Some domains may return multiple businesses (e.g., franchises, multiple locations).
- Check the `count` field to see how many businesses were returned.
- Access each business using array notation:
  - `businesses[0].email_1` → First business
  - `businesses[1].email_1` → Second business
  - `businesses[2].email_1` → Third business

**To flatten into separate rows:**
- Click on the HTTP API column cell.
- Find the `businesses` key.
- Click dropdown → **"Take action on list"** → **"Write each item to new row in other table."**
- Create a new table for flattened results.

---

### **9. Final Review**

- Verify email fields are populated correctly
- Check that `count` matches expected number of results
- Remove any test rows or incomplete data
- Export cleaned data for outreach campaigns

---

### **10. Troubleshooting**

**Issue:** Status code 404
- **Cause:** Incorrect URL
- **Fix:** Ensure URL includes `/api/v1/outscraper` prefix

**Issue:** Returns `count: 0` for known domains
- **Cause:** Domain not in database or no emails exist
- **Solution:** Expected behavior - try different domain variation

**Issue:** No email fields returned
- **Cause:** Business has no emails in database
- **Solution:** Check `count` field (should be 0), skip to next row

**Issue:** Returns all 111 fields instead of filtered results
- **Cause:** Using wrong endpoint
- **Fix:** Ensure you're using `/domain/emails-only` (not `/business/by-domain`)

**Issue:** Returns empty email fields (null values)
- **Cause:** This shouldn't happen with emails-only endpoint
- **Fix:** Email-only endpoint automatically filters null fields

---

### **Endpoint Comparison**

| Endpoint | Use Case | Data Returned | Best For |
|----------|----------|---------------|----------|
| `/emails-only` | Quick email lookup | 4-13 fields | Email validation ⭐ |
| `/contact-info` | Outreach prep | ~23 fields | Phone + location |
| `/full-profile` | Full research | ~33 fields | Social media + details |

---

### **Test Domains**

Use these to test your setup:

**Has Email:**
```
themoonnoho.com
Expected: 1 business with email
```

**No Email:**
```
example.com
Expected: count: 0, businesses: []
```

**Multiple Businesses:**
```
ubereats.com
Expected: count > 1, multiple businesses
```

---

**End of SOP**
