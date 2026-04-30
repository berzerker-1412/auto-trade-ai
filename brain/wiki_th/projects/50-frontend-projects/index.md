---
title: "50 Front-end Projects"
type: project
tags: [frontend, html, css, javascript, react, learning, portfolio]
created: 2026-04-13 00:00
updated: 2026-04-13 00:00
---

A curated collection of 50 frontend projects by [Sudeep Acharjee](https://sudeep-portfolio.netlify.app/), covering a wide spectrum of frontend development skills — from static landing pages to interactive games and UI clones.

**Local path:** `~/Desktop/50-frontend-projects/`
**GitHub:** https://github.com/SudeepAcharjee/The-50-Front-end-Project

## Purpose

Learning resource and portfolio foundation. Each project is self-contained — its own folder with HTML/CSS/JS files, openable directly in a browser. Good for:

- Referencing implementation patterns (canvas games, API integrations, DOM manipulation)
- Using as a starter template when building similar features
- Understanding how common UI components are built from scratch

## Tech Stack

| Technology | Usage |
| --- | --- |
| HTML5 | Structure for all projects |
| CSS3 | Styling; some use Bootstrap or Tailwind |
| Vanilla JavaScript | Logic for majority of projects |
| React | Used in select projects (clones, dashboards) |
| Bootstrap | Some landing pages |
| Tailwind CSS | Some landing pages |

No build tooling — projects run directly in a browser via `index.html`.

## Project Categories

Five broad categories across 50 projects:

| Category | Count | Examples |
| --- | --- | --- |
| Landing Pages | 8 | Company Portfolio, Blog, E-commerce, Hotel |
| Utility Tools | 14 | Password Gen, QR Code, Weather, Image Resizer |
| Games | 10 | Chess, Snake, Car Racing, Tic-Tac-Toe |
| Media & Creative | 8 | Music Player, Drawing App, Photo Editor, Piano |
| UI Clones & Apps | 10 | Twitter Clone, Whatsapp Clone, Admin Dashboard |

See [[50-frontend-projects/catalog|Full Catalog]] for complete list with live demo links.

## Key Patterns Observed

- **Canvas API** — Drawing App (#14), Car Racing (#25), Snake Game (#37): direct pixel manipulation, game loop with `requestAnimationFrame`
- **Web APIs** — Weather App (#11) uses Fetch + OpenWeather API; Translator (#19) uses a translation API; Dictionary (#36) uses dictionary API
- **LocalStorage** — Note App (#34), Todo List (#41): persist state without a backend
- **DOM-heavy games** — Chess (#24), Connect Game (#26), Snake & Ladder (#27): state encoded in DOM classes
- **Media APIs** — Music Player (#31): `<audio>` element control; Video 2 Audio (#46): File API + Web Audio
- **UI Clones** — Twitter (#42), Whatsapp (#45): static HTML/CSS clones demonstrating layout skill, not live functionality

## Sub-pages

- [[50-frontend-projects/catalog|Catalog]] — full list of all 50 projects with category, tech notes, and live demo links
