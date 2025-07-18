# 🚀 Data Science Portfolio

A modern, responsive portfolio website showcasing data science projects with integrated Streamlit applications.

## 🌟 Features

- **Responsive Design**: Mobile-friendly with a dark theme inspired by Twitch
- **Dynamic Content**: Portfolio data loaded from `config.json`
- **Interactive Streamlit Apps**: Three sample applications demonstrating different data science concepts
- **Modern UI**: Clean animations and hover effects
- **GitHub Pages Ready**: Easy deployment with custom domain support

## 📁 Project Structure

```
├── index.html              # Main portfolio website
├── styles.css              # CSS styling with dark theme
├── script.js               # JavaScript for dynamic content loading
├── config.json             # Portfolio configuration and project data
├── CNAME                   # Custom domain configuration for GitHub Pages
├── streamlit_apps/         # Streamlit applications
│   ├── requirements.txt    # Python dependencies
│   ├── stock_dashboard/    # Stock price visualization app
│   │   └── app.py
│   ├── text_analyzer/      # Text sentiment analysis app
│   │   └── app.py
│   └── weather_predictor/  # Weather forecasting app
│       └── app.py
└── README.md               # This file
```

## 🎨 Design Theme

- **Background**: `#0e0e10` (Dark)
- **Primary Accent**: `#9146FF` (Twitch Purple)
- **Text**: `#f2f2f2` (Light Gray/White)
- **Font**: Inter (Google Fonts)

## 🛠️ Setup Instructions

### 1. Portfolio Website (GitHub Pages)

1. **Fork/Clone this repository**
2. **Edit `config.json`** with your personal information:
   ```json
   {
     "name": "Your Name",
     "bio": "Your bio description",
     "email": "your.email@example.com",
     "github": "https://github.com/yourusername",
     "linkedin": "https://linkedin.com/in/yourprofile",
     "projects": [...]
   }
   ```
3. **Update CNAME** with your domain name
4. **Enable GitHub Pages** in repository settings
5. **Configure DNS** (see Domain Setup section below)

### 2. Streamlit Apps Setup

1. **Create virtual environment**:
   ```bash
   python -m venv st_portfolio
   ```

2. **Activate virtual environment**:
   ```bash
   # Windows
   st_portfolio\Scripts\activate
   
   # macOS/Linux
   source st_portfolio/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r streamlit_apps/requirements.txt
   ```

4. **Run individual apps**:
   ```bash
   # Stock Dashboard
   streamlit run streamlit_apps/stock_dashboard/app.py --server.port 8501
   
   # Text Analyzer
   streamlit run streamlit_apps/text_analyzer/app.py --server.port 8502
   
   # Weather Predictor
   streamlit run streamlit_apps/weather_predictor/app.py --server.port 8503
   ```

## 🌐 Domain Setup with Porkbun

### Step 1: Configure DNS Records

In your Porkbun DNS management:

1. **Main Domain (abcd.com)**:
   - Type: `CNAME`
   - Host: `@` or leave blank
   - Answer: `yourusername.github.io`

2. **Streamlit Subdomains**:
   - Type: `CNAME`
   - Host: `stock`
   - Answer: `your-streamlit-hosting-service.com`
   
   - Type: `CNAME`
   - Host: `sentiment`
   - Answer: `your-streamlit-hosting-service.com`
   
   - Type: `CNAME`
   - Host: `weather`
   - Answer: `your-streamlit-hosting-service.com`

### Step 2: Deploy Streamlit Apps

You can deploy your Streamlit apps using several services:

#### Option 1: Streamlit Cloud (Recommended)
1. Push your apps to separate GitHub repositories
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy each app and get the URLs
4. Update DNS records to point subdomains to Streamlit Cloud

#### Option 2: Heroku
1. Create separate Heroku apps for each Streamlit app
2. Deploy using Git
3. Configure custom domains in Heroku
4. Update DNS records

#### Option 3: Railway/Render
1. Connect GitHub repositories
2. Deploy each app
3. Configure custom domains
4. Update DNS records

### Step 3: Update config.json

Update the project URLs in `config.json` to use your actual deployed URLs:

```json
{
  "projects": [
    {
      "title": "Stock Price Dashboard",
      "description": "...",
      "url": "https://stock.abcd.com"
    },
    {
      "title": "Text Sentiment Analyzer", 
      "description": "...",
      "url": "https://sentiment.abcd.com"
    },
    {
      "title": "Weather Predictor",
      "description": "...", 
      "url": "https://weather.abcd.com"
    }
  ]
}
```

## 📱 Sample Streamlit Apps

### 1. Stock Price Dashboard
- Interactive stock price visualization
- Mock data with realistic trends
- Multiple stock symbols
- Charts and metrics

### 2. Text Sentiment Analyzer
- Word-based sentiment analysis
- Word frequency visualization
- Text statistics
- Sample text examples

### 3. Weather Predictor
- Mock weather forecasting
- Multiple cities
- Historical and predicted data
- Interactive charts

## 🔧 Customization

### Adding New Projects
1. Update `config.json` with new project details
2. The website will automatically display the new project

### Modifying Design
- Edit `styles.css` for visual changes
- Modify `script.js` for functionality updates
- Update `index.html` for structural changes

### Creating New Streamlit Apps
1. Create new folder in `streamlit_apps/`
2. Add `app.py` with your Streamlit code
3. Update `requirements.txt` if needed
4. Deploy and update `config.json`

## 🚀 Deployment Checklist

- [ ] Repository created and configured
- [ ] `config.json` updated with personal information
- [ ] GitHub Pages enabled
- [ ] Custom domain configured in repository settings
- [ ] DNS records added in Porkbun
- [ ] Streamlit apps deployed to hosting service
- [ ] Subdomain DNS records pointing to Streamlit hosting
- [ ] All URLs in `config.json` updated
- [ ] Website tested and functional

## 📝 License

MIT License - Feel free to use this template for your own portfolio!

## 🤝 Contributing

Suggestions and improvements are welcome! Please feel free to submit issues or pull requests.

---

**Note**: This is a template portfolio with sample Streamlit applications. Replace the sample apps with your actual data science projects to showcase your real work. 