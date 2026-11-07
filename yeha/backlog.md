# Curbwise backlog

Work top-down. One item per night. Seasonal items jump the line when their window is close. Move finished items to **Done** with the date.

## Check first (possible corrections)

- **Electronics guide: TV limit.** A fact-check on Nov 7 read Metro's Electronic Waste Recycling page as allowing 1 TV (no wider than 80 inches). The guide mentions the 80-inch width but no per-visit TV count. Fetch the page yourself and update `/nashville/electronics-tvs/` only if the page says so.

## Next up

1. **Nashville: Christmas trees (seasonal, publish by Dec 10).** Metro's tree recycling dates and drop-off sites for 2026–27. Don't publish until Metro posts this season's details. *(Nothing posted as of Nov 6. Last season's program was covered by local news around Dec 18, 2025, so start checking Dec 1.)*
2. **Nashville: construction debris and remodel waste.** Metro's Convenience Centers page (updated May 28, 2026) lists construction and demolition material at Omohundro only: $20, up to 2 cubic yards, 1 visit a day. It points to an "accepted materials" list that isn't on the page, and it shows no call-ahead rule. Find what C&D material is accepted, plus where larger loads can legally go (verify each site officially). Dumpster rental is a paid option, so name no companies unless they're verified and labeled. *Research note (2026-11-07): Metro's Bulky Item Collection page (updated Sept 17, 2025) still says DIY C&D is limited to 1 cubic yard at Omohundro, so the data file now says "call to confirm"; settle it (call or a newer page) and fix `cnd` in `data/nashville.json`. That page also names three sites for bigger loads (American Farms on Smith Springs Rd, Triune Residuals Management at the MS-COT landfill in Hermitage, and MTEC at WM's Southern Services Landfill) and links a 2023 PDF of C&D recycling processors. Verify each before listing it. Metro's Trash Guidelines say residential construction waste must go with a private hauler or contractor.*
3. **Nashville: batteries, propane tanks and light bulbs.** What the HHW program takes, which retailers take back batteries (only if verified on the retailer's own page), and the fire risk of lithium batteries.
4. **Nashville: hard-to-get-rid-of items.** Hot tubs, pianos, carpet, exercise equipment. One combined guide, every route verified.
5. **Nashville: foam and recycling drop-off sites.** Free foam recycling at East (food-service foam and foam packaging) and seven recycling drop-off sites, per the official Convenience Centers and Hours and Locations pages. A short guide or a hub section. *Research note (2026-11-07): the Hours and Locations page (updated Oct 21, 2026) lists the seven sites with addresses and hours, and says the centers also take glass recycling and compostable materials. Cardboard is banned from trash carts, so this guide can also answer "where do moving boxes go?"*
6. **Nashville: a moving-out checklist** for getting rid of everything (aim for late July, before the August move-out rush).
7. **Next city: Murfreesboro / Rutherford County.** Build `data/murfreesboro.json` from official sources first, then the hub and the mattress or couch guide. *Research note (2026-11-07): a local news site reported that Rutherford County Solid Waste limited bulk items and stopped taking building materials until further notice (date unclear), so check rutherfordcountytn.gov/solidwaste for the current rules before writing anything. Local TV covered a Rutherford County mattress drop-off event in July 2026, so the mattress guide is a good first page.*
8. **Then:** Clarksville–Montgomery County, Franklin–Williamson County, Memphis–Shelby County, Knoxville–Knox County, Chattanooga–Hamilton County.

## Seasonal and as-needed

- **Early January 2027: refresh the holiday section of `/nashville/bulk-trash/`.** Its dates end with New Year's (Friday routes picked up Monday, Jan 4, 2027). Replace them with Metro's 2027 holiday schedule from the Curbside Trash and Recycling Services page, or cut the dated list if nothing is posted.
- **Every fall (September–October): re-check the yard-waste guide.** Read NDOT's new brush and leaf schedule flyer. The 2026–27 flyer (linked from NDOT's brush page) couldn't be fetched on Nov 6, so try it first; it may also settle the unclear stump-length rule in NDOT's May 15, 2026 release.
- **After a big storm: storm debris.** Only when NDOT announces a special collection. Explain its rules and link NDOT's notice. Don't publish without a current official notice.

## Site to-dos (need Micaiah)

- **Affiliate programs:** apply to LoadUp's affiliate program and to College HUNKS (it runs through an affiliate network). Once approved, paste the tracking links in a chat with Claude; Yeha never adds a tracking link on its own.
- **Suggestion form** (Tally) URL → `config.json` `suggest_form_url`
- **Google Search Console** verification code → `config.json` `search_console_verification`
- **Custom domain** (optional) → `config.json` `site_url` and `base_path`, then set it in GitHub Pages

## Done

- 2026-11-05: Launched Curbwise with Nashville: home, the Nashville hub (centers, hours, rules, fees), and six item guides (mattress, couch and furniture, appliances, TVs and electronics, paint and chemicals, tires), plus About, Disclosures and Suggest pages.
- 2026-11-06: Nashville leaves, brush and yard waste guide (/nashville/yard-waste/): NDOT's quarterly curbside pickup, set-out rules, free Living Earth drop-off, compost bins, and what not to do. Also corrected `data/nashville.json`: construction debris is up to 2 cubic yards, 1 visit a day (the "1–2 cubic yard" and "call ahead" wording wasn't on Metro's page); big loads are 1 visit a day; chain-link, rebar and radioactive material added to not-accepted; yard-waste drop-off and compost-bin rows added.
- 2026-11-07: Nashville bulk trash and curbside pickup guide (/nashville/bulk-trash/): Metro doesn't pick up bulky items or anything outside the cart; curbside carts are for single-family homes in the USD (outside it, a private hauler); extra trash cart $65, up to 2 recycling carts free, replacement $65; what's banned from trash; cart rules; the February 2026 Tuesday–Friday schedule; holiday dates through Jan 4, 2027; Convenience Center holiday closures. `data/nashville.json`: cart rows added, the construction-debris limit flags Metro's conflicting pages, fees, rules, hours and addresses re-verified (last_checked 2026-11-07). The furniture guide links to the new page, and long source links now wrap on phones.
