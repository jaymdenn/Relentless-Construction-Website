#!/usr/bin/env python3
"""Generate city hub + service-in-city pages for SEO.

Outputs to website/locations/<city-slug>/index.html
and website/locations/<city-slug>/<service>/index.html for top markets.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "website"
OUT = ROOT / "locations"

# ---------- Service definitions ----------
SERVICES = {
    "roofing": {
        "label": "Roofing",
        "icon": "fa-home",
        "img": "service-roof.webp",
        "blurb_ut": "Asphalt shingle, metal, and tile roofing built for Utah's freeze-thaw cycles, heavy snow loads, and intense summer UV.",
        "blurb_az": "Tile, foam, and shingle roofing engineered for Arizona heat, monsoon hail, and three decades of relentless UV.",
        "systems_ut": [
            ("Asphalt Shingle Replacement", "fa-home", "Cool-roof rated, impact-resistant shingles built for Wasatch Front snow loads and summer UV. 25-50 year manufacturer warranties."),
            ("Metal Roofing", "fa-industry", "Standing seam and metal shingle systems — the longest-lasting option for Utah climates. Sheds snow, reflects heat, lasts 50+ years."),
            ("Tile Roofing", "fa-th-large", "Concrete and clay tile for Mediterranean and Spanish-style homes. Premium curb appeal with multi-decade durability."),
            ("Storm Damage Repair", "fa-cloud-showers-heavy", "Hail, wind, and ice-dam damage. Insurance claim documentation and direct carrier coordination."),
            ("Roof Repair & Maintenance", "fa-tools", "Targeted leak repair, flashing replacement, and ventilation upgrades to extend roof life."),
            ("Free Roof Inspections", "fa-search", "Drone-assisted inspection with full photo documentation. Honest assessments — no upselling."),
        ],
        "systems_az": [
            ("Concrete & Clay Tile", "fa-th-large", "The gold standard for Arizona. 50+ year service life. We re-felt with high-temp underlayment when existing tiles can be re-laid — saving thousands."),
            ("Foam (SPF) Roofing", "fa-cloud", "Spray polyurethane foam for flat and low-slope desert homes. Seamless, reflective, recoatable every 10-15 years instead of full replacement."),
            ("Cool-Roof Shingles", "fa-home", "Class 4 impact-rated, cool-roof rated asphalt — built to handle monsoon hail and reflect desert heat."),
            ("Monsoon Storm Damage", "fa-cloud-showers-heavy", "Same-day emergency tarping during monsoon season. Full insurance documentation and claim advocacy."),
            ("Repairs & Re-felt", "fa-tools", "Targeted repairs and tile re-felts that extend roof life by 20+ years at a fraction of replacement cost."),
            ("Free Roof Inspections", "fa-search", "Drone-assisted, full-photo inspection reports. Honest recommendations — no upselling."),
        ],
    },
    "windows": {
        "label": "Window Installation",
        "icon": "fa-window-maximize",
        "img": "service-windows.webp",
        "blurb_ut": "Energy-efficient replacement windows that cut heating bills, eliminate drafts, and stand up to Utah temperature swings.",
        "blurb_az": "Low-E, dual-pane windows that slash summer cooling bills, block desert UV, and protect interiors from sun fade.",
        "systems_ut": [
            ("Vinyl Replacement Windows", "fa-window-maximize", "Energy Star certified vinyl windows with multi-chamber frames built for Utah's wide temperature range."),
            ("Wood & Clad Windows", "fa-tree", "Premium wood-interior, aluminum-clad exterior windows for historic and high-end Utah homes."),
            ("Bay & Bow Windows", "fa-expand", "Custom bay and bow installations to add light, space, and dramatic curb appeal."),
            ("Egress Windows", "fa-door-open", "Code-compliant basement egress windows — required for any below-grade bedroom and a major safety upgrade."),
            ("Patio & Sliding Doors", "fa-arrows-alt-h", "Energy-efficient patio doors with multi-point locking and low-E glass."),
            ("Storm Window Replacement", "fa-shield-alt", "Replacement of storm-damaged windows with full insurance coordination."),
        ],
        "systems_az": [
            ("Low-E Dual Pane Replacement", "fa-window-maximize", "Sun-blocking low-E coatings and argon-filled dual pane glass — engineered to cut Arizona cooling bills by 25%+."),
            ("Impact-Resistant Windows", "fa-shield-alt", "Reinforced windows that resist monsoon debris, blowing dust, and break-in attempts."),
            ("Sliding & Patio Doors", "fa-arrows-alt-h", "Energy-efficient sliding glass doors built for desert heat and constant indoor-outdoor use."),
            ("Custom Arched Windows", "fa-expand", "Mediterranean and Spanish-style architectural windows. Custom shapes, colors, and grids."),
            ("Bay & Garden Windows", "fa-tree", "Custom bay, bow, and garden window installations to expand light and living space."),
            ("Window Repair", "fa-tools", "Seal failure, broken glass, and frame repair — often more economical than full replacement."),
        ],
    },
    "basement": {
        "label": "Basement Finishing",
        "icon": "fa-couch",
        "img": "service-basement.webp",
        "blurb_ut": "Turn unused below-grade square footage into legal living space — bedrooms, theaters, gyms, in-law suites — with full permits and code-compliant egress.",
        "blurb_az": "Below-grade finishing is rare in Arizona — but for homes that have it, we deliver complete remodels with proper moisture control for desert conditions.",
        "systems_ut": [
            ("Full Basement Finishing", "fa-couch", "Framing, electrical, plumbing, HVAC, drywall, flooring, and finishes — turnkey from concrete to move-in ready."),
            ("Basement Apartments & ADUs", "fa-key", "Legal accessory dwelling units with separate entrance, kitchen, and code-compliant egress."),
            ("Basement Bathrooms", "fa-bath", "Adding or remodeling below-grade bathrooms with proper ejector pump systems."),
            ("Egress Window Installation", "fa-door-open", "Required for any basement bedroom — we cut concrete, install window wells, and pass inspection."),
            ("Home Theaters & Gyms", "fa-tv", "Acoustic insulation, dedicated electrical, and finish-grade construction for high-use spaces."),
            ("Waterproofing & Moisture Control", "fa-shield-alt", "Vapor barriers, sealants, and drainage upgrades — critical for Utah basements before any finish work."),
        ],
        "systems_az": [
            ("Basement Refinishing", "fa-couch", "Full remodels of existing basements with desert-appropriate moisture control and ventilation."),
            ("Basement Bathrooms", "fa-bath", "Adding or remodeling below-grade bathrooms with proper plumbing and ventilation."),
            ("Home Theaters & Gyms", "fa-tv", "Sound insulation and dedicated systems for high-use entertainment and fitness spaces."),
            ("In-Law Suites", "fa-key", "Self-contained below-grade living spaces with private entrance options."),
            ("Moisture Control", "fa-shield-alt", "Vapor barriers and dehumidification — even in dry climates, below-grade spaces need proper moisture management."),
            ("Custom Storage & Finish Work", "fa-tools", "Built-ins, wine cellars, and custom millwork."),
        ],
    },
    "hardscapes": {
        "label": "Hardscapes",
        "icon": "fa-th-large",
        "img": "service-hardscape.webp",
        "blurb_ut": "Patios, retaining walls, fire pits, and outdoor kitchens engineered for Utah freeze-thaw cycles and built to last decades.",
        "blurb_az": "Pavers, retaining walls, outdoor kitchens, and pool decks built for Arizona's outdoor-living lifestyle and heat-resistant material requirements.",
        "systems_ut": [
            ("Paver Patios & Walkways", "fa-th-large", "Permeable and traditional paver systems with proper base prep for Utah freeze-thaw cycles."),
            ("Retaining Walls", "fa-grip-lines-vertical", "Engineered segmental retaining walls — load-rated and built to last on hillside Utah lots."),
            ("Outdoor Kitchens", "fa-utensils", "Custom outdoor kitchens with grills, refrigeration, and weather-protected finishes."),
            ("Fire Pits & Fireplaces", "fa-fire", "Wood and gas fire features for year-round outdoor use in Utah's variable climate."),
            ("Driveways & Aprons", "fa-road", "Concrete and paver driveways built to handle snow plowing and heavy vehicles."),
            ("Drainage & Grading", "fa-water", "Swales, French drains, and grading to protect your foundation from snowmelt and runoff."),
        ],
        "systems_az": [
            ("Paver Patios & Pool Decks", "fa-th-large", "Heat-reflective pavers and travertine for poolside and patio use."),
            ("Outdoor Kitchens", "fa-utensils", "Full custom outdoor kitchens — Arizona's most-used room for 9 months of the year."),
            ("Retaining Walls", "fa-grip-lines-vertical", "Engineered walls for desert hillside lots and grade transitions."),
            ("Fire Pits & Features", "fa-fire", "Gas fire pits and water features for cool desert evenings."),
            ("Driveways & Walkways", "fa-road", "Pavers, stamped concrete, and decorative finishes built for desert sun and monsoon runoff."),
            ("Pergolas & Shade Structures", "fa-umbrella-beach", "Custom shade structures — essential for usable Arizona outdoor space."),
        ],
    },
    "siding": {
        "label": "Siding",
        "icon": "fa-grip-lines",
        "img": "service-siding.webp",
        "blurb_ut": "Fiber cement, vinyl, and engineered wood siding built to handle Utah's UV, hail, and temperature swings.",
        "blurb_az": "Stucco repair, fiber cement, and siding systems engineered to resist sun fade, monsoon driving rain, and Arizona thermal cycling.",
        "systems_ut": [
            ("James Hardie Fiber Cement", "fa-grip-lines", "The gold-standard siding for Utah climates. Won't crack, rot, or fade — backed by 30-year warranties."),
            ("Vinyl Siding", "fa-grip-lines", "Cost-effective, low-maintenance vinyl siding in dozens of colors and profiles."),
            ("Engineered Wood Siding", "fa-tree", "LP SmartSide and similar systems — the look of wood with the durability of engineered materials."),
            ("Stucco Repair & Application", "fa-paint-roller", "Repair and full stucco systems for Mediterranean and Southwestern Utah homes."),
            ("Trim & Soffit", "fa-grip-lines-vertical", "PVC and composite trim, soffit, and fascia for a complete weather-tight envelope."),
            ("Insurance Restoration", "fa-shield-alt", "Hail and storm damage siding restoration with full insurance claim coordination."),
        ],
        "systems_az": [
            ("Stucco Repair & Recoat", "fa-paint-roller", "Stucco crack repair, recoats, and color matching — Arizona's most common siding system needs regular care."),
            ("James Hardie Fiber Cement", "fa-grip-lines", "Sun-stable, color-locked fiber cement for desert installations."),
            ("Synthetic Stucco (EIFS)", "fa-paint-roller", "EIFS systems and repairs for energy-efficient exterior finishes."),
            ("Trim & Fascia", "fa-grip-lines-vertical", "PVC and composite trim that won't warp or fade in desert sun."),
            ("Color Matching", "fa-palette", "Precise stucco and paint color matching for HOA-compliant repairs."),
            ("Storm Damage Restoration", "fa-shield-alt", "Monsoon and hail damage repair with insurance coordination."),
        ],
    },
    "gutters": {
        "label": "Gutters",
        "icon": "fa-water",
        "img": "service-gutters.webp",
        "blurb_ut": "Seamless aluminum and copper gutters sized to handle Utah snowmelt and protect your foundation year-round.",
        "blurb_az": "Seamless gutters and oversized downspouts sized for monsoon-volume rainfall — critical protection for stucco and foundations.",
        "systems_ut": [
            ("Seamless Aluminum Gutters", "fa-water", "On-site rolled seamless gutters in 5\" and 6\" sizes, sized for Utah snowmelt and roof area."),
            ("Copper Gutters", "fa-coins", "Premium copper gutter systems for heritage and luxury Utah homes."),
            ("Heated Gutters & De-Icing", "fa-fire", "Heat cable systems to prevent ice dams in mountain and high-elevation Utah homes."),
            ("Gutter Guards & Leaf Protection", "fa-shield-alt", "Micro-mesh and reverse-curve gutter protection — eliminates cleaning."),
            ("Downspout & Drainage", "fa-tint", "Oversized downspouts and underground drainage to move water safely away from foundations."),
            ("Gutter Repair", "fa-tools", "Sagging, leaking, and storm-damaged gutter repair."),
        ],
        "systems_az": [
            ("Seamless Aluminum Gutters", "fa-water", "On-site rolled seamless gutters sized for monsoon rainfall — undersized gutters fail fast in Arizona."),
            ("Oversized Downspouts", "fa-tint", "6\" downspouts and double-outlet systems for high-volume monsoon storms."),
            ("Gutter Guards", "fa-shield-alt", "Micro-mesh gutter protection — critical with Arizona dust, palo verde debris, and palm fronds."),
            ("Stucco Protection", "fa-paint-roller", "Proper gutter sizing prevents the #1 cause of stucco damage in Arizona homes."),
            ("Drainage Systems", "fa-water", "Underground drainage to move monsoon volume safely away from foundations and slabs."),
            ("Gutter Repair", "fa-tools", "Storm damage, sagging, and leaking gutter repair."),
        ],
    },
}

# ---------- City data ----------
# Each: (slug, name, state, lat, lng, top_market, hero_subtitle, intro, neighborhoods[3 groups], nearby[6])
CITIES = [
    # ===== UTAH =====
    ("salt-lake-city-ut", "Salt Lake City", "UT", 40.7608, -111.8910, True,
     "From the Avenues to Sugar House to Daybreak, we deliver roofing, windows, and full home improvement built for Wasatch Front winters and high-altitude UV.",
     "Salt Lake City's housing stock spans everything from 1900s Victorians in the Avenues to mid-century ramblers in Sugar House to brand-new builds on the west side. Each comes with its own challenges — and all of them face the same Wasatch Front realities: heavy snow loads, freeze-thaw cycles that destroy poor flashing, intense summer UV, and inversion-driven moisture issues. Relentless Construction is built for SLC homes specifically.",
     [("DOWNTOWN & EAST SIDE", ["The Avenues", "Federal Heights", "Sugar House", "Liberty Wells", "9th & 9th", "Yalecrest"]),
      ("WEST & SOUTH SIDE", ["Rose Park", "Glendale", "Poplar Grove", "Fairpark", "East Bench", "Foothill"]),
      ("NEARBY CITIES", [("Murray", "murray-ut"), ("Holladay", "holladay-ut"), ("Millcreek", "millcreek-ut"), ("West Valley City", "west-valley-city-ut"), ("South Salt Lake", "south-salt-lake-ut"), ("Cottonwood Heights", "cottonwood-heights-ut")])]),

    ("west-valley-city-ut", "West Valley City", "UT", 40.6916, -112.0011, False,
     "Utah's second-largest city — we serve Valley Crossing, Granger, and West Valley homes with roofing, windows, and complete home improvement.",
     "West Valley City is one of Utah's most diverse housing markets — older 60s-70s ranches, 80s-90s subdivisions, and newer construction throughout. The common thread: high winds off the Oquirrh Mountains, heavy winter snow, and aging roofs nearing the end of their life cycle. We work all over WVC.",
     [("WEST VALLEY NEIGHBORHOODS", ["Valley Crossing", "Granger", "Hunter", "Chesterfield", "Redwood", "Lake Park"]),
      ("COMMON HOME TYPES", ["1960s-70s ranches", "80s-90s subdivisions", "Newer west-side builds", "Townhomes & condos", "Bi-level homes", "Multi-generational properties"]),
      ("NEARBY CITIES", [("Salt Lake City", "salt-lake-city-ut"), ("Taylorsville", "taylorsville-ut"), ("Kearns", "kearns-ut"), ("West Jordan", "west-jordan-ut"), ("South Salt Lake", "south-salt-lake-ut"), ("Magna", "magna-ut")])]),

    ("west-jordan-ut", "West Jordan", "UT", 40.6097, -111.9391, False,
     "Serving West Jordan from Jordan Landing to The District — full home improvement built for the rapid growth and varied housing of the SW valley.",
     "West Jordan has exploded in the last 20 years, mixing established 80s-90s neighborhoods with newer master-planned communities. Snow loads, summer UV, and aging roof systems on the older stock keep our crews busy year-round.",
     [("WEST JORDAN NEIGHBORHOODS", ["Jordan Landing area", "The District", "Sunset Ridge", "Highland Park", "Westland Cove", "Jordan Hills"]),
      ("HOA COMMUNITIES", ["We work with most West Jordan HOAs", "Architectural review packets", "Color matching & approvals", "Complete documentation", "On-time inspections", "Bonded & licensed"]),
      ("NEARBY CITIES", [("South Jordan", "south-jordan-ut"), ("Riverton", "riverton-ut"), ("Taylorsville", "taylorsville-ut"), ("Murray", "murray-ut"), ("Sandy", "sandy-ut"), ("Herriman", "herriman-ut")])]),

    ("south-jordan-ut", "South Jordan", "UT", 40.5621, -111.9297, False,
     "Daybreak, The District, Glenmoor — we deliver roofing, windows, and full home improvement across South Jordan's master-planned communities.",
     "South Jordan is dominated by master-planned communities like Daybreak, where strict architectural review boards govern every exterior change. We've completed dozens of South Jordan projects with full HOA approval, color-matched specs, and on-time delivery.",
     [("SOUTH JORDAN COMMUNITIES", ["Daybreak", "The District", "Glenmoor", "South Jordan Heights", "River's Bend", "Welby"]),
      ("HOA EXPERIENCE", ["Daybreak ARC submissions", "Color & material matching", "Full spec packages", "Approved contractor lists", "Architectural reviews", "Documentation handling"]),
      ("NEARBY CITIES", [("West Jordan", "west-jordan-ut"), ("Riverton", "riverton-ut"), ("Herriman", "herriman-ut"), ("Bluffdale", "bluffdale-ut"), ("Draper", "draper-ut"), ("Sandy", "sandy-ut")])]),

    ("sandy-ut", "Sandy", "UT", 40.5649, -111.8389, False,
     "From Pepperwood to Granite to Alta — Sandy roofing, windows, and home improvement built for foothill homes and east-bench challenges.",
     "Sandy mixes high-end foothill homes with established mid-century neighborhoods and newer subdivisions. East-bench homes face heavier snow, more wind, and steeper drainage challenges than valley properties — we build accordingly.",
     [("SANDY NEIGHBORHOODS", ["Pepperwood", "Granite", "Alta", "Sandy Hills", "Crescent", "Quail Hollow"]),
      ("FOOTHILL CONSIDERATIONS", ["Steep grade drainage", "Heavier snow loads", "Wind exposure", "Hillside hardscapes", "Premium materials", "Engineered systems"]),
      ("NEARBY CITIES", [("Draper", "draper-ut"), ("Cottonwood Heights", "cottonwood-heights-ut"), ("Midvale", "midvale-ut"), ("South Jordan", "south-jordan-ut"), ("West Jordan", "west-jordan-ut"), ("Holladay", "holladay-ut")])]),

    ("draper-ut", "Draper", "UT", 40.5247, -111.8638, False,
     "Suncrest to SunCrest, Corner Canyon to Draper Heights — we serve Draper's hillside homes with roofing, windows, and complete home improvement.",
     "Draper's east-bench and SunCrest neighborhoods sit at the highest elevations on the Wasatch Front, taking the brunt of mountain weather. Heavier snow, stronger winds, and steeper grades all factor into our Draper installations.",
     [("DRAPER NEIGHBORHOODS", ["SunCrest", "Corner Canyon", "Draper Heights", "South Mountain", "Steep Mountain", "Suncrest Ridge"]),
      ("HIGH-ELEVATION CHALLENGES", ["Premium roofing systems", "Heated gutters/de-icing", "Engineered drainage", "Wind-rated installations", "Snow load engineering", "HOA compliance"]),
      ("NEARBY CITIES", [("Sandy", "sandy-ut"), ("Riverton", "riverton-ut"), ("Bluffdale", "bluffdale-ut"), ("Lehi", "lehi-ut"), ("Alpine", "alpine-ut"), ("Highland", "highland-ut")])]),

    ("riverton-ut", "Riverton", "UT", 40.5219, -111.9391, False,
     "Riverton's mix of established neighborhoods and newer construction gets full home improvement service from a licensed Utah contractor.",
     "Riverton sits at the south end of the Salt Lake Valley with newer construction dominating recent decades. Common needs: roof replacements on the original 90s-2000s installations, energy-efficiency upgrades, and outdoor-living additions.",
     [("RIVERTON NEIGHBORHOODS", ["Western Springs", "Riverton Ranch", "Western Hills", "Old Town Riverton", "Riverbend", "Highbury"]),
      ("COMMON PROJECTS", ["Original-roof replacements", "Window upgrades", "Hardscape additions", "Basement finishing", "Siding refresh", "Gutter upgrades"]),
      ("NEARBY CITIES", [("Herriman", "herriman-ut"), ("South Jordan", "south-jordan-ut"), ("Bluffdale", "bluffdale-ut"), ("West Jordan", "west-jordan-ut"), ("Draper", "draper-ut"), ("Sandy", "sandy-ut")])]),

    ("herriman-ut", "Herriman", "UT", 40.5141, -112.0330, False,
     "One of Utah's fastest-growing cities — we serve Herriman's new construction and established neighborhoods with full home improvement.",
     "Herriman is one of Utah's fastest-growing cities, with brand-new master-planned communities going up alongside older neighborhoods. We handle warranty-period roof issues, builder-grade window upgrades, and outdoor-living projects across the entire city.",
     [("HERRIMAN COMMUNITIES", ["Rosecrest", "Herriman Heights", "Anthem", "Juniper Crest", "Hidden Oaks", "Butterfield Canyon"]),
      ("BUILDER-HOME UPGRADES", ["Builder-grade window swaps", "Roof underlayment failures", "Hardscape additions", "Basement finishing", "Energy efficiency", "Storm damage"]),
      ("NEARBY CITIES", [("Riverton", "riverton-ut"), ("South Jordan", "south-jordan-ut"), ("Bluffdale", "bluffdale-ut"), ("Daybreak (South Jordan)", "south-jordan-ut"), ("West Jordan", "west-jordan-ut"), ("Copperton", "copperton-ut")])]),

    ("murray-ut", "Murray", "UT", 40.6669, -111.8880, False,
     "From historic Murray to East Murray — full home improvement service for one of the valley's most established communities.",
     "Murray's housing stock skews older — lots of 1950s-70s ramblers and bungalows, plus a healthy mix of newer infill. Older homes mean original roofs at end of life, single-pane windows, and foundation drainage that needs attention.",
     [("MURRAY NEIGHBORHOODS", ["Historic Murray", "East Murray", "Murray Park", "Olympus Cove area", "Vine Street", "Cottonwood"]),
      ("OLDER-HOME PROJECTS", ["End-of-life roof replacement", "Single-pane window upgrades", "Foundation drainage", "Egress windows", "Hardscape additions", "Siding refresh"]),
      ("NEARBY CITIES", [("Holladay", "holladay-ut"), ("Salt Lake City", "salt-lake-city-ut"), ("Midvale", "midvale-ut"), ("South Salt Lake", "south-salt-lake-ut"), ("Cottonwood Heights", "cottonwood-heights-ut"), ("Millcreek", "millcreek-ut")])]),

    ("holladay-ut", "Holladay", "UT", 40.6688, -111.8244, False,
     "Holladay's high-end foothill homes get premium roofing, windows, and home improvement from a contractor who matches the standard.",
     "Holladay is one of the Salt Lake Valley's most premium residential markets, with custom homes, established neighborhoods, and discerning homeowners. Material quality, craftsmanship, and project management all need to match the bar Holladay homes set.",
     [("HOLLADAY NEIGHBORHOODS", ["Olympus Cove", "Holladay Hills", "Cottonwood", "Walker Lane", "Casto Lane", "Holladay Boulevard"]),
      ("PREMIUM PROJECT FOCUS", ["Custom-home craftsmanship", "Premium roofing materials", "Wood-clad windows", "Custom hardscapes", "High-end basement finishing", "Copper gutters"]),
      ("NEARBY CITIES", [("Murray", "murray-ut"), ("Cottonwood Heights", "cottonwood-heights-ut"), ("Millcreek", "millcreek-ut"), ("Salt Lake City", "salt-lake-city-ut"), ("Sandy", "sandy-ut"), ("East Millcreek", "millcreek-ut")])]),

    ("cottonwood-heights-ut", "Cottonwood Heights", "UT", 40.6196, -111.8101, False,
     "Foothill living at its best — Cottonwood Heights roofing, windows, and home improvement built for east-bench homes.",
     "Cottonwood Heights sits at the mouth of Big and Little Cottonwood Canyons, exposed to canyon winds, heavier snow, and full mountain weather. Homes here need premium-grade systems and careful drainage planning.",
     [("COTTONWOOD HEIGHTS NEIGHBORHOODS", ["Bywater", "Old Mill", "Bella Vista", "Mountview", "Cherry Hill", "Solitude"]),
      ("CANYON-MOUTH CONSIDERATIONS", ["Canyon wind ratings", "Heavier snow design", "Engineered drainage", "Premium materials", "Heated gutters", "Storm-rated installs"]),
      ("NEARBY CITIES", [("Holladay", "holladay-ut"), ("Sandy", "sandy-ut"), ("Murray", "murray-ut"), ("Midvale", "midvale-ut"), ("Salt Lake City", "salt-lake-city-ut"), ("Millcreek", "millcreek-ut")])]),

    ("midvale-ut", "Midvale", "UT", 40.6111, -111.8956, False,
     "Midvale's mix of historic and newer homes gets full-service home improvement from a licensed local contractor.",
     "Midvale spans historic Old Town to newer transit-oriented developments near the Trax line. Mixed housing stock means mixed needs — original roof replacements on the older homes and quality upgrades on newer ones.",
     [("MIDVALE NEIGHBORHOODS", ["Old Town Midvale", "Bingham Junction", "View Heights", "East Midvale", "Union", "Mountview"]),
      ("COMMON PROJECTS", ["Historic-home careful upgrades", "Roof replacements", "Window energy upgrades", "Basement finishing", "Hardscape additions", "Siding refresh"]),
      ("NEARBY CITIES", [("Sandy", "sandy-ut"), ("Murray", "murray-ut"), ("West Jordan", "west-jordan-ut"), ("Cottonwood Heights", "cottonwood-heights-ut"), ("South Salt Lake", "south-salt-lake-ut"), ("Taylorsville", "taylorsville-ut")])]),

    ("taylorsville-ut", "Taylorsville", "UT", 40.6677, -111.9388, False,
     "Taylorsville's established neighborhoods get reliable roofing, windows, and full home improvement.",
     "Taylorsville is dominated by established 70s-90s subdivisions, where original roofs are at or past their replacement window. We handle full replacements, energy-efficiency upgrades, and outdoor-living additions across the city.",
     [("TAYLORSVILLE NEIGHBORHOODS", ["Atherton Park", "Taylorsville Heights", "Bennion", "Westwood", "Taylor Hills", "Fairfield"]),
      ("END-OF-LIFE PROJECTS", ["Original roof replacements", "Window upgrades", "Siding renewal", "Gutter replacement", "Basement finishing", "Hardscape additions"]),
      ("NEARBY CITIES", [("West Valley City", "west-valley-city-ut"), ("Murray", "murray-ut"), ("West Jordan", "west-jordan-ut"), ("Kearns", "kearns-ut"), ("Midvale", "midvale-ut"), ("Salt Lake City", "salt-lake-city-ut")])]),

    ("millcreek-ut", "Millcreek", "UT", 40.6869, -111.8757, False,
     "Millcreek's tree-lined neighborhoods and custom homes get premium home improvement from Relentless Construction.",
     "Millcreek is one of the valley's most established communities — mature trees, tight lots, and a mix of mid-century classics and high-end remodels. We handle premium projects with the careful execution Millcreek homes deserve.",
     [("MILLCREEK NEIGHBORHOODS", ["East Millcreek", "Mount Olympus", "Canyon Rim", "Olympus Hills", "Millcreek Canyon area", "St. Marys"]),
      ("MATURE-NEIGHBORHOOD CARE", ["Tree-protection prep", "Tight-lot logistics", "Premium materials", "Historic-style matching", "Custom hardscapes", "Discrete crews"]),
      ("NEARBY CITIES", [("Holladay", "holladay-ut"), ("Salt Lake City", "salt-lake-city-ut"), ("Murray", "murray-ut"), ("Cottonwood Heights", "cottonwood-heights-ut"), ("South Salt Lake", "south-salt-lake-ut"), ("Sugar House (SLC)", "salt-lake-city-ut")])]),

    ("provo-ut", "Provo", "UT", 40.2338, -111.6585, True,
     "From the Tree Streets to East Bay to Edgemont — Provo roofing, windows, and full home improvement for Utah Valley's flagship city.",
     "Provo's housing spans BYU-area student rentals, historic Tree Streets bungalows, established east-bench homes, and brand-new master-planned communities. Each comes with its own challenges, and Utah Valley climate adds heavy snow, hard freezes, and intense summer UV. We work across all of Provo.",
     [("PROVO NEIGHBORHOODS", ["Tree Streets", "Edgemont", "East Bay", "Indian Hills", "Foothills", "Joaquin"]),
      ("PROVO HOUSING TYPES", ["Historic bungalows", "BYU-area rentals", "East-bench customs", "New construction", "Townhomes", "Multi-gen homes"]),
      ("NEARBY CITIES", [("Orem", "orem-ut"), ("Springville", "springville-ut"), ("Mapleton", "mapleton-ut"), ("Spanish Fork", "spanish-fork-ut"), ("Lindon", "lindon-ut"), ("Pleasant Grove", "pleasant-grove-ut")])]),

    ("orem-ut", "Orem", "UT", 40.2969, -111.6946, False,
     "Family City USA gets full home improvement service — roofing, windows, basements, and more across all of Orem.",
     "Orem's housing skews family-oriented with lots of 70s-90s subdivisions plus newer construction on the city's edges. Original roofs at end-of-life and energy upgrades dominate our work in Orem.",
     [("OREM NEIGHBORHOODS", ["North Orem", "Cherry Hill", "Geneva Heights", "Lakeridge", "Sunset Heights", "Orchard"]),
      ("COMMON OREM PROJECTS", ["Original roof replacements", "Window upgrades", "Siding renewal", "Basement finishing", "Hardscape additions", "Gutter upgrades"]),
      ("NEARBY CITIES", [("Provo", "provo-ut"), ("Lindon", "lindon-ut"), ("Pleasant Grove", "pleasant-grove-ut"), ("Vineyard", "vineyard-ut"), ("Lehi", "lehi-ut"), ("American Fork", "american-fork-ut")])]),

    ("lehi-ut", "Lehi", "UT", 40.3916, -111.8508, False,
     "Silicon Slopes is booming — Lehi roofing, windows, and complete home improvement built for new construction and master-planned communities.",
     "Lehi has exploded with Silicon Slopes growth, mixing Traverse Mountain custom homes, master-planned Holbrook Farms communities, and brand-new builds across the city. Builder-grade roof and window upgrades, plus warranty-period failures, make up most of our Lehi work.",
     [("LEHI COMMUNITIES", ["Traverse Mountain", "Holbrook Farms", "Spring Creek", "Thanksgiving Point area", "Saddleback", "Ivory Ridge"]),
      ("NEW-CONSTRUCTION FOCUS", ["Builder-grade upgrades", "Warranty-period roofs", "Window energy upgrades", "Custom hardscapes", "Premium siding", "Basement finishing"]),
      ("NEARBY CITIES", [("American Fork", "american-fork-ut"), ("Saratoga Springs", "saratoga-springs-ut"), ("Eagle Mountain", "eagle-mountain-ut"), ("Pleasant Grove", "pleasant-grove-ut"), ("Highland", "highland-ut"), ("Alpine", "alpine-ut")])]),

    ("american-fork-ut", "American Fork", "UT", 40.3769, -111.7958, False,
     "American Fork roofing, windows, and home improvement — serving historic downtown to new master-planned communities.",
     "American Fork mixes historic downtown homes with brand-new builds along the I-15 corridor. Snow loads, summer UV, and aging roofs dominate our older-home work; builder-grade upgrades drive the newer-home projects.",
     [("AMERICAN FORK NEIGHBORHOODS", ["Downtown American Fork", "Highland Glen", "Cedar Hills border", "American Fork Canyon area", "Westfield", "Trefoil Ranch"]),
      ("MIXED PROJECT TYPES", ["Historic-home upgrades", "New-build warranty work", "Roof replacements", "Window upgrades", "Hardscape additions", "Basement finishing"]),
      ("NEARBY CITIES", [("Lehi", "lehi-ut"), ("Pleasant Grove", "pleasant-grove-ut"), ("Highland", "highland-ut"), ("Cedar Hills", "cedar-hills-ut"), ("Alpine", "alpine-ut"), ("Lindon", "lindon-ut")])]),

    ("pleasant-grove-ut", "Pleasant Grove", "UT", 40.3641, -111.7385, False,
     "Pleasant Grove home improvement — full-service roofing, windows, and remodeling from a licensed Utah contractor.",
     "Pleasant Grove balances historic Grove neighborhoods with newer construction along the foothills. Mixed housing stock means mixed needs — and PG's foothill homes face heavier snow and steeper drainage challenges.",
     [("PLEASANT GROVE NEIGHBORHOODS", ["Historic Grove", "Manila", "Grove Creek", "Battle Creek", "Foothills", "Pleasant Grove Heights"]),
      ("FOOTHILL FACTORS", ["Steeper drainage", "Wind exposure", "Heavier snow design", "Premium materials", "Engineered systems", "Custom hardscapes"]),
      ("NEARBY CITIES", [("American Fork", "american-fork-ut"), ("Lindon", "lindon-ut"), ("Highland", "highland-ut"), ("Lehi", "lehi-ut"), ("Cedar Hills", "cedar-hills-ut"), ("Orem", "orem-ut")])]),

    ("saratoga-springs-ut", "Saratoga Springs", "UT", 40.3494, -111.9038, False,
     "Saratoga Springs is one of Utah's fastest-growing cities — full home improvement service for new and established homes.",
     "Saratoga Springs has grown explosively along Utah Lake's west side. Most homes are 10-20 years old, with original roofs and builder-grade systems hitting end-of-life. We handle the whole spectrum.",
     [("SARATOGA SPRINGS COMMUNITIES", ["Fox Hollow", "Talons Cove", "Harvest Hills", "Horseshoe Bend", "Springside", "The Ranches"]),
      ("BUILDER-AGE PROJECTS", ["Original roof replacements", "Builder-window upgrades", "Hardscape additions", "Basement finishing", "Siding refresh", "Gutter upgrades"]),
      ("NEARBY CITIES", [("Eagle Mountain", "eagle-mountain-ut"), ("Lehi", "lehi-ut"), ("Bluffdale", "bluffdale-ut"), ("Cedar Fort", "cedar-fort-ut"), ("Vineyard", "vineyard-ut"), ("American Fork", "american-fork-ut")])]),

    ("eagle-mountain-ut", "Eagle Mountain", "UT", 40.3144, -112.0064, False,
     "Eagle Mountain home improvement service for one of Utah's largest and fastest-growing cities.",
     "Eagle Mountain spans miles of newer construction across multiple master-planned communities. Original-installation roof failures, window upgrades, and outdoor-living additions are our most common projects here.",
     [("EAGLE MOUNTAIN COMMUNITIES", ["The Ranches", "City Center", "Silverlake", "Sage Hills", "SkyRidge", "Hidden Hollow"]),
      ("NEW-COMMUNITY FOCUS", ["Original-roof failures", "Window upgrades", "Hardscape buildout", "Basement finishing", "HOA compliance", "Premium materials"]),
      ("NEARBY CITIES", [("Saratoga Springs", "saratoga-springs-ut"), ("Lehi", "lehi-ut"), ("Cedar Fort", "cedar-fort-ut"), ("Fairfield", "fairfield-ut"), ("Bluffdale", "bluffdale-ut"), ("Herriman", "herriman-ut")])]),

    ("spanish-fork-ut", "Spanish Fork", "UT", 40.1149, -111.6549, False,
     "Spanish Fork home improvement service — roofing, windows, and remodeling for South Utah Valley homes.",
     "Spanish Fork combines established downtown neighborhoods with rapidly growing newer construction along the foothills and west side. Snow, UV, and aging systems define our work here.",
     [("SPANISH FORK NEIGHBORHOODS", ["Downtown Spanish Fork", "East Foothills", "Maple Mountain area", "Westside", "Canyon Creek", "Palmyra"]),
      ("MIXED PROJECT TYPES", ["Historic-home work", "New-construction upgrades", "Roof replacements", "Window energy upgrades", "Hardscape additions", "Basement finishing"]),
      ("NEARBY CITIES", [("Springville", "springville-ut"), ("Mapleton", "mapleton-ut"), ("Provo", "provo-ut"), ("Salem", "salem-ut"), ("Payson", "payson-ut"), ("Spring Lake", "spring-lake-ut")])]),

    ("layton-ut", "Layton", "UT", 41.0602, -111.9711, False,
     "Layton home improvement — full-service roofing, windows, and remodeling for Davis County's largest city.",
     "Layton's housing stock includes everything from Hill AFB neighborhoods to established subdivisions to newer foothill builds. Lake-effect snow off the Great Salt Lake adds extra winter punch — we account for it.",
     [("LAYTON NEIGHBORHOODS", ["East Layton", "Layton Hills", "Adams Heights", "Heritage Park", "Antelope Drive area", "Foothills"]),
      ("DAVIS COUNTY CONDITIONS", ["Lake-effect snow", "Heavy winter loads", "Foothill drainage", "Premium materials", "Heated gutters available", "Engineered systems"]),
      ("NEARBY CITIES", [("Kaysville", "kaysville-ut"), ("Clearfield", "clearfield-ut"), ("Syracuse", "syracuse-ut"), ("South Weber", "south-weber-ut"), ("Roy", "roy-ut"), ("Farmington", "farmington-ut")])]),

    ("kaysville-ut", "Kaysville", "UT", 41.0353, -111.9383, False,
     "Kaysville home improvement service — roofing, windows, and remodeling for Davis County's premium residential market.",
     "Kaysville has become one of Davis County's most desirable cities, with custom homes, established neighborhoods, and premium remodels. Material quality and craftsmanship need to match the standard.",
     [("KAYSVILLE NEIGHBORHOODS", ["Crestwood", "Mountain Road area", "Kaysville Heights", "East Kaysville", "Old Town", "Foothills"]),
      ("PREMIUM-MARKET WORK", ["Custom-grade craftsmanship", "Premium materials", "Wood-clad windows", "Custom hardscapes", "High-end remodeling", "Discrete crews"]),
      ("NEARBY CITIES", [("Layton", "layton-ut"), ("Farmington", "farmington-ut"), ("Fruit Heights", "fruit-heights-ut"), ("Syracuse", "syracuse-ut"), ("Centerville", "centerville-ut"), ("Bountiful", "bountiful-ut")])]),

    ("farmington-ut", "Farmington", "UT", 40.9805, -111.8874, False,
     "Farmington home improvement — full-service roofing, windows, and remodeling for one of Davis County's most established cities.",
     "Farmington combines historic homes near downtown with newer custom builds on the east bench. Foothill exposure, heavy snow, and a discerning customer base shape our Farmington projects.",
     [("FARMINGTON NEIGHBORHOODS", ["Historic Farmington", "Farmington Greens", "Station Park area", "East Bench", "Compton Bench", "Old Town"]),
      ("FARMINGTON FOCUS", ["Historic-home careful work", "Custom-home craftsmanship", "Premium materials", "East-bench drainage", "HOA work", "Insurance restoration"]),
      ("NEARBY CITIES", [("Kaysville", "kaysville-ut"), ("Centerville", "centerville-ut"), ("Bountiful", "bountiful-ut"), ("Layton", "layton-ut"), ("Fruit Heights", "fruit-heights-ut"), ("Woods Cross", "woods-cross-ut")])]),

    ("bountiful-ut", "Bountiful", "UT", 40.8894, -111.8807, False,
     "Bountiful home improvement — roofing, windows, and remodeling for South Davis County's flagship city.",
     "Bountiful's housing stock is dominated by established homes — 60s-80s ranches, mature east-bench customs, and tightly built older neighborhoods. End-of-life roofs and energy upgrades make up most Bountiful projects.",
     [("BOUNTIFUL NEIGHBORHOODS", ["Bountiful Heights", "East Bench", "Mueller Park area", "Holbrook Farms", "Val Verda", "South Bountiful"]),
      ("ESTABLISHED-HOME PROJECTS", ["End-of-life roof replacement", "Single-pane window upgrades", "Foundation drainage", "Egress windows", "Hardscape additions", "Siding refresh"]),
      ("NEARBY CITIES", [("Centerville", "centerville-ut"), ("Woods Cross", "woods-cross-ut"), ("North Salt Lake", "north-salt-lake-ut"), ("Farmington", "farmington-ut"), ("West Bountiful", "west-bountiful-ut"), ("Salt Lake City", "salt-lake-city-ut")])]),

    ("centerville-ut", "Centerville", "UT", 40.9180, -111.8722, False,
     "Centerville home improvement — full-service roofing, windows, and remodeling between Bountiful and Farmington.",
     "Centerville is a quieter, established Davis County city with mature neighborhoods and consistent housing stock. End-of-life roofs and energy upgrades dominate our work here.",
     [("CENTERVILLE NEIGHBORHOODS", ["East Centerville", "Founders Park area", "Parrish Lane corridor", "Centerville Heights", "Pages Lane area", "South Centerville"]),
      ("CENTERVILLE PROJECTS", ["Roof replacements", "Window upgrades", "Siding refresh", "Hardscape additions", "Basement finishing", "Insurance restoration"]),
      ("NEARBY CITIES", [("Bountiful", "bountiful-ut"), ("Farmington", "farmington-ut"), ("Woods Cross", "woods-cross-ut"), ("Kaysville", "kaysville-ut"), ("Fruit Heights", "fruit-heights-ut"), ("West Bountiful", "west-bountiful-ut")])]),

    ("ogden-ut", "Ogden", "UT", 41.2230, -111.9738, True,
     "Historic Ogden to East Bench to Mountain Green — we serve all of Ogden with roofing, windows, and full home improvement.",
     "Ogden's housing spans some of Utah's oldest buildings — historic 1900s homes near 25th Street, 60s-70s east-bench builds, and newer subdivisions across the city. Lake-effect snow, mountain weather off the Wasatch, and aging building stock all shape our Ogden work.",
     [("OGDEN NEIGHBORHOODS", ["Historic 25th Street", "East Bench", "Mount Ogden", "Shadow Valley", "Polk Avenue", "Lorin Farr"]),
      ("OGDEN HOUSING TYPES", ["Historic Victorians", "Mid-century east-bench", "Mountain-view customs", "Established subdivisions", "New construction", "Mountain Green homes"]),
      ("NEARBY CITIES", [("South Ogden", "south-ogden-ut"), ("North Ogden", "north-ogden-ut"), ("Roy", "roy-ut"), ("Riverdale", "riverdale-ut"), ("Pleasant View", "pleasant-view-ut"), ("Washington Terrace", "washington-terrace-ut")])]),

    ("roy-ut", "Roy", "UT", 41.1616, -112.0263, False,
     "Roy home improvement — full-service roofing, windows, and remodeling for Weber County families.",
     "Roy is family-oriented with mostly established subdivisions from the 70s-90s plus newer construction along the city's edges. Original roof replacements and energy upgrades make up most of our Roy work.",
     [("ROY NEIGHBORHOODS", ["West Roy", "Roy Heights", "Sandridge", "1900 South corridor", "5600 South area", "East Roy"]),
      ("ROY PROJECT TYPES", ["End-of-life roof replacement", "Energy-efficiency upgrades", "Window replacement", "Siding refresh", "Hardscape additions", "Basement finishing"]),
      ("NEARBY CITIES", [("Riverdale", "riverdale-ut"), ("Clearfield", "clearfield-ut"), ("Hooper", "hooper-ut"), ("West Haven", "west-haven-ut"), ("Ogden", "ogden-ut"), ("Sunset", "sunset-ut")])]),

    ("clearfield-ut", "Clearfield", "UT", 41.1102, -112.0263, False,
     "Clearfield home improvement service for Hill AFB and surrounding Davis County neighborhoods.",
     "Clearfield's housing is shaped by Hill Air Force Base — lots of mid-century military-era homes, established neighborhoods, and newer construction. Aging roofs and energy upgrades dominate.",
     [("CLEARFIELD NEIGHBORHOODS", ["Antelope Drive area", "1700 South corridor", "Clearfield Hills", "West Clearfield", "Center Street area", "Steed Pond area"]),
      ("CLEARFIELD WORK", ["Roof replacements", "Window upgrades", "Siding refresh", "Hardscape additions", "Basement finishing", "Insurance restoration"]),
      ("NEARBY CITIES", [("Layton", "layton-ut"), ("Roy", "roy-ut"), ("Syracuse", "syracuse-ut"), ("Sunset", "sunset-ut"), ("Hooper", "hooper-ut"), ("West Point", "west-point-ut")])]),

    ("syracuse-ut", "Syracuse", "UT", 41.0891, -112.0658, False,
     "Syracuse home improvement — roofing, windows, and remodeling for one of Davis County's fastest-growing cities.",
     "Syracuse has grown rapidly along Antelope Island Drive and the lake. Newer construction dominates, with original-installation issues and outdoor-living additions being our most common Syracuse projects.",
     [("SYRACUSE NEIGHBORHOODS", ["Bluff Road area", "Antelope Island Drive", "Bluff Park", "1700 South area", "Gentile Street area", "Lakeview"]),
      ("SYRACUSE PROJECTS", ["Original-installation issues", "Window upgrades", "Outdoor-living buildouts", "Basement finishing", "Hardscape additions", "Premium siding"]),
      ("NEARBY CITIES", [("Layton", "layton-ut"), ("West Point", "west-point-ut"), ("Clearfield", "clearfield-ut"), ("Kaysville", "kaysville-ut"), ("Hooper", "hooper-ut"), ("Clinton", "clinton-ut")])]),

    ("park-city-ut", "Park City", "UT", 40.6461, -111.4980, False,
     "Park City home improvement — premium roofing, windows, and remodeling built for mountain weather and high-end mountain homes.",
     "Park City is a different climate from the valley — colder, snowier, and harder on building systems. Premium roofing, ice-dam protection, and mountain-grade everything are non-negotiable. We build for the mountain.",
     [("PARK CITY AREAS", ["Old Town Park City", "Park Meadows", "Deer Valley", "The Canyons (Park City Mountain)", "Promontory", "Silver Springs"]),
      ("MOUNTAIN-HOME ESSENTIALS", ["Heavy snow load engineering", "Heated gutters / de-icing", "Ice & water shield throughout", "Standing seam metal", "Wind-rated installs", "Premium underlayments"]),
      ("NEARBY CITIES", [("Heber City", "heber-city-ut"), ("Midway", "midway-ut"), ("Kamas", "kamas-ut"), ("Coalville", "coalville-ut"), ("Snyderville", "snyderville-ut"), ("Oakley", "oakley-ut")])]),

    ("tooele-ut", "Tooele", "UT", 40.5308, -112.2983, False,
     "Tooele home improvement — full-service roofing, windows, and remodeling for the Tooele Valley.",
     "Tooele Valley has its own conditions — high winds off the desert, heavier dust exposure, and a mix of older town homes with newer subdivisions. We work all over the valley.",
     [("TOOELE NEIGHBORHOODS", ["Old Tooele", "Overlake", "Stansbury Park area", "Canyon Rim", "South Willow Estates", "Tooele Heights"]),
      ("TOOELE-VALLEY FACTORS", ["High wind exposure", "Heavy dust", "Variable snow", "Extended summer UV", "Mixed housing stock", "Drainage planning"]),
      ("NEARBY CITIES", [("Stansbury Park", "stansbury-park-ut"), ("Grantsville", "grantsville-ut"), ("Erda", "erda-ut"), ("Lake Point", "lake-point-ut"), ("Stockton", "stockton-ut"), ("Pine Canyon", "pine-canyon-ut")])]),

    # ===== ARIZONA =====
    ("mesa-az", "Mesa", "AZ", 33.4152, -111.8315, True,
     "From Eastmark and Las Sendas to Red Mountain Ranch and downtown — Mesa roofing, windows, hardscapes, and full home improvement built for Arizona heat and monsoon storms.",
     "Mesa is one of the fastest-growing cities in the Southwest — and its mix of mid-century ranches, newer master-planned communities like Eastmark and Mountain Bridge, and historic homes near downtown all face the same enemies: relentless UV exposure, monsoon-driven hail and wind, and clay-heavy soils that move with every rain. Relentless Construction is built around those realities. We use materials, underlayments, and installation methods chosen specifically for the Sonoran climate, not generic national-builder specs.",
     [("EAST MESA", ["Eastmark", "Mountain Bridge", "Las Sendas", "Red Mountain Ranch", "Augusta Ranch", "Sunland Village"]),
      ("CENTRAL & WEST MESA", ["Downtown Mesa", "Dobson Ranch", "Lehi", "Alta Mesa", "Superstition Springs", "Fiesta District"]),
      ("NEARBY CITIES", [("Gilbert", "gilbert-az"), ("Chandler", "chandler-az"), ("Tempe", "tempe-az"), ("Scottsdale", "scottsdale-az"), ("Queen Creek", "queen-creek-az"), ("Apache Junction", "apache-junction-az")])]),

    ("phoenix-az", "Phoenix", "AZ", 33.4484, -112.0740, True,
     "From Arcadia to Ahwatukee, North Phoenix to Laveen — Phoenix's roofing, windows, and full home improvement contractor for every neighborhood.",
     "Phoenix is the fifth-largest U.S. city and one of the most punishing climates in the country. 115° summers, monsoon hail, three decades of relentless UV, and clay-heavy soils define every project here. Material specs that work in cooler climates fail fast in Phoenix — we use Arizona-specific systems on every install.",
     [("PHOENIX NEIGHBORHOODS", ["Arcadia", "Ahwatukee", "Biltmore", "North Central Phoenix", "Moon Valley", "Desert Ridge"]),
      ("OTHER PHOENIX AREAS", ["Laveen", "South Mountain", "Maryvale", "Sunnyslope", "Paradise Valley Village", "Encanto"]),
      ("NEARBY CITIES", [("Scottsdale", "scottsdale-az"), ("Tempe", "tempe-az"), ("Glendale", "glendale-az"), ("Mesa", "mesa-az"), ("Chandler", "chandler-az"), ("Peoria", "peoria-az")])]),

    ("scottsdale-az", "Scottsdale", "AZ", 33.4942, -111.9261, True,
     "Scottsdale home improvement — premium roofing, windows, and remodeling for one of Arizona's most discerning markets.",
     "Scottsdale demands the best — premium materials, careful HOA compliance, and craftsmanship that matches the neighborhood. From Old Town to North Scottsdale to McDowell Mountain Ranch, we deliver to Scottsdale's standard.",
     [("SCOTTSDALE NEIGHBORHOODS", ["Old Town Scottsdale", "McDowell Mountain Ranch", "Desert Mountain", "Troon", "Grayhawk", "DC Ranch"]),
      ("PREMIUM-MARKET FOCUS", ["Custom-grade craftsmanship", "Premium roofing materials", "Wood-clad & impact windows", "Strict HOA compliance", "Custom hardscapes", "Discrete crews"]),
      ("NEARBY CITIES", [("Phoenix", "phoenix-az"), ("Paradise Valley", "paradise-valley-az"), ("Tempe", "tempe-az"), ("Mesa", "mesa-az"), ("Fountain Hills", "fountain-hills-az"), ("Cave Creek", "cave-creek-az")])]),

    ("chandler-az", "Chandler", "AZ", 33.3062, -111.8413, True,
     "Chandler home improvement — full roofing, windows, and remodeling for one of the East Valley's premium markets.",
     "Chandler combines Ocotillo's master-planned communities with established neighborhoods and brand-new builds. Tech-industry homeowners expect premium work — and Arizona climate demands climate-specific specs. We deliver both.",
     [("CHANDLER COMMUNITIES", ["Ocotillo", "Sun Lakes", "Fulton Ranch", "South Chandler", "Downtown Chandler", "Pecos Ranch"]),
      ("CHANDLER WORK", ["Tile & foam roofing", "Low-E window upgrades", "Custom hardscapes", "Pool-deck pavers", "Stucco repair", "HOA-compliant installs"]),
      ("NEARBY CITIES", [("Gilbert", "gilbert-az"), ("Mesa", "mesa-az"), ("Tempe", "tempe-az"), ("Queen Creek", "queen-creek-az"), ("Ahwatukee (Phoenix)", "phoenix-az"), ("Maricopa", "maricopa-az")])]),

    ("gilbert-az", "Gilbert", "AZ", 33.3528, -111.7890, True,
     "Gilbert home improvement — premium roofing, windows, and remodeling for one of America's most desirable suburbs.",
     "Gilbert has grown into one of America's most family-friendly cities, with Power Ranch, Seville, and Val Vista master-planned communities defining the housing market. HOA-compliance, premium materials, and craftsmanship matter here. We deliver all three.",
     [("GILBERT COMMUNITIES", ["Power Ranch", "Seville", "Val Vista Lakes", "Agritopia", "Morrison Ranch", "Gilbert Heritage"]),
      ("GILBERT FOCUS", ["HOA-compliant tile roofing", "Energy-efficient windows", "Custom hardscapes", "Outdoor kitchens", "Stucco repair", "Premium siding"]),
      ("NEARBY CITIES", [("Chandler", "chandler-az"), ("Mesa", "mesa-az"), ("Queen Creek", "queen-creek-az"), ("Tempe", "tempe-az"), ("San Tan Valley", "san-tan-valley-az"), ("Apache Junction", "apache-junction-az")])]),

    ("tempe-az", "Tempe", "AZ", 33.4255, -111.9400, False,
     "Tempe home improvement — roofing, windows, and remodeling for ASU-area homes and established Tempe neighborhoods.",
     "Tempe's housing skews older — historic Mitchell Park, mid-century South Tempe, and ASU-area rentals dominate. End-of-life roof systems, single-pane windows, and aging stucco all need attention.",
     [("TEMPE NEIGHBORHOODS", ["Mitchell Park", "Maple-Ash", "South Tempe", "Warner Ranch", "Lakes", "Tempe Junction"]),
      ("TEMPE PROJECT TYPES", ["End-of-life roofs", "Single-pane upgrades", "Historic-home work", "Stucco repair", "Hardscape additions", "Insurance restoration"]),
      ("NEARBY CITIES", [("Mesa", "mesa-az"), ("Chandler", "chandler-az"), ("Phoenix", "phoenix-az"), ("Scottsdale", "scottsdale-az"), ("Gilbert", "gilbert-az"), ("Ahwatukee (Phoenix)", "phoenix-az")])]),

    ("glendale-az", "Glendale", "AZ", 33.5387, -112.1860, False,
     "Glendale home improvement — full-service roofing, windows, and remodeling for the West Valley.",
     "Glendale spans historic downtown to Arrowhead Ranch to newer master-planned communities. West Valley heat is even harsher than central Phoenix, and roofs/AC systems take a serious beating.",
     [("GLENDALE NEIGHBORHOODS", ["Arrowhead Ranch", "Sierra Verde", "Historic Downtown Glendale", "Stetson Hills", "Westgate area", "Catlin Court"]),
      ("WEST-VALLEY FACTORS", ["Extreme heat exposure", "Reflective roofing critical", "Premium underlayments", "Energy-efficient windows", "HOA work", "Stucco repair"]),
      ("NEARBY CITIES", [("Peoria", "peoria-az"), ("Phoenix", "phoenix-az"), ("Surprise", "surprise-az"), ("Avondale", "avondale-az"), ("Goodyear", "goodyear-az"), ("Sun City", "sun-city-az")])]),

    ("peoria-az", "Peoria", "AZ", 33.5806, -112.2374, False,
     "Peoria home improvement — roofing, windows, and remodeling for one of the West Valley's fastest-growing cities.",
     "Peoria stretches from Old Town up into the hills with Vistancia and other master-planned communities defining recent growth. Original-installation roof failures and HOA-compliant work dominate.",
     [("PEORIA COMMUNITIES", ["Vistancia", "Westwing Mountain", "Trilogy at Vistancia", "Old Town Peoria", "Fletcher Heights", "Sundance"]),
      ("PEORIA WORK", ["Original-roof failures", "HOA-compliant installs", "Energy-efficient windows", "Custom hardscapes", "Stucco repair", "Premium siding"]),
      ("NEARBY CITIES", [("Glendale", "glendale-az"), ("Surprise", "surprise-az"), ("Sun City", "sun-city-az"), ("Phoenix", "phoenix-az"), ("Sun City West", "sun-city-west-az"), ("El Mirage", "el-mirage-az")])]),

    ("surprise-az", "Surprise", "AZ", 33.6292, -112.3679, False,
     "Surprise home improvement — full-service roofing, windows, and remodeling for the West Valley's growth corridor.",
     "Surprise has exploded with Sun City Grand, Marley Park, and other master-planned growth. Most homes are 10-25 years old — original roofs and builder-grade systems hitting end-of-life dominate our work here.",
     [("SURPRISE COMMUNITIES", ["Sun City Grand", "Marley Park", "Surprise Farms", "Sierra Verde", "Greer Ranch", "Asante"]),
      ("BUILDER-AGE PROJECTS", ["Original-roof replacements", "Builder-window upgrades", "Tile re-felts", "Hardscape additions", "Stucco repair", "HOA compliance"]),
      ("NEARBY CITIES", [("Peoria", "peoria-az"), ("Glendale", "glendale-az"), ("Sun City West", "sun-city-west-az"), ("El Mirage", "el-mirage-az"), ("Buckeye", "buckeye-az"), ("Goodyear", "goodyear-az")])]),

    ("goodyear-az", "Goodyear", "AZ", 33.4355, -112.3576, False,
     "Goodyear home improvement — roofing, windows, and remodeling for one of the West Valley's fastest-growing cities.",
     "Goodyear's growth has been explosive — Estrella, PebbleCreek, and other master-planned communities fill what was farmland a decade ago. Builder-grade upgrades and original-installation failures dominate.",
     [("GOODYEAR COMMUNITIES", ["Estrella", "PebbleCreek", "Palm Valley", "Canyon Trails", "Sedella", "Wildflower Ranch"]),
      ("GOODYEAR PROJECT FOCUS", ["Tile re-felts", "Builder-grade upgrades", "Energy-efficient windows", "Custom hardscapes", "HOA-compliant installs", "Premium materials"]),
      ("NEARBY CITIES", [("Avondale", "avondale-az"), ("Buckeye", "buckeye-az"), ("Litchfield Park", "litchfield-park-az"), ("Surprise", "surprise-az"), ("Glendale", "glendale-az"), ("Tolleson", "tolleson-az")])]),

    ("avondale-az", "Avondale", "AZ", 33.4356, -112.3496, False,
     "Avondale home improvement — full-service roofing, windows, and remodeling for the West Valley.",
     "Avondale combines established neighborhoods with rapidly growing newer construction. Roof replacements on aging stock and energy upgrades on builder-grade homes are our most common projects here.",
     [("AVONDALE NEIGHBORHOODS", ["Garden Lakes", "Rancho Santa Fe", "Crystal Gardens", "Roosevelt Park", "Coldwater Springs", "Old Avondale"]),
      ("AVONDALE WORK", ["Aging-roof replacement", "Builder-grade upgrades", "Stucco repair", "Hardscape additions", "Insurance restoration", "Premium siding"]),
      ("NEARBY CITIES", [("Goodyear", "goodyear-az"), ("Tolleson", "tolleson-az"), ("Buckeye", "buckeye-az"), ("Litchfield Park", "litchfield-park-az"), ("Glendale", "glendale-az"), ("Phoenix", "phoenix-az")])]),

    ("buckeye-az", "Buckeye", "AZ", 33.3703, -112.5838, False,
     "Buckeye home improvement — roofing, windows, and remodeling for one of America's fastest-growing cities.",
     "Buckeye is one of the fastest-growing cities in the U.S., with Verrado, Sundance, and other master-planned communities expanding rapidly. Most homes are newer — but Arizona heat doesn't care how new your roof is.",
     [("BUCKEYE COMMUNITIES", ["Verrado", "Sundance", "Sun City Festival", "Tartesso", "Westpark", "Spurlock Ranch"]),
      ("BUCKEYE FOCUS", ["Original-installation issues", "HOA compliance", "Energy-efficient windows", "Custom hardscapes", "Tile re-felts", "Premium siding"]),
      ("NEARBY CITIES", [("Goodyear", "goodyear-az"), ("Avondale", "avondale-az"), ("Surprise", "surprise-az"), ("Litchfield Park", "litchfield-park-az"), ("Tonopah", "tonopah-az"), ("Wickenburg", "wickenburg-az")])]),

    ("queen-creek-az", "Queen Creek", "AZ", 33.2487, -111.6343, False,
     "Queen Creek home improvement — roofing, windows, and remodeling for one of the East Valley's fastest-growing cities.",
     "Queen Creek has transformed from rural farmland to one of the East Valley's premium suburbs. Master-planned communities like Encanterra and Cortina dominate, with HOA compliance and premium materials being non-negotiable.",
     [("QUEEN CREEK COMMUNITIES", ["Encanterra", "Cortina", "Pecan Creek", "Hastings Farms", "Charleston Estates", "Queen Creek Station area"]),
      ("QUEEN CREEK PROJECTS", ["HOA-compliant tile roofing", "Builder-grade window upgrades", "Custom hardscapes", "Outdoor kitchens", "Premium stucco repair", "Pool-deck pavers"]),
      ("NEARBY CITIES", [("San Tan Valley", "san-tan-valley-az"), ("Gilbert", "gilbert-az"), ("Chandler", "chandler-az"), ("Mesa", "mesa-az"), ("Apache Junction", "apache-junction-az"), ("Florence", "florence-az")])]),

    ("maricopa-az", "Maricopa", "AZ", 33.0581, -112.0476, False,
     "Maricopa home improvement — full-service roofing, windows, and remodeling for one of Arizona's fastest-growing cities.",
     "Maricopa has grown explosively south of Phoenix, with Province, Glennwilde, and other master-planned communities. Most homes are 10-15 years old — prime time for original-roof issues and energy upgrades.",
     [("MARICOPA COMMUNITIES", ["Province", "Glennwilde", "Rancho El Dorado", "Cobblestone Farms", "Senita", "The Lakes at Rancho El Dorado"]),
      ("MARICOPA WORK", ["Original-roof failures", "Builder-window upgrades", "Tile re-felts", "Custom hardscapes", "HOA compliance", "Stucco repair"]),
      ("NEARBY CITIES", [("Chandler", "chandler-az"), ("Casa Grande", "casa-grande-az"), ("Queen Creek", "queen-creek-az"), ("Gilbert", "gilbert-az"), ("Florence", "florence-az"), ("Eloy", "eloy-az")])]),

    ("apache-junction-az", "Apache Junction", "AZ", 33.4150, -111.5496, False,
     "Apache Junction home improvement — roofing, windows, and remodeling at the foot of the Superstition Mountains.",
     "Apache Junction sits at the East Valley's edge against the Superstitions, with mixed housing — established mobile home communities, mid-century neighborhoods, and newer construction. Mountain weather adds wind and runoff considerations.",
     [("APACHE JUNCTION AREAS", ["Superstition Foothills", "Apache Junction Heights", "Old West Highway area", "Tomahawk", "Goldfield Ranch area", "Mountainbrook Village"]),
      ("APACHE JUNCTION FACTORS", ["Mountain wind exposure", "Monsoon runoff", "Mixed housing stock", "Premium materials", "Engineered drainage", "Storm-rated installs"]),
      ("NEARBY CITIES", [("Mesa", "mesa-az"), ("Gold Canyon", "gold-canyon-az"), ("Queen Creek", "queen-creek-az"), ("Gilbert", "gilbert-az"), ("Florence Junction", "florence-junction-az"), ("San Tan Valley", "san-tan-valley-az")])]),
]

TOP_MARKET_SLUGS = {c[0] for c in CITIES if c[5]}

# ---------- HTML templates ----------

HEAD_COMMON = """<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HNHMDQVL37"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-HNHMDQVL37');
</script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="Relentless Construction">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">

    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{og_description}">
    <meta property="og:image" content="https://relentlessconstruction.io/assets/images/og-image.jpg">
    <meta property="og:site_name" content="Relentless Construction">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="geo.region" content="US-{state}">
    <meta name="geo.placename" content="{city_name}">
    <meta name="geo.position" content="{lat};{lng}">
    <meta name="ICBM" content="{lat}, {lng}">
    <meta name="theme-color" content="#2d8a5e">

    <link rel="icon" type="image/png" href="{asset_prefix}assets/images/logo.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;500;600;700;800&family=Host+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="{asset_prefix}assets/css/styles.css">

{schemas}
</head>"""

HEADER_HTML = """<body>
    <header class="header">
        <div class="top-bar">
            <div class="container">
                <div class="top-bar-content">
                    <div class="top-bar-left">
                        <a href="tel:801-923-4634"><i class="fas fa-phone"></i> 801-923-4634</a>
                        <a href="mailto:info@relentlessconstruction.io"><i class="fas fa-envelope"></i> info@relentlessconstruction.io</a>
                        <span><i class="fas fa-clock"></i> Mon-Sat 8AM-6PM</span>
                    </div>
                    <div class="top-bar-right">
                        <span>Follow Us:</span>
                        <div class="social-icons">
                            <a href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                            <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                            <a href="#" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="header-main">
            <div class="container">
                <div class="header-content">
                    <a href="{p}index.html" class="logo">
                        <img src="{p}assets/images/full-logo.png" alt="Relentless Construction">
                    </a>
                    <nav class="nav">
                        <ul class="nav-list">
                            <li><a href="{p}index.html">Home</a></li>
                            <li><a href="{p}about.html">About</a></li>
                            <li class="dropdown">
                                <a href="{p}services.html">Services <i class="fas fa-chevron-down" style="font-size: 10px; margin-left: 5px;"></i></a>
                                <ul class="dropdown-menu">
                                    <li><a href="{p}windows.html">Window Installation</a></li>
                                    <li><a href="{p}roofing.html">Roofing</a></li>
                                    <li><a href="{p}basement.html">Basement Finishing</a></li>
                                    <li><a href="{p}hardscapes.html">Hardscapes</a></li>
                                </ul>
                            </li>
                            <li><a href="{p}portfolio.html">Portfolio</a></li>
                            <li><a href="{locations_link}">Locations</a></li>
                        </ul>
                    </nav>
                    <div class="header-cta">
                        <a href="tel:801-923-4634" class="header-phone">
                            <i class="fas fa-phone"></i>
                            <span>Ready, Contact Now</span>
                        </a>
                        <button class="btn btn-primary" onclick="openFormPopup()">Free Estimate</button>
                    </div>
                    <button class="mobile-menu-btn" aria-label="Toggle menu">
                        <span></span><span></span><span></span>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <div id="form-popup" class="form-popup-overlay" onclick="closeFormPopup(event)">
        <div class="form-popup-content" onclick="event.stopPropagation()">
            <button class="form-popup-close" onclick="closeFormPopup()">&times;</button>
            <iframe
                src="https://links.relentlessconstruction.io/widget/form/Orv2CdmAE25WUp8hdIoW"
                style="width:100%;height:700px;border:none;border-radius:3px"
                id="inline-Orv2CdmAE25WUp8hdIoW"
                data-form-name="Main Page contact Form "
                data-form-id="Orv2CdmAE25WUp8hdIoW"
                title="Main Page contact Form "
            ></iframe>
        </div>
    </div>"""

FOOTER_HTML = """    <footer class="footer section-with-bg bg-construction-2">
        <div class="container">
            <div class="footer-top">
                <div class="footer-info-card">
                    <i class="fas fa-phone"></i>
                    <h4>Call Us</h4>
                    <a href="tel:801-923-4634">801-923-4634</a>
                </div>
                <div class="footer-info-card">
                    <i class="fas fa-clock"></i>
                    <h4>Hours</h4>
                    <p>Monday-Friday: 8AM - 6PM<br>Saturday: By Appointment</p>
                </div>
                <div class="footer-info-card">
                    <i class="fas fa-map-marker-alt"></i>
                    <h4>Service Areas</h4>
                    <p>Utah & Arizona<br><a href="{locations_link}" style="color: inherit;">View all locations</a></p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Relentless Construction. All rights reserved.</p>
                <div class="footer-social">
                    <a href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                    <a href="#" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
                    <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                    <a href="#" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                </div>
            </div>
        </div>
    </footer>

    <script src="https://links.relentlessconstruction.io/js/form_embed.js"></script>
    <script src="{p}assets/js/main.js"></script>
</body>
</html>"""


def neighborhoods_html(groups, asset_prefix_for_links):
    """Render 3 neighborhood/info area cards. asset_prefix_for_links is `../` from city hub or `../../` from service page."""
    cards = []
    for title, items in groups:
        lis = []
        for item in items:
            if isinstance(item, tuple):
                label, slug = item
                lis.append(f'<li><a href="{asset_prefix_for_links}{slug}/">{label}</a></li>')
            else:
                lis.append(f"<li>{item}</li>")
        cards.append(f"""                <div class="area-card">
                    <h3><i class="fas fa-map-marker-alt"></i> {title}</h3>
                    <ul>
                        {chr(10).join(lis)}
                    </ul>
                </div>""")
    return "\n".join(cards)


def build_city_hub(city):
    slug, name, state, lat, lng, top, hero_sub, intro, groups = city
    canonical = f"https://relentlessconstruction.io/locations/{slug}/"
    state_full = "Utah" if state == "UT" else "Arizona"
    asset_prefix = "../../"
    p = asset_prefix
    locations_link = "../"

    schemas = f"""    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "GeneralContractor",
        "name": "Relentless Construction - {name}, {state}",
        "description": "Full-service construction and home improvement contractor serving {name}, {state_full}.",
        "url": "{canonical}",
        "telephone": "+1-801-923-4634",
        "email": "info@relentlessconstruction.io",
        "image": "https://relentlessconstruction.io/assets/images/og-image.jpg",
        "priceRange": "$$",
        "areaServed": {{"@type": "City", "name": "{name}", "containedInPlace": {{"@type": "State", "name": "{state_full}"}}}},
        "address": {{"@type": "PostalAddress", "addressLocality": "{name}", "addressRegion": "{state}", "addressCountry": "US"}},
        "geo": {{"@type": "GeoCoordinates", "latitude": {lat}, "longitude": {lng}}},
        "openingHoursSpecification": [{{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
            "opens": "08:00", "closes": "18:00"
        }}]
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://relentlessconstruction.io/"}},
            {{"@type": "ListItem", "position": 2, "name": "Locations", "item": "https://relentlessconstruction.io/locations/"}},
            {{"@type": "ListItem", "position": 3, "name": "{name}, {state}", "item": "{canonical}"}}
        ]
    }}
    </script>"""

    title = f"Construction & Home Improvement in {name}, {state} | Roofing, Windows, Hardscapes | Relentless Construction"
    description = f"Trusted {name}, {state} contractor for roofing, windows, basement finishing, hardscapes, siding & gutters. Licensed, insured, and built for {state_full} conditions. Free estimates: 801-923-4634."
    keywords = f"{name} {state} contractor, {name} roofing, {name} window replacement, {name} hardscape, home improvement {name} {state_full}, construction company {name}"
    og_title = f"{name}, {state} Construction & Home Improvement | Relentless Construction"
    og_description = f"Roofing, windows, basements, hardscapes & more in {name}, {state_full}. Free estimates from a licensed local contractor."

    head = HEAD_COMMON.format(
        title=title, description=description, keywords=keywords, canonical=canonical,
        og_title=og_title, og_description=og_description, state=state,
        city_name=name, lat=lat, lng=lng, asset_prefix=asset_prefix, schemas=schemas,
    )
    header = HEADER_HTML.format(p=p, locations_link=locations_link)
    footer = FOOTER_HTML.format(p=p, locations_link=locations_link)

    # Hero
    hero_img = "service-roof.webp"
    hero_title_state = "ARIZONA" if state == "AZ" else "UTAH"
    hero = f"""
    <section class="hero hero-centered" style="background-image: url('{asset_prefix}assets/images/{hero_img}');">
        <div class="hero-overlay"></div>
        <div class="container">
            <div class="hero-content-centered">
                <span class="hero-badge-centered"><i class="fas fa-map-marker-alt"></i> Serving {name}, {state_full}</span>
                <h1 class="hero-title-large">{name.upper()}'S <span class="highlight">RELENTLESS</span> CONTRACTOR</h1>
                <p class="hero-subtitle">{hero_sub}</p>
                <div class="hero-buttons-centered">
                    <button class="btn btn-primary" onclick="openFormPopup()">Get Free Estimate</button>
                    <a href="tel:801-923-4634" class="btn btn-secondary">Call 801-923-4634</a>
                </div>
            </div>
        </div>
    </section>"""

    intro_section = f"""
    <section class="services-section section-with-bg bg-construction-1">
        <div class="container">
            <div class="section-header">
                <span class="section-badge">Local Expertise</span>
                <h2>BUILT FOR {name.upper()} HOMES</h2>
                <p>{intro}</p>
            </div>
        </div>
    </section>"""

    # Services grid - link to service page if top market, else to main service page
    service_cards = []
    for skey, svc in SERVICES.items():
        blurb = svc[f"blurb_{state.lower()}"]
        if top:
            link = f'<a href="{skey}/" class="btn btn-outline" style="margin-top: 15px;">{name} {svc["label"]} &rarr;</a>'
        else:
            link = f'<a href="{asset_prefix}{skey}.html" class="btn btn-outline" style="margin-top: 15px;">Learn More &rarr;</a>'
        service_cards.append(f"""                <div class="roofing-card">
                    <div class="roofing-card-icon"><i class="fas {svc['icon']}"></i></div>
                    <h3>{svc['label']}</h3>
                    <p>{blurb}</p>
                    {link}
                </div>""")

    services_section = f"""
    <section class="services-section section-with-bg bg-construction-2 bg-opacity-6">
        <div class="container">
            <div class="section-header">
                <span class="section-badge">Our Services</span>
                <h2>WHAT WE DO IN {name.upper()}</h2>
            </div>
            <div class="roofing-solutions-grid">
{chr(10).join(service_cards)}
            </div>
        </div>
    </section>"""

    # Why us
    climate_blurb_ut = "We don't install desert specs in Utah. Class 4 impact-rated systems, ice and water shield, snow-load engineering, and high-altitude UV-stable materials are standard on every project."
    climate_blurb_az = "We don't install Midwest specs in the desert. Cool-roof shingles, tile underlayments rated for 250°F+ deck temps, and UV-stable sealants are standard on every project."
    climate_blurb = climate_blurb_ut if state == "UT" else climate_blurb_az

    storm_blurb_ut = "Hail, wind, and ice-dam damage drive Utah emergency calls. We're set up for fast tarp-and-secure response and full insurance documentation."
    storm_blurb_az = "July-September monsoons drive most of our emergency calls. We're set up for fast tarp-and-secure response and full insurance documentation for hail, wind, and microburst damage."
    storm_blurb = storm_blurb_ut if state == "UT" else storm_blurb_az

    license_text = "Fully licensed Utah contractor, bonded, and insured." if state == "UT" else "Fully licensed Arizona contractor (ROC), bonded, and insured."

    why_section = f"""
    <section class="difference-section section-with-bg bg-construction-3">
        <div class="container">
            <div class="section-header">
                <span class="section-badge">Why {name} Homeowners Choose Us</span>
                <h2>THE RELENTLESS DIFFERENCE</h2>
            </div>
            <div class="difference-content">
                <div class="difference-list">
                    <div class="difference-item">
                        <div class="difference-number">01</div>
                        <div>
                            <h4>{state_full}-Specific Materials</h4>
                            <p>{climate_blurb}</p>
                        </div>
                    </div>
                    <div class="difference-item">
                        <div class="difference-number">02</div>
                        <div>
                            <h4>Storm Damage Specialists</h4>
                            <p>{storm_blurb}</p>
                        </div>
                    </div>
                    <div class="difference-item">
                        <div class="difference-number">03</div>
                        <div>
                            <h4>HOA-Friendly Process</h4>
                            <p>{name}'s HOA communities have strict architectural review boards. We handle submissions, color matching, and approvals as part of our standard process.</p>
                        </div>
                    </div>
                    <div class="difference-item">
                        <div class="difference-number">04</div>
                        <div>
                            <h4>Licensed in {state_full}</h4>
                            <p>{license_text} Real warranties backed by a real company you can reach.</p>
                        </div>
                    </div>
                </div>
                <div class="redefining-icons">
                    <div class="icon-card"><i class="fas fa-file-contract"></i><span>Licensed</span></div>
                    <div class="icon-card"><i class="fas fa-shield-alt"></i><span>Fully Insured</span></div>
                    <div class="icon-card"><i class="fas fa-star"></i><span>5-Star Rated</span></div>
                    <div class="icon-card"><i class="fas fa-bolt"></i><span>Same-Day Quotes</span></div>
                </div>
            </div>
        </div>
    </section>"""

    # Neighborhoods
    nbhds = neighborhoods_html(groups, "../")
    areas_section = f"""
    <section class="areas-section section-with-bg bg-construction-4 bg-opacity-6">
        <div class="container">
            <div class="section-header">
                <span class="section-badge">{name} Neighborhoods</span>
                <h2>WHERE WE WORK IN {name.upper()}</h2>
                <p>We serve all of {name} and the surrounding area, including:</p>
            </div>
            <div class="areas-grid">
{nbhds}
            </div>
        </div>
    </section>"""

    # FAQ
    faq_state_q = "Are you a licensed contractor in Utah?" if state == "UT" else "Are you a licensed contractor in Arizona?"
    faq_state_a = "Yes. Relentless Construction is fully licensed in Utah, bonded, and carries general liability and workers' comp insurance." if state == "UT" else "Yes. Relentless Construction holds an active Arizona Registrar of Contractors (ROC) license, is fully bonded, and carries general liability and workers' comp insurance."
    season_q = "What's the best time of year to schedule construction in " + name + "?"
    if state == "UT":
        season_a = "Spring through fall is ideal for most exterior work in " + name + " — but we work year-round. Roofing and siding can be installed in winter with proper planning. Schedule early — Utah's busy season books out 4-8 weeks ahead."
    else:
        season_a = "October through May is peak season in " + name + " — cooler temps mean faster cures and easier crew conditions. Summer projects are absolutely doable; we shift schedules to early-morning starts to handle the heat."

    faq_section = f"""
    <section class="faq-section section-with-bg bg-construction-5">
        <div class="container">
            <div class="section-header">
                <span class="section-badge">FAQ</span>
                <h2>{name.upper()} HOME IMPROVEMENT FAQS</h2>
            </div>
            <div class="faq-grid">
                <div class="faq-item">
                    <button class="faq-question"><span>Do you offer free estimates in {name}?</span><i class="fas fa-chevron-down"></i></button>
                    <div class="faq-answer"><p>Yes — every estimate is free, on-site, and detailed. No high-pressure sales, no surprise charges. Most {name} estimates are scheduled within 48 hours of your call.</p></div>
                </div>
                <div class="faq-item">
                    <button class="faq-question"><span>{faq_state_q}</span><i class="fas fa-chevron-down"></i></button>
                    <div class="faq-answer"><p>{faq_state_a} We'll provide license numbers and proof of insurance with every estimate.</p></div>
                </div>
                <div class="faq-item">
                    <button class="faq-question"><span>Do you handle insurance claims in {name}?</span><i class="fas fa-chevron-down"></i></button>
                    <div class="faq-answer"><p>Yes. We document storm damage with full photo reports, work directly with adjusters, and advocate for fair claim settlements. We won't push you into a claim that won't be covered.</p></div>
                </div>
                <div class="faq-item">
                    <button class="faq-question"><span>{season_q}</span><i class="fas fa-chevron-down"></i></button>
                    <div class="faq-answer"><p>{season_a}</p></div>
                </div>
                <div class="faq-item">
                    <button class="faq-question"><span>Do you work with HOAs in {name}?</span><i class="fas fa-chevron-down"></i></button>
                    <div class="faq-answer"><p>Yes — we handle architectural review submissions, color and material matching, and full documentation as part of our standard process. We've worked with most {name}-area HOAs.</p></div>
                </div>
            </div>
        </div>
    </section>"""

    cta_section = f"""
    <section class="cta-section section-with-bg bg-construction-1 bg-opacity-8">
        <div class="container">
            <div class="cta-content">
                <h2>Ready to Get Started in {name}?</h2>
                <p>Free, no-obligation estimate from a licensed {state_full} contractor.</p>
                <div class="cta-buttons">
                    <button class="btn btn-primary btn-large" onclick="openFormPopup()">Get Free Estimate</button>
                    <a href="tel:801-923-4634" class="btn btn-secondary btn-large">Call (801) 923-4634</a>
                </div>
            </div>
        </div>
    </section>"""

    return head + header + hero + intro_section + services_section + why_section + areas_section + faq_section + cta_section + "\n" + footer


def build_service_page(city, service_key):
    slug, name, state, lat, lng, top, hero_sub, intro, groups = city
    svc = SERVICES[service_key]
    canonical = f"https://relentlessconstruction.io/locations/{slug}/{service_key}/"
    state_full = "Utah" if state == "UT" else "Arizona"
    asset_prefix = "../../../"
    p = asset_prefix
    locations_link = "../../"

    service_label = svc["label"]
    blurb = svc[f"blurb_{state.lower()}"]
    systems = svc[f"systems_{state.lower()}"]

    schemas = f"""    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": "{service_label}",
        "name": "{service_label} in {name}, {state}",
        "description": "{blurb}",
        "provider": {{
            "@type": "GeneralContractor",
            "name": "Relentless Construction",
            "telephone": "+1-801-923-4634",
            "url": "https://relentlessconstruction.io/"
        }},
        "areaServed": {{"@type": "City", "name": "{name}", "containedInPlace": {{"@type": "State", "name": "{state_full}"}}}}
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://relentlessconstruction.io/"}},
            {{"@type": "ListItem", "position": 2, "name": "Locations", "item": "https://relentlessconstruction.io/locations/"}},
            {{"@type": "ListItem", "position": 3, "name": "{name}, {state}", "item": "https://relentlessconstruction.io/locations/{slug}/"}},
            {{"@type": "ListItem", "position": 4, "name": "{service_label}", "item": "{canonical}"}}
        ]
    }}
    </script>"""

    title = f"{service_label} in {name}, {state} | Licensed Contractor | Relentless Construction"
    description = f"{service_label} services in {name}, {state}. {blurb} Licensed, insured, free estimates: 801-923-4634."
    keywords = f"{name} {service_label.lower()}, {service_label.lower()} contractor {name} {state}, {service_label.lower()} {name}, {name} {state} {service_label.lower()}"
    og_title = f"{service_label} in {name}, {state} | Relentless Construction"
    og_description = blurb

    head = HEAD_COMMON.format(
        title=title, description=description, keywords=keywords, canonical=canonical,
        og_title=og_title, og_description=og_description, state=state,
        city_name=name, lat=lat, lng=lng, asset_prefix=asset_prefix, schemas=schemas,
    )
    header = HEADER_HTML.format(p=p, locations_link=locations_link)
    footer = FOOTER_HTML.format(p=p, locations_link=locations_link)

    hero = f"""
    <section class="hero hero-centered" style="background-image: url('{asset_prefix}assets/images/{svc['img']}');">
        <div class="hero-overlay"></div>
        <div class="container">
            <div class="hero-content-centered">
                <span class="hero-badge-centered"><i class="fas fa-map-marker-alt"></i> {name}, {state} {service_label}</span>
                <h1 class="hero-title-large">{service_label.upper()} BUILT FOR <span class="highlight">{name.upper()}</span></h1>
                <p class="hero-subtitle">{blurb}</p>
                <div class="hero-buttons-centered">
                    <button class="btn btn-primary" onclick="openFormPopup()">Get Free Estimate</button>
                    <a href="tel:801-923-4634" class="btn btn-secondary">Call 801-923-4634</a>
                </div>
            </div>
        </div>
    </section>"""

    # City-specific intro (combine local context + service angle)
    intro_section = f"""
    <section class="services-section section-with-bg bg-construction-1">
        <div class="container">
            <div class="section-header">
                <span class="section-badge">{name} {service_label}</span>
                <h2>{service_label.upper()} IN {name.upper()}</h2>
                <p>{intro}</p>
            </div>
        </div>
    </section>"""

    # Systems grid
    sys_cards = []
    for sys_name, sys_icon, sys_desc in systems:
        sys_cards.append(f"""                <div class="roofing-card">
                    <div class="roofing-card-icon"><i class="fas {sys_icon}"></i></div>
                    <h3>{sys_name}</h3>
                    <p>{sys_desc}</p>
                </div>""")
    systems_section = f"""
    <section class="services-section section-with-bg bg-construction-2 bg-opacity-6">
        <div class="container">
            <div class="section-header">
                <span class="section-badge">Service Options</span>
                <h2>{name.upper()} {service_label.upper()} SERVICES</h2>
            </div>
            <div class="roofing-solutions-grid">
{chr(10).join(sys_cards)}
            </div>
        </div>
    </section>"""

    process_section = f"""
    <section class="process-section section-with-bg bg-construction-3">
        <div class="container">
            <div class="section-header">
                <h2>FROM CONSULTATION TO COMPLETION</h2>
            </div>
            <div class="process-steps">
                <div class="process-step">
                    <div class="step-number">01</div>
                    <div class="step-icon"><i class="fas fa-search"></i></div>
                    <h3>Free Consultation</h3>
                    <p>On-site assessment with full documentation, often within 48 hours of your call.</p>
                </div>
                <div class="process-step">
                    <div class="step-number">02</div>
                    <div class="step-icon"><i class="fas fa-file-alt"></i></div>
                    <h3>Detailed Proposal</h3>
                    <p>Itemized written quote with material options, HOA-ready specs, and clear timeline. No haggling.</p>
                </div>
                <div class="process-step">
                    <div class="step-number">03</div>
                    <div class="step-icon"><i class="fas fa-hammer"></i></div>
                    <h3>Expert Installation</h3>
                    <p>{name}-experienced crews. Property protection, daily cleanup, and tight schedules.</p>
                </div>
                <div class="process-step">
                    <div class="step-number">04</div>
                    <div class="step-icon"><i class="fas fa-check-circle"></i></div>
                    <h3>Final Walkthrough</h3>
                    <p>Quality inspection, warranty documentation, and satisfaction guarantee.</p>
                </div>
            </div>
        </div>
    </section>"""

    # Cross-link to other services in same city
    other_services = []
    for skey, sv in SERVICES.items():
        if skey == service_key:
            continue
        other_services.append(f'<li><a href="../{skey}/">{sv["label"]} in {name}</a></li>')
    cross_section = f"""
    <section class="areas-section section-with-bg bg-construction-4 bg-opacity-6">
        <div class="container">
            <div class="section-header">
                <span class="section-badge">More Services</span>
                <h2>OTHER SERVICES IN {name.upper()}</h2>
            </div>
            <div class="areas-grid">
                <div class="area-card">
                    <h3><i class="fas fa-th-large"></i> ALL {name.upper()} SERVICES</h3>
                    <ul>
                        {chr(10).join(other_services)}
                    </ul>
                </div>
                <div class="area-card">
                    <h3><i class="fas fa-map-marker-alt"></i> {name.upper()} OVERVIEW</h3>
                    <ul>
                        <li><a href="../">{name}, {state} home page</a></li>
                        <li><a href="{asset_prefix}{service_key}.html">All {service_label.lower()} services</a></li>
                        <li><a href="{locations_link}">All service locations</a></li>
                        <li><a href="{asset_prefix}portfolio.html">Project portfolio</a></li>
                        <li><a href="{asset_prefix}about.html">About Relentless Construction</a></li>
                        <li><a href="{asset_prefix}contact.html">Contact us</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </section>"""

    cta_section = f"""
    <section class="cta-section section-with-bg bg-construction-1 bg-opacity-8">
        <div class="container">
            <div class="cta-content">
                <h2>Ready for {service_label} in {name}?</h2>
                <p>Free, no-obligation estimate from a licensed {state_full} contractor.</p>
                <div class="cta-buttons">
                    <button class="btn btn-primary btn-large" onclick="openFormPopup()">Get Free Estimate</button>
                    <a href="tel:801-923-4634" class="btn btn-secondary btn-large">Call (801) 923-4634</a>
                </div>
            </div>
        </div>
    </section>"""

    return head + header + hero + intro_section + systems_section + process_section + cross_section + cta_section + "\n" + footer


def build_locations_index():
    """Top-level /locations/ directory page."""
    canonical = "https://relentlessconstruction.io/locations/"
    asset_prefix = "../"
    p = asset_prefix
    locations_link = "./"

    schemas = """    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://relentlessconstruction.io/"},
            {"@type": "ListItem", "position": 2, "name": "Locations", "item": "https://relentlessconstruction.io/locations/"}
        ]
    }
    </script>"""

    head = HEAD_COMMON.format(
        title="Service Areas | Utah & Arizona Locations | Relentless Construction",
        description="Relentless Construction serves homeowners across Utah's Wasatch Front and Arizona's Phoenix metro. Find your city for local roofing, windows, hardscapes, and home improvement.",
        keywords="construction service areas, Utah contractor locations, Arizona contractor locations, Wasatch Front, Phoenix metro",
        canonical=canonical,
        og_title="Service Areas | Relentless Construction",
        og_description="Find your local Utah or Arizona service area.",
        state="UT",
        city_name="Salt Lake City",
        lat="40.7608", lng="-111.8910",
        asset_prefix=asset_prefix, schemas=schemas,
    )
    header = HEADER_HTML.format(p=p, locations_link=locations_link)
    footer = FOOTER_HTML.format(p=p, locations_link=locations_link)

    ut_cities = [c for c in CITIES if c[2] == "UT"]
    az_cities = [c for c in CITIES if c[2] == "AZ"]

    def city_list(cities):
        return "\n".join(f'                        <li><a href="{c[0]}/">{c[1]}</a></li>' for c in sorted(cities, key=lambda x: x[1]))

    hero = """
    <section class="hero hero-centered" style="background-image: url('../assets/images/service-roof.webp');">
        <div class="hero-overlay"></div>
        <div class="container">
            <div class="hero-content-centered">
                <span class="hero-badge-centered"><i class="fas fa-map-marker-alt"></i> Service Areas</span>
                <h1 class="hero-title-large">UTAH & ARIZONA <span class="highlight">SERVICE LOCATIONS</span></h1>
                <p class="hero-subtitle">Find your city for local roofing, windows, hardscapes, basement finishing, siding, and gutter services.</p>
                <div class="hero-buttons-centered">
                    <button class="btn btn-primary" onclick="openFormPopup()">Get Free Estimate</button>
                    <a href="tel:801-923-4634" class="btn btn-secondary">Call 801-923-4634</a>
                </div>
            </div>
        </div>
    </section>"""

    main = f"""
    <section class="areas-section section-with-bg bg-construction-1">
        <div class="container">
            <div class="section-header">
                <span class="section-badge">Find Your City</span>
                <h2>WHERE WE WORK</h2>
                <p>Click your city for local service details, neighborhood-specific info, and a free estimate.</p>
            </div>
            <div class="areas-grid">
                <div class="area-card">
                    <h3><i class="fas fa-map-marker-alt"></i> UTAH</h3>
                    <p class="area-subtitle">Wasatch Front & Surrounding</p>
                    <ul>
{city_list(ut_cities)}
                    </ul>
                </div>
                <div class="area-card">
                    <h3><i class="fas fa-map-marker-alt"></i> ARIZONA</h3>
                    <p class="area-subtitle">Phoenix Metro & East/West Valley</p>
                    <ul>
{city_list(az_cities)}
                    </ul>
                </div>
            </div>
        </div>
    </section>"""

    cta = """
    <section class="cta-section section-with-bg bg-construction-1 bg-opacity-8">
        <div class="container">
            <div class="cta-content">
                <h2>Don't see your city?</h2>
                <p>We serve many areas beyond those listed — call to confirm service for your address.</p>
                <div class="cta-buttons">
                    <button class="btn btn-primary btn-large" onclick="openFormPopup()">Get Free Estimate</button>
                    <a href="tel:801-923-4634" class="btn btn-secondary btn-large">Call (801) 923-4634</a>
                </div>
            </div>
        </div>
    </section>"""

    return head + header + hero + main + cta + "\n" + footer


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # Locations index
    (OUT / "index.html").write_text(build_locations_index())
    print(f"Wrote {OUT / 'index.html'}")

    # City hubs + service pages
    written = 1
    for city in CITIES:
        slug = city[0]
        city_dir = OUT / slug
        city_dir.mkdir(parents=True, exist_ok=True)
        (city_dir / "index.html").write_text(build_city_hub(city))
        written += 1

        if city[5]:  # top market
            for skey in SERVICES:
                svc_dir = city_dir / skey
                svc_dir.mkdir(parents=True, exist_ok=True)
                (svc_dir / "index.html").write_text(build_service_page(city, skey))
                written += 1

    print(f"Wrote {written} files total")


if __name__ == "__main__":
    main()
