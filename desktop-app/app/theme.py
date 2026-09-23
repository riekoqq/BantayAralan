"""Design tokens for the native app -- mirrors the values used in the
earlier web prototype (../../admin-ui/frontend/css/tokens.css) so both
share one visual language, ported to Qt (QSS + Python constants instead of
CSS custom properties, since QSS has no variables).
"""

# ---- Neutrals ----
GRAY_50 = "#F8F9FB"
GRAY_100 = "#EEF1F5"
GRAY_200 = "#E1E5EB"
GRAY_300 = "#C7CDD6"
GRAY_400 = "#9AA3B1"
GRAY_500 = "#6B7382"
GRAY_600 = "#4B525F"
GRAY_700 = "#343A45"
GRAY_800 = "#20242C"
GRAY_900 = "#12151A"
WHITE = "#FFFFFF"

# ---- Brand ----
BRAND = "#0E7C86"
BRAND_HOVER = "#0B636B"

# ---- Status ----
SUCCESS = "#1E8E5A"
SUCCESS_BG = "#E5F5ED"
WARNING = "#B7791F"
WARNING_BG = "#FBF1DE"
DANGER = "#C0344B"
DANGER_BG = "#FBE9EC"

# ---- Semantic ----
BG_PAGE = GRAY_50
BG_SURFACE = WHITE
BG_SURFACE_ALT = GRAY_100
BG_INVERSE = GRAY_900
BORDER_DEFAULT = GRAY_200
BORDER_STRONG = GRAY_300
TEXT_PRIMARY = GRAY_900
TEXT_SECONDARY = GRAY_600
TEXT_TERTIARY = GRAY_400
TEXT_INVERSE = WHITE

# ---- Event categories -- always paired with an icon + text label ----
CATEGORY_COLORS = {
    "standing": {"fg": WARNING, "bg": WARNING_BG, "icon": "standing"},
    "trash": {"fg": DANGER, "bg": DANGER_BG, "icon": "trash"},
    "misaligned": {"fg": "#6E4FA6", "bg": "#EFE9F7", "icon": "misaligned"},
    "other": {"fg": "#475266", "bg": "#EAEDF3", "icon": "other"},
}

# ---- Spacing ----
SPACE_XS = 4
SPACE_SM = 8
SPACE_MD = 12
SPACE_LG = 16
SPACE_XL = 24
SPACE_2XL = 32
SPACE_3XL = 48

# ---- Radius ----
RADIUS_SM = 6
RADIUS_MD = 10
RADIUS_LG = 16
RADIUS_FULL = 999

SIDEBAR_WIDTH = 232
FONT_FAMILY = "Segoe UI, Inter, Arial, sans-serif"

STYLESHEET = f"""
* {{
    font-family: {FONT_FAMILY};
}}
QMainWindow, QWidget#Root {{
    background: {BG_PAGE};
}}
QLabel {{
    color: {TEXT_PRIMARY};
}}

/* ---- Sidebar ---- */
QFrame#Sidebar {{
    background: {BG_SURFACE};
    border-right: 1px solid {BORDER_DEFAULT};
}}
QLabel#Wordmark {{
    font-size: 16px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
}}
QPushButton#NavItem {{
    text-align: left;
    padding: 10px 12px;
    border-radius: {RADIUS_MD}px;
    border: none;
    background: transparent;
    color: {TEXT_SECONDARY};
    font-size: 14px;
    font-weight: 500;
}}
QPushButton#NavItem:hover {{
    background: {BG_SURFACE_ALT};
}}
QPushButton#NavItem[active="true"] {{
    background: {BRAND};
    color: {WHITE};
    font-weight: 600;
}}
QFrame#StatusBox {{
    background: {BG_SURFACE_ALT};
    border-radius: {RADIUS_MD}px;
}}
QLabel#StatusLine {{
    font-size: 11.5px;
    color: {TEXT_SECONDARY};
}}

/* ---- Page ---- */
QLabel#PageTitle {{
    font-size: 26px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
}}
QLabel#PageSubtitle {{
    font-size: 13.5px;
    color: {TEXT_SECONDARY};
}}
QLabel#SectionTitle {{
    font-size: 18px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
}}
QPushButton#LinkButton {{
    border: none;
    background: transparent;
    color: {BRAND};
    font-size: 13px;
    font-weight: 500;
}}
QPushButton#LinkButton:hover {{
    color: {BRAND_HOVER};
    text-decoration: underline;
}}

/* ---- Cards ---- */
QFrame#Card {{
    background: {BG_SURFACE};
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_LG}px;
}}
QFrame#Card:hover {{
    border: 1px solid {BORDER_STRONG};
}}
QLabel#StatLabel {{
    font-size: 11px;
    font-weight: 600;
    color: {TEXT_SECONDARY};
    letter-spacing: 1px;
}}
QLabel#StatNumber {{
    font-size: 28px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
}}
QLabel#StatSub {{
    font-size: 12px;
    color: {TEXT_TERTIARY};
}}
QLabel#EventTitle {{
    font-size: 15px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
}}
QLabel#EventDesc {{
    font-size: 13px;
    color: {TEXT_SECONDARY};
}}
QLabel#EventMeta {{
    font-size: 12px;
    font-weight: 500;
    color: {TEXT_TERTIARY};
}}

/* ---- Badges ---- */
QFrame#Badge {{
    border-radius: {RADIUS_FULL}px;
}}
QLabel#BadgeText {{
    font-size: 12px;
    font-weight: 600;
}}
QFrame#EvidenceTag {{
    background: {SUCCESS_BG};
    border-radius: {RADIUS_SM}px;
}}
QFrame#EvidenceTag[unavailable="true"] {{
    background: {BG_SURFACE_ALT};
}}
QLabel#EvidenceText {{
    font-size: 11.5px;
    font-weight: 500;
    color: {SUCCESS};
}}
QLabel#EvidenceText[unavailable="true"] {{
    color: {TEXT_TERTIARY};
}}

/* ---- Toolbar / inputs ---- */
QLineEdit#SearchField {{
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_MD}px;
    padding: 8px 12px;
    font-size: 13px;
    background: {BG_SURFACE};
    color: {TEXT_PRIMARY};
}}
QComboBox {{
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_MD}px;
    padding: 7px 10px;
    font-size: 13px;
    background: {BG_SURFACE};
    color: {TEXT_PRIMARY};
    min-width: 110px;
}}
QComboBox::drop-down {{
    border: none;
    width: 22px;
}}
QComboBox QAbstractItemView {{
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_SM}px;
    background: {BG_SURFACE};
    color: {TEXT_PRIMARY};
    padding: 4px;
    outline: none;
    selection-background-color: {BRAND};
    selection-color: {WHITE};
}}
QComboBox QAbstractItemView::item {{
    min-height: 26px;
    padding: 2px 8px;
    color: {TEXT_PRIMARY};
}}
QPushButton#Tab {{
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_SM}px;
    padding: 7px 16px;
    font-size: 13px;
    font-weight: 500;
    background: {BG_SURFACE};
    color: {TEXT_SECONDARY};
}}
QPushButton#Tab[active="true"] {{
    background: {BG_INVERSE};
    border-color: {BG_INVERSE};
    color: {WHITE};
    font-weight: 600;
}}

/* ---- Event list rows ---- */
QFrame#EventRow {{
    background: {BG_SURFACE};
    border-bottom: 1px solid {BORDER_DEFAULT};
}}
QFrame#EventRow:hover {{
    background: {BG_SURFACE_ALT};
}}
QFrame#EventListContainer {{
    background: {BG_SURFACE};
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_LG}px;
}}

/* ---- Buttons ---- */
QPushButton#PrimaryButton {{
    background: {BRAND};
    color: {WHITE};
    border: none;
    border-radius: {RADIUS_MD}px;
    padding: 9px 20px;
    font-size: 14px;
    font-weight: 500;
}}
QPushButton#PrimaryButton:hover {{ background: {BRAND_HOVER}; }}
QPushButton#SecondaryButton {{
    background: {BG_SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_STRONG};
    border-radius: {RADIUS_MD}px;
    padding: 9px 20px;
    font-size: 14px;
    font-weight: 500;
}}
QPushButton#SecondaryButton:hover {{ background: {BG_SURFACE_ALT}; }}
QPushButton#BackLink {{
    border: none;
    background: transparent;
    color: {TEXT_SECONDARY};
    font-size: 13.5px;
    font-weight: 500;
}}
QPushButton#BackLink:hover {{ color: {TEXT_PRIMARY}; }}

/* ---- Evidence card / tabs ---- */
QFrame#EvidenceCard {{
    background: {BG_SURFACE};
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_LG}px;
}}
QPushButton#EvidenceTabBtn {{
    border: none;
    border-bottom: 2px solid transparent;
    background: transparent;
    padding: 12px;
    font-size: 13.5px;
    font-weight: 500;
    color: {TEXT_SECONDARY};
}}
QPushButton#EvidenceTabBtn[active="true"] {{
    color: {BRAND};
    font-weight: 600;
    border-bottom: 2px solid {BRAND};
}}

/* ---- Video player ---- */
QFrame#VideoStage {{
    background: {GRAY_900};
    border-radius: {RADIUS_MD}px;
}}
QFrame#VideoControls {{
    background: {GRAY_900};
    border-bottom-left-radius: {RADIUS_MD}px;
    border-bottom-right-radius: {RADIUS_MD}px;
}}
QPushButton#PlayCircle {{
    background: rgba(255,255,255,235);
    border-radius: 28px;
    border: none;
}}
QLabel#TimestampBadge {{
    background: rgba(0,0,0,140);
    color: white;
    border-radius: {RADIUS_SM}px;
    padding: 4px 8px;
    font-size: 11px;
}}
QSlider#VideoTrack::groove:horizontal {{
    height: 4px;
    background: rgba(255,255,255,50);
    border-radius: 2px;
}}
QSlider#VideoTrack::sub-page:horizontal {{
    height: 4px;
    background: {BRAND};
    border-radius: 2px;
}}
QSlider#VideoTrack::handle:horizontal {{
    width: 10px;
    margin: -4px 0;
    background: white;
    border-radius: 5px;
}}
QLabel#VideoTime {{
    color: rgba(255,255,255,210);
    font-size: 11.5px;
}}
QLabel#VideoDisclaimer {{
    color: {TEXT_TERTIARY};
    font-size: 11px;
}}
QPushButton#IconButton {{
    border: none;
    background: transparent;
}}

/* ---- States ---- */
QLabel#StateTitle {{
    font-size: 15px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
}}
QLabel#StateDesc {{
    font-size: 13px;
    color: {TEXT_SECONDARY};
}}

/* ---- Screenshot viewer ---- */
QFrame#ScreenshotFrame {{
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_MD}px;
}}
QLabel#ScreenshotCaption {{
    font-size: 12px;
    color: {TEXT_SECONDARY};
    background: {BG_SURFACE};
    padding: 10px 14px;
}}

QScrollArea {{ border: none; background: transparent; }}
QScrollArea > QWidget > QWidget {{ background: transparent; }}
"""
