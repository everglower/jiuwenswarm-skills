# JiuwenSwarm Skills Collection

10 high-quality skills for JiuwenSwarm / OpenClaw-compatible agents, collected from open-source GitHub repositories.

## Skills Overview

### Finance (5)

| Skill | Category | Source | Stars | License |
|-------|----------|--------|-------|---------|
| china-housing-forecast | Real Estate | [luyou666/china-housing-forecast-lite-skill](https://github.com/luyou666/china-housing-forecast-lite-skill) | 27 | MIT |
| gl-recon | Banking | [CuteGhost222/financial-services](https://github.com/CuteGhost222/financial-services) | 0 | Apache-2.0 |
| nav-tieout | Insurance | [CuteGhost222/financial-services](https://github.com/CuteGhost222/financial-services) | 0 | Apache-2.0 |
| dcf-model | Securities | [CuteGhost222/financial-services](https://github.com/CuteGhost222/financial-services) | 0 | Apache-2.0 |
| comps-analysis | Securities | [CuteGhost222/financial-services](https://github.com/CuteGhost222/financial-services) | 0 | Apache-2.0 |

### Health & Lifestyle (5)

| Skill | Source | Stars | License | Trigger Example |
|-------|--------|-------|---------|-----------------|
| tcm-constitution | [fxw-labs/tcm-constitution](https://github.com/fxw-labs/tcm-constitution) | 0 | MIT | "我是什么体质" / "中医养生建议" |
| health-mood | [sanool/healthskills](https://github.com/sanool/healthskills) | 0 | MIT | "我心情不好" / "帮我记录情绪" |
| health-break | [sanool/healthskills](https://github.com/sanool/healthskills) | 0 | MIT | "提醒我休息" / "久坐提醒" |
| mojo-food-log | [mojoapp-ai/agent-skills](https://github.com/mojoapp-ai/agent-skills) | 2 | MIT | "记录今天吃了什么" / "饮食日志" |
| informed-patient | [DrCatHicks/informed-patient](https://github.com/DrCatHicks/informed-patient) | 121 | CC-BY-4.0 | "我最近总头痛" / "帮我准备看医生" |

All health skills are conversation-based - no data files required. Just describe your need and the skill activates.

## Installation

Copy the `skills/` directory contents into your JiuwenSwarm agent workspace:

```
~/.jiuwenswarm/agent/workspace/skills/<skill-name>/
```

Each skill folder contains a `SKILL.md` that defines the trigger conditions, workflow, and output format.

## License

Each skill retains its original license. See individual `LICENSE` files or source repositories for details.
