# Clay Integration Template - Outscraper Lean Endpoints

**Base URL:** `https://data.eagleinfoservice.com/api/v1/outscraper`

**Authentication:** Not required (internal use)

---

## 📋 Three Available Endpoints

### 1. Emails-Only Endpoint ⭐ **RECOMMENDED**

**Best for:** Email validation, simple email lookups

**Clay HTTP API Configuration:**
```
Method: GET
URL: https://data.eagleinfoservice.com/api/v1/outscraper/business/domain/emails-only?domain={{Company Domain}}
```

**Clay Field Mapping:**
```
businesses[0].email_1           → Primary Email
businesses[0].email_1_full_name → Contact Name (if available)
businesses[0].email_1_title     → Contact Title (if available)
businesses[0].email_1_phone      → Contact Phone (if available)
businesses[0].email_2            → Secondary Email (if available)
businesses[0].email_3            → Tertiary Email (if available)
businesses[0].name               → Company Name
businesses[0].site               → Website
count                            → Number of results (use in conditional logic)
```

**Response Example:**
```json
{
  "count": 1,
  "businesses": [
    {
      "id": 108,
      "name": "The Moon Café",
      "site": "https://www.themoonnoho.com/",
      "email_1": "themoonnoho@gmail.com"
    }
  ],
  "domain_query": "themoonnoho.com",
  "timestamp": "2026-02-04T07:15:00.000000"
}
```

**Key Features:**
- ✅ Returns ONLY email fields that have values (excludes null/empty fields)
- ✅ Dynamic response structure (adapts to available data)
- ✅ Returns `count: 0` if no emails found
- ✅ Cleanest output for Clay workflows

---

### 2. Contact-Info Endpoint

**Best for:** Basic outreach with phone numbers

**Clay HTTP API Configuration:**
```
Method: GET
URL: https://data.eagleinfoservice.com/api/v1/outscraper/business/domain/contact-info?domain={{Company Domain}}
```

**Additional Fields (beyond emails):**
- All phone numbers (phone, phone_1, phone_2, phone_3)
- Location (city, state, full_address)
- Category

---

### 3. Full-Profile Endpoint

**Best for:** Complete outreach campaigns with social media

**Clay HTTP API Configuration:**
```
Method: GET
URL: https://data.eagleinfoservice.com/api/v1/outscraper/business/domain/full-profile?domain={{Company Domain}}
```

**Additional Fields (beyond contact-info):**
- Social media: linkedin, facebook, instagram, twitter
- Business details: description, rating, reviews, type
- Extended address: postal_code

---

## 🔄 Clay Workflow Logic

### Handle No Results

**Conditional Logic in Clay:**
```
IF count == 0:
  → Log "No emails found for this domain"
  → Skip to next record
ELSE:
  → Import email fields
  → Continue with enrichment
```

### Handle Multiple Emails

The endpoint may return 1-3 emails. In Clay:

**Import Logic:**
```
Primary Email:   businesses[0].email_1
Secondary Email: businesses[0].email_2 (if present)
Tertiary Email:  businesses[0].email_3 (if present)
```

**Email Choice Logic:**
```
IF businesses[0].email_1 IS NOT EMPTY:
  → Use email_1 as primary
ELSE IF businesses[0].email_2 IS NOT EMPTY:
  → Use email_2 as primary
ELSE IF businesses[0].email_3 IS NOT EMPTY:
  → Use email_3 as primary
```

---

## 🧪 Test in Clay

### Test Domain (Has Email)
```
Domain: themoonnoho.com
Expected: Should return "themoonnoho@gmail.com"
Expected Count: 1
```

### Test Domain (No Email)
```
Domain: example.com
Expected: count: 0, businesses: []
```

### Test Domain (Multiple Emails)
```
Domain: ubereats.com
Expected: Multiple businesses with different emails
Expected Count: > 1
```

---

## ⚠️ Important Notes

1. **No Authentication Required:** API is open for internal use
2. **No Rate Limiting:** Currently none configured (internal use)
3. **Response Format:** JSON with consistent structure
4. **Empty Results:** Returns `{"count": 0, "businesses": []}` - NOT an error
5. **Smart Filtering:** Automatically excludes null/empty email fields
6. **Base Domain:** Use just the domain (e.g., "example.com", not "https://example.com")

---

## 🔧 Troubleshooting in Clay

### Issue: 404 Not Found

**Cause:** URL is incorrect

**Solution:**
- Ensure URL includes `/api/v1/outscraper` prefix
- Verify endpoint path is correct
- Example: `https://data.eagleinfoservice.com/api/v1/outscraper/business/domain/emails-only?domain=example.com`

### Issue: Empty Response (count: 0)

**Cause:** Domain not found in database or no emails exist

**Solution:**
- This is expected behavior
- Use conditional logic: `IF count > 0`
- Not an error condition

### Issue: No Email Fields Returned

**Cause:** Business has no emails in database

**Solution:**
- Check `count` field (should be 0)
- Move to next record in Clay workflow

---

## 📊 Data Reduction Comparison

| Endpoint | Fields | Original (111) | Reduction | Use Case |
|----------|--------|---------------|-----------|----------|
| Emails-only | 4-13* | 111 | 88-96% | Email validation ⭐ |
| Contact-info | ~23 | 111 | 77% | Basic outreach |
| Full-profile | ~33 | 111 | 64% | Full campaigns |

*Emails-only returns only the fields that have values (typically 4-6 fields instead of all 13)

---

## 🚀 Quick Start Copy-Paste

### For Clay HTTP API Enrichment (Emails-Only)

**Complete URL:**
```
https://data.eagleinfoservice.com/api/v1/outscraper/business/domain/emails-only?domain={{Your Domain Field}}
```

**Response Path:**
```
businesses[0].email_1
```

**Conditional Logic:**
```
IF {{count}} > 0:
  → Import businesses[0].email_1
  → Import businesses[0].name
  → Continue workflow
ELSE:
  → Log "No emails found"
  → Skip to next
```

---

## ✅ Verification Checklist

Before using in production Clay workflow:

- [ ] Test endpoint with: `domain=themoonnoho.com` (should return email)
- [ ] Test endpoint with: `domain=example.com` (should return count: 0)
- [ ] Verify response structure matches Clay field mapping
- [ ] Set up conditional logic for count == 0 (no results)
- [ ] Test email choice logic for multiple emails
- [ ] Verify error handling in Clay workflow

---

## 🎯 Best Practices

1. **Use Emails-Only First:** Start with the leanest endpoint, upgrade if needed
2. **Always Check Count:** Use `count > 0` before accessing business fields
3. **Handle Empty Results:** Expect count: 0 for domains without emails
4. **Extract Domain:** Ensure you're passing clean domain (e.g., "example.com")
5. **Test Edge Cases:** Test with domains that have no emails

---

## 📈 Performance Benefits

Using these endpoints in Clay:

- **Faster Processing:** 88-96% less data to parse
- **Cleaner JSON:** No null/empty fields to filter through
- **Dynamic Structure:** Only relevant data included
- **Consistent Format:** Predictable response structure
- **Reliable:** Built on proven Outscraper database (3M+ businesses)

---

## 📞 Support

For issues or questions:
- Check endpoint status: `https://data.eagleinfoservice.com/api/v1/outscraper/health`
- View API docs: `https://data.eagleinfoservice.com/api/v1/outscraper/docs`
- Test manually: Use curl examples above

---

**Template Created:** 2026-02-04
**Status:** ✅ Production Ready
**Authentication:** ❌ Not Required (Internal Use)
