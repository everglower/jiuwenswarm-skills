# JiuwenSwarm Skills Collection

10 high-quality skills for JiuwenSwarm / OpenClaw-compatible agents, collected from open-source GitHub repositories.

## Skills Overview

### Finance (5)

| Skill | Category | Source | License |
|-------|----------|--------|---------|
| china-housing-forecast | Real Estate | [luyou666/china-housing-forecast-lite-skill](https://github.com/luyou666/china-housing-forecast-lite-skill) | MIT |
| gl-recon | Banking | [CuteGhost222/financial-services](https://github.com/CuteGhost222/financial-services) | Apache-2.0 |
| nav-tieout | Insurance | [CuteGhost222/financial-services](https://github.com/CuteGhost222/financial-services) | Apache-2.0 |
| dcf-model | Securities | [CuteGhost222/financial-services](https://github.com/CuteGhost222/financial-services) | Apache-2.0 |
| comps-analysis | Securities | [CuteGhost222/financial-services](https://github.com/CuteGhost222/financial-services) | Apache-2.0 |

### Health & Lifestyle (5)

| Skill | Source | License | Trigger Example |
|-------|--------|---------|-----------------|
| tcm-constitution | [fxw-labs/tcm-constitution](https://github.com/fxw-labs/tcm-constitution) | MIT | "我是什么体质" / "中医养生建议" |
| health-mood | [sanool/healthskills](https://github.com/sanool/healthskills) | MIT | "我心情不好" / "帮我记录情绪" |
| health-break | [sanool/healthskills](https://github.com/sanool/healthskills) | MIT | "提醒我休息" / "久坐提醒" |
| mojo-food-log | [mojoapp-ai/agent-skills](https://github.com/mojoapp-ai/agent-skills) | MIT | "记录今天吃了什么" / "饮食日志" |
| personal-trainer | [npapatheodorou/personal-trainer-skill](https://github.com/npapatheodorou/personal-trainer-skill) | MIT | "帮我制定训练计划" / "增肌方案" |

All health skills are conversation-based - no data files required. Just describe your need and the skill activates.

## Installation

Copy the `skills/` directory contents into your JiuwenSwarm agent workspace:

```
~/.jiuwenswarm/agent/workspace/skills/<skill-name>/
```

Each skill folder contains a `SKILL.md` that defines the trigger conditions, workflow, and output format.

## License

Each skill retains its original license. See individual `LICENSE` files or source repositories for details.
