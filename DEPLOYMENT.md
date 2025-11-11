# Deployment Guide - Streamlit Community Cloud

This guide explains how to deploy the Application Assistant to Streamlit Community Cloud so your friends can use it.

## Prerequisites

1. ✅ Supabase project created
2. ✅ Database tables created
3. ✅ Supabase URL and API key ready
4. ✅ GitHub repository with this code

## Step 1: Configure Supabase Email Authentication

Before deploying, enable email authentication in Supabase:

1. Go to your Supabase dashboard: https://supabase.com/dashboard
2. Select your project
3. Navigate to **Authentication** → **Providers** (left sidebar)
4. Find **Email** provider
5. Toggle it **ON** if not already enabled
6. Configure email templates (optional):
   - Go to **Authentication** → **Email Templates**
   - Customize the confirmation email if desired
   - For development, you can disable email confirmation (not recommended for production)

### Disable Email Confirmation (For Testing Only)

1. Go to **Authentication** → **Settings**
2. Under "Email Settings", toggle **OFF** the "Enable email confirmations" option
3. This allows users to sign up and log in immediately without email verification
4. **Important**: Re-enable this for production deployment!

## Step 2: Push Code to GitHub

1. Create a new GitHub repository
2. Push your code:

```bash
git init
git add .
git commit -m "Initial commit with Supabase integration"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## Step 3: Deploy to Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository
5. Set main file path: `app.py`
6. Click **"Advanced settings"**
7. Add secrets (see below)
8. Click **"Deploy"**

## Step 4: Configure Secrets

In the Advanced Settings → Secrets section, add:

```toml
# Supabase credentials
SUPABASE_URL = "your-supabase-url-here"
SUPABASE_KEY = "your-supabase-anon-key-here"

# Anthropic API key
ANTHROPIC_API_KEY = "your-anthropic-api-key-here"
```

**Get your actual values from:**
- **SUPABASE_URL**: Supabase Dashboard → Settings → API → Project URL
- **SUPABASE_KEY**: Supabase Dashboard → Settings → API → `anon` `public` key
- **ANTHROPIC_API_KEY**: Anthropic Console → API Keys

**Note**: You're sharing your Anthropic API key with friends. Consider:
- Setting up usage limits in your Anthropic account
- Monitoring usage regularly
- OR having each friend use their own API key (would require app modification)

## Step 5: Share with Friends

Once deployed, share the URL with your friends:
- URL format: `https://YOUR_APP_NAME.streamlit.app`
- Each friend will need to create their own account (email + password)
- Their data will be completely isolated from each other
- All resumes, cover letters, and ratings are private to each user

## Architecture Overview

**Multi-User Setup:**
- Supabase handles authentication (email/password)
- Row Level Security (RLS) ensures users only see their own data
- Each user has their own profile, resumes, cover letters, and ratings
- All data stored in PostgreSQL database (not local files)

**How It Works:**
1. User creates account → Supabase creates user record
2. User logs in → Session stored in Streamlit
3. User saves resume → Stored with their user_id
4. User generates cover letter → Can only access their own resumes
5. User logs out → Session cleared

## Monitoring & Maintenance

**Check Supabase Usage:**
1. Go to Supabase Dashboard → **Settings** → **Usage**
2. Free tier includes:
   - 500MB database storage
   - 50,000 monthly active users
   - 2GB bandwidth

**Check Anthropic API Usage:**
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. View **Usage** tab
3. Each cover letter costs ~$0.0004-0.0008

## Troubleshooting

**Users can't sign up:**
- Check Supabase email confirmation settings
- Verify SMTP settings if using custom email
- Check Supabase logs: **Logs** → **Postgres Logs**

**Users can see each other's data:**
- This shouldn't happen! Check RLS policies
- Go to **Database** → **Tables** → Select table → **Policies**
- Ensure policies match the SQL script from setup

**App is slow:**
- Check Streamlit Community Cloud resource usage
- Consider upgrading to paid Streamlit plan
- Optimize database queries if needed

## Optional: API Key Per User

If you want each friend to use their own Anthropic API key:

1. Add API key field to profile table
2. Modify generate_cover_letter() to use user's API key
3. Add UI field in sidebar for users to input their key
4. Store encrypted API keys in Supabase

This prevents you from paying for everyone's usage!

## Security Notes

- Never commit secrets to GitHub
- `.env` file is in `.gitignore`
- Secrets are only in Streamlit Cloud settings
- Supabase API key is "anon" key (safe for client-side use)
- RLS policies prevent unauthorized data access
- Consider enabling 2FA on your Supabase account

## Updating the Deployed App

To update after making changes:

1. Push changes to GitHub:
```bash
git add .
git commit -m "Description of changes"
git push
```

2. Streamlit will automatically redeploy
3. Check logs for any errors

That's it! Your Application Assistant is now live and multi-user ready!
