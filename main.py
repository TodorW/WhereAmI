import requests
import time
from urllib.parse import quote

class SuperEmailChecker:
    def __init__(self, email):
        self.email = email
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def check_site(self, site_name, url, success_codes=[200], method='get'):
        """Generic site checking function"""
        try:
            if method == 'get':
                response = self.session.get(url, timeout=8, allow_redirects=False)
            else:
                response = self.session.head(url, timeout=8, allow_redirects=False)
            
            if response.status_code in success_codes:
                return "✓ Possible account exists"
            elif response.status_code == 404:
                return "✗ No account found"
            else:
                return f"? Status: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "⏰ Timeout"
        except requests.exceptions.ConnectionError:
            return "🔌 Connection failed"
        except requests.exceptions.RequestException:
            return "❌ Request failed"
        except Exception as e:
            return f"⚠️ Error: {str(e)}"
    
    def run_mega_check(self):
        """Check hundreds of popular sites"""
        sites = {
            # 🔐 Social Media
            "Facebook": f"https://www.facebook.com/{quote(self.email)}",
            "Twitter/X": f"https://twitter.com/{quote(self.email)}", 
            "Instagram": f"https://www.instagram.com/{quote(self.email)}",
            "LinkedIn": f"https://www.linkedin.com/in/{quote(self.email)}",
            "Pinterest": f"https://www.pinterest.com/{quote(self.email)}/",
            "TikTok": f"https://www.tiktok.com/@{quote(self.email)}",
            "Snapchat": f"https://www.snapchat.com/add/{quote(self.email)}",
            "Reddit": f"https://www.reddit.com/user/{quote(self.email)}",
            "Tumblr": f"https://{quote(self.email)}.tumblr.com/",
            "VK": f"https://vk.com/{quote(self.email)}",
            "Weibo": f"https://weibo.com/{quote(self.email)}",
            
            # 💼 Professional
            "GitHub": f"https://github.com/{quote(self.email)}",
            "GitLab": f"https://gitlab.com/{quote(self.email)}",
            "Bitbucket": f"https://bitbucket.org/{quote(self.email)}/",
            "StackOverflow": f"https://stackoverflow.com/users/{quote(self.email)}",
            "Dribbble": f"https://dribbble.com/{quote(self.email)}",
            "Behance": f"https://www.behance.net/{quote(self.email)}",
            "Medium": f"https://medium.com/@{quote(self.email)}",
            "Dev.to": f"https://dev.to/{quote(self.email)}",
            
            # 🎬 Video & Streaming
            "YouTube": f"https://www.youtube.com/@{quote(self.email)}",
            "Twitch": f"https://www.twitch.tv/{quote(self.email)}",
            "Vimeo": f"https://vimeo.com/{quote(self.email)}",
            "Dailymotion": f"https://www.dailymotion.com/{quote(self.email)}",
            "Netflix": "https://www.netflix.com/",  # Can't check directly
            "Spotify": f"https://open.spotify.com/user/{quote(self.email)}",
            "SoundCloud": f"https://soundcloud.com/{quote(self.email)}",
            
            # 📧 Email Providers
            "Gmail": "https://mail.google.com/",  # Can't check directly
            "Outlook": "https://outlook.live.com/",
            "Yahoo Mail": "https://mail.yahoo.com/",
            "ProtonMail": "https://mail.protonmail.com/",
            
            # 🛒 E-commerce
            "Amazon": "https://www.amazon.com/",  # Can't check directly
            "eBay": f"https://www.ebay.com/usr/{quote(self.email)}",
            "Etsy": f"https://www.etsy.com/people/{quote(self.email)}",
            "Shopify": "https://www.shopify.com/",
            
            # 📚 Education
            "Coursera": "https://www.coursera.org/",
            "Udemy": "https://www.udemy.com/",
            "Khan Academy": "https://www.khanacademy.org/",
            "EdX": "https://www.edx.org/",
            
            # 💰 Finance
            "PayPal": "https://www.paypal.com/",  # Can't check directly
            "Venmo": f"https://venmo.com/{quote(self.email)}",
            "CashApp": "https://cash.app/",
            "Robinhood": "https://robinhood.com/",
            
            # 🎮 Gaming
            "Steam": f"https://steamcommunity.com/id/{quote(self.email)}",
            "Epic Games": "https://www.epicgames.com/",
            "Xbox Live": "https://www.xbox.com/",
            "PlayStation": "https://www.playstation.com/",
            "Discord": f"https://discord.com/users/{quote(self.email)}",
            "Roblox": f"https://www.roblox.com/user.aspx?username={quote(self.email)}",
            
            # 📷 Photo
            "Flickr": f"https://www.flickr.com/people/{quote(self.email)}",
            "500px": f"https://500px.com/{quote(self.email)}",
            "Imgur": f"https://imgur.com/user/{quote(self.email)}",
            "VSCO": f"https://vsco.co/{quote(self.email)}",
            
            # 🏃‍♂️ Health & Fitness
            "Strava": f"https://www.strava.com/athletes/{quote(self.email)}",
            "Fitbit": "https://www.fitbit.com/",
            "MyFitnessPal": f"https://www.myfitnesspal.com/{quote(self.email)}",
            
            # 🎵 Music
            "Last.fm": f"https://www.last.fm/user/{quote(self.email)}",
            "Pandora": "https://www.pandora.com/",
            "Bandcamp": f"https://bandcamp.com/{quote(self.email)}",
            
            # ✈️ Travel
            "TripAdvisor": f"https://www.tripadvisor.com/members/{quote(self.email)}",
            "Airbnb": f"https://www.airbnb.com/users/show/{quote(self.email)}",
            "Booking.com": "https://www.booking.com/",
            "Uber": "https://www.uber.com/",
            "Lyft": "https://www.lyft.com/",
            
            # 🍕 Food
            "Uber Eats": "https://www.ubereats.com/",
            "DoorDash": "https://www.doordash.com/",
            "Grubhub": "https://www.grubhub.com/",
            "Yelp": f"https://www.yelp.com/user_details?userid={quote(self.email)}",
            
            # 📰 News
            "Quora": f"https://www.quora.com/profile/{quote(self.email)}",
            "Flipboard": f"https://flipboard.com/@{quote(self.email)}",
            
            # 🔧 Development
            "npm": f"https://www.npmjs.com/~{quote(self.email)}",
            "Docker Hub": f"https://hub.docker.com/u/{quote(self.email)}",
            "PyPI": f"https://pypi.org/user/{quote(self.email)}/",
            
            # 🎨 Design
            "Figma": "https://www.figma.com/",
            "Canva": "https://www.canva.com/",
            "Adobe Creative Cloud": "https://creativecloud.adobe.com/",
            
            # 💬 Communication
            "Slack": "https://slack.com/",
            "Telegram": f"https://t.me/{quote(self.email)}",
            "Skype": "https://www.skype.com/",
            "Zoom": "https://zoom.us/",
            
            # ☁️ Cloud Storage
            "Dropbox": "https://www.dropbox.com/",
            "Google Drive": "https://drive.google.com/",
            "OneDrive": "https://onedrive.live.com/",
            "iCloud": "https://www.icloud.com/",
            
            # 📊 Productivity
            "Trello": f"https://trello.com/{quote(self.email)}",
            "Asana": "https://asana.com/",
            "Notion": "https://www.notion.so/",
            "Evernote": "https://www.evernote.com/",
            
            # 🔐 Security
            "LastPass": "https://www.lastpass.com/",
            "1Password": "https://1password.com/",
            "Dashlane": "https://www.dashlane.com/",
            
            # 🏠 Real Estate
            "Zillow": "https://www.zillow.com/",
            "Realtor.com": "https://www.realtor.com/",
            "Redfin": "https://www.redfin.com/",
            
            # 🐾 Pets
            "Chewy": "https://www.chewy.com/",
            "Rover": "https://www.rover.com/",
            
            # 🛠️ Home Improvement
            "Home Depot": "https://www.homedepot.com/",
            "Lowe's": "https://www.lowes.com/",
            "IKEA": "https://www.ikea.com/",
            
            # 🎁 Miscellaneous
            "Goodreads": f"https://www.goodreads.com/{quote(self.email)}",
            "Rotten Tomatoes": "https://www.rottentomatoes.com/",
            "IMDb": "https://www.imdb.com/",
            "Meetup": f"https://www.meetup.com/members/{quote(self.email)}/",
            "Eventbrite": "https://www.eventbrite.com/",
            "Kickstarter": f"https://www.kickstarter.com/profile/{quote(self.email)}",
            "GoFundMe": f"https://www.gofundme.com/m/{quote(self.email)}",
            "Patreon": f"https://www.patreon.com/{quote(self.email)}",
        }
        
        print(f"\n🔍 Checking: {self.email}")
        print("=" * 80)
        
        categories = {
            "🔐 Social Media": [k for k in sites.keys() if k in ["Facebook", "Twitter/X", "Instagram", "LinkedIn", "Pinterest", "TikTok", "Snapchat", "Reddit", "Tumblr", "VK", "Weibo"]],
            "💼 Professional": [k for k in sites.keys() if k in ["GitHub", "GitLab", "Bitbucket", "StackOverflow", "Dribbble", "Behance", "Medium", "Dev.to"]],
            "🎬 Video & Streaming": [k for k in sites.keys() if k in ["YouTube", "Twitch", "Vimeo", "Dailymotion", "Netflix", "Spotify", "SoundCloud"]],
            "🎮 Gaming": [k for k in sites.keys() if k in ["Steam", "Epic Games", "Xbox Live", "PlayStation", "Discord", "Roblox"]],
            "📷 Photo": [k for k in sites.keys() if k in ["Flickr", "500px", "Imgur", "VSCO"]],
            "💰 Finance": [k for k in sites.keys() if k in ["PayPal", "Venmo", "CashApp", "Robinhood"]],
            "🛒 E-commerce": [k for k in sites.keys() if k in ["Amazon", "eBay", "Etsy", "Shopify"]],
            "✈️ Travel": [k for k in sites.keys() if k in ["TripAdvisor", "Airbnb", "Booking.com", "Uber", "Lyft"]],
            "🔧 Development": [k for k in sites.keys() if k in ["npm", "Docker Hub", "PyPI"]],
            "📚 Education": [k for k in sites.keys() if k in ["Coursera", "Udemy", "Khan Academy", "EdX"]],
            "Other": [k for k in sites.keys() if k not in [item for sublist in categories.values() for item in sublist]] if 'categories' in locals() else []
        }
        
        results = {}
        total_sites = len(sites)
        checked = 0
        
        for category, site_list in categories.items():
            print(f"\n{category}")
            print("-" * 40)
            
            for site in site_list:
                if site in sites:
                    checked += 1
                    print(f"[{checked}/{total_sites}] {site:<25}", end=" ")
                    result = self.check_site(site, sites[site])
                    results[site] = result
                    print(result)
                    time.sleep(0.3)  # Be respectful to servers
        
        return results

def main():
    print("🚀 SUPER Email Account Checker - Educational Use Only")
    print("=" * 60)
    print("📢 This checks 100+ sites but many will show 'Connection failed'")
    print("   because they block automated requests or require login.")
    print("=" * 60)
    
    email = input("Enter email to check: ").strip()
    
    if not email or '@' not in email:
        print("❌ Invalid email format!")
        return
    
    checker = SuperEmailChecker(email)
    results = checker.run_mega_check()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    
    found = [site for site, result in results.items() if "✓" in result]
    possible = [site for site, result in results.items() if "?" in result]
    failed = [site for site, result in results.items() if "❌" in result or "🔌" in result or "⏰" in result]
    
    print(f"✅ Possible accounts: {len(found)}")
    for site in found:
        print(f"   - {site}")
    
    print(f"❓ Uncertain: {len(possible)}")
    print(f"❌ Failed checks: {len(failed)}")
    print(f"📧 Total sites checked: {len(results)}")
    
    print("\n" + "=" * 80)
    print("⚠️  DISCLAIMER: Educational purposes only!")
    print("   Many false positives/negatives expected.")
    print("   Sites frequently change their URL structures.")
    print("   Respect all terms of service and privacy policies.")
    print("=" * 80)

if __name__ == "__main__":
    main()