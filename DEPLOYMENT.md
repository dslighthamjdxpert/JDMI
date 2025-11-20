# Job IQ Assessment Tool - Deployment Guide

## Quick Deploy to Streamlit Cloud (Recommended)

Streamlit Cloud is the easiest way to deploy this app. It's **free** for public apps and handles all infrastructure.

### Step 1: Prepare GitHub Repository

1. **Create a GitHub repository** (if you haven't already):
   ```bash
   cd /Users/dslightham/Library/CloudStorage/Dropbox/4_Utility/CODE/JDX
   git init
   git add 2_Tactics/Campaigns/JDX_SkillsGov_Campaign_2025Q4/JobIQ/Streamlit/
   git commit -m "Add Job IQ assessment tool"
   ```

2. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_ORG/jdx-campaign.git
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**

2. **Sign in with GitHub**

3. **Click "New app"**

4. **Configure deployment**:
   - **Repository**: Select your GitHub repo
   - **Branch**: `main`
   - **Main file path**: `2_Tactics/Campaigns/JDX_SkillsGov_Campaign_2025Q4/JobIQ/Streamlit/app.py`
   - **App URL** (optional): Choose a custom subdomain (e.g., `jdx-jobiq-assessment`)

5. **Click "Deploy"**

6. **Wait 2-3 minutes** for the app to build and launch

7. **Your app is live!** You'll get a URL like:
   ```
   https://jdx-jobiq-assessment.streamlit.app
   ```

### Step 3: Configure Custom Domain (Optional)

1. **In Streamlit Cloud app settings**:
   - Go to **Settings** → **Domains**
   - Add custom domain: `assessment.jdxpert.com`

2. **Update DNS records** (with your domain provider):
   - Add CNAME record:
     ```
     assessment.jdxpert.com  →  jdx-jdmi-assessment.streamlit.app
     ```

3. **SSL certificate** is automatically provisioned

---

## Alternative: Deploy to Production Server

If you need more control, deploy to your own server.

### Option A: Docker Deployment

1. **Create `Dockerfile`** (in Streamlit folder):
   ```dockerfile
   FROM python:3.10-slim

   WORKDIR /app

   # Install dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application files
   COPY . .

   # Expose Streamlit port
   EXPOSE 8501

   # Health check
   HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

   # Run the app
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build Docker image**:
   ```bash
   cd /path/to/JobIQ/Streamlit
   docker build -t jobiq-assessment:latest .
   ```

3. **Run container**:
   ```bash
   docker run -d \
     --name jdmi-app \
     -p 8501:8501 \
     --restart unless-stopped \
     jobiq-assessment:latest
   ```

4. **Access app** at `http://your-server-ip:8501`

### Option B: AWS EC2 Deployment

1. **Launch EC2 instance**:
   - AMI: Amazon Linux 2 or Ubuntu 22.04
   - Instance type: t3.small (2 vCPU, 2GB RAM)
   - Security group: Allow port 8501 (or 80/443 with reverse proxy)

2. **SSH into instance**:
   ```bash
   ssh -i your-key.pem ec2-user@your-instance-ip
   ```

3. **Install dependencies**:
   ```bash
   sudo yum update -y
   sudo yum install python3 python3-pip git -y
   ```

4. **Clone your repository**:
   ```bash
   git clone https://github.com/YOUR_ORG/jdx-campaign.git
   cd jdx-campaign/2_Tactics/Campaigns/JDX_SkillsGov_Campaign_2025Q4/Streamlit
   ```

5. **Install Python packages**:
   ```bash
   pip3 install -r requirements.txt
   ```

6. **Run with systemd** (persistent service):
   
   Create `/etc/systemd/system/jdmi.service`:
   ```ini
   [Unit]
   Description=JDMI Assessment Tool
   After=network.target

   [Service]
   Type=simple
   User=ec2-user
   WorkingDirectory=/home/ec2-user/jdx-campaign/.../Streamlit
   ExecStart=/usr/local/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable jdmi
   sudo systemctl start jdmi
   sudo systemctl status jdmi
   ```

7. **Set up Nginx reverse proxy** (optional, for HTTPS):
   ```bash
   sudo yum install nginx certbot python3-certbot-nginx -y
   ```

   Configure `/etc/nginx/conf.d/jdmi.conf`:
   ```nginx
   server {
       listen 80;
       server_name assessment.jdxpert.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

   Enable HTTPS:
   ```bash
   sudo certbot --nginx -d assessment.jdxpert.com
   ```

### Option C: Heroku Deployment

1. **Install Heroku CLI**:
   ```bash
   brew install heroku/brew/heroku
   heroku login
   ```

2. **Create `Procfile`** (in Streamlit folder):
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

3. **Create `.streamlit/config.toml`**:
   ```toml
   [server]
   headless = true
   enableCORS = false
   port = $PORT
   ```

4. **Deploy**:
   ```bash
   cd /path/to/JobIQ/Streamlit
   heroku create jdx-jobiq-assessment
   git init
   git add .
   git commit -m "Deploy Job IQ assessment"
   git push heroku main
   ```

5. **Open app**:
   ```bash
   heroku open
   ```

---

## Post-Deployment Checklist

### 1. Test Core Functionality
- [ ] Assessment form loads correctly
- [ ] All 7 dimensions are scoreable
- [ ] Scores calculate correctly
- [ ] Radar chart displays
- [ ] Recommendations generate
- [ ] "Retake Assessment" resets form

### 2. Customize Branding
- [ ] Replace placeholder logo in sidebar
- [ ] Update contact links (email, booking URL)
- [ ] Customize color scheme in CSS
- [ ] Update footer company name

### 3. Analytics Setup (Optional)
- [ ] Add Google Analytics tracking code
- [ ] Set up conversion tracking for "Schedule Consultation" clicks
- [ ] Track assessment completion rate

### 4. SEO & Marketing
- [ ] Set page title and meta description
- [ ] Add Open Graph tags for social sharing
- [ ] Create short URL (e.g., `jdx.link/assess`)
- [ ] Add UTM parameters for campaign tracking

### 5. Monitoring
- [ ] Set up uptime monitoring (e.g., Pingdom, UptimeRobot)
- [ ] Configure error logging (Streamlit Cloud has built-in logs)
- [ ] Test mobile responsiveness

---

## Environment Variables (if needed)

If you add backend integrations (API, CRM, email), use environment variables:

### Streamlit Cloud:
1. Go to app settings
2. Add secrets in `.streamlit/secrets.toml` format:
   ```toml
   API_KEY = "your-api-key"
   CRM_ENDPOINT = "https://api.hubspot.com/..."
   ```

### Docker/Server:
Pass as environment variables:
```bash
docker run -d \
  -e API_KEY="your-api-key" \
  -e CRM_ENDPOINT="https://..." \
  -p 8501:8501 \
  jdmi-assessment:latest
```

---

## Troubleshooting

### App won't start
- Check logs: `streamlit run app.py --logger.level=debug`
- Verify Python version: `python3 --version` (need 3.8+)
- Reinstall dependencies: `pip install --force-reinstall -r requirements.txt`

### Charts not rendering
- Clear browser cache
- Check Plotly version: `pip show plotly`
- Test in incognito mode

### Slow performance
- Increase Streamlit Cloud resources (upgrade plan)
- Add caching decorators: `@st.cache_data`
- Optimize radar chart rendering

### Session state errors
- Add `st.session_state` initialization checks
- Clear browser cookies
- Restart Streamlit: `Ctrl+C` then `streamlit run app.py`

---

## Scaling Considerations

### For High Traffic (1000+ users/day)

1. **Use Redis for session state**:
   ```bash
   pip install streamlit-redis
   ```

2. **Add caching layer**:
   ```python
   @st.cache_data(ttl=3600)
   def get_recommendations(scores, level):
       # ...
   ```

3. **Consider API-based architecture**:
   - Move scoring logic to backend API (FastAPI, Flask)
   - Streamlit frontend → API backend
   - Scale API independently

4. **Database for assessment storage**:
   - Store responses in PostgreSQL/MongoDB
   - Build admin dashboard for analytics

---

## Maintenance

### Regular Updates

1. **Update dependencies monthly**:
   ```bash
   pip install --upgrade streamlit plotly pandas
   pip freeze > requirements.txt
   ```

2. **Refresh benchmark data** (quarterly):
   - Update `BENCHMARK_DIMENSION_SCORES` in `config.py`
   - Recalculate averages from latest research

3. **Monitor user feedback**:
   - Track "Schedule Consultation" conversion rate
   - A/B test question wording
   - Iterate on recommendations

### Backup Strategy

- **Code**: Stored in GitHub (version controlled)
- **Assessment data** (if collected): Daily backup to S3 or DB backup
- **Secrets**: Store in password manager (1Password, LastPass)

---

## Support

For deployment issues:
- **Streamlit Community**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues**: [Create issue in your repo]
- **JDX Tech Team**: [your-tech-email@jdxpert.com]

---

**Last Updated**: November 2025  
**Framework Version**: Job IQ v1.0

