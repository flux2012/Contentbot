# AI Content Pipeline — Setup Guide (Step by Step)

Ye system rozana khud script likhega, video banaayega, aur Instagram + YouTube par post karega — poori tarah free.

## Kaise kaam karega (overview)
Har din GitHub ka server (free) apne aap jaagega, ek naya video banaayega, aur post kar dega. Aapka computer on rakhne ki zarurat nahi.

## Setup Steps

### 1. GitHub account aur repo
1. https://github.com par free account banaaiye (agar nahi hai).
2. Naya **private repository** banaaiye, naam kuch bhi rakh sakte hain (e.g. `content-bot`).
3. Is poore folder (`ai-content-pipeline`) ka saara content us repo mein upload kar dijiye
   (GitHub website par "Add file -> Upload files" se bhi ho jaata hai, koi command line zaroori nahi).

### 2. Gemini API key (script likhne ke liye) — FREE
1. https://aistudio.google.com/app/apikey par jaaiye, Google account se login kijiye.
2. "Create API Key" par click kijiye, key copy kar lijiye.
3. Apne GitHub repo mein: **Settings -> Secrets and variables -> Actions -> New repository secret**
   - Name: `GEMINI_API_KEY`
   - Value: (jo key copy ki thi)

### 3. YouTube setup — FREE (thoda lamba hai, ek baar hi karna hai)
1. https://console.cloud.google.com par ek naya project banaaiye.
2. "APIs & Services -> Library" mein jaakar **YouTube Data API v3** ko enable kijiye.
3. "APIs & Services -> Credentials -> Create Credentials -> OAuth client ID" chuniye,
   type: **Desktop app**. Download button se `client_secret.json` download kijiye.
4. Apne computer par (GitHub par nahi) ye file `ai-content-pipeline` folder mein rakhiye.
5. Apne computer par terminal khol kar chalaaiye:
   ```
   pip install google-auth-oauthlib
   python src/get_youtube_token.py
   ```
   Ye browser kholega, apne us YouTube channel se login kijiye jahan post karna hai, allow kijiye.
   Iske baad `token.json` file ban jaayegi.
6. `token.json` file ka poora content copy kijiye, GitHub Secret banaaiye:
   - Name: `YOUTUBE_TOKEN_JSON`
   - Value: (poora JSON content paste kar dijiye)

### 4. Instagram setup — FREE
1. Apna Instagram account app mein jaakar **Professional Account (Business/Creator)** mein badaliye
   (Settings -> Account type).
2. Facebook par ek Page banaaiye (agar nahi hai), aur usse apne Instagram se link kijiye
   (Instagram Settings -> Linked Accounts -> Facebook).
3. https://developers.facebook.com par jaakar login kijiye, "My Apps -> Create App" -> type **Business**.
4. App ke andar "Add Product -> Instagram Graph API" add kijiye.
5. Graph API Explorer (developers.facebook.com/tools/explorer) se apna Page Access Token
   aur Instagram Business Account ID nikaaliye (Meta ke docs is link par step-by-step hain:
   https://developers.facebook.com/docs/instagram-api/getting-started).
6. GitHub Secrets banaaiye:
   - Name: `IG_ACCESS_TOKEN`, Value: (page access token)
   - Name: `IG_ACCOUNT_ID`, Value: (instagram business account id)

### 5. Bas ho gaya!
- Pipeline automatically har roz chalega (workflow file mein time set hai, chaho to badal sakte ho).
- Manually turant test karne ke liye: apne GitHub repo mein **Actions tab -> Daily AI Content Pipeline -> Run workflow** par click kijiye.
- Agar kahin error aaye, Actions tab mein us run par click karke poora log dikh jaayega — vo error mujhe (Claude ko) copy-paste kar dijiye, main fix bata dunga.

## Content niche badalna
`.github/workflows/daily_post.yml` file mein `CONTENT_NICHE` line ko edit kar dijiye —
jaise "personal finance tips", "interesting science facts", "startup advice" — jo bhi topic chaahiye.

## Kharcha
Sab kuchh free tier mein hai. Sirf itna dhyaan rakhiye:
- Gemini free tier: roz kuch requests free hain (ek video/din ke liye kaafi hai)
- GitHub Actions: private repo mein 2000 free minutes/month milte hain, ye pipeline ek run mein ~5 minute leta hai
- YouTube API: free daily quota hai, ek video/din aasani se aa jaata hai
