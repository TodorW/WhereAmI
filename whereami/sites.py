"""Curated database of sites that expose a per-user profile URL.

Every entry here must point at a URL that actually varies per account and
that returns a genuinely different response for an existing vs. missing
account. Homepage URLs ("can't check directly") are deliberately excluded:
a homepage always returns 200 and would report a false "account exists"
for every single lookup, which is worse than not checking at all.

`confidence` is an honest signal, not a formality:
  - HIGH   : JSON/API-backed or a server-rendered page with a reliable 404.
  - MEDIUM : server-rendered page, generally reliable but occasionally flaky.
  - LOW    : client-rendered (SPA) or bot-protected page that often returns
             200 regardless of whether the account exists. Still useful as
             a lead, never as proof.
"""

from dataclasses import dataclass
from enum import Enum


class Category(str, Enum):
    SOCIAL = "Social Media"
    PROFESSIONAL = "Professional"
    VIDEO = "Video & Streaming"
    MUSIC = "Music"
    GAMING = "Gaming"
    PHOTO = "Photo"
    DEVELOPMENT = "Development"
    DESIGN = "Design"
    PRODUCTIVITY = "Productivity"
    COMMUNITY = "Community & Forums"
    FITNESS = "Fitness"
    FUNDING = "Funding & Crowdsourcing"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass(frozen=True)
class Site:
    name: str
    category: Category
    url_template: str  # must contain "{value}" and use https
    confidence: Confidence
    method: str = "get"
    success_codes: frozenset = frozenset({200})
    not_found_codes: frozenset = frozenset({404})
    not_found_marker: str | None = None  # substring present when account is absent

    def __post_init__(self):
        if "{value}" not in self.url_template:
            raise ValueError(f"{self.name}: url_template must contain '{{value}}'")
        if not self.url_template.startswith("https://"):
            raise ValueError(f"{self.name}: url_template must use https")


SITES: list[Site] = [
    # Development
    Site("GitHub", Category.DEVELOPMENT, "https://api.github.com/users/{value}", Confidence.HIGH),
    Site("GitLab", Category.DEVELOPMENT, "https://gitlab.com/{value}", Confidence.MEDIUM),
    Site("Bitbucket", Category.DEVELOPMENT, "https://bitbucket.org/{value}/", Confidence.MEDIUM),
    Site("Docker Hub", Category.DEVELOPMENT, "https://hub.docker.com/v2/users/{value}/", Confidence.HIGH),
    Site("PyPI", Category.DEVELOPMENT, "https://pypi.org/user/{value}/", Confidence.HIGH),
    Site(
        "npm",
        Category.DEVELOPMENT,
        "https://registry.npmjs.org/-/user/org.couchdb.user:{value}",
        Confidence.HIGH,
    ),
    Site("Dev.to", Category.DEVELOPMENT, "https://dev.to/api/users/by_username?url={value}", Confidence.HIGH),
    Site("Keybase", Category.DEVELOPMENT, "https://keybase.io/{value}", Confidence.MEDIUM),

    # Professional
    Site("Medium", Category.PROFESSIONAL, "https://medium.com/@{value}", Confidence.MEDIUM),
    Site("Behance", Category.PROFESSIONAL, "https://www.behance.net/{value}", Confidence.MEDIUM),
    Site("Dribbble", Category.PROFESSIONAL, "https://dribbble.com/{value}", Confidence.MEDIUM),

    # Social Media
    Site("Reddit", Category.SOCIAL, "https://www.reddit.com/user/{value}/about.json", Confidence.HIGH),
    Site("Pinterest", Category.SOCIAL, "https://www.pinterest.com/{value}/", Confidence.MEDIUM),
    Site("VK", Category.SOCIAL, "https://vk.com/{value}", Confidence.MEDIUM),
    Site("Tumblr", Category.SOCIAL, "https://{value}.tumblr.com/", Confidence.MEDIUM),
    Site("Instagram", Category.SOCIAL, "https://www.instagram.com/{value}/", Confidence.LOW),
    Site("Twitter/X", Category.SOCIAL, "https://x.com/{value}", Confidence.LOW),
    Site("TikTok", Category.SOCIAL, "https://www.tiktok.com/@{value}", Confidence.LOW),
    Site("Facebook", Category.SOCIAL, "https://www.facebook.com/{value}", Confidence.LOW),
    Site("Snapchat", Category.SOCIAL, "https://www.snapchat.com/add/{value}", Confidence.LOW),

    # Video & Streaming
    Site("YouTube", Category.VIDEO, "https://www.youtube.com/@{value}", Confidence.MEDIUM),
    Site("Vimeo", Category.VIDEO, "https://vimeo.com/{value}", Confidence.MEDIUM),
    Site("Dailymotion", Category.VIDEO, "https://www.dailymotion.com/{value}", Confidence.MEDIUM),
    Site("Twitch", Category.VIDEO, "https://www.twitch.tv/{value}", Confidence.LOW),

    # Music
    Site("SoundCloud", Category.MUSIC, "https://soundcloud.com/{value}", Confidence.MEDIUM),
    Site("Spotify", Category.MUSIC, "https://open.spotify.com/user/{value}", Confidence.MEDIUM),
    Site("Last.fm", Category.MUSIC, "https://www.last.fm/user/{value}", Confidence.MEDIUM),
    Site("Bandcamp", Category.MUSIC, "https://www.bandcamp.com/{value}", Confidence.MEDIUM),

    # Gaming
    Site(
        "Steam",
        Category.GAMING,
        "https://steamcommunity.com/id/{value}",
        Confidence.MEDIUM,
        not_found_marker="The specified profile could not be found",
    ),
    Site("Roblox", Category.GAMING, "https://www.roblox.com/user.aspx?username={value}", Confidence.LOW),

    # Photo
    Site("Flickr", Category.PHOTO, "https://www.flickr.com/people/{value}", Confidence.MEDIUM),
    Site("500px", Category.PHOTO, "https://500px.com/{value}", Confidence.LOW),
    Site("Imgur", Category.PHOTO, "https://imgur.com/user/{value}", Confidence.MEDIUM),
    Site("VSCO", Category.PHOTO, "https://vsco.co/{value}", Confidence.LOW),

    # Design
    Site("Figma", Category.DESIGN, "https://www.figma.com/@{value}", Confidence.LOW),

    # Productivity
    Site("Trello", Category.PRODUCTIVITY, "https://trello.com/{value}", Confidence.MEDIUM),

    # Fitness
    Site("Strava", Category.FITNESS, "https://www.strava.com/athletes/{value}", Confidence.LOW),
    Site("MyFitnessPal", Category.FITNESS, "https://www.myfitnesspal.com/profile/{value}", Confidence.MEDIUM),

    # Community & Forums
    Site("Quora", Category.COMMUNITY, "https://www.quora.com/profile/{value}", Confidence.LOW),
    Site(
        "Hacker News",
        Category.COMMUNITY,
        "https://news.ycombinator.com/user?id={value}",
        Confidence.MEDIUM,
        not_found_marker="No such user.",
    ),
    Site("Goodreads", Category.COMMUNITY, "https://www.goodreads.com/{value}", Confidence.MEDIUM),
    Site("Meetup", Category.COMMUNITY, "https://www.meetup.com/members/{value}/", Confidence.LOW),
    Site("Telegram", Category.COMMUNITY, "https://t.me/{value}", Confidence.LOW),

    # Funding & Crowdsourcing
    Site("Kickstarter", Category.FUNDING, "https://www.kickstarter.com/profile/{value}", Confidence.MEDIUM),
    Site("Patreon", Category.FUNDING, "https://www.patreon.com/{value}", Confidence.MEDIUM),
    Site("GoFundMe", Category.FUNDING, "https://www.gofundme.com/f/{value}", Confidence.LOW),
]


def sites_by_category() -> dict[Category, list[Site]]:
    grouped: dict[Category, list[Site]] = {c: [] for c in Category}
    for site in SITES:
        grouped[site.category].append(site)
    return {category: entries for category, entries in grouped.items() if entries}
