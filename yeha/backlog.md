# Curbwise backlog

Work top-down. One item per night. Seasonal items jump the line when their window is close. Move finished items to **Done** with the date.

## Next up

1. **Nashville: what Metro picks up at the curb.** Bulky items and big loads (brush and leaves are now covered in the yard-waste guide). Find out how curbside service differs inside and outside the Urban Services District, how to request a pickup (hubNashville?), and the limits. Official nashville.gov pages only. *Research note (2026-11-06): the fetch tool refused Waste Services URLs that hadn't appeared in a search result first (the Waste Services home page, bulky-item-collection). Search for each page, then fetch it.*
2. **Nashville: Christmas trees (seasonal, publish by Dec 10).** Metro's tree recycling dates and drop-off sites for 2026–27. Don't publish until Metro posts this season's details. *(Nothing posted as of Nov 6. Last season's program was covered by local news around Dec 18, 2025, so start checking Dec 1.)*
3. **Nashville: construction debris and remodel waste.** Metro's Convenience Centers page (updated May 28, 2026) lists construction and demolition material at Omohundro only: $20, up to 2 cubic yards, 1 visit a day. It points to an "accepted materials" list that isn't on the page, and it shows no call-ahead rule. Find what C&D material is accepted, plus where larger loads can legally go (verify each site officially). Dumpster rental is a paid option, so name no companies unless they're verified and labeled.
4. **Nashville: batteries, propane tanks and light bulbs.** What the HHW program takes, which retailers take back batteries (only if verified on the retailer's own page), and the fire risk of lithium batteries.
5. **Nashville: hard-to-get-rid-of items.** Hot tubs, pianos, carpet, exercise equipment. One combined guide, every route verified.
6. **Nashville: foam and recycling drop-off sites.** Free foam recycling at East (food-service foam and foam packaging) and seven recycling drop-off sites, per the official Convenience Centers and Hours and Locations pages. A short guide or a hub section.
7. **Nashville: a moving-out checklist** for getting rid of everything (aim for late July, before the August move-out rush).
8. **Next city: Murfreesboro / Rutherford County.** Build `data/murfreesboro.json` from official sources first, then the hub and the mattress or couch guide.
9. **Then:** Clarksville–Montgomery County, Franklin–Williamson County, Memphis–Shelby County, Knoxville–Knox County, Chattanooga–Hamilton County.

## Seasonal and as-needed

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
