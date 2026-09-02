# Abdul Noman — Daily Job Search & Auto-Apply Agent

Har roz khud-ba-khud UK, USA, Canada, aur remote-friendly (UAE/Portugal covering)
jobs dhoondta hai, aap ki CV se match karta hai, jahan email se apply hoti hai
wahan khud application bhej deta hai, aur baaki jobs ek "ready to click" list
mein email + WhatsApp pe bhej deta hai.

**Koi coding zaroori nahi** — bas neeche diye steps follow karein.

---

## Ye system kya karta hai (aur kya NAHI karta)

✅ Roz Adzuna (UK/US/Canada), Remotive, RemoteOK, aur Arbeitnow se naye jobs
   fetch karta hai
✅ Aap ki asal skills (graphic design, embroidery digitizing, web development)
   se match karta hai
✅ Jahan job posting mein seedha "apply by email" diya ho, wahan khud ek
   tailored application email + CV bhej deta hai
✅ Baaki jobs (jo LinkedIn/Indeed/company-portal jaisi cheez pe apply hoti hain)
   ek daily email + WhatsApp message mein bhej deta hai, ek click ke saath
✅ Purani/dohrai hui jobs dobara nahi bhejta

❌ LinkedIn ya Indeed pe **khud se login karke apply nahi karta** — ye dono
   platforms bots ko detect karke account ban kar dete hain, is liye jaan-boojh
   kar chhoda gaya hai. In jobs ke links aap ko email/WhatsApp mil jayenge,
   ek click mein aap khud apply kar lein.

---

## Setup — Step by Step

### 1. Ye folder GitHub pe daalein
1. github.com pe login karein, naya **private** repository banayein (jaise `job-search-agent`)
2. Is poore folder (`job-auto-apply`) ko us repository mein upload kar dein —
   ya to GitHub web interface se ("uploading an existing file") ya git command line se:
   ```
   git init
   git add .
   git commit -m "first version"
   git branch -M main
   git remote add origin https://github.com/<aapka-username>/job-search-agent.git
   git push -u origin main
   ```

### 2. Adzuna API key lein (UK/USA/Canada jobs ke liye — free)
1. https://developer.adzuna.com/ pe jayein, free account banayein
2. Dashboard mein **App ID** aur **App Key** milega — dono copy kar lein

### 3. Gmail App Password banayein (applications bhejne ke liye)
Normal Gmail password kaam nahi karega — Google alag se ek "App Password" mangta hai:
1. `abdulnoman2026@gmail.com` mein 2-Step Verification on karein (agar nahi hai):
   myaccount.google.com/security
2. Phir myaccount.google.com/apppasswords pe jayein
3. "App name" mein kuch bhi likh dein (jaise "job agent"), Generate dabayein
4. 16-digit code milega — yehi hai apka `GMAIL_APP_PASSWORD`

### 4. WhatsApp notification setup (CallMeBot — free, 1-time)
1. Apne phone se is number ko WhatsApp message bhejein: **+34 644 59 71 67**
2. Message ye likhein: `I allow callmebot to send me messages`
3. Jawab mein ek **API Key** milega — wahi copy kar lein
4. `WHATSAPP_PHONE` = apka number country code ke saath (jaise `+923352646059`)

### 5. (Optional lekin recommended) Anthropic API key
Isse har job ke liye AI khud ek specific, personalized ek-line pitch aur
application email likhta hai — na ho to bhi system chalega, bas thoda generic
likha jayega.
1. https://console.anthropic.com/ pe account banayein
2. API key generate karein

### 6. GitHub mein Secrets add karein
Apni repository mein: **Settings → Secrets and variables → Actions → New repository secret**

Ye sab add karein (naam bilkul yehi rakhein):

| Secret name | Value |
|---|---|
| `ADZUNA_APP_ID` | Step 2 se |
| `ADZUNA_APP_KEY` | Step 2 se |
| `GMAIL_ADDRESS` | `abdulnoman2026@gmail.com` |
| `GMAIL_APP_PASSWORD` | Step 3 se (16-digit code) |
| `WHATSAPP_PHONE` | Apka number, jaise `+923352646059` |
| `CALLMEBOT_APIKEY` | Step 4 se |
| `ANTHROPIC_API_KEY` | Step 5 se (optional) |

### 7. Test karein
1. Repository ke **Actions** tab mein jayein
2. "Daily Job Search" workflow select karein
3. **Run workflow** button dabayein — turant chala kar dekh sakte hain, roz ka
   wait nahi karna padega
4. 1-2 minute mein `abdulnoman2026@gmail.com` pe ek summary email aani chahiye,
   aur WhatsApp pe bhi ek message

Agar kuch fail ho to Actions tab mein us run ke andar poora log dikh jayega —
wo error message mujhe bhi bhej dein, theek kar dunga.

---

## Roz ye khud kab chalega?

Har roz **subah 10:00 AM (Pakistan time)** apne aap chal jayega — koi PC on
rakhne ki zaroorat nahi. Time badalna ho to
`.github/workflows/daily-job-search.yml` file mein `cron: "0 5 * * *"` wali
line edit kar dein (ye UTC time hai).

---

## Roz kya settings badal sakte hain

`scripts/config.py` file mein:
- `SEARCH_TERMS` — kaunse roles dhoonde (design, web dev, embroidery, etc.)
- `SKILL_KEYWORDS` — matching ke liye kaunse keywords use hon
- `MIN_SCORE_TO_KEEP` — kitna match hone par job list mein aaye
- `MAX_JOBS_PER_RUN` — ek din mein zyada se zyada kitni jobs process hon

Koi bhi cheez badal kar bas file save karein aur GitHub pe upload kar dein —
agli run se naya rule lagu ho jayega.

---

## Aage kya add ho sakta hai (V2 ideas)

- Greenhouse/Lever jaisi common ATS websites ke liye pura auto-fill-and-submit
  (in ki form structure fixed hoti hai isliye safe automation possible hai)
- Dubai/UAE-specific job boards jab koi public API mile
- Har application ka apna tracking dashboard (jaisa portfolio admin tool hai)
