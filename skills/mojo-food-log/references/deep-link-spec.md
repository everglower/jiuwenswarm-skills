# mojo import link — parameter spec

This is the detailed reference for the link produced by the food-analysis mode. The agent does not need to load this every time; only read it when the user asks about parameter names, encoding rules, or what happens when the link is tapped.

## URL pattern

```
https://api.mojoapp.ai/nutrition/add
    ?calories=<int kcal>            # required, > 0
    &protein=<number, g>            # optional, ≥ 0
    &carbs=<number, g>              # optional, ≥ 0
    &fat=<number, g>                # optional, ≥ 0
    &fiber=<number, g>              # optional, ≥ 0
    &sugar=<number, g>              # optional, ≥ 0
    &sodium=<number, mg>            # optional, ≥ 0
    &mealType=<breakfast|lunch|dinner|snack>  # optional; falls back to breakfast
    &date=<YYYY-MM-DD>              # optional, defaults to today on the device
    &servingSize=<number>           # optional, ≥ 0
    &servingUnit=<string>           # optional; common values: "g", "ml", "servings"
    &foodName=<string, free text>   # optional; keep LAST so numeric params survive link truncation
```

## Validation rules in the app

- `calories` is the **only required** parameter. Without it (or with `calories ≤ 0`) the app rejects the link entirely.
- All numeric fields are decimal numbers. Negative values are silently dropped.
- `mealType` must be one of the four enum values; anything else falls back to `breakfast`.
- `date` must be ISO `YYYY-MM-DD`; on a parse failure the app uses today's date.
- String values reach the app URL-decoded (UTF-8). Encode them with a real code tool (`urllib.parse.quote` / `encodeURIComponent`) for an all-ASCII link. Without a code tool, write non-ASCII text (Chinese / Japanese) raw — the browser percent-encodes it on tap — but DO encode the reserved ASCII characters (fixed single-byte mappings): space → `%20`, `&` → `%26`, `#` → `%23`, `+` → `%2B`, `%` → `%25`. **Never hand-write `%XX` bytes for non-ASCII characters from memory**: LLM-recalled byte sequences are frequently wrong and produce mojibake in the app.

## Rounding

The in-app AI prompt asks the analyzing LLM to round numeric values to integers before generating the link. Sub-gram precision is not useful for daily logging and creates ugly links — stick to integers.

## What happens when the link is tapped

1. `api.mojoapp.ai/nutrition/add?...` responds with HTTP 200 and a small HTML page.
2. That page tries `window.location = "mojo://nutrition/add?..."` to launch the app via URL scheme.
3. After 2 seconds, if the app did not open:
   - On iOS: redirects to the App Store listing.
   - On Android: redirects to the Play Store listing.
   - On desktop browsers: displays a `"Please open this on your phone to use Mojo App"` prompt (no store redirect).
4. Once the app opens, it parses the same query string and shows a prefilled import sheet.
5. If the user is signed in and has a **mojo Premium subscription**, the import is accepted. Otherwise the app shows a paywall and the import is not saved.

## Why it is not a true universal link

The host does **not** serve `.well-known/apple-app-site-association` or `.well-known/assetlinks.json` — by design. The link is a web → URL-scheme bridge that works in any messaging or AI agent that renders a clickable link, including agents that strip non-https schemes.

This trade-off is intentional:

| | Universal link | This web-redirect |
|---|---|---|
| Works in mail / chat clients | sometimes blocked | always (just an https link) |
| Works on first install | no, must install first | yes, falls back to App Store |
| Needs DNS + AASA + assetlinks | yes | no |
| Desktop behaviour | broken | shows "open on phone" |

For an AI agent embedding the link in a chat reply, the web-redirect form is the more robust option.

## Examples

A simple breakfast:

```
https://api.mojoapp.ai/nutrition/add?calories=320&protein=18&carbs=42&fat=9&mealType=breakfast&foodName=Oatmeal%20with%20banana
```

A Taiwanese lunchbox (combined totals, raw Chinese food name):

```
https://api.mojoapp.ai/nutrition/add?calories=720&protein=38&carbs=85&fat=24&fiber=6&mealType=lunch&date=2026-05-27&foodName=雞腿便當
```
